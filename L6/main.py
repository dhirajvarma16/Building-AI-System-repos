import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_output_moderation import demo as moderation_demo
from check_output_self_eval import demo as self_eval_demo


def separator(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def main():
    separator("1. Check Outputs with Moderation API")
    moderation_demo()

    separator("2. Check Outputs with Model Self-Evaluation")
    self_eval_demo()

    print()
    print("=" * 60)
    print("  Done! L6 complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
