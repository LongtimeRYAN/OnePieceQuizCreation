import streamlit as st

class TriviaGame:
    def __init__(self):
        self.questions = []
        self.keywords = []
        self.score = 0
        self.correct_count = 0
        self.incorrect_count = 0

    def add_question(self, question, keywords):
        self.questions.append(question)
        self.keywords.append([keyword.lower() for keyword in keywords])

    def has_more_questions(self):
        return st.session_state.current_question < len(self.questions)

    def get_current_question(self):
        if self.has_more_questions():
            return self.questions[st.session_state.current_question]
        return None

def main():
    # Initialize session state variables for the quiz
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'finished' not in st.session_state:
        st.session_state.finished = False
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False
    if 'correct_clicked' not in st.session_state:
        st.session_state.correct_clicked = False
    if 'incorrect_clicked' not in st.session_state:
        st.session_state.incorrect_clicked = False

    # Start screen or quiz rendering logic
    if not st.session_state.quiz_started:
        display_start_screen()
    else:
        if st.session_state.finished:
            display_end_screen(st.session_state.game)
        else:
            render_quiz(st.session_state.game)

def display_start_screen():
    st.markdown("<h1 style='text-align: center;'>THE ULTIMATE ONE PIECE QUIZ</h1>", unsafe_allow_html=True)
    st.write("Test your knowledge of the entire One Piece series. Do you remember every chapter by heart? Are you a real fan? Or are you fake?")

    if st.button("Begin Quiz"):
        st.session_state.quiz_started = True
        st.rerun()

def render_quiz(game):
    # Calculate progress
    progress = (st.session_state.current_question + 1) / len(game.questions)
    st.progress(progress)
    st.write(f"Progress: {st.session_state.current_question + 1}/{len(game.questions)}")

    if game.has_more_questions():
        question = game.get_current_question()
        st.header(f"Question {st.session_state.current_question + 1}")
        st.write(question)

        # Input and answer buttons
        answer = st.text_input("Your answer:", key=f'input_answer_{st.session_state.current_question}')

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Reveal Answer") and not st.session_state.answer_submitted:
                correct_keywords = ", ".join(game.keywords[st.session_state.current_question])
                st.write(f"Correct Answer: {correct_keywords}")
                st.session_state.answer_submitted = True

        with col2:
            if st.session_state.answer_submitted and not (st.session_state.correct_clicked or st.session_state.incorrect_clicked):
                if st.button("Correct"):
                    game.score += 1
                    game.correct_count += 1
                    st.session_state.correct_clicked = True

        with col3:
            if st.session_state.answer_submitted and not (st.session_state.correct_clicked or st.session_state.incorrect_clicked):
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

def display_end_screen(game):
    st.header("Quiz Completed!")
    st.write(f"Your final score is: {game.score}/{len(game.questions)}")
    st.write(f"Correct Answers: {game.correct_count}")
    st.write(f"Incorrect Answers: {game.incorrect_count}")

    total_questions = len(game.questions)
    total_answered = game.correct_count + game.incorrect_count
    if total_questions > 0:
        percentage_correct = (game.correct_count / total_questions) * 100
        st.write(f"Percentage Correct: {percentage_correct:.1f}% ({game.correct_count}/{total_questions})")

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

# Initialize the TriviaGame and start the quiz
if __name__ == "__main__":
    if 'game' not in st.session_state:
        st.session_state.game = TriviaGame()
        st.session_state.finished = False
        # Add questions to the game
        st.session_state.game.add_question(
            "What was the first ever named attack used by Luffy?", ["pistol"])
        st.session_state.game.add_question(
            "What did Don Krieg want to steal from Red Leg Zeff specifically? Not his Restaurant", ["log", "grand", "line"])
        st.session_state.game.add_question(
            "How did Dorry trap Luffy on Little Garden?", ["skeleton", "cave"])

    main()
