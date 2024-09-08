# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 13:56:59 2024

@author: Ryan
"""

import tkinter as tk
from tkinter import messagebox


class TriviaGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia Quiz")
        self.questions = []
        self.keywords = []
        self.score = 0
        self.current_question = 0

        # Creating GUI elements
        self.question_label = tk.Label(root, text="", wraplength=400, justify="left")
        self.question_label.pack(pady=20)

        self.answer_entry = tk.Entry(root, width=50)
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(root, text=f"Score: {self.score}")
        self.score_label.pack(pady=10)

        # Add your questions here
        self.add_question(
            "What was the first ever named attack used by Luffy?", ["pistol"]
        )
        self.add_question(
            "What did Don Krieg want to steal from Red Leg Zeff specifically? Not his Restaurant",
            ["log", "grand", "line"],
        )
        self.add_question(
            "How did Dorry trap Luffy on Little Garden?", ["skeleton", "cave"]
        )

        self.display_question()

    def add_question(self, question, keywords):
        """
        Add a trivia question and its associated keywords.
        :param question: str, the trivia question with a blank (e.g., "The capital of France is _____")
        :param keywords: list, a list of acceptable keywords (e.g., ["paris"])
        """
        self.questions.append(question)
        self.keywords.append([keyword.lower() for keyword in keywords])

    def display_question(self):
        """Display the current question."""
        if self.current_question < len(self.questions):
            self.question_label.config(text=self.questions[self.current_question])
            self.answer_entry.delete(0, tk.END)
            self.result_label.config(text="")
        else:
            self.end_quiz()

    def check_answer(self):
        """Check the user's answer and update the score."""
        answer = self.answer_entry.get().strip().lower()
        answer_words = answer.split()

        if any(
            keyword in answer_words for keyword in self.keywords[self.current_question]
        ):
            self.result_label.config(text="Correct!", fg="green")
            self.score += 1
        else:
            self.result_label.config(text="Incorrect!", fg="red")

        self.score_label.config(text=f"Score: {self.score}")
        self.current_question += 1
        self.root.after(2000, self.display_question)

    def end_quiz(self):
        """Display final score and end the quiz."""
        messagebox.showinfo(
            "Quiz Completed", f"Your final score is: {self.score}/{len(self.questions)}"
        )
        self.root.quit()


def main():
    root = tk.Tk()
    app = TriviaGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
