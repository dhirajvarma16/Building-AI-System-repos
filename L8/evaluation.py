import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from products import read_string_to_list
from utils import find_category_and_product_v1, find_category_and_product_v2
from test_cases import dev_set


def eval_response_vs_ideal(response, ideal_answer):
    """
    Compare model output to ideal answer.
    Returns a score between 0.0 and 1.0.

    Scoring:
    - Parse model response into {category: set(products)} format
    - Compare each category and its products against ideal
    - 1.0 = perfect match, proportional score for partial matches
    """
    # Parse model response
    if response is None or response.strip() == "":
        if not ideal_answer:
            return 1.0
        return 0.0

    parsed = read_string_to_list(response)

    # If parsing failed
    if parsed is None:
        if not ideal_answer:
            return 1.0
        return 0.0

    # Build {category: set(products)} from model response
    response_dict = {}
    for item in parsed:
        if isinstance(item, dict):
            cat = item.get("category", "")
            prods = item.get("products", [])
            if cat:
                if cat not in response_dict:
                    response_dict[cat] = set()
                if prods:
                    response_dict[cat].update(prods)

    # Handle empty ideal (no products expected)
    if not ideal_answer:
        if not response_dict and (not parsed or parsed == []):
            return 1.0
        return 0.0

    # Compare response vs ideal
    # Score = average of per-category scores
    if not ideal_answer:
        return 1.0 if not response_dict else 0.0

    total_categories = len(ideal_answer)
    matched_score = 0.0

    for category, ideal_products in ideal_answer.items():
        if category not in response_dict:
            # Category missing entirely
            continue

        response_products = response_dict[category]

        if not ideal_products and not response_products:
            # Both empty — category-only match
            matched_score += 1.0
        elif not ideal_products:
            # Ideal has no specific products (category-level query)
            matched_score += 1.0
        else:
            # Compare product sets
            ideal_set = ideal_products if isinstance(ideal_products, set) else set(ideal_products)
            resp_set = response_products if isinstance(response_products, set) else set(response_products)

            if ideal_set == resp_set:
                matched_score += 1.0
            elif ideal_set & resp_set:
                # Partial match: fraction of ideal products found
                matched_score += len(ideal_set & resp_set) / len(ideal_set)
            # else: 0 for this category

    # Check for extra categories in response not in ideal
    extra_categories = set(response_dict.keys()) - set(ideal_answer.keys())
    penalty = len(extra_categories) * 0.1  # Small penalty for hallucinated categories

    score = (matched_score / total_categories) - penalty if total_categories > 0 else (1.0 if not response_dict else 0.0)
    return max(0.0, min(1.0, score))


def run_evaluation(find_fn, prompt_name=""):
    """Run evaluation over the full dev set using the given extraction function."""
    print(f"Running evaluation with: {prompt_name}")
    print("-" * 50)

    total_score = 0.0
    num_examples = len(dev_set)

    for i, example in enumerate(dev_set):
        customer_msg = example["customer_message"]
        ideal = example["ideal_answer"]

        # Get model response
        response = find_fn(customer_msg)

        # Score it
        score = eval_response_vs_ideal(response, ideal)
        total_score += score

        status = "PASS" if score >= 0.8 else "FAIL"
        print(f"  Example {i}: [{status}] score={score:.2f} | {customer_msg[:60]}...")

    accuracy = total_score / num_examples
    print()
    print(f"Overall accuracy: {accuracy:.1%} ({total_score:.1f}/{num_examples})")
    return accuracy


def demo():
    # Evaluate Prompt v1
    print("=== Prompt v1 Evaluation ===")
    print()
    acc_v1 = run_evaluation(find_category_and_product_v1, "find_category_and_product_v1")
    print()

    # Evaluate Prompt v2 (refined)
    print("=== Prompt v2 Evaluation (refined) ===")
    print()
    acc_v2 = run_evaluation(find_category_and_product_v2, "find_category_and_product_v2")
    print()

    # Compare
    print("=== Comparison ===")
    print(f"  Prompt v1: {acc_v1:.1%}")
    print(f"  Prompt v2: {acc_v2:.1%}")
    if acc_v2 > acc_v1:
        print("  -> v2 is better!")
    elif acc_v2 == acc_v1:
        print("  -> Same performance.")
    else:
        print("  -> v1 was better — v2 regressed!")


if __name__ == "__main__":
    demo()
