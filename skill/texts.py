import random


class SpeechText:
    def __init__(self, text, tts=None):
        if len(text) > 1024:
            raise ValueError("Length of text cannot be more than 1024 symbols.")
        self.text = text
        if tts is None:
            self.tts = self.text
        else:
            if len(tts) > 1024:
                raise ValueError("Length of tts cannot be more than 1024 symbols.")
            self.tts = tts

    def add_sound(self, sound):
        sound_wrapper = f"<speaker audio='{sound}'>"
        if len(self.tts + sound_wrapper) > 1024:
            raise ValueError(
                "It impossible to add this sound because of size of tts attribute."
            )
        self.tts = sound_wrapper + self.tts

    def __add__(self, other):
        if isinstance(other, str):
            return SpeechText(self.text + other, self.tts + other)
        if isinstance(other, SpeechText):
            return SpeechText(self.text + other.text, self.tts + other.tts)
        raise TypeError(
            f'Can only concatenate str or SpeechText (not "{other.__class__.__name__}") to SpeechText'
        )


_TEXT_VARIABLES = {
    "greetings": ["Привет", "Здравствуй", "Добро пожаловать", "Привет-привет"],
    "ok": ["Отлично", "Прекрасно", "Супер", "Хорошо", "ОК", "Класс", "Чудно",],
    "trip_asking": [
        "Подскажи, пожалуйста,",
        "Как ты думаешь,",
        "Скажи, пожалуйста,",
        "Подумай:",
    ],
    "try_word": [
        "Вот тебе слово",
        "Попробуй вот это слово",
        "Отгадай антоним к этому слову",
        "Есть вот такое слово",
        "Попробуй отгадать антоним к слову",
    ],
}


def get_dynamic_text(text, **game_elements):
    phrases = {}
    for k, variables in _TEXT_VARIABLES.items():
        phrases[k] = random.choice(variables)
    if game_elements is not None:
        phrases.update(game_elements)

    if isinstance(text, str):
        return text.format(**phrases)
    return SpeechText(text.text.format(**phrases), text.tts.format(**phrases))


WHAT_YOU_CAN_TEXT = """
Я умею играть с тобой в такие игры, как «Веселый поход», «Скажи по-другому» и «Угадай профессию».
"""

# Main menu texts

GREETINGS = """
{greetings}! Я и Запоминайка очень рады тебя видеть! 
Поиграем во-что нибудь? Нажми на любую игру и я расскажу тебе правила!
"""

MAIN_MENU = """
Мы в главном меню! Во что хочешь поиграть?
"""

CHOOSE_GAME = "Выбери одну из игр ниже."

MAIN_MENU_HELP = """
Сейчас ты находишься в главном меню и тебе нужно выбрать одну из игр. Просто произнеси её название.
"""

# Game #1 (Trip game) texts

TRIP_GAME_START = """
{ok}, отправляемся в поход! Но для начала нам нужно собрать вещи. Поможешь мне в этом?
"""

TRIP_GAME_CHOOSE_THING = """
{ok}! {trip_asking} какой из этих предметов {category}?
"""

TRIP_WRONG_ANSWER = """
Хм, нет, на самом деле этот предмет {wrong_category}. Попробуй ещё раз: какой из этих предметов {category}?
"""

TRIP_GAME_UNKNOWN_VARIABLE = """
Ой, кажется, такого варианта нет. Используй кнопки ниже.
"""

TRIP_QUIZ_FINISH = """
Ура! Все вещи собраны и мы можем отправиться в поход! Готов к приключению?
"""

TRIP_GAME_END = SpeechText(
    """
Кажется, дождь начинается... Нам пора возвращаться домой. Хочешь попробовать еще раз?
"""
)
TRIP_GAME_END.add_sound("alice-sounds-nature-rain-1.opus")

TRIP_GAME_QUIZ_HELP = """
Сейчас мы играем с тобой в игру «Веселый поход». 
Мы собираем вещи в поход. Я задаю тебе вопрос и даю варианты ответа в виде кнопок ниже.
"""

TRIP_GAME_EXCURSION_HELP = """
Сейчас мы играем с тобой в игру «Веселый поход». 
Мы идем по лесу, встречаем различных зверюшек и попадаем в интересные места. Просто говори мне, когда готов идти дальше.
"""

TRIP_GAME_END_HELP = """
Мы вернулись с похода домой. Если хочешь попробовать поиграть еще раз, скажи «Хочу в поход!» или можешь вернуться в главное меню.
"""

# Game #2 (Antonyms game) texts

ANTONYMS_GAME_START = """
{ok}. Правила простые: я буду называть тебе слово, а ты противоположное по значению слово к нему. 
Смотри пример:
Сильный - слабый, твердый - мягкий, белый - черный, и так далее.
Начинаем?
"""

ANTONYMS_RIGHT_ANSWER = SpeechText(
    """
{ok}."""
)

ANTONYM_WRONG_ANSWER = """
Нет, это неправильный ответ. Попробуй еще раз :) Если не знаешь, скажи «Не знаю».
"""

ANTONYM_DONT_KNOW = SpeechText(
    """
Ничего страшного. Запомни: «{question}» - «{answer}».
"""
)

ANTONYM_NEXT_WORD = SpeechText(
    """
{try_word}:
{next_question}
"""
)

ANTONYMS_GAME_END = SpeechText(
    """
Ты молодец! На этом наша игра закончилась. Хочешь попробовать еще раз или вернуться в главное меню?
"""
)
ANTONYMS_GAME_END.add_sound("alice-sounds-game-win-2.opus")

ANTONYMS_TIP_ALREADY_USED = """
Подсказка уже использована. Если не знаешь ответ, скажи «Не знаю».
"""

ANTONYMS_GAME_HELP = """
Сейчас мы играем с тобой в игру «Скажи по-другому». 
Я называю тебе слово, а ты должен назвать противоположное по значению слово. Например, белый - черный, сильный - слабый.
"""

ANTONYMS_GAME_END_HELP = """
Мы закончили играть в «Скажи по-другому». 
Если хочешь попробовать еще раз, скажи «Хочу отгадывать антонимы!» или можешь вернуться в главное меню. 
"""

# Game #3 (Professions game) texts

PROFESSIONS_GAME_START = """
{ok}. Сейчас я буду задавать тебе вопрос о профессии (например, «Кто готовит еду?»), а ты должен будешь назвать эту профессию (например, повар).
Начинаем?
"""

PROFESSIONS_GAME_END = SpeechText(
    """
Сейчас мы изучили с тобой такие профессии, как: {professions}. 
Понравилось? Хочешь попробовать еще раз или вернуться в главное меню?
"""
)
PROFESSIONS_GAME_END.add_sound("alice-sounds-game-win-3.opus")

PROFESSIONS_GAME_ANSWER_HELP = """
Сейчас мы играем с тобой в игру «Угадай профессию».
Я задаю тебе вопрос о профессии, а ты должен её назвать.
"""

PROFESSIONS_GAME_NEXT_HELP = """
Сейчас мы играем с тобой в игру «Угадай профессию».
Мы готовы идти дальше! Просто скажи «Идём дальше» и я задам тебе следующий вопрос. 
"""

PROFESSIONS_GAME_END_HELP = """
Мы закончили играть в «Угадай профессию».
Если хочешь попробовать еще раз, просто скажи «Хочу отгадывать профессии!» или можешь вернуться в главное меню.
"""
