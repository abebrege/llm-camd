"""Score a detection run against the benchmark ground truth.

The benchmark defines the labels, so every model is scored against the dataset
itself rather than against another model's answers:

  misuse (py_full_unsafe)  - every file contains exactly one known misuse, so the
                             questions are "was a misuse flagged at all?" and
                             "was it the right rule?"
  trap   (pysafe_trapfile) - every file is safe, so the question is "did the model
                             stay quiet?"

The passed file is scored side by side with the DeepSeek and Kimi-K2 baselines
for the same dataset.

    uv run scripts/score_results.py --type misuse --file output/sonnet/.../x.csv
"""

import argparse
import csv
import datetime as dt
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = ROOT / "foo" / "Detection_Result_CSV"
DEFAULT_BENCHMARK = ROOT / "benchmark" / "python" / "Xiong_PyCryptoBench"
DEFAULT_OUTPUT_DIR = ROOT / "output" / "analysis_reports"

# Categorical slots 1-3 of the validated palette, in fixed order.
SERIES_COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]
GRID_COLOR = "#d7d7d4"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
SURFACE = "#fcfcfb"

# py_full_unsafe file names are grouped by test group, not by rule id: group 00
# and group 05 are both insecure-randomness variants (rule 5). Every other group
# number is the rule id itself.
GROUP_RULE_OVERRIDES = {0: 5}

DATASETS = {
    "misuse": {"dir": "py_full_unsafe", "label": "misuse (py_full_unsafe)"},
    "trap": {"dir": "pysafe_trapfile", "label": "trap (pysafe_trapfile)"},
}

BASELINES = [("deepseek", "DeepSeek-V3.1"), ("kimi", "Kimi-K2")]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score a result CSV against benchmark ground truth, next to the DeepSeek and Kimi-K2 baselines.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--type", choices=sorted(DATASETS), required=True,
                        help="Which benchmark dataset the result file was produced on.")
    parser.add_argument("--file", required=True,
                        help="Result CSV to score, e.g. output/sonnet/py_full_unsafe/20260809_182052_output.csv")
    parser.add_argument("--label", default=None,
                        help="Name for the scored run in tables and charts. Defaults to the model directory or file stem.")
    parser.add_argument("--baseline-variant", default="CoT-1",
                        help="Baseline run suffix to compare against, e.g. CoT-1, 1, CoT-ex1.")
    parser.add_argument("--base-dir", default=str(DEFAULT_BASE),
                        help="Directory holding misuse_files/ and trap_files/ baselines.")
    parser.add_argument("--benchmark-dir", default=str(DEFAULT_BENCHMARK),
                        help="Directory holding py_full_unsafe/ and pysafe_trapfile/ source files.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR),
                        help="Directory for the generated report and charts.")
    parser.add_argument("--no-charts", action="store_true", help="Skip PNG chart generation.")
    return parser.parse_args()


def basename(value: str) -> str:
    return Path(str(value).replace("\\", "/")).name.strip().lower()


def parse_rule_ids(value: str) -> set[int]:
    """Parse a 'Rule IDs' cell such as '7|9' or '-1' into a set of rule ids."""
    cleaned = str(value or "").replace("﻿", "").strip()
    ids: set[int] = set()
    for token in re.split(r"[|,]", cleaned):
        token = token.strip()
        if not token or token == "-1":
            continue
        try:
            ids.add(int(token))
        except ValueError:
            continue
    return ids


def ground_truth(dataset: str, benchmark_dir: Path) -> tuple[dict[str, int | None], dict[str, int | None]]:
    """Return (expected rule per file, mimicked rule per file) keyed by lowercase filename.

    For misuse the expected rule is the real label. For trap the expected rule is
    None (the file is safe) and the mimicked rule is what the trap imitates.
    """
    folder = benchmark_dir / DATASETS[dataset]["dir"]
    if not folder.is_dir():
        raise FileNotFoundError(f"Benchmark folder not found: {folder}")

    expected: dict[str, int | None] = {}
    mimicked: dict[str, int | None] = {}
    for path in sorted(folder.glob("*.py")):
        key = path.name.lower()
        if dataset == "misuse":
            match = re.match(r"rule_(\d+)_", path.name)
            if not match:
                continue
            group = int(match.group(1))
            expected[key] = GROUP_RULE_OVERRIDES.get(group, group)
            mimicked[key] = expected[key]
        else:
            match = re.search(r"rule_(\d+)_trapfile", path.name)
            expected[key] = None
            mimicked[key] = int(match.group(1)) if match else None
    if not expected:
        raise ValueError(f"No labelled files found in {folder}")
    return expected, mimicked


