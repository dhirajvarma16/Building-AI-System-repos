import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
client = OpenAI()

delimiter = "####"

system_message = f"""\
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Classify each query into a primary category \
and a secondary category.
Provide your output in json format with the \
keys: primary and secondary.

Primary categories: Billing, Technical Support, \
Account Management, or General Inquiry.

Billing secondary categories:
Unsubscribe or upgrade
Add a payment method
Explanation for charge
Dispute a charge

Technical Support secondary categories:
General troubleshooting
Device compatibility
Software updates

Account Management secondary categories:
Password reset
Update personal information
Close account
Account security

General Inquiry secondary categories:
Product information
Pricing
Feedback
Speak to a human
"""


def classify_query(user_message, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_message}{delimiter}"},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


def demo():
    # Example 1: Account Management — Close account
    query_1 = "I want you to delete my profile and all of my user data"
    print(f"Customer query: {query_1}")
    print(f"Classification:\n{classify_query(query_1)}")
    print()

    # Example 2: General Inquiry — Product information
    query_2 = "Tell me more about your flat screen TVs"
    print(f"Customer query: {query_2}")
    print(f"Classification:\n{classify_query(query_2)}")


if __name__ == "__main__":
    demo()
