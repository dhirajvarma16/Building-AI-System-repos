import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from completion import get_completion
from tokens import demo as tokens_demo
from chat_format import get_completion_from_messages, demo as chat_format_demo
from token_count import get_completion_and_token_count, demo as token_count_demo


def separator(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def main():
    separator("1. Basic Completion")
    print("Prompt: What is the capital of France?")
    response = get_completion("What is the capital of France?")
    print(f"Response: {response}")

    separator("2. Tokens & Tokenization")
    tokens_demo()

    separator("3. Chat Format (System / User / Assistant)")
    chat_format_demo()

    separator("4. Token Counting")
    token_count_demo()

    print()
    print("=" * 60)
    print("  Done! L1 complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
