from L1 import completion, tokens, chat_format, token_count


def separator(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def main():
    separator("1. Basic Completion")
    completion.demo()

    separator("2. Tokens & Tokenization")
    tokens.demo()

    separator("3. Chat Format (System / User / Assistant)")
    chat_format.demo()

    separator("4. Token Counting")
    token_count.demo()

    print()
    print("=" * 60)
    print("  Done! L1 complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