def load_predictions(csv_path: Path) -> tuple[dict[str, set[int]], int]:
    """Return (rule ids per filename, error row count)."""
    predictions: dict[str, set[int]] = {}
    errors = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            raw = str(row.get("File Path") or "").strip()
            if not raw:
                continue
            if raw.lower() == "miss":
                errors += 1
                continue
            predictions[basename(raw)] = parse_rule_ids(row.get("Rule IDs"))
    return predictions, errors


@dataclass
class Score:
    label: str
    source: Path
    dataset: str
    scored: int = 0
    missing: int = 0
    errors: int = 0
    detected: int = 0        # flagged at least one misuse
    exact: int = 0           # flagged the ground-truth rule (misuse only)
    per_rule: dict[int, dict[str, int]] = field(default_factory=dict)

    @property
    def quiet(self) -> int:
        return self.scored - self.detected

    def headline(self) -> dict[str, float]:
        n = self.scored or 1
        if self.dataset == "misuse":
            return {
                "Detection rate": self.detected / n,
                "Correct rule": self.exact / n,
                "Missed entirely": self.quiet / n,
            }
        return {
            "Stayed quiet (TNR)": self.quiet / n,
            "False positives": self.detected / n,
        }


def score(label: str, csv_path: Path, dataset: str,
          expected: dict[str, int | None], mimicked: dict[str, int | None]) -> Score:
    predictions, errors = load_predictions(csv_path)
    result = Score(label=label, source=csv_path, dataset=dataset, errors=errors)

    for key, truth in expected.items():
        if key not in predictions:
            result.missing += 1
            continue
        predicted = predictions[key]
        result.scored += 1
        bucket = result.per_rule.setdefault(
            mimicked.get(key) or 0, {"n": 0, "detected": 0, "exact": 0}
        )
        bucket["n"] += 1
        if predicted:
            result.detected += 1
            bucket["detected"] += 1
        if truth is not None and truth in predicted:
            result.exact += 1
            bucket["exact"] += 1
    return result


def resolve_result_file(value: str) -> Path:
    path = Path(value).expanduser()
    for candidate in ([path] if path.is_absolute() else [Path.cwd() / path, ROOT / path, path]):
        if candidate.is_file():
            return candidate.resolve()
    matches = sorted((ROOT / "output").rglob(path.name)) if path.name else []
    if matches:
        return matches[0].resolve()
    raise FileNotFoundError(f"Could not find result file: {value}")


def find_baselines(base_dir: Path, dataset: str, variant: str) -> list[tuple[str, Path]]:
    folder = base_dir / f"{dataset}_files"
    if not folder.is_dir():
        raise FileNotFoundError(f"Baseline folder not found: {folder}")

    suffix = f"-{variant.lower()}.csv"
    variant_is_cot = "cot" in variant.lower()
    found: list[tuple[str, Path]] = []
    for token, label in BASELINES:
        matches = [
            p for p in sorted(folder.glob("*.csv"))
            if token in p.name.lower()
            and p.name.lower().endswith(suffix)
            and ("cot" in p.name.lower()) == variant_is_cot
        ]
        if not matches:
            available = sorted({
                m.group(1) for p in folder.glob("*.csv") if token in p.name.lower()
                if (m := re.search(r"-((?:CoT-)?(?:ex)?\d+)$", p.stem, re.IGNORECASE))
            })
            raise FileNotFoundError(
                f"No {label} baseline with variant {variant!r} in {folder}.\n"
                f"Available variants: {', '.join(available)}"
            )
        found.append((f"{label} ({variant})", matches[0]))
    return found


