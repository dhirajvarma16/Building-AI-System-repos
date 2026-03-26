import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tiktoken
from completion import get_completion


def demo():
    # Demo 1: Reverse "lollipop" — model struggles with tokenization
    print("Prompt: Take the letters in lollipop and reverse them")
    response = get_completion("Take the letters in lollipop and reverse them")
    print(f"Response: {response}")
    print()

    # Demo 2: Reverse with dashes — each letter becomes its own token
    print("Prompt: Take the letters in l-o-l-l-i-p-o-p and reverse them")
    response = get_completion(
        "Take the letters in l-o-l-l-i-p-o-p and reverse them"
    )
    print(f"Response: {response}")
    print()

    # Demo 3: Visualize tokenization with tiktoken
    print("--- Tokenization Visualization ---")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    text = "lollipop"
    tokens = encoding.encode(text)
    print(f"Text: {text}")
    print(f"Tokens: {tokens}")
    print(f"Token strings: {[encoding.decode([t]) for t in tokens]}")
    print(f"Number of tokens: {len(tokens)}")
    print()

    text2 = "l-o-l-l-i-p-o-p"
    tokens2 = encoding.encode(text2)
    print(f"Text: {text2}")
    print(f"Tokens: {tokens2}")
    print(f"Token strings: {[encoding.decode([t]) for t in tokens2]}")
    print(f"Number of tokens: {len(tokens2)}")


if __name__ == "__main__":
    demo()
