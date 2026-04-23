import json
import random
import os

def load_questions():
    """
    Load questions from JSON file safely (works locally + on Streamlit Cloud)
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "questions.json")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_questions(role):
    """
    Get all questions for a specific role
    """
    data = load_questions()

    if role not in data:
        return []

    return data[role]


def get_random_question(role):
    """
    Get one random question in a clean standardized format
    ALWAYS returns:
    {
        "question": "...",
        "answer": "..."
    }
    """
    data = load_questions()

    if role not in data or not data[role]:
        return None

    q = random.choice(data[role])

    return {
        "question": q.get("question", "No question found"),
        "answer": q.get("ideal_answer", "No ideal answer provided")
    }
