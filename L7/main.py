import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from process_user_message import process_user_message


def separator(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def main():
    separator("L7: End-to-End Customer Service Chatbot")
    print("Type your message (or 'quit' to exit).")
    print("The system runs a 5-step pipeline for every message:")
    print("  1. Input moderation")
    print("  2. Product/category extraction")
    print("  3. Product info lookup")
    print("  4. Response generation (with conversation history)")
    print("  5. Output moderation")
    print()

    all_messages = []

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        response = process_user_message(user_input, all_messages)
        print(f"Assistant: {response}")
        print()

        # Maintain conversation history
        all_messages.append({"role": "user", "content": user_input})
        all_messages.append({"role": "assistant", "content": response})

    print()
    print("=" * 60)
    print("  Done! L7 complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
