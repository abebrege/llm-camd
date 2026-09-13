import os
from pathlib import Path
import csv
from src import rules as ru
import re

def find_java_files(folder_path: str) -> list:
    java_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".java"):
                java_files.append(Path(root) / file)
    return java_files


def find_py_files(folder_path: str) -> list:
    py_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                py_files.append(Path(root) / file)
    return py_files


def find_js_files(folder_path: str) -> list:
    js_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".js"):
                js_files.append(Path(root) / file)
    return js_files


def find_go_files(folder_path: str) -> list:
    go_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".go"):
                go_files.append(Path(root) / file)
    return go_files


def find_general_files(folder_path: str) -> list:
    return find_py_files(folder_path) + find_java_files(folder_path) + find_js_files(folder_path) + find_go_files(folder_path)


def load_security_rules(code_type: str = None) -> (dict, dict):
    """Load rule_groups from rule_source.py"""
    try:
        if code_type == 'java':
            return ru.rule_groups_java
        elif code_type == 'py':
            return ru.rule_groups
        elif code_type == 'js':
            return ru.rule_groups_js
        elif code_type == 'go':
            return ru.rule_groups_go
        elif code_type == 'general':
            return ru.rule_groups_general
    except ImportError:
        raise RuntimeError("Cannot Load rule_groups!")


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

