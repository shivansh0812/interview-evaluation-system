import json
import random


def load_questions():
    with open("data/questions.json", "r") as file:
        data = json.load(file)
    return data


def get_all_questions(role):
    data = load_questions()

    if role not in data:
        return None

    return data[role]


def get_random_question(role):
    data = load_questions()

    if role not in data:
        return None

    return random.choice(data[role])