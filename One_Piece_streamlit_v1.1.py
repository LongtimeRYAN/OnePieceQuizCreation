import json
import os

import streamlit as st

import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class TriviaGame:
    def __init__(self):
        self.questions = []
        self.answers = []
        self.score = 0
        self.correct_count = 0
        self.incorrect_count = 0

    def add_question(self, question, answer):
        self.questions.append(question)
        self.answers.append(answer)

    def has_more_questions(self):
        return st.session_state.current_question < len(self.questions)

    def get_current_question(self):
        if self.has_more_questions():
            return self.questions[st.session_state.current_question]
        return None

    def get_current_answer(self):
        if self.has_more_questions():
            return self.answers[st.session_state.current_question]
        return None

    # New method to initialize questions from JSON data
    def initialize_questions(self, json_data):
        # Assuming json_data is a dictionary with 'questions' being a list of dictionaries
        for question_data in json_data.get("questions", []):
            question = question_data["question"]
            answer = question_data["answer"]
            self.add_question(question, answer)


def load_questions_from_file(arc_name: str):
    # Mapping arc names to JSON file names
    arc_file_mapping = {
        "Arlong Park": "arlong_park.json",
        "Syrup Village": "syrup_village.json",
    }

    # Get the correct directory of the script (absolute path)
    # script_dir = r"C:\Users\Ryan\Desktop\Code\OnePieceQuiz"  # Your folder path
    script_dir = os.path.dirname(
        os.path.abspath(__file__)
    )  # This gets the current directory of the script

    # Construct the full file path
    logger.info(str(arc_name))

    file_path = os.path.join(script_dir, arc_file_mapping[arc_name])

    # Debugging: Show the file path and check if it exists
    st.write(f"Attempting to load questions from file: {file_path}")
    file_exists = os.path.exists(file_path)
    st.write(f"File exists: {file_exists}")

    # If the file doesn't exist, return an empty list
    if not file_exists:
        st.error(f"No questions found for the arc: {arc_name} {script_dir}")
        return []

    # Try loading the file, catch any issues
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            print(f"Loaded data from {arc_name}: {data}")  # Print full JSON data
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return []

    # Check if 'questions' exists in the data, print questions and return them
    questions = data.get("questions", [])
    st.write(f"Questions loaded for {arc_name}: {questions}")
    return questions


def initialize_questions(game, arc_name):
    # Load questions from JSON file
    questions = load_questions_from_file(arc_name)
    for q in questions:
        game.add_question(q["question"], q["answer"])
        return game


def main():
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

    # if 'questions_initialized' not in st.session_state:
    #     st.session_state.game = initialize_questions(st.session_state.game, st.session_state.selected_arc)
    #     st.session_state.questions_initialized = True

    if (
        "questions_initialized" not in st.session_state
        and st.session_state.selected_arc is not None
    ):
        st.session_state.game = initialize_questions(
            st.session_state.game, st.session_state.selected_arc
        )
        st.session_state.questions_initialized = True

    if st.session_state.finished:
        display_end_screen(st.session_state.game)
    else:
        render_quiz(st.session_state.game)
    # else:
    #     if 'questions_initialized' not in st.session_state:
    #         st.session_state.game = initialize_questions(st.session_state.game, st.session_state.selected_arc)
    #         st.session_state.questions_initialized = True

    #     if st.session_state.finished:
    #         display_end_screen(st.session_state.game)
    #     else:
    #         render_quiz(st.session_state.game)


def display_start_screen():
    st.markdown(
        "<h1 style='text-align: center;'>THE ULTIMATE ONE PIECE QUIZ</h1>",
        unsafe_allow_html=True,
    )
    st.write(
        "Test your knowledge of the entire One Piece series. Do you remember every chapter by heart? Are you a real fan? Or are you fake?"
    )

    if st.button("Begin Quiz"):
        st.session_state.quiz_started = True
        st.rerun()


def update_selected_arc():
    # st.session_state.selected_arc = arc
    st.session_state.game = initialize_questions(
        st.session_state.game, st.session_state.selected_arc
    )
    st.session_state.questions_initialized = True


def display_arc_selection():
    st.markdown(
        "<h2 style='text-align: center;'>Select an Arc:</h2>", unsafe_allow_html=True
    )
    arcs = ["Arlong Park", "Syrup Village"]  # Add more arcs as needed
    selected_arc = st.selectbox(
        label="Select an arc",
        options=arcs,
        on_change=update_selected_arc,
    )
    st.session_state.selected_arc = selected_arc
    logger.info(selected_arc)

    # logger.info(selected_arc)
    # st.session_state.selected_arc = selected_arc

    if st.button("Start Quiz"):
        st.session_state.selected_arc = selected_arc
        st.session_state.quiz_started = True
        st.session_state.questions_initialized = (
            False  # To ensure questions are initialized only once
        )
        st.rerun()

    # if (
    #     'questions_initialized' not in st.session_state
    #     and st.session_state.selected_arc is not None
    # ):
    #     st.session_state.game = initialize_questions(st.session_state.game, st.session_state.selected_arc)
    #     st.session_state.questions_initialized = True


def render_quiz(game):
    total_questions = len(game.questions)

    if total_questions == 0:
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


def display_end_screen(game):
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


# Initialize the TriviaGame and start the quiz
if __name__ == "__main__":
    main()
