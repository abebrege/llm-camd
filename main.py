import argparse
import os
from src.processor import process
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def main():
    parser = argparse.ArgumentParser(
        description="LLM-based Cryptographic API Misuse Detection",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--target",
        type=str,
        default="./py_full_unsafe",
        help="Path to the file or folder containing source code file(s) to be analyzed. If pointed to a directory, it will automatically batch scan the source files in the directory."
    )
    args = parser.parse_args()
    target_path = args.target

    model_name = 'deepseek-ai/DeepSeek-V3.1-Terminus'
    # model_name = 'moonshotai/Kimi-K2-Instruct'  # model name from SiliconFlow page: https://cloud.siliconflow.cn/sft-143zof85kk/models
    API_Key = os.getenv('API_Key')
    if not API_Key:
        raise RuntimeError("API_Key is not set. Please set it in the .env file.")
    process(target_path, 'py', model_name, API_Key, 1)

if __name__ == "__main__":
    main()
