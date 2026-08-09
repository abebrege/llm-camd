import argparse
from src.processor import process

def main():
    parser = argparse.ArgumentParser(
        description="LLM-based Cryptographic API Misuse Detection",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # folder_path = './pysafe_trapfile'     # folder path be analyzed
    folder_path = './py_full_unsafe'  # folder path be analyzed

    model_name = 'deepseek-ai/DeepSeek-V3.1-Terminus'
    # model_name = 'moonshotai/Kimi-K2-Instruct'  # model name from SiliconFlow page: https://cloud.siliconflow.cn/sft-143zof85kk/models

    API_Key = 'sk-cvjxxxx'  # Please fill in your own SiliconFlow API key.

    process(folder_path, 'py', model_name, API_Key, 1)

if __name__ == "__main__":
    main()
