from skill.texts.texts import get_dynamic_text as d, MAIN_MENU, CHOOSE_GAME
from skill.handlers.handler import Handler
from aioalice.types import MediaButton, Image


class MainMenuHandler(Handler):
    async def handle(self, alice_request):
        return alice_request.response_items_list(
            text=d(MAIN_MENU),
            header=CHOOSE_GAME,
            items=[
                Image('1540737/1c2ce7cc72e3b9c1b0aa',
                      'Веселый поход',
                      'Собери вещи в поход и отправься в виртуальную экскурсию по лесу!',
                      MediaButton('Веселый поход', None)),
                Image('965417/d574f5b123b1a3907ef0',
                      'Создай персонажа',
                      'Учимся различать предметы и смотрим, как их использовать =)',
                      MediaButton('Создай персонажа', None)),
                Image('1540737/5bc4c807098457bc0383',
                      'Угадай профессию',
                      'Проверь, насколько хорошо ты знаешь профессии!',
                      MediaButton('Угадай профессию', None))
            ]
        )

    def register_handlers(self):
        self.dispatcher.register_request_handler(
            self.handle,
            func=lambda req: req.session.new
        )