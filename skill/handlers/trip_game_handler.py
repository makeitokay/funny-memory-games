from skill.texts.texts import get_dynamic_text as d, TRIP_GAME_START
from skill.states import TripGameStates
from skill.handlers.handler import Handler


class TripGameHandler(Handler):
    TRIP_GAME_START_KEYWORDS = ["Да", "Погнали", "Начинаем"]

    async def game_start_handle(self, alice_request):
        return alice_request.response("Игра началась...")

    def register_handlers(self):
        self.dispatcher.register_request_handler(
            self.game_start_handle,
            state=TripGameStates.TRIP_GAME_START,
            contains=self.TRIP_GAME_START_KEYWORDS
        )
