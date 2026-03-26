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


# -------------------------------------------------------
# Step 1: Extract products and categories from user query
# -------------------------------------------------------

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


# -------------------------------------------------------
# Step 2: Look up product information (via helper functions in products.py)
# -------------------------------------------------------
# This step uses: read_string_to_list() + generate_output_string()


# -------------------------------------------------------
# Step 3: Generate final customer service response
# -------------------------------------------------------

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


# -------------------------------------------------------
# Full chain: Step 1 -> Step 2 -> Step 3
# -------------------------------------------------------

def process_user_query(user_message, model="gpt-3.5-turbo"):
    """Run the full 3-step prompt chain."""
    # Step 1: Extract categories and products
    print("  Step 1: Extracting categories/products...")
    extraction = extract_category_and_products(user_message, model=model)
    print(f"  Model output: {extraction}")
    print()

    # Step 2: Look up product info
    print("  Step 2: Looking up product information...")
    category_product_list = read_string_to_list(extraction)
    product_info = generate_output_string(category_product_list)
    print(f"  Product info retrieved: {len(product_info)} chars")
    print()

    # Step 3: Generate final response
    print("  Step 3: Generating response...")
    response = generate_response(user_message, product_info, model=model)
    return response


def demo():
    # Example 1: User asks about specific products + a category
    print("=== Example 1: Specific products + category ===")
    print()
    user_msg_1 = "tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what tvs do you have?"
    print(f"User: {user_msg_1}")
    print()
    response = process_user_query(user_msg_1)
    print(f"Final Response:\n{response}")
    print()

    # Example 2: User asks about something not in our catalog
    print("=== Example 2: Product not in catalog ===")
    print()
    user_msg_2 = "my router isn't working"
    print(f"User: {user_msg_2}")
    print()
    response = process_user_query(user_msg_2)
    print(f"Final Response:\n{response}")


if __name__ == "__main__":
    demo()
