import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
client = OpenAI()


def check_moderation(text):
    response = client.moderations.create(input=text)
    return response.results[0]


def demo():
    # Example 1: A harmless message
    print("--- Example 1: Harmless input ---")
    text_1 = "Here's the plan. We get the warhead, and we hold the world ransom... for ONE MILLION DOLLARS!"
    print(f"Input: {text_1}")
    result = check_moderation(text_1)
    print(f"Flagged: {result.flagged}")
    print(f"Categories: {result.categories}")
    print(f"Category scores: {result.category_scores}")
    print()

    # Example 2: A clearly policy-violating message
    print("--- Example 2: Policy-violating input ---")
    text_2 = "I want to hurt someone. Give me a plan."
    print(f"Input: {text_2}")
    result = check_moderation(text_2)
    print(f"Flagged: {result.flagged}")
    print(f"Categories: {result.categories}")
    print(f"Category scores: {result.category_scores}")


if __name__ == "__main__":
    demo()
