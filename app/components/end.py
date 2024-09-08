from logging import Logger
import streamlit as st

from game import TriviaGame
from logger import get_logger

logger: Logger = get_logger("components-end")


def display_end_screen(game: TriviaGame):
    st.header("Quiz Completed!")
    st.write(f"Your final score is: {game.score}/{len(game.questions)}")
    st.write(f"Correct Answers: {game.correct_count}")
    st.write(f"Incorrect Answers: {game.incorrect_count}")

    total_questions = len(game.questions)
    total_answered = game.correct_count + game.incorrect_count
    if total_questions > 0:
        percentage_correct = (game.correct_count / total_questions) * 100
        st.write(
            f"Percentage Correct: {percentage_correct:.1f}% ({game.correct_count}/{total_questions})"
        )

        # Customize messages based on the score
        if percentage_correct == 100:
            st.write("👑 You are the King of the Pirates!")
        elif 90 <= percentage_correct < 100:
            st.write("🧠 Are you from Egghead?")
        elif 70 <= percentage_correct < 90:
            st.write("💥 Supernova!")
        else:
            st.write("😞 Better luck next time!")

    # Option to restart the quiz
    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
