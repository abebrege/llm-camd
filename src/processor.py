import time
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
from src.model import Model
from src.util import find_java_files, find_py_files, load_security_rules, read_code_file, save_to_csv, parse_analysis_result, clean_response

def prepare_prompt(source_code: str, rule_groups: dict) -> str:
    rule_descriptions = []
    for i, rules in rule_groups.items():
        group_id, group_info = i, rules
        rule_desc = (f"Rule ID: {group_id}\n"
            f"Rule Name: {group_info.get('name', 'UNKNOW')} \n"
            f"Rule description: {group_info.get('Message', 'UNKNOW')} \n"
            "------"
        )
        rule_descriptions.append(rule_desc)
    rules_str = "\n".join(rule_descriptions)
    instruction = f"""
        [Misuse Rule List]
        {rules_str}

        [Source Code]
        {source_code}

        [Detection Steps]
        [1] Line-by-line analyze code:
        Analyze the code line by line, ensuring correctly understanding of the function of each line and the variable and parameter passing between lines; Differentiating between 'module import code' and 'body code'.
        [2] Must Exclude the unused module import code:
        Confirm the import modules be used in body code; Must Exclude them if unused right now without speculate. If there is no body code, directly Skip to step [5].
        [3] Locate body code lines related to [Misuse Rule List]:
        Locate body code lines related to [Misuse Rule List], and determine the body code executed condition during runtime; Must Exclude them if unexecuted right now without speculate.
        [4] Trace each used parameter related to [Misuse Rule List]:
        Understanding the code through step [1], [2] and [3], Trace each used parameter related to [Misuse Rule List] origins (keys/salts/iterations/regex).
        [5] Draw a judgment conclusion:
        Based on the above analysis steps, draw a judgment conclusion of actual execution body code against the [Misuse Rule List]. If there is no body code, judge as no misuse.
        [6] Output Detection Result:
        Output the Detection Result of step [5] according to the requirements and format.

        ### Task Requirements
        As a professional Python programmer, strictly execute the [Detection Steps] sequentially to analyze the [Source Code] for Cryptographic API Misuse Detection. 

        ### Detection Result Output Requirements:
        1. Strictly executed all [Detection Steps] at first, Output the Detection Result later.
        2. Separate misuse line numbers with commas ','.
        3. If multiple rules are violated, merge into a single entry.
        4. Separate field values with '|'; for the same rule, keep line numbers comma-separated.
        5. Strictly maintain field order and format (retain titles before ':').

        ### Detection Result Output Format:
        Line Numbers: (same-rule lines comma-separated, different rules separated by '|', e.g., 1,3|2,5. If the detection result is no misused, set it to None.)
        Rule IDs: (multiple numbers separated by '|'. If the detection result is no misused, set it to -1.)
        Rule Names: (multiple names separated by '|'. If the detection result is no misused, set it to UNKNOWN.)
        Misused Modules: (multiple modules separated by '|'. If the detection result is no misused, set it to None.)
        Misused path:
    """
    return instruction

def process_single_file(file_path: Path, rule_groups: dict, model: Model) -> dict:
    """process single files and return a dict result"""
    try:
        code_content = read_code_file(str(file_path))
        prompt = prepare_prompt(code_content, rule_groups)
        raw_result = clean_response(model.complete(prompt))
        result = parse_analysis_result(raw_result, str(file_path))
        result["Time_Taken/s"] = '0.01'
        return result
    except Exception as e:
        return {
        "File Path": 'miss',
        "Line Numbers": 'miss',
        "Rule IDs": 'miss',
        "Rule Names": 'miss',
        "Misused Modules": str(e),
        "Time_Taken/s": '0.01'
    }

def process(target_path: str, codetype: str, model: Model, i, output_dir: str | None = None):
    try:
        rule_groups = load_security_rules(codetype)
    except Exception as e:
        raise RuntimeError(f"fail load rule_groups: {str(e)}")

    target = Path(target_path)
    if target.is_file():
        if codetype == 'java' and target.suffix == '.java':
            code_files = [target]
        elif codetype == 'py' and target.suffix == '.py':
            code_files = [target]
        else:
            raise ValueError("Target file extension does not match the specified codetype.")
    elif target.is_dir():
        if codetype == 'java':
            java_files = find_java_files(target_path)
            if not java_files:
                raise ValueError("No Found .java files")
            code_files = java_files
        elif codetype == 'py':
            py_files = find_py_files(target_path)
            if not py_files:
                raise ValueError("No Found .py files")
            code_files = py_files
        else:
            raise ValueError("Please enter a valid codetype: 'py' or 'java'.")
    else:
        raise ValueError("Target path does not exist.")

    model_name = model.name.replace('/', '_').replace(':', '_')
    target_name = target.stem if target.is_file() else target.name
    if output_dir is None:
        output_path = Path("./output") / model_name / target_name
    else:
        output_path = Path(output_dir)

    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = output_path / f"{timestamp}_output.csv"

    results = []
    progress_bar = tqdm(code_files, desc="analyze progress", unit="file")
    for file_path in progress_bar:
        start_time = time.time()
        progress_bar.set_postfix({"current file": file_path.name})
        try:
            file_results = process_single_file(
                file_path=file_path,
                rule_groups=rule_groups,
                model=model
            )
            elapsed = round(time.time() - start_time, 2)
            file_results["Time_Taken/s"] = f"{elapsed}"
        except Exception as e:
            elapsed = round(time.time() - start_time, 2)
            error_result = {
                    "File Path": 'miss',
                    "Line Numbers": 'miss',
                    "Rule IDs": 'miss',
                    "Rule Names": 'miss',
                    "Misused Modules": str(e),
                    "Time_Taken/s": f"{elapsed}"
                }
            file_results = error_result
        results.append(file_results)

    save_to_csv(results, str(output_csv))
    print(f"\n Analysis cycle {i} has been completed! Results save to: {output_csv} \n\n")