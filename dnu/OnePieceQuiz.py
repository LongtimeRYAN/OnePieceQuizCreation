# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 13:43:57 2024

@author: Ryan
"""


class TriviaGame:
    def __init__(self):
        self.questions = []
        self.keywords = []
        self.score = 0

    def add_question(self, question, keywords):
        """
        Add a trivia question and its associated keywords.

        :param question: str, the trivia question with a blank (e.g., "The capital of France is _____")
        :param keywords: list, a list of acceptable keywords (e.g., ["paris"])
        """
        self.questions.append(question)
        self.keywords.append([keyword.lower() for keyword in keywords])

    def ask_questions(self):
        """
        Ask the trivia questions to the user, check their answers, and update the score.
        """
        for i, question in enumerate(self.questions):
            print(f"\nQuestion {i+1}: {question}")
            answer = input("Your answer: ").strip().lower()
            answer_words = answer.split()  # Split the answer into individual words

            # Check if any word in the answer matches any keyword
            if any(keyword in answer_words for keyword in self.keywords[i]):
                print("Correct!")
                self.score += 1
            else:
                print("Incorrect!")

        print(f"\nYour final score is: {self.score}/{len(self.questions)}")


def main():
    game = TriviaGame()

    # Example of adding questions and associated keywords
    game.add_question("What was the first ever named attack used by Luffy?", ["pistol"])
    game.add_question(
        "What did Don Krieg want to steal from Red Leg Zeff specifically? Not his Restaurant",
        ["log", "grand", "line"],
    )
    game.add_question(
        "How did Dorry trap Luffy on Little Garden?", ["skeleton", "cave"]
    )

    # Start the game
    game.ask_questions()


if __name__ == "__main__":
    main()
