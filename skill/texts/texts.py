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
    ]
}


def get_dynamic_text(text):
    phrases = {}
    for k, variables in _TEXT_VARIABLES.items():
        phrases[k] = random.choice(variables)
    if isinstance(text, str):
        return text.format(**phrases)
    return SpeechText(text.text.format(**phrases), text.tts.format(**phrases))


# Main menu texts

GREETINGS = '''
{greetings}! Рад тебя видеть! 
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
