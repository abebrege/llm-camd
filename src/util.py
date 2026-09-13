import os
from pathlib import Path
import csv
from src import rules as ru
import re

def find_files(folder_path: str, extension: str) -> list:
    files = []
    for root, _, names in os.walk(folder_path):
        for name in names:
            if name.endswith(extension):
                files.append(Path(root) / name)
    return files


def ruleset_by_name(name: str) -> dict:
    if name == 'py':
        return ru.rule_groups
    elif name == 'java':
        return ru.rule_groups_java
    elif name == 'js':
        return ru.rule_groups_js
    elif name == 'go':
        return ru.rule_groups_go
    elif name == 'general':
        return ru.rule_groups_general
    else:
        raise ValueError(f"Unknown ruleset '{name}'")


def load_security_rules(langs: list[str], rulesets: list[str] | None = None) -> dict:
    rules = [
        rule
        for name in (rulesets or langs)
        for rule_id, rule in ruleset_by_name(name).items()
        if rule_id != -1
    ]
    merged = {i: rule for i, rule in enumerate(rules, start=1)}
    merged[-1] = ru.rule_groups[-1]
    return merged


def read_code_file(file_path: str) -> str:
    try:
        path = Path(file_path)
        if not path.is_file():
            raise ValueError("Path is not files")
        if path.suffix not in ['.py', '.java', '.js', '.go']:
            raise ValueError("Only support .py, .java, .js and .go files")

        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        numbered_lines = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
        content = ''.join(numbered_lines)

        return content

    except Exception as e:
        raise RuntimeError(f"Fail read files: {str(e)}")

def save_to_csv(results: list[dict], output_path: str):
    """save structure result to CSV"""
    fieldnames = ["File Path", "Line Numbers", "Rule IDs", "Rule Names", "Misused Modules", "Time_Taken/s"]

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def parse_analysis_result(text: str, file_path: str) -> dict:
    result = {
        "File Path": '',
        "Line Numbers": '',
        "Rule IDs": '',
        "Rule Names": '',
        "Misused Modules": ''
    }
    result["File Path"] = file_path
    patterns = [
        r'Line Numbers[::]\s*([^.\n]+?)\s*\n',
        r'Rule IDs[::]\s*([\d\s,\|\-]+)\n',
        r'Rule Names[::]\s*([^.\n]+?)\s*\n',
        r'Misused Modules[::]\s*([^.\n]+?)\s*\n'
    ]

    match1 = re.search(patterns[0], text)
    if match1:
        result['Line Numbers'] = match1.group(1)
    match2 = re.search(patterns[1], text)
    if match2:
        result['Rule IDs'] = match2.group(1)
    match3 = re.search(patterns[2], text)
    if match3:
        result['Rule Names'] = match3.group(1)
    match4 = re.search(patterns[3], text)
    if match4:
        result['Misused Modules'] = match4.group(1)

    return result

def clean_response(content: str) -> str:
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0].strip()
    return content.replace('"', '').replace('{', '').replace('}', '').replace('*', '').replace('#', '')

