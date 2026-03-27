import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from products import products, get_product_by_name, get_products_by_category

_ = load_dotenv(find_dotenv())
client = OpenAI()


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def generate_assistant_response(customer_message, product_context, model="gpt-3.5-turbo"):
    """Generate a customer service response given product context."""
    system_message = """\
You are a customer service assistant for a \
large electronic store. \
Respond in a friendly and helpful tone, \
with very concise answers. \
Make sure to ask the user relevant follow-up questions."""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": customer_message},
        {"role": "assistant", "content": f"Relevant product information:\n{product_context}"},
    ]
    return get_completion_from_messages(messages, model=model)


def eval_vs_ideal(customer_message, ideal_answer, assistant_response, model="gpt-3.5-turbo"):
    """
    Ideal-answer comparison: compare model output against an expert-written
    reference response. Returns a letter grade (A-E) with explanation.

    Grading scale:
      A - Assistant answer is a subset of the expert answer and is fully consistent
      B - Assistant answer is a superset of the expert answer and is fully consistent
      C - Assistant answer contains all the same details as the expert answer
      D - There is a disagreement between the assistant answer and the expert answer
      E - The answers differ, but these differences are not factually important
    """
    system_message = """\
You are an assistant that evaluates how well the customer service agent \
answers a user question by comparing the response to the ideal (expert) \
human-written response.

Output a single letter and then a space and then an explanation of why \
that grade was assigned.

Compare the factual content of the submitted answer with the expert answer. \
Ignore any differences in style, grammar, or punctuation.

The important thing is the factual content.

Grade the submission based on the following criteria:
A - The submitted answer is a subset of the expert answer and is fully consistent with it.
B - The submitted answer is a superset of the expert answer and is fully consistent with it.
C - The submitted answer contains all the same details as the expert answer.
D - There is a disagreement between the submitted answer and the expert answer.
E - The answers differ, but these differences don't matter from a factual standpoint.

Grade (A-E):"""

    messages = [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": f"""\
Customer message: ```{customer_message}```
Ideal answer: ```{ideal_answer}```
Submitted answer: ```{assistant_response}```

Compare the submitted answer to the ideal answer. Grade:""",
        },
    ]
    return get_completion_from_messages(messages, model=model, max_tokens=500)


def demo():
    # --- Test Case ---
    customer_message = "tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what TVs do you have?"

    # Build product context
    product_context = ""
    for name in ["SmartX ProPhone", "FotoSnap DSLR Camera"]:
        product = get_product_by_name(name)
        if product:
            product_context += json.dumps(product, indent=2) + "\n\n"
    for product in get_products_by_category("Televisions and Home Theater Systems"):
        product_context += json.dumps(product, indent=2) + "\n\n"

    # Expert ideal answer
    ideal_answer = """\
Of course! Here's what I know:

The SmartX ProPhone (SX-PP10) is priced at $899.99. It has a 6.1-inch display, \
128GB storage, a 12MP dual camera, and 5G connectivity. It comes with a 1-year warranty.

The FotoSnap DSLR Camera (FS-DSLR200) is $599.99. It features a 24.2MP sensor, \
1080p video, a 3-inch LCD, and interchangeable lenses. It also has a 1-year warranty.

As for TVs, we have:
1. CineView 4K TV (55", $599.99)
2. CineView 8K TV (65", $2999.99)
3. CineView OLED TV (55", $1499.99)
4. SoundMax Home Theater ($399.99)
5. SoundMax Soundbar ($199.99)

Is there a specific product you'd like more details on?"""

    # Generate assistant response
    print("=== Generating Assistant Response ===")
    print(f"Customer: {customer_message}")
    print()
    assistant_response = generate_assistant_response(customer_message, product_context)
    print(f"Assistant: {assistant_response}")
    print()

    # Evaluate vs ideal
    print("=== Ideal Answer Comparison (A-E Grading) ===")
    print()
    print("Grading scale:")
    print("  A = Subset of expert, fully consistent")
    print("  B = Superset of expert, fully consistent")
    print("  C = Contains all same details as expert")
    print("  D = Disagreement with expert answer")
    print("  E = Differences are not factually important")
    print()
    grade = eval_vs_ideal(customer_message, ideal_answer, assistant_response)
    print(f"Grade: {grade}")
    print()

    # --- Test with a deliberately bad response ---
    print("=== Evaluating a Bad Response ===")
    print()
    bad_response = "The SmartX ProPhone costs $500 and has a 48MP camera. We don't carry any TVs."
    print(f"Bad response: {bad_response}")
    print()
    grade_bad = eval_vs_ideal(customer_message, ideal_answer, bad_response)
    print(f"Grade: {grade_bad}")


if __name__ == "__main__":
    demo()
