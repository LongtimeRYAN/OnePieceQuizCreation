import streamlit as st


def display_start_screen() -> None:
    st.markdown(
        "<h1 style='text-align: center;'>THE ULTIMATE ONE PIECE QUIZ</h1>",
        unsafe_allow_html=True,
    )
    st.write(
        "Test your knowledge of the entire One Piece series. Do you remember every chapter by heart? Are you a real fan? Or are you fake?"
    )

    if st.button("Begin Quiz"):
        st.session_state.quiz_started = True
        st.session_state.selected_arc = (
            None  # Reset selected arc when starting new quiz
        )
        st.rerun()
