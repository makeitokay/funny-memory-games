from skill import settings
from skill.texts.texts import get_dynamic_text as d, MAIN_MENU, CHOOSE_GAME, GREETINGS, TRIP_GAME_START
from skill.handlers.handler import Handler
from skill.states import MainMenuStates, TripGameStates
from aioalice.types import MediaButton, Image, Button


class MainMenuHandler(Handler):
    GAME_ITEMS = [
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

    BACK_TO_MENU_KEYWORDS = ["Вернуться в меню", "Главное меню", "Другая игра", "В начало"]
    TRIP_GAME_SELECT_KEYWORDS = ["Поход"]

    async def handle_greetings(self, alice_request):
        user_id = alice_request.session.user_id
        await self.dispatcher.storage.set_state(user_id, MainMenuStates.SELECT_GAME)
        await self.dispatcher.storage.reset_data(user_id)
        return alice_request.response_items_list(
            text=d(GREETINGS),
            header=CHOOSE_GAME,
            items=self.GAME_ITEMS
        )

    async def handle_back_to_menu(self, alice_request):
        user_id = alice_request.session.user_id
        await self.dispatcher.storage.set_state(user_id, MainMenuStates.SELECT_GAME)
        await self.dispatcher.storage.reset_data(user_id)
        return alice_request.response_items_list(
            text=MAIN_MENU,
            header=CHOOSE_GAME,
            items=self.GAME_ITEMS
        )

    async def handle_select_trip_game(self, alice_request):
        user_id = alice_request.session.user_id
        await self.dispatcher.storage.set_state(user_id, TripGameStates.TRIP_GAME_QUIZ)
        await self.dispatcher.storage.reset_data(user_id)
        return alice_request.response(
            d(TRIP_GAME_START),
            buttons=[Button("Да!")]
        )

    def register_handlers(self):
        self.dispatcher.register_request_handler(
            self.handle_greetings,
            func=lambda req: req.session.new,
            state="*"
        )
        self.dispatcher.register_request_handler(
            self.handle_back_to_menu,
            state="*",
            contains=self.BACK_TO_MENU_KEYWORDS
        )
        self.dispatcher.register_request_handler(
            self.handle_select_trip_game,
            state=[MainMenuStates.SELECT_GAME, TripGameStates.TRIP_GAME_END],
            contains=self.TRIP_GAME_SELECT_KEYWORDS
        )