def default_label(path: Path) -> str:
    # output/<model>/<dataset>/<stamp>_output.csv -> <model>
    parts = path.parts
    if "output" in parts:
        index = len(parts) - 1 - parts[::-1].index("output")
        if index + 1 < len(parts) - 1:
            return parts[index + 1]
    return path.stem


def fmt_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [max(len(headers[i]), *(len(r[i]) for r in rows)) if rows else len(headers[i])
              for i in range(len(headers))]
    def line(cells: list[str]) -> str:
        return "| " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    out = [line(headers), "| " + " | ".join("-" * w for w in widths) + " |"]
    out.extend(line(r) for r in rows)
    return "\n".join(out)


def summary_table(scores: list[Score]) -> str:
    metrics = list(scores[0].headline())
    headers = ["Model", "Files"] + metrics + ["Errors"]
    rows = []
    for s in scores:
        head = s.headline()
        rows.append([s.label, str(s.scored)] + [fmt_pct(head[m]) for m in metrics] + [str(s.errors)])
    return render_table(headers, rows)


def per_rule_table(scores: list[Score], dataset: str) -> str:
    key = "detected" if dataset == "trap" else "exact"
    rule_ids = sorted({r for s in scores for r in s.per_rule})
    headers = ["Rule", "Files"] + [s.label for s in scores]
    rows = []
    for rule_id in rule_ids:
        n = next((s.per_rule[rule_id]["n"] for s in scores if rule_id in s.per_rule), 0)
        cells = []
        for s in scores:
            bucket = s.per_rule.get(rule_id)
            cells.append(fmt_pct(bucket[key] / bucket["n"]) if bucket and bucket["n"] else "-")
        rows.append([str(rule_id), str(n)] + cells)
    return render_table(headers, rows)


def _style_axes(ax):
    ax.set_facecolor(SURFACE)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=9, length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["bottom"].set_color(GRID_COLOR)


