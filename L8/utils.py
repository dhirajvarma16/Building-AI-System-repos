import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from products import products_by_category

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


def find_category_and_product_v1(user_message, model="gpt-3.5-turbo"):
    """Prompt v1: basic extraction."""
    system_message = f"""\
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Output a python list of json objects, where each object has \
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


def find_category_and_product_v2(user_message, model="gpt-3.5-turbo"):
    """Prompt v2: refined with stricter JSON-only output instruction."""
    system_message = f"""\
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Output a python list of json objects, where each object has \
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

Do not output any additional text that is not in JSON format.
Do not write any explanatory text after outputting the requested JSON.

Allowed products:

Computers and Laptops category:
{json.dumps(products_by_category["Computers and Laptops"], indent=2)}

Smartphones and Accessories category:
{json.dumps(products_by_category["Smartphones and Accessories"], indent=2)}

Televisions and Home Theater Systems category:
{json.dumps(products_by_category["Televisions and Home Theater Systems"], indent=2)}

Gaming Consoles and Accessories category:
{json.dumps(products_by_category["Gaming Consoles and Accessories"], indent=2)}

Audio Equipment category:
{json.dumps(products_by_category["Audio Equipment"], indent=2)}

Cameras and Camcorders category:
{json.dumps(products_by_category["Cameras and Camcorders"], indent=2)}

Only output the list of objects, with nothing else.
"""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_message}{delimiter}"},
    ]
    return get_completion_from_messages(messages, model=model)
