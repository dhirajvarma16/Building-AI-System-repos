import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chaining_prompts import demo as chaining_demo


def separator(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def main():
    separator("L5: Chaining Prompts")
    chaining_demo()

    print()
    print("=" * 60)
    print("  Done! L5 complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
