import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from products import products

_ = load_dotenv(find_dotenv())
client = OpenAI()

delimiter = "####"

system_message = f"""\
Follow these steps to answer the customer queries.
The customer query will be delimited with four hashtags, \
i.e. {delimiter}.

Step 1:{delimiter} First decide whether the user is \
asking a question about a specific product or products. \
Product category doesn't count.

Step 2:{delimiter} If the user is asking about \
specific products, identify whether \
the products are in the following list.
All available products:
{json.dumps(products, indent=2)}

Step 3:{delimiter} If the message contains products \
in the list above, list any assumptions that the \
user is making in their message e.g. that Laptop X \
is bigger than Laptop Y, or that Laptop Z has a 2 year \
warranty.

Step 4:{delimiter} If the user made any assumptions, \
figure out whether the assumption is true based on your \
product information.

Step 5:{delimiter} First, politely correct the \
customer's incorrect assumptions if applicable. \
Only mention or reference products in the list of \
5 available products, as these are the only 5 \
products that the store sells. \
Answer the customer in a friendly tone.

Use the following format:
Step 1:{delimiter} <step 1 reasoning>
Step 2:{delimiter} <step 2 reasoning>
Step 3:{delimiter} <step 3 reasoning>
Step 4:{delimiter} <step 4 reasoning>
Response to user:{delimiter} <response to customer>

Make sure to include {delimiter} to separate every step.
"""


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def process_user_message(user_message, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_message}{delimiter}"},
    ]
    response = get_completion_from_messages(messages, model=model)
    return response


def extract_final_response(full_response):
    """Inner monologue: extract only the user-facing response, hide reasoning steps."""
    try:
        final_response = full_response.split(delimiter)[-1].strip()
    except Exception:
        final_response = "Sorry, I'm having trouble right now. Please try asking another question."
    return final_response


def demo():
    # Example 1: User asks about a specific product with an incorrect assumption
    print("=== Example 1: Incorrect assumption about price ===")
    print()
    user_msg_1 = "by how much is the BlueWave Chromebook more expensive than the TechPro Desktop"
    print(f"User: {user_msg_1}")
    print()

    full_response = process_user_message(user_msg_1)
    print("--- Full Chain of Thought (hidden from user) ---")
    print(full_response)
    print()

    final = extract_final_response(full_response)
    print("--- Response shown to user (inner monologue) ---")
    print(final)
    print()

    # Example 2: User asks a general question (not about specific products)
    print("=== Example 2: General question ===")
    print()
    user_msg_2 = "do you sell tvs"
    print(f"User: {user_msg_2}")
    print()

    full_response = process_user_message(user_msg_2)
    print("--- Full Chain of Thought ---")
    print(full_response)
    print()

    final = extract_final_response(full_response)
    print("--- Response shown to user ---")
    print(final)


if __name__ == "__main__":
    demo()
