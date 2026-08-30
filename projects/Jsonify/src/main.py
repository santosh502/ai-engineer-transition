import argparse

from src.core.extractor import extract_json
from src.core.models import User


def main():
    parser = argparse.ArgumentParser(
        description="This is cli tool to extract user json"
    )
    parser.add_argument("message", help="please enter user messgae")
    args = parser.parse_args()
    try:
        user: User = extract_json(message=args.message)
        print(user.model_dump_json(indent=4))
    except Exception as e:
        print(f"Error: failed to extract JSON — {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
