import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
client = OpenAI()


def get_completion_and_token_count(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    content = response.choices[0].message.content

    token_dict = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return content, token_dict


def demo():
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
    response, token_count = get_completion_and_token_count(messages)
    print(f"Response:\n{response}")
    print()
    print(f"Prompt tokens:     {token_count['prompt_tokens']}")
    print(f"Completion tokens: {token_count['completion_tokens']}")
    print(f"Total tokens:      {token_count['total_tokens']}")


if __name__ == "__main__":
    demo()
