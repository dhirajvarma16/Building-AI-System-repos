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


def eval_with_rubric(customer_message, product_context, assistant_response, model="gpt-3.5-turbo"):
    """
    Rubric-based evaluation: evaluate response quality against specific criteria
    without needing a reference answer.
    """
    system_message = """\
You are an assistant that evaluates how well the customer service agent \
answers a user question by looking at the context that the customer \
service agent is using to generate its response.

Evaluate the response based on the following criteria:

1. Is the Assistant response based only on the context provided? (Y or N)
2. Does the answer include information that is NOT provided in the context? (Y or N)
3. Is there any disagreement between the response and the context? (Y or N)
4. Count how many of the user's questions the Assistant answered.
5. For each question the user asked, is there a corresponding answer?
   List each question and its answer.

Provide detailed evaluation addressing each criterion above."""

    messages = [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": f"""\
Customer message: ```{customer_message}```
Context: ```{product_context}```
Agent response: ```{assistant_response}```

Evaluate the agent's response.""",
        },
    ]
    return get_completion_from_messages(messages, model=model, max_tokens=1000)


def demo():
    # Build product context for a test scenario
    customer_message = "tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what TVs do you have?"

    # Gather relevant product info
    product_context = ""
    for name in ["SmartX ProPhone", "FotoSnap DSLR Camera"]:
        product = get_product_by_name(name)
        if product:
            product_context += json.dumps(product, indent=2) + "\n\n"
    for product in get_products_by_category("Televisions and Home Theater Systems"):
        product_context += json.dumps(product, indent=2) + "\n\n"

    # Generate assistant response
    print("=== Generating Assistant Response ===")
    print(f"Customer: {customer_message}")
    print()
    assistant_response = generate_assistant_response(customer_message, product_context)
    print(f"Assistant: {assistant_response}")
    print()

    # Evaluate with rubric
    print("=== Rubric-Based Evaluation ===")
    print()
    evaluation = eval_with_rubric(customer_message, product_context, assistant_response)
    print(evaluation)


if __name__ == "__main__":
    demo()
