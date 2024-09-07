# trivia_game_streamlit.py

import streamlit as st

class TriviaGame:
    def __init__(self):
        self.questions = []
        self.keywords = []
        self.score = 0
        self.current_question = 0

    def add_question(self, question, keywords):
        """
        Add a trivia question and its associated keywords.

        :param question: str, the trivia question with a blank (e.g., "The capital of France is _____")
        :param keywords: list, a list of acceptable keywords (e.g., ["paris"])
        """
        self.questions.append(question)
        self.keywords.append([keyword.lower() for keyword in keywords])

    def check_answer(self, answer):
        """
        Check the user's answer against the current question's keywords.

        :param answer: str, the user's answer
        :return: bool, True if correct, False otherwise
        """
        answer_words = answer.strip().lower().split()
        if any(keyword in answer_words for keyword in self.keywords[self.current_question]):
            self.score += 1
            return True
        return False

    def has_more_questions(self):
        return self.current_question < len(self.questions)

    def get_current_question(self):
        if self.has_more_questions():
            return self.questions[self.current_question]
        return None

    def next_question(self):
        self.current_question += 1

def main():
    st.title("One Piece Trivia Quiz")
    st.write("Test your One Piece knowledge!")

    # Initialize the game in session state
    if 'game' not in st.session_state:
        st.session_state.game = TriviaGame()
        # Add questions
        st.session_state.game.add_question(
            "What was the first ever named attack used by Luffy?", ["pistol"])
        st.session_state.game.add_question(
            "What did Don Krieg want to steal from Red Leg Zeff specifically? Not his Restaurant", ["log", "grand", "line"])
        st.session_state.game.add_question(
            "How did Dorry trap Luffy on Little Garden?", ["skeleton", "cave"])

    game = st.session_state.game

    # Initialize user's answer in session state
    if 'answer' not in st.session_state:
        st.session_state.answer = ''

    # Initialize feedback in session state
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ''

    # Display current question
    if game.has_more_questions():
        question = game.get_current_question()
        st.header(f"Question {game.current_question + 1}")
        st.write(question)
        # Input for the answer
        st.session_state.answer = st.text_input("Your answer:", key='input_answer')

        # Button to submit the answer
        if st.button("Submit Answer"):
            if st.session_state.answer:
                correct = game.check_answer(st.session_state.answer)
                if correct:
                    st.session_state.feedback = "✅ Correct!"
                else:
                    correct_keywords = ", ".join(game.keywords[game.current_question])
                    st.session_state.feedback = f"❌ Incorrect! Acceptable answers include: {correct_keywords}."
                # Move to the next question after a short delay
                game.next_question()
            else:
                st.session_state.feedback = "Please enter an answer."

        # Display feedback
        if st.session_state.feedback:
            st.write(st.session_state.feedback)
    else:
        # Quiz is over
        st.header("Quiz Completed!")
        st.write(f"Your final score is: {game.score}/{len(game.questions)}")
        # Option to restart the quiz
        if st.button("Restart Quiz"):
            st.session_state.game = TriviaGame()
            game = st.session_state.game
            # Re-add questions
            game.add_question(
                "What was the first ever named attack used by Luffy?", ["pistol"])
            game.add_question(
                "What did Don Krieg want to steal from Red Leg Zeff specifically? Not his Restaurant", ["log", "grand", "line"])
            game.add_question(
                "How did Dorry trap Luffy on Little Garden?", ["skeleton", "cave"])
            st.experimental_rerun()

if __name__ == "__main__":
    main()
