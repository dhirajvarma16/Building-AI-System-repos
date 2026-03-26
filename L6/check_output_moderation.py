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


def check_moderation(text):
    """Run the Moderation API on a given text."""
    response = client.moderations.create(input=text)
    return response.results[0]


def demo():
    # Step 1: Generate a response
    print("--- Step 1: Generate a model response ---")
    system_message = """\
You are a customer service assistant for a large electronic store. \
Respond in a friendly and helpful tone, with very concise answers."""

    user_message = "tell me about the smartx pro phone"

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    response = get_completion_from_messages(messages)
    print(f"User: {user_message}")
    print(f"Response: {response}")
    print()

    # Step 2: Check the response with Moderation API
    print("--- Step 2: Check response with Moderation API ---")
    moderation_result = check_moderation(response)
    print(f"Flagged: {moderation_result.flagged}")
    print(f"Categories: {moderation_result.categories}")
    print()

    # Step 3: Decision logic
    if moderation_result.flagged:
        print("Output was flagged! Returning fallback response.")
        print("Fallback: Sorry, I'm unable to provide that information.")
    else:
        print("Output passed moderation. Safe to show to user.")


if __name__ == "__main__":
    demo()
