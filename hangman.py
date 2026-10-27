"""Task 1: Hangman Word Guessing Game (Console).

Guess the hidden word one letter at a time. You get 6 wrong guesses.
Repeated guesses are not penalised.
"""
import os
import random

STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========""",
]

MAX_MISTAKES = 6
DEFAULT_WORDS = [
    "python", "variable", "function", "internship", "keyboard", "algorithm",
    "developer", "terminal", "software", "database", "network", "compiler",
]


def load_words():
    """Load words from words.txt if present, else use the built-in list."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            words = [w.strip().lower() for w in f if w.strip().isalpha() and len(w.strip()) >= 4]
        if words:
            return words
    return DEFAULT_WORDS


def masked(word, guessed):
    return " ".join(c if c in guessed else "_" for c in word)


def play(words):
    word = random.choice(words)
    guessed = set()
    mistakes = 0

    print("\n=== HANGMAN ===")
    while True:
        print(STAGES[mistakes])
        print("\nWord:", masked(word, guessed))
        print("Guessed:", " ".join(sorted(guessed)) or "-")
        print(f"Mistakes left: {MAX_MISTAKES - mistakes}")

        if all(c in guessed for c in word):
            print(f"\n🎉 You won! The word was '{word}'.")
            return
        if mistakes >= MAX_MISTAKES:
            print(f"\n💀 You lost. The word was '{word}'.")
            return

        guess = input("\nGuess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
        elif guess in guessed:
            print(f"You already guessed '{guess}'. No penalty.")
        else:
            guessed.add(guess)
            if guess in word:
                print("Correct!")
            else:
                mistakes += 1
                print("Wrong!")


def main():
    words = load_words()
    while True:
        play(words)
        if input("\nPlay again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
