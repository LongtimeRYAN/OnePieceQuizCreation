import streamlit as st

class TriviaGame:
    def __init__(self):
        self.questions = []
        self.answers = []  # Store full sentence answers
        self.keywords = []
        self.score = 0
        self.correct_count = 0
        self.incorrect_count = 0

    def add_question(self, question, answer, keywords):
        self.questions.append(question)
        self.answers.append(answer)  # Add the answer
        self.keywords.append([keyword.lower() for keyword in keywords])

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

    # Initialize session state for selected arc
    if 'selected_arc' not in st.session_state:
        st.session_state.selected_arc = None

    # Initialize the game object if not already initialized
    if 'game' not in st.session_state:
        st.session_state.game = TriviaGame()
        initialize_questions(st.session_state.game)

    # Arc selection or all questions quiz rendering logic
    if not st.session_state.quiz_started:
        display_start_screen()
    elif st.session_state.selected_arc is None:
        display_arc_selection()
    else:
        if st.session_state.finished:
            display_end_screen(st.session_state.game)
        else:
            render_quiz(st.session_state.game)

def initialize_questions(game):
    # Add questions and answers for the Arlong Park arc
    game.add_question("What object does Genzo have on his hat?", "A pinwheel", ["arlong park"])
    game.add_question("What was Nami caught stealing from her village as a child?", "Books. Charting/navigation books", ["arlong park"])
    game.add_question("How did the Arlong pirates spot Bellemere’s house?", "Smoke from cooking", ["arlong park"])
    game.add_question("Why did the Arlong Pirates want Nami?", "The maps she drew", ["arlong park"])
    game.add_question("Who sent the marines to find Nami’s money?", "Arlong", ["arlong park"])
    game.add_question("Who prevented the villagers from rushing into Arlong park just to die?", "Johnny and Yosaku", ["arlong park"])
    game.add_question("How does Luffy get his feet stuck in the ground while fighting Arlong?", "He stomped the ground too hard", ["arlong park"])
    game.add_question("How does Arlong take Luffy out of the fight almost immediately?", "Picking him up and throwing him into the sea", ["arlong park"])
    game.add_question("How many swords does Hachi use?", "6", ["arlong park"])
    game.add_question("How do Genzo and Nojiko get Luffy air while he is trapped?", "They stretch his neck", ["arlong park"])
    game.add_question("How did Sanji stun Kuroobi long enough to prevent himself from drowning?", "Forced air into his gills", ["arlong park"])

    # Add questions and answers for the Syrup Village arc
    game.add_question("How does the butler Klahadore adjust his glasses?", "By using his palm to push them up", ["syrup village"])
    game.add_question("How did Luffy know Usopp's dad back at Syrup Village?", "Yassop is a member of the Red Hair Pirates", ["syrup village"])
    game.add_question("Why was Kuro undercover as a butler for three years?", "To steal Kaya’s wealth without arousing any suspicion", ["syrup village"])
    game.add_question("For what occasion did Kaya buy a present for Klahadore?", "His 3-year anniversary of working for her", ["syrup village"])
    game.add_question("Who was the first ally to engage the Kuro Pirates after they changed locations?", "Usopp", ["syrup village"])
    game.add_question("How did Zoro get out of the oil slick in Syrup Village?", "He used his swords to climb out", ["syrup village"])
    game.add_question("How did the Kuro Pirates suddenly get stronger during the fight?", "Jango's hypnotism", ["syrup village"])
    game.add_question("Name one of the Nyaban Brothers.", "Buchi and Sham", ["syrup village"])
    game.add_question("What do the Symbols on Kuro’s coat represent?", "It’s poop", ["syrup village"])
    game.add_question("Why does Kuro adjust his glasses the way he does?", "A habit he picked up from having swords for hands", ["syrup village"])

def display_start_screen():
    st.markdown("<h1 style='text-align: center;'>THE ULTIMATE ONE PIECE QUIZ</h1>", unsafe_allow_html=True)
    st.write("Test your knowledge of the entire One Piece series. Do you remember every chapter by heart? Are you a real fan? Or are you fake?")

    if st.button("Begin Quiz"):
        st.session_state.quiz_started = True
        st.rerun()

def display_arc_selection():
    st.markdown("<h2 style='text-align: center;'>Select an Arc:</h2>", unsafe_allow_html=True)
    arcs = ["All Arcs", "Arlong Park", "Syrup Village"]  # Add more arcs as needed
    selected_arc = st.selectbox("", arcs)

    if st.button("Start Quiz"):
        st.session_state.selected_arc = selected_arc
        st.session_state.quiz_started = True
        if selected_arc == "All Arcs":
            # No filtering, use all questions
            pass 
        else:
            # Filter questions, answers, and keywords based on the selected arc
            filtered_questions = []
            filtered_answers = []
            filtered_keywords = []

            for question, answer, keywords in zip(st.session_state.game.questions, st.session_state.game.answers, st.session_state.game.keywords):
                if selected_arc.lower() in [kw.lower() for kw in keywords]:
                    filtered_questions.append(question)
                    filtered_answers.append(answer)
                    filtered_keywords.append(keywords)
            
            st.session_state.game.questions = filtered_questions
            st.session_state.game.answers = filtered_answers
            st.session_state.game.keywords = filtered_keywords

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
                correct_answer = game.get_current_answer() 
                st.write(f"Correct Answer: {correct_answer}")
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
    main()
