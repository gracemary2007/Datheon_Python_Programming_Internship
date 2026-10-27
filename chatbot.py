"""Task 4: Rule-Based Interactive Terminal Assistant (Chatbot).

Matches user input against regex patterns loaded from faqs.json.
Supports multiple intents in one message, a fallback reply, and exit commands.
"""
import json
import os
import re

EXIT_WORDS = {"bye", "exit", "quit"}
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faqs.json")


def load_data(path=DATA_FILE):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for intent in data["intents"]:
        intent["compiled"] = [re.compile(p) for p in intent["patterns"]]
    return data


def normalize(text):
    text = text.lower().strip()
    return re.sub(r"[^\w\s]", "", text)


def match_intents(text, intents):
    """Return all intents whose patterns match (multi-intent support)."""
    return [i for i in intents if any(p.search(text) for p in i["compiled"])]


def respond(user_input, data):
    text = normalize(user_input)
    if not text:
        return "Please type something."
    matches = match_intents(text, data["intents"])
    if not matches:
        return data["fallback"]
    return "\n".join(m["response"] for m in matches)


def main():
    try:
        data = load_data()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise SystemExit(f"Could not load faqs.json: {e}")

    print("ShopBot: Hi! Type 'bye', 'exit' or 'quit' to leave.")
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nShopBot: Goodbye!")
            break
        if normalize(user) in EXIT_WORDS:
            print("ShopBot: Goodbye! Have a great day.")
            break
        print("ShopBot:", respond(user, data))


if __name__ == "__main__":
    main()
