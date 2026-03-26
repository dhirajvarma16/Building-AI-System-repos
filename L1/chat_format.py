import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
client = OpenAI()


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


def demo():
    # Demo 1: Dr. Seuss style
    print("System: You are an assistant who responds in the style of Dr. Seuss.")
    print("User: write me a very short poem about a happy carrot")
    messages = [
        {
            "role": "system",
            "content": "You are an assistant who responds in the style of Dr. Seuss.",
        },
        {
            "role": "user",
            "content": "write me a very short poem about a happy carrot",
        },
    ]
    response = get_completion_from_messages(messages, temperature=1)
    print(f"Response:\n{response}")
    print()

    # Demo 2: One-sentence style
    print("System: You are an assistant who responds in one sentence.")
    print("User: write me a very short poem about a happy carrot")
    messages = [
        {
            "role": "system",
            "content": "You are an assistant who responds in one sentence.",
        },
        {
            "role": "user",
            "content": "write me a very short poem about a happy carrot",
        },
    ]
    response = get_completion_from_messages(messages, temperature=1)
    print(f"Response:\n{response}")


if __name__ == "__main__":
    demo()
