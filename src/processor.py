import time
import requests
import argparse
from pathlib import Path
from tqdm import tqdm
import random
from util import find_java_files, find_py_files, load_security_rules, read_code_file, save_to_csv, parse_analysis_result

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

def analyze_with_llm(prompt: str, model_name: str, API_KEY: str, timeout: int = 120):
    """
    Use LLMs by API
    Suggest LLMs：
    SiliconFlow：THUDM/GLM-4-32B-0414、moonshotai/Kimi-K2-Instruct
    OpenAI：GPT4.1、GPT4
    """

    endpoint = "https://api.siliconflow.cn/v1/chat/completions"  # siliconflow request adress
    # endpoint = "http://localhost:11434/api/generate"  # siliconflow request adress
    # endpoint = " https://api.apiyi.com/v1/chat/completions"  # OpenAI request adress
    # endpoint = "https://api.openai.com/v1/chat/completions"  # OpenAI request adress
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # Please fill in your own SiliconFlow API key.
        # "Authorization": f"Bearer {'Your—API-Key'}",  # Please fill in your own OpenAI API key.
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    max_retries = 5
    base_delay = 1
    retry_count = 0

    while retry_count <= max_retries:
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()['choices'][0]['message']

            content_str = result.get('content', '')
            if '```json' in content_str:
                json_part = content_str.split('```json')[1].split('```')[0].strip()
                cleaned_json = json_part.replace('"', '').replace('{', '').replace('}', '').replace('*', '').replace('#', '')
            else:
                cleaned_json = content_str.replace('"', '').replace('{', '').replace('}', '').replace('*', '').replace('#', '')

            final_output = cleaned_json
            return final_output

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                retry_count += 1
                retry_after = e.response.headers.get('Retry-After')
                if retry_after and retry_after.isdigit():
                    wait_time = int(retry_after)
                else:
                    wait_time = (2 ** retry_count) * base_delay + random.uniform(0, 0.5)
                print(f"⚠️ Triggle speed limit(429), {retry_count}/{max_retries} times retry，waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                if retry_count > max_retries:
                    raise RuntimeError(f"API error: retry invalid")
                print(f"⚠️ Triggle speed limit(429),  {retry_count}/{max_retries} times retry，waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)

            else:
                error_msg = f"HTTP error {e.response.status_code}"
                if e.response.status_code == 401:
                    error_msg += " | API Key invalid"
                raise RuntimeError(f"API error: {error_msg}")

        except Exception as e:
            raise RuntimeError(f"Fail use LLMs: {str(e)}")


def analyze_with_ollama(prompt: str, model_name: str, timeout: int = 200):
    """
    Call the local Ollama large model (fix streaming response handling)
    """
    endpoint = "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 2000
        }
    }

    try:
        # Add the `stream=True` parameter to handle streaming responses
        response = requests.post(
            endpoint,
            json=payload,
            stream=False,
            timeout=timeout
        )
        data = response.json()
        content_str = data["response"].strip()
        if '```json' in content_str:
            # Extract the JSON portion and remove the markers.
            json_part = content_str.split('```json')[1].split('```')[0].strip()

            # Remove all double quotes, curly braces, and commas.
            cleaned_json = json_part.replace('"', '').replace('{', '').replace('}', '').replace('*', '').replace('#', '')
        else:
            # Directly handle non-JSON content.
            cleaned_json = content_str.replace('"', '').replace('{', '').replace('}', '').replace('*', '').replace('#', '')
        return cleaned_json

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ollama API call failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing the response: {str(e)}")


def process_single_file(file_path: Path, rule_groups: dict, model_name: str, API_KEY:str) -> dict:
    """process single files and return a dict result"""
    try:
        code_content = read_code_file(str(file_path))
        prompt = prepare_prompt(code_content, rule_groups)
        # raw_result = analyze_with_ollama(prompt, model_name)
        raw_result = analyze_with_llm(prompt, model_name, API_KEY)
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

def process(target_path: str, codetype: str, model_name: str, API_KEY: str, i):
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
        output_dir = target.parent
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
        output_dir = target
    else:
        raise ValueError("Target path does not exist.")
    results = []
    progress_bar = tqdm(code_files, desc="analyze progress", unit="file")
    for file_path in progress_bar:
        start_time = time.time()
        progress_bar.set_postfix({"current file": file_path.name})
        try:
            file_results = process_single_file(
                file_path=file_path,
                rule_groups=rule_groups,
                model_name=model_name,
                API_KEY=API_KEY
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

    output_csv = output_dir / f"analysis_result_by_{model_name.replace('/', '_')}-CoT-{i}.csv"
    save_to_csv(results, str(output_csv))
    print(f"\n Analysis cycle {i} has been completed! Results save to: {output_csv} \n\n")