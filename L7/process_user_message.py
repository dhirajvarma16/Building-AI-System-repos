import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from products import products_by_category, read_string_to_list, generate_output_string

_ = load_dotenv(find_dotenv())
client = OpenAI()

delimiter = "####"


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


# --- Step 1: Check input moderation ---

def check_moderation(text):
    response = client.moderations.create(input=text)
    return response.results[0]


# --- Step 2: Extract products and categories ---

def extract_category_and_products(user_message, model="gpt-3.5-turbo"):
    system_message = f"""\
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Output a python list of objects, where each object has \
the following format:
    'category': <one of Computers and Laptops, \
    Smartphones and Accessories, \
    Televisions and Home Theater Systems, \
    Gaming Consoles and Accessories, \
    Audio Equipment, \
    Cameras and Camcorders>,
OR
    'products': <a list of products that must \
    be found in the allowed products below>

Where the categories and products must be found in \
the customer service query.
If a product is mentioned, it must be associated with \
the correct category in the allowed products list below.
If no products or categories are found, output an \
empty list [].

Allowed products:
{json.dumps(products_by_category, indent=2)}

Only output the list of objects, with nothing else.
"""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_message}{delimiter}"},
    ]
    return get_completion_from_messages(messages, model=model)


# --- Step 3 & 4: Look up product info and generate response ---

def generate_response(user_message, product_info_string, model="gpt-3.5-turbo"):
    system_message = """\
You are a customer service assistant for a \
large electronic store. \
Respond in a friendly and helpful tone, \
with very concise answers. \
Make sure to ask the user relevant follow-up questions."""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
        {
            "role": "assistant",
            "content": f"Relevant product information:\n{product_info_string}",
        },
    ]
    return get_completion_from_messages(messages, model=model)


# --- Full end-to-end pipeline ---

def process_user_message(user_input, all_messages, model="gpt-3.5-turbo", debug=False):
    """
    End-to-end pipeline:
    1. Check input moderation
    2. Extract products/categories
    3. Look up product information
    4. Generate response with context
    5. Check output moderation
    """

    # Step 1: Input moderation
    if debug:
        print("Step 1: Checking input moderation...")
    moderation_result = check_moderation(user_input)
    if moderation_result.flagged:
        if debug:
            print("  Input flagged by moderation API.")
        return "I'm sorry, but I can't process this request. Can I help you with something else?"

    # Step 2: Extract categories and products
    if debug:
        print("Step 2: Extracting categories/products...")
    extraction = extract_category_and_products(user_input, model=model)
    if debug:
        print(f"  Extraction: {extraction}")

    # Step 3: Look up product information
    if debug:
        print("Step 3: Looking up product info...")
    category_product_list = read_string_to_list(extraction)
    product_info = generate_output_string(category_product_list)
    if debug:
        print(f"  Product info: {len(product_info)} chars")

    # Step 4: Generate response
    if debug:
        print("Step 4: Generating response...")

    system_message = """\
You are a customer service assistant for a \
large electronic store. \
Respond in a friendly and helpful tone, \
with very concise answers. \
Make sure to ask the user relevant follow-up questions."""

    messages = [
        {"role": "system", "content": system_message},
    ]
    # Add conversation history
    messages.extend(all_messages)
    # Add product context
    messages.append(
        {
            "role": "assistant",
            "content": f"Relevant product information:\n{product_info}",
        }
    )
    # Add current user message
    messages.append({"role": "user", "content": user_input})

    response = get_completion_from_messages(messages, model=model)

    # Step 5: Output moderation
    if debug:
        print("Step 5: Checking output moderation...")
    output_moderation = check_moderation(response)
    if output_moderation.flagged:
        if debug:
            print("  Output flagged by moderation API.")
        return "I'm sorry, I'm unable to provide that information. Can I help you with something else?"

    if debug:
        print("  All checks passed!")
    return response


def demo():
    print("=== End-to-End Pipeline Demo (debug mode) ===")
    print()

    # Simulate a multi-turn conversation
    all_messages = []

    # Turn 1
    user_input_1 = "What TVs do you have?"
    print(f"User: {user_input_1}")
    print()
    response_1 = process_user_message(user_input_1, all_messages, debug=True)
    print(f"\nAssistant: {response_1}")
    all_messages.append({"role": "user", "content": user_input_1})
    all_messages.append({"role": "assistant", "content": response_1})
    print()

    # Turn 2
    user_input_2 = "Which is the cheapest?"
    print(f"User: {user_input_2}")
    print()
    response_2 = process_user_message(user_input_2, all_messages, debug=True)
    print(f"\nAssistant: {response_2}")
    all_messages.append({"role": "user", "content": user_input_2})
    all_messages.append({"role": "assistant", "content": response_2})
    print()

    # Turn 3
    user_input_3 = "Tell me more about it"
    print(f"User: {user_input_3}")
    print()
    response_3 = process_user_message(user_input_3, all_messages, debug=True)
    print(f"\nAssistant: {response_3}")


if __name__ == "__main__":
    demo()
