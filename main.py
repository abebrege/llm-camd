import argparse
from pathlib import Path

import yaml
from dotenv import load_dotenv

from src.model import get_model
from src.processor import process, LANG_EXTENSIONS, RULESETS

load_dotenv()

DEFAULT_CONFIG_PATH = "config.yaml"
ALL_LANGS = list(LANG_EXTENSIONS)


def load_config(config_path: str) -> dict:
    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    langs = config.get("langs") or ALL_LANGS
    if not isinstance(langs, list):
        raise ValueError("'langs' in config must be an array of language codes.")
    invalid_langs = [lang for lang in langs if lang not in LANG_EXTENSIONS]
    if invalid_langs:
        raise ValueError(f"Unknown lang(s) in config: {invalid_langs}. Valid langs: {sorted(LANG_EXTENSIONS)}.")

    rulesets = config.get("rulesets") or langs
    if not isinstance(rulesets, list):
        raise ValueError("'rulesets' in config must be an array of ruleset names.")
    invalid_rulesets = [ruleset for ruleset in rulesets if ruleset not in RULESETS]
    if invalid_rulesets:
        raise ValueError(f"Unknown ruleset(s) in config: {invalid_rulesets}. Valid rulesets: {sorted(RULESETS)}.")

    config["langs"] = langs
    config["rulesets"] = rulesets
    config.setdefault("target", "./benchmark/python/Xiong_PyCryptoBench")
    config.setdefault("model", "sonnet")
    config.setdefault("output_dir", None)
    return config


def main():
    parser = argparse.ArgumentParser(
        description="LLM-based Cryptographic API Misuse Detection"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to the YAML config file (default: {DEFAULT_CONFIG_PATH})."
    )
    args = parser.parse_args()

    config = load_config(args.config)

    model = get_model(config["model"])
    process(config["target"], config["langs"], config["rulesets"], model, 1, config["output_dir"])

if __name__ == "__main__":
    main()
