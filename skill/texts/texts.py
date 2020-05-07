import random


class SpeechText:
    def __init__(self, text, tts=None):
        self.text = text
        self.tts = tts
        if self.tts is None:
            self.tts = self.text

    def add_sound(self, sound):
        if len(self.tts + sound.tts) > 1024:
            raise ValueError('It impossible to add this sound because of size of tts attribute.')
        self.tts = sound.tts + self.tts


_TEXT_VARIABLES = {
    "greetings": [
        'Привет',
        'Здравствуй',
        'Добро пожаловать'
    ],
    "ok": [
        "Отлично",
        "Прекрасно",
        "Супер",
        "Хорошо",
        "ОК",
        "Класс",
        "Чудно",
    ],
    "trip_asking": [
        "Подскажи, пожалуйста,",
        "Как ты думаешь,",
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


# Main menu texts

GREETINGS = '''
{greetings}! Я и Запоминайка очень рады тебя видеть! 
Поиграем во-что нибудь? Нажми на любую игру и я расскажу тебе правила!
'''

MAIN_MENU = '''
Мы в главном меню! Во что хочешь поиграть?
'''

CHOOSE_GAME = 'Выбери одну из игр ниже.'

# Game #1 (Trip game) texts

TRIP_GAME_START = '''
{ok}, отправляемся в поход! Но для начала нам нужно собрать вещи. Поможешь мне в этом?
'''

TRIP_GAME_CHOOSE_THING = '''
{ok}! {trip_asking} какой из этих предметов {category}?
'''

TRIP_USE_BUTTONS = '''
Пожалуйста, используй кнопки, которые я показала тебе в сообщении выше. 
'''

TRIP_WRONG_ANSWER = '''
Хм, нет, на самом деле этот предмет {category}. Попробуй ещё раз.
'''

TRIP_QUIZ_FINISH = '''
Ура! Все вещи собраны и мы можем отправиться в поход! Готов к приключению?
'''