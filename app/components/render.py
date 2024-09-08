from logging import Logger
import streamlit as st

from game import TriviaGame

from logger import get_logger

logger: Logger = get_logger("components-render")


def render_quiz(game: TriviaGame):
    total_questions = len(game.questions)

    if total_questions == 0:
        st.error("No questions available for the selected arc.")
        return  # Stop rendering if there are no questions

    # Calculate progress
    progress = (st.session_state.current_question + 1) / total_questions
    st.progress(progress)
    st.write(f"Progress: {st.session_state.current_question + 1}/{total_questions}")

    if game.has_more_questions():
        question = game.get_current_question()
        st.header(f"Question {st.session_state.current_question + 1}")
        st.write(question)

        # Input and answer buttons
        answer = st.text_input(
            "Your answer:", key=f"input_answer_{st.session_state.current_question}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Reveal Answer") and not st.session_state.answer_submitted:
                correct_answer = game.get_current_answer()
                st.write(f"Correct Answer: {correct_answer}")
                st.session_state.answer_submitted = True

        with col2:
            if st.session_state.answer_submitted and not (
                st.session_state.correct_clicked or st.session_state.incorrect_clicked
            ):
                if st.button("Correct"):
                    game.score += 1
                    game.correct_count += 1
                    st.session_state.correct_clicked = True

        with col3:
            if st.session_state.answer_submitted and not (
                st.session_state.correct_clicked or st.session_state.incorrect_clicked
            ):
                if st.button("Incorrect"):
                    game.incorrect_count += 1
                    st.session_state.incorrect_clicked = True

        # "Next Question" button, always visible after answer reveal
        if st.session_state.answer_submitted:
            if st.button("Next Question"):
                st.session_state.current_question += 1
                if not game.has_more_questions():
                    st.session_state.finished = True
                st.session_state.answer_submitted = False
                st.session_state.correct_clicked = False
                st.session_state.incorrect_clicked = False
                st.rerun()

    # Display stats throughout the quiz
    st.write("---")
    st.write(f"Correct: {game.correct_count}")
    st.write(f"Incorrect: {game.incorrect_count}")
    total_answered = game.correct_count + game.incorrect_count
    if total_answered > 0:
        percentage_correct = (game.correct_count / total_answered) * 100
        st.write(f"Percentage Correct: {percentage_correct:.1f}%")
