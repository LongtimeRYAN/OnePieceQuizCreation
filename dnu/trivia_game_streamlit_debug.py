import streamlit as st


class TriviaGame:
    def __init__(self):
        self.questions = []
        self.keywords = []
        self.score = 0

    def add_question(self, question, keywords):
        self.questions.append(question)
        self.keywords.append([keyword.lower() for keyword in keywords])

    def check_answer(self, answer):
        answer_words = answer.strip().lower().split()
        if any(
            keyword in answer_words
            for keyword in self.keywords[st.session_state.current_question]
        ):
            self.score += 1
            return True
        return False

    def has_more_questions(self):
        return st.session_state.current_question < len(self.questions)

    def get_current_question(self):
        if self.has_more_questions():
            return self.questions[st.session_state.current_question]
        return None


def main():
    st.title("One Piece Trivia Quiz")
    st.write("Test your One Piece knowledge!")

    # Initialize session state
    if "game" not in st.session_state:
        st.session_state.game = TriviaGame()
        st.session_state.feedback = None
        st.session_state.answer_submitted = False
        st.session_state.current_question = 0
        st.session_state.finished = False

        st.session_state.game.add_question(
            "What was the first ever named attack used by Luffy?", ["pistol"]
        )
        st.session_state.game.add_question(
            "What did Don Krieg want to steal from Red Leg Zeff specifically? Not his Restaurant",
            ["log", "grand", "line"],
        )
        st.session_state.game.add_question(
            "How did Dorry trap Luffy on Little Garden?", ["skeleton", "cave"]
        )

    game = st.session_state.game

    # Debugging information
    st.write("### Debug Info:")
    st.write(f"Current Question Index: {st.session_state.current_question}")
    st.write(f"Answer Submitted: {st.session_state.answer_submitted}")
    st.write(f"Feedback: {st.session_state.feedback}")
    st.write(f"Finished: {st.session_state.finished}")

    if st.session_state.finished:
        st.header("Quiz Completed!")
        st.write(f"Your final score is: {game.score}/{len(game.questions)}")
        if st.button("Restart Quiz"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
    else:
        render_quiz(game)


def render_quiz(game):
    progress = st.session_state.current_question / len(game.questions)
    st.progress(progress)

    if game.has_more_questions():
        question = game.get_current_question()
        st.header(f"Question {st.session_state.current_question + 1}")
        st.write(question)

        answer = st.text_input(
            "Your answer:", key=f"input_answer_{st.session_state.current_question}"
        )

        if st.button("Submit Answer") and not st.session_state.answer_submitted:
            if answer:
                correct = game.check_answer(answer)
                if correct:
                    st.session_state.feedback = "✅ Correct!"
                else:
                    correct_keywords = ", ".join(
                        game.keywords[st.session_state.current_question]
                    )
                    st.session_state.feedback = (
                        f"❌ Incorrect! Acceptable answers include: {correct_keywords}."
                    )

                st.session_state.answer_submitted = True

        if st.session_state.answer_submitted:
            st.write(st.session_state.feedback)
            if st.button("Next Question"):
                st.write("Next Question button pressed!")  # Debugging statement
                st.session_state.current_question += 1
                st.session_state.answer_submitted = False
                st.session_state.feedback = None


# Run the application
if __name__ == "__main__":
    main()
