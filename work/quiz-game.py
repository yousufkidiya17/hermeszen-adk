import json
import random
import sys

LETTERS = "abcd"


def load_questions(path="questions.json"):
    """Load and shuffle 10 random questions from the JSON file."""
    with open(path) as f:
        data = json.load(f)
    questions = data["questions"]
    if len(questions) < 10:
        raise ValueError("Need at least 10 questions in questions.json")
    return random.sample(questions, 10)


def ask(question):
    """Ask one multiple-choice question; return True if answered correctly."""
    options = question["options"]
    print("\n" + question["question"])
    for i, opt in enumerate(options):
        print(f"  {LETTERS[i]}) {opt}")
    while True:
        answer = input("Your answer (a/b/c/d): ").strip().lower()
        if answer in LETTERS:
            return answer == question["answer"]
        print("Please enter a, b, c or d.")


def main():
    try:
        questions = load_questions()
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print("Could not load questions:", e)
        sys.exit(1)

    score = 0
    total = len(questions)
    for num, q in enumerate(questions, 1):
        print(f"\nQuestion {num} of {total}")
        correct = ask(q)
        if correct:
            score += 1
            print("Correct!")
        else:
            idx = LETTERS.index(q["answer"])
            print(f"Wrong. The answer was: {q['options'][idx]}")

    print(f"\nFinal result: {score}/{total}")
    if score == total:
        print("Perfect score — excellent!")
    elif score >= 7:
        print("Good job!")
    else:
        print("Better luck next time.")


if __name__ == "__main__":
    main()