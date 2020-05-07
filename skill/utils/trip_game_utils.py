import json
import random

from aioalice.types import Button


def get_random_question(exclude_categories=None):
    if exclude_categories is None:
        exclude_categories = []
    with open('skill/assets/trip_game_words.json', encoding='utf-8') as f:
        data = list(json.load(f).items())

    right_category = random.choice(data)
    while right_category[0] in exclude_categories:
        right_category = random.choice(data)
    right_answer = (right_category[0], random.choice(right_category[1]))

    variables = []
    for i in range(3):
        wrong_category = random.choice(data)
        while wrong_category[0] == right_category[0]:
            wrong_category = random.choice(data)
        wrong_answer = (wrong_category[0], random.choice(wrong_category[1]))
        while wrong_answer[1] == right_answer[1] or wrong_answer in variables:
            wrong_answer = (wrong_category[0], random.choice(wrong_category[1]))
        variables.append(wrong_answer)
    return variables, right_answer


def generate_answers_suggests(variables, right_answer):
    buttons = [
        Button(name, payload={"category": category, "right": False}, hide=False)
        for category, name in variables
    ]
    buttons.append(Button(right_answer[1], payload={"category": right_answer[0], "right": True}, hide=False))
    random.shuffle(buttons)
    return buttons
