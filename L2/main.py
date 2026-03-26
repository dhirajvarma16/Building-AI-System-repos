import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from classification import classify_query, demo as classification_demo


def separator(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def main():
    separator("L2: Evaluate Inputs — Classification")
    classification_demo()

    print()
    print("=" * 60)
    print("  Done! L2 complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
