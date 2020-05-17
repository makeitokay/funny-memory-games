from skill.handlers.handler import Handler
from skill.states import (AntonymsGameStates, MainMenuStates,
                          ProfessionsGameStates, TripGameStates)
from skill.texts import (
    ANTONYMS_GAME_END_HELP, ANTONYMS_GAME_HELP, MAIN_MENU_HELP,
    PROFESSIONS_GAME_ANSWER_HELP, PROFESSIONS_GAME_END_HELP,
    PROFESSIONS_GAME_NEXT_HELP, TRIP_GAME_END_HELP, TRIP_GAME_EXCURSION_HELP,
    TRIP_GAME_QUIZ_HELP, WHAT_YOU_CAN_TEXT)


class HelpHandler(Handler):
    HELP_KEYWORDS = [
        "помощь",
        "помоги",
        "я запутался",
        "запуталась",
        "ничего не понятно",
    ]
    WHAT_YOU_CAN_KEYWORDS = ["что ты умеешь"]

    HELP_TEXTS = {
        MainMenuStates.SELECT_GAME: MAIN_MENU_HELP,
        TripGameStates.TRIP_GAME_QUIZ: TRIP_GAME_QUIZ_HELP,
        TripGameStates.TRIP_GAME_EXCURSION: TRIP_GAME_EXCURSION_HELP,
        TripGameStates.TRIP_GAME_END: TRIP_GAME_END_HELP,
        AntonymsGameStates.ANTONYMS_GAME: ANTONYMS_GAME_HELP,
        AntonymsGameStates.ANTONYMS_GAME_END: ANTONYMS_GAME_END_HELP,
        ProfessionsGameStates.PROFESSIONS_CHECK_ANSWER: PROFESSIONS_GAME_ANSWER_HELP,
        ProfessionsGameStates.PROFESSIONS_GO_NEXT: PROFESSIONS_GAME_NEXT_HELP,
        ProfessionsGameStates.PROFESSIONS_GAME_END: PROFESSIONS_GAME_END_HELP,
    }

    async def handle_help(self, alice_request):
        user_id = alice_request.session.user_id
        state = await self.dispatcher.storage.get_state(user_id)

        text = ""
        if "что ты умеешь" in alice_request.request.command:
            text += WHAT_YOU_CAN_TEXT
        text += self.HELP_TEXTS[state]

        user_data = await self.dispatcher.storage.get_data(user_id)
        last_suggests = user_data.get("last_suggests")

        return alice_request.response(text, buttons=last_suggests)

    def register_handlers(self):
        self.dispatcher.register_request_handler(
            self.handle_help,
            state="*",
            contains=self.HELP_KEYWORDS + self.WHAT_YOU_CAN_KEYWORDS,
        )