def chart_headline(scores: list[Score], dataset: str, path: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    metrics = list(scores[0].headline())
    x = np.arange(len(metrics))
    width = 0.26
    fig, ax = plt.subplots(figsize=(1.9 * len(metrics) + 3.2, 4.4), facecolor=SURFACE)

    for i, s in enumerate(scores):
        values = [s.headline()[m] * 100 for m in metrics]
        offset = (i - (len(scores) - 1) / 2) * width
        bars = ax.bar(x + offset, values, width * 0.92, label=s.label,
                      color=SERIES_COLORS[i % len(SERIES_COLORS)], linewidth=0)
        # Direct labels: required relief for the low-contrast slot.
        ax.bar_label(bars, fmt="%.1f", padding=2, fontsize=8, color=TEXT_PRIMARY)

    ax.set_xticks(x, metrics, color=TEXT_SECONDARY)
    ax.set_ylabel("% of files", color=TEXT_SECONDARY, fontsize=9)
    ax.set_ylim(0, 105)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title(f"{DATASETS[dataset]['label']} - scored against benchmark ground truth",
                 color=TEXT_PRIMARY, fontsize=11, pad=12, loc="left")
    _style_axes(ax)
    ax.legend(frameon=False, fontsize=9, labelcolor=TEXT_SECONDARY, ncols=len(scores),
              loc="upper center", bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)


def chart_per_rule(scores: list[Score], dataset: str, path: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    key = "detected" if dataset == "trap" else "exact"
    title = ("False-positive rate by imitated rule" if dataset == "trap"
             else "Correct-rule rate by rule")
    rule_ids = sorted({r for s in scores for r in s.per_rule})
    y = np.arange(len(rule_ids))
    height = 0.26
    fig, ax = plt.subplots(figsize=(8.5, 0.46 * len(rule_ids) + 2.4), facecolor=SURFACE)

    for i, s in enumerate(scores):
        values = []
        for rule_id in rule_ids:
            bucket = s.per_rule.get(rule_id)
            values.append(bucket[key] / bucket["n"] * 100 if bucket and bucket["n"] else 0.0)
        offset = (i - (len(scores) - 1) / 2) * height
        ax.barh(y + offset, values, height * 0.92, label=s.label,
                color=SERIES_COLORS[i % len(SERIES_COLORS)], linewidth=0)
        # Selective direct labels: a 0% bar has no length, so mark it explicitly
        # rather than leaving it indistinguishable from missing data.
        for pos, value in zip(y + offset, values):
            if value == 0:
                ax.text(0.7, pos, "0", va="center", ha="left", fontsize=7.5, color=TEXT_SECONDARY)

    ax.set_yticks(y, [f"rule {r}" for r in rule_ids], color=TEXT_SECONDARY)
    ax.invert_yaxis()
    ax.set_xlabel("% of files", color=TEXT_SECONDARY, fontsize=9)
    ax.set_xlim(0, 105)
    ax.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title(title, color=TEXT_PRIMARY, fontsize=11, pad=12, loc="left")
    _style_axes(ax)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.legend(frameon=False, fontsize=9, labelcolor=TEXT_SECONDARY, ncols=len(scores),
               loc="lower center", bbox_to_anchor=(0.5, 0.004))
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    dataset = args.type
    result_path = resolve_result_file(args.file)
    base_dir = Path(args.base_dir).resolve()
    benchmark_dir = Path(args.benchmark_dir).resolve()

    expected, mimicked = ground_truth(dataset, benchmark_dir)
    label = args.label or default_label(result_path)

    scores = [score(label, result_path, dataset, expected, mimicked)]
    for baseline_label, baseline_path in find_baselines(base_dir, dataset, args.baseline_variant):
        scores.append(score(baseline_label, baseline_path, dataset, expected, mimicked))

    note = ""
    if len({s.scored for s in scores}) > 1:
        note = ("Coverage differs between runs; rates are per model's own scored files.\n"
                + "\n".join(f"  - {s.label}: {s.scored}/{len(expected)} files"
                            f"{f', {s.missing} absent' if s.missing else ''}" for s in scores))

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir).resolve() / f"{dataset}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    charts: list[tuple[str, Path]] = []
    if not args.no_charts:
        headline_png = output_dir / "headline.png"
        per_rule_png = output_dir / "per_rule.png"
        chart_headline(scores, dataset, headline_png)
        chart_per_rule(scores, dataset, per_rule_png)
        charts = [("Headline metrics", headline_png), ("Per-rule breakdown", per_rule_png)]

    truth_note = (
        "Every file contains one known misuse, so higher is better on detection rate and correct rule."
        if dataset == "misuse" else
        "Every file is safe, so any detection is a false positive: higher is better on 'stayed quiet'."
    )

    lines = [
        f"# {DATASETS[dataset]['label']} scoring",
        "",
        f"- Scored file: `{result_path}`",
        f"- Ground truth: `{benchmark_dir / DATASETS[dataset]['dir']}` ({len(expected)} files)",
        f"- {truth_note}",
        "",
        "## Summary",
        "",
        summary_table(scores),
    ]
    if note:
        lines += ["", note]
    lines += ["", "## Per-rule breakdown", "",
              ("Share of trap files wrongly flagged, by the rule the trap imitates."
               if dataset == "trap" else
               "Share of files where the model named the correct rule."),
              "", per_rule_table(scores, dataset)]
    for title, png in charts:
        lines += ["", f"## {title}", "", f"![{title}]({png.name})"]
    report = "\n".join(lines) + "\n"

    (output_dir / "report.md").write_text(report, encoding="utf-8")
    with (output_dir / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
        metrics = list(scores[0].headline())
        writer = csv.writer(handle)
        writer.writerow(["Model", "Files scored"] + metrics + ["Errors"])
        for s in scores:
            head = s.headline()
            writer.writerow([s.label, s.scored] + [round(head[m], 4) for m in metrics] + [s.errors])

    print(report)
    print(f"Report saved to: {output_dir / 'report.md'}")


if __name__ == "__main__":
    import sys

    try:
        main()
    except (FileNotFoundError, ValueError) as error:
        sys.exit(f"error: {error}")
