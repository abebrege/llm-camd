import argparse
from src.model import get_model, list_models
from src.processor import process
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser(
        description="LLM-based Cryptographic API Misuse Detection",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--target",
        type=str,
        default="./benchmark/python/Xiong_PyCryptoBench",
        help="Path to the file or folder containing source code file(s) to be analyzed. If pointed to a directory, it will automatically batch scan the source files in the directory."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="sonnet",
        help=f"Model to analyze with. One of: {', '.join(list_models())}. An unlisted model can be given as 'provider:model_id'."
    )
    args = parser.parse_args()

    model = get_model(args.model)
    process(args.target, 'py', model, 1)

if __name__ == "__main__":
    main()
