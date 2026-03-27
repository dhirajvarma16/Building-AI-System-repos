import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eval_rubric import demo as rubric_demo
from eval_vs_ideal import demo as ideal_demo


def separator(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def main():
    separator("1. Rubric-Based Evaluation")
    rubric_demo()

    separator("2. Ideal Answer Comparison (A-E Grading)")
    ideal_demo()

    print()
    print("=" * 60)
    print("  Done! L9 complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
