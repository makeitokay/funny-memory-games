from aioalice.types import Image, MediaButton

from skill.handlers.handler import Handler
from skill.states import (AntonymsGameStates, MainMenuStates,
                          ProfessionsGameStates, TripGameStates)
from skill.texts import (ANTONYMS_GAME_START, CHOOSE_GAME, GREETINGS,
                         MAIN_MENU, PROFESSIONS_GAME_START, TRIP_GAME_START)
from skill.texts import get_dynamic_text as d


class MainMenuHandler(Handler):
    GAME_ITEMS = [
        Image(
            "1540737/1c2ce7cc72e3b9c1b0aa",
            "Веселый поход",
            "Собери вещи в поход и отправься в виртуальную экскурсию по лесу!",
            MediaButton("Веселый поход", None),
        ),
        Image(
            "965417/487a2e723f457db73400",
            "Скажи по-другому",
            "Подбери антонимы к моим словам!",
            MediaButton("Скажи по-другому", None),
        ),
        Image(
            "1540737/5bc4c807098457bc0383",
            "Угадай профессию",
            "Проверь, насколько хорошо ты знаешь профессии!",
            MediaButton("Угадай профессию", None),
        ),
    ]

    BACK_TO_MENU_KEYWORDS = [
        "Вернуться в меню",
        "Главное меню",
        "Другая игра",
        "В начало",
    ]
    TRIP_GAME_SELECT_KEYWORDS = ["Поход"]
    ANTONYMS_GAME_SELECT_KEYWORDS = ["по-другому", "по другому", "антоним"]
    PROFESSIONS_GAME_SELECT_KEYWORDS = ["профессия", "профессию", "профессии"]

    ARE_YOU_READY_SUGGESTS = ["Да!"]

    async def handle_greetings(self, alice_request):
        user_id = alice_request.session.user_id
        await self.dispatcher.storage.set_state(user_id, MainMenuStates.SELECT_GAME)
        await self.dispatcher.storage.reset_data(user_id)
        return alice_request.response_items_list(
            text=d(GREETINGS), header=CHOOSE_GAME, items=self.GAME_ITEMS
        )

    async def handle_back_to_menu(self, alice_request):
        user_id = alice_request.session.user_id
        await self.dispatcher.storage.set_state(user_id, MainMenuStates.SELECT_GAME)
        await self.dispatcher.storage.reset_data(user_id)
        return alice_request.response_items_list(
            text=MAIN_MENU, header=CHOOSE_GAME, items=self.GAME_ITEMS
        )

    async def handle_select_trip_game(self, alice_request):
        user_id = alice_request.session.user_id
        await self.dispatcher.storage.set_state(user_id, TripGameStates.TRIP_GAME_QUIZ)
        await self.dispatcher.storage.reset_data(user_id)
        return alice_request.response(
            d(TRIP_GAME_START), buttons=self.ARE_YOU_READY_SUGGESTS
        )

    async def handle_select_antonyms_game(self, alice_request):
        user_id = alice_request.session.user_id
        await self.dispatcher.storage.set_state(
            user_id, AntonymsGameStates.ANTONYMS_GAME
        )
        await self.dispatcher.storage.reset_data(user_id)
        return alice_request.response(
            d(ANTONYMS_GAME_START), buttons=self.ARE_YOU_READY_SUGGESTS
        )

    async def handle_select_professions_game(self, alice_request):
        user_id = alice_request.session.user_id
        await self.dispatcher.storage.set_state(
            user_id, ProfessionsGameStates.PROFESSIONS_GO_NEXT
        )
        await self.dispatcher.storage.reset_data(user_id)
        return alice_request.response(
            d(PROFESSIONS_GAME_START), buttons=self.ARE_YOU_READY_SUGGESTS
        )

    def register_handlers(self):
        self.dispatcher.register_request_handler(
            self.handle_greetings, func=lambda req: req.session.new, state="*"
        )
        self.dispatcher.register_request_handler(
            self.handle_back_to_menu, state="*", contains=self.BACK_TO_MENU_KEYWORDS
        )
        self.dispatcher.register_request_handler(
            self.handle_select_trip_game,
            state=[MainMenuStates.SELECT_GAME, TripGameStates.TRIP_GAME_END],
            contains=self.TRIP_GAME_SELECT_KEYWORDS,
        )
        self.dispatcher.register_request_handler(
            self.handle_select_antonyms_game,
            state=[MainMenuStates.SELECT_GAME, AntonymsGameStates.ANTONYMS_GAME_END],
            contains=self.ANTONYMS_GAME_SELECT_KEYWORDS,
        )
        self.dispatcher.register_request_handler(
            self.handle_select_professions_game,
            state=[
                MainMenuStates.SELECT_GAME,
                ProfessionsGameStates.PROFESSIONS_GAME_END,
            ],
            contains=self.PROFESSIONS_GAME_SELECT_KEYWORDS,
        )
