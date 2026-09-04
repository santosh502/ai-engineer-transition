import argparse
import tiktoken

def token_counter(prompt: str):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(prompt))

def main():
    parser = argparse.ArgumentParser(description="CLI to count tokens in text")
    parser.add_argument("prompt", help="text to count tokens for")
    args = parser.parse_args()
    count = token_counter(args.prompt)
    print(f"Token count: {count}")

if __name__ == "__main__":
    main()