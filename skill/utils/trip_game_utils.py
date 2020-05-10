import json
import random

from aioalice.types import Button

from skill import settings


async def get_random_questions():
    with open('skill/assets/trip_game_words.json', encoding='utf-8') as f:
        data = list(json.load(f).items())

    results = []
    right_answers = random.sample(data, k=settings.TRIP_GAME_QUESTIONS)
    for category, variables in right_answers:
        answer = random.choice(variables)
        wrong_variables = []
        for _ in range(3):
            wrong_items = random.choice(data)
            while wrong_items[0] == category:  # wrong_items[0] is a category
                wrong_items = random.choice(data)
            wrong_answer = random.choice(wrong_items[1])
            while any(wrong_answer == item[1] for item in wrong_variables):
                wrong_answer = random.choice(wrong_items[1])
            wrong_variables.append((wrong_items[0], wrong_answer))
        results.append((wrong_variables, (category, answer)))
    return iter(results)


async def generate_answers_suggests(variables, right_answer):
    buttons = [
        Button(name, payload={"category": category, "right": False})
        for category, name in variables
    ]
    buttons.append(Button(right_answer[1], payload={"category": right_answer[0], "right": True}))
    random.shuffle(buttons)
    return buttons


async def get_random_locations():
    with open('skill/assets/trip_game_locations.json', encoding='utf-8') as f:
        data = list(json.load(f))
    # data[0] is forest location. It is the first location by default
    result = [data[0]]
    for _ in range(settings.TRIP_EXCURSION_LOCATIONS - 1):
        random_location = random.choice(data)
        while random_location in result:
            random_location = random.choice(data)
        result.append(random_location)
    return iter(result)

