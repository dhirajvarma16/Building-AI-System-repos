import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

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


# Sample product information (used as ground truth for evaluation)
product_info = """\
SmartX ProPhone:
- Brand: SmartX
- Model: SX-PP10
- Price: $899.99
- Warranty: 1 year
- Rating: 4.6/5
- Features: 6.1-inch display, 128GB storage, 12MP dual camera, 5G
- Description: A powerful smartphone with advanced camera features.
"""


def evaluate_response(customer_message, assistant_response, product_information, model="gpt-3.5-turbo"):
    """Ask the model to evaluate whether the response is accurate and helpful."""
    system_message = """\
You are an assistant that evaluates whether \
customer service agent responses sufficiently \
answer customer questions, and also validates that \
all the facts the assistant cites from the product \
information are correct.
The product information and user and agent messages \
will be delimited by 3 backticks, i.e. ```.
Respond with a Y or N character, with no punctuation:
Y - if the output sufficiently answers the question \
AND the response correctly uses product information
N - otherwise

Output a single character."""

    messages = [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": f"""\
Customer message: ```{customer_message}```
Product information: ```{product_information}```
Agent response: ```{assistant_response}```

Does the response use the retrieved information correctly?
Does the response sufficiently answer the question?

Output Y or N""",
        },
    ]
    return get_completion_from_messages(messages, model=model, max_tokens=1)


def demo():
    # Step 1: Simulate a customer question and agent response
    customer_message = "tell me about the smartx pro phone and its camera. Is it worth the price?"

    # Good response (uses product info correctly)
    good_response = """\
The SmartX ProPhone (SX-PP10) is priced at $899.99. \
It features a 6.1-inch display, 128GB storage, and a \
12MP dual camera system with 5G connectivity. \
With a rating of 4.6 out of 5, it's well-regarded. \
The camera is great for everyday photography. \
It comes with a 1-year warranty. \
Would you like to know about any accessories for it?"""

    # Bad response (contains incorrect facts)
    bad_response = """\
The SmartX ProPhone costs $499.99 and has a \
48MP triple camera system with 256GB storage. \
It has a 2-year warranty and is rated 4.9 out of 5. \
Definitely worth the price!"""

    # Step 2: Evaluate the good response
    print("=== Evaluating Good Response ===")
    print(f"Customer: {customer_message}")
    print(f"Agent: {good_response}")
    print()
    result = evaluate_response(customer_message, good_response, product_info)
    print(f"Evaluation result: {result}")
    print()

    # Step 3: Evaluate the bad response (incorrect facts)
    print("=== Evaluating Bad Response (incorrect facts) ===")
    print(f"Customer: {customer_message}")
    print(f"Agent: {bad_response}")
    print()
    result = evaluate_response(customer_message, bad_response, product_info)
    print(f"Evaluation result: {result}")


if __name__ == "__main__":
    demo()
