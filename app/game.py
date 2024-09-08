import streamlit as st

from typing import List, AnyStr


class TriviaGame:
    def __init__(self):
        self.questions: List[str] = []
        self.answers: List[str] = []
        self.score: int = 0
        self.correct_count: int = 0
        self.incorrect_count: int = 0

    def add_question(self, question: str, answer: str) -> None:
        self.questions.append(question)
        self.answers.append(answer)

    def has_more_questions(self) -> bool:
        return st.session_state.current_question < len(self.questions)

    def get_current_question(self) -> List[AnyStr] | None:
        if self.has_more_questions():
            return self.questions[st.session_state.current_question]
        return None

    def get_current_answer(self) -> List[AnyStr] | None:
        if self.has_more_questions():
            return self.answers[st.session_state.current_question]
        return None
