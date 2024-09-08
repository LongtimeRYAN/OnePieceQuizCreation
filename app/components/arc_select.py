from logging import Logger
import streamlit as st

from game import TriviaGame
from logger import get_logger

logger: Logger = get_logger("arc-select")


def reset_on_arc_change() -> None:
    """Reset questions_initialized state on selectbox change"""
    st.session_state.questions_initialized = False


def display_arc_selection():
    """display selectbox for arc selection"""
    st.markdown(
        "<h2 style='text-align: center;'>Select an Arc:</h2>", unsafe_allow_html=True
    )
    arcs = ["Arlong Park", "Syrup Village"]
    selected_arc = st.selectbox(
        label="Choose an arc",
        options=arcs,
        index=None,
        on_change=reset_on_arc_change,
        key="arc_selection",
    )

    # Log the selected arc to confirm it's correct
    logger.info(f"Arc selected: {selected_arc}")
    st.write(f"Selected arc: {selected_arc}")

    # st.session_state.selected_arc = selected_arc

    if st.button("Start Quiz"):
        st.session_state.selected_arc = selected_arc

        # Reset game and session state when starting a new quiz
        st.session_state.game = TriviaGame()
        st.session_state.quiz_started = True
        st.session_state.questions_initialized = False
        st.session_state.current_question = 0  # Reset current question
        st.session_state.finished = False
        st.session_state.answer_submitted = False
        st.session_state.correct_clicked = False
        st.session_state.incorrect_clicked = False
        st.rerun()
