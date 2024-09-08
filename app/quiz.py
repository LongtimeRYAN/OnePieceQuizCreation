import streamlit as st


from game import TriviaGame
from components.arc_select import display_arc_selection
from components.questions import initialize_questions
from components.render import render_quiz
from components.start import display_start_screen
from components.end import display_end_screen

from logger import get_logger

logger = get_logger(__name__)


def main():
    """start app"""
    # Initialize session state variables for the quiz
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "finished" not in st.session_state:
        st.session_state.finished = False
    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False
    if "correct_clicked" not in st.session_state:
        st.session_state.correct_clicked = False
    if "incorrect_clicked" not in st.session_state:
        st.session_state.incorrect_clicked = False

    # Initialize session state for selected arc
    if "selected_arc" not in st.session_state:
        st.session_state.selected_arc = None

    # Initialize the game object if not already initialized
    if "game" not in st.session_state:
        st.session_state.game = TriviaGame()

    # Arc selection or all questions quiz rendering logic
    if not st.session_state.quiz_started:
        display_start_screen()
    elif st.session_state.selected_arc is None:
        display_arc_selection()
    else:
        # Initialize questions after arc is selected and quiz is started
        if (
            "questions_initialized" not in st.session_state
            or not st.session_state.questions_initialized
        ):
            st.session_state.game = initialize_questions(
                game=st.session_state.game, arc_name=st.session_state.selected_arc
            )
            st.session_state.questions_initialized = True

        if st.session_state.finished:
            display_end_screen(st.session_state.game)
        else:
            render_quiz(st.session_state.game)


# Initialize the TriviaGame and start the quiz
if __name__ == "__main__":
    main()
