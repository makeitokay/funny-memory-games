import json
import random

from skill import settings
from skill.utils.question_set import QuestionSet


async def get_random_antonyms():
    with open("skill/assets/antonyms_game_words.json", encoding="utf-8") as f:
        data = json.load(f)

    questions = random.sample(data, k=settings.ANTONYMS_GAME_QUESTIONS)
    for question in questions:
        random.shuffle(question)

    return QuestionSet(questions)


async def get_tip_for_question(question):
    answer = question[1]
    return (
        f"В слове {len(answer)} букв, а начинается оно на букву «{answer[0].upper()}»"
    )
