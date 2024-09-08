from logging import Logger
from typing import List

from game import TriviaGame
from data import load_questions_from_file
from logger import get_logger

logger: Logger = get_logger("component-questions")


def initialize_questions(game: TriviaGame, arc_name: str):
    # Clear old questions before loading new ones
    game.questions = []
    game.answers = []

    # Load questions from JSON file
    questions: List[str] = load_questions_from_file(arc_name)
    for q in questions:
        game.add_question(q["question"], q["answer"])
    return game
