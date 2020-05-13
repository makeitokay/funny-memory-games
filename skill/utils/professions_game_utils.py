import json
import random

from skill import settings
from skill.utils.question_set import QuestionSet


async def get_random_professions():
    with open('skill/assets/professions.json', encoding='utf-8') as f:
        data = json.load(f)

    return QuestionSet(random.sample(data, k=settings.PROFESSIONS_GAME_QUESTIONS), save_objects=True)
