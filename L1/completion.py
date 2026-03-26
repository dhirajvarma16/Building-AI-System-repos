from L1.setup import client


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


def demo():
    print("Prompt: What is the capital of France?")
    response = get_completion("What is the capital of France?")
    print(f"Response: {response}")


if __name__ == "__main__":
    demo()
