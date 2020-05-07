from aioalice.types import RequestType

from skill import settings
from skill.texts.texts import get_dynamic_text as d, TRIP_GAME_CHOOSE_THING, TRIP_QUIZ_FINISH, TRIP_WRONG_ANSWER
from skill.states import TripGameStates
from skill.utils.trip_game_utils import get_random_question, generate_answers_suggests
from skill.handlers.handler import Handler


class TripGameHandler(Handler):
    async def get_user_data(self, user_id):
        data = await self.dispatcher.storage.get_data(user_id)
        return data

    async def quiz_start_handle(self, alice_request):
        user_id = alice_request.session.user_id

        wrong_variables, right_answer = get_random_question()
        await self.dispatcher.storage.update_data(
            user_id, trip_game_questions_left=settings.TRIP_GAME_QUESTIONS - 1,
        )
        await self.dispatcher.storage.set_state(user_id, TripGameStates.TRIP_GAME_QUIZ)
        return alice_request.response(
            d(TRIP_GAME_CHOOSE_THING, category=right_answer[0]),
            buttons=generate_answers_suggests(wrong_variables, right_answer)
        )

    async def quiz_process_handle(self, alice_request):
        user_id = alice_request.session.user_id
        user_data = await self.get_user_data(user_id)
        questions_left = user_data.get('trip_game_questions_left')
        if questions_left == 0:
            return alice_request.response(TRIP_QUIZ_FINISH, buttons=['Да!'])
        payload = alice_request.request.payload
        if payload.get('right') is True:
            exclude_categories = user_data.get('exclude_categories', [])
            exclude_categories.append(payload.get('category'))
            wrong_variables, right_answer = get_random_question(exclude_categories)
            await self.dispatcher.storage.update_data(
                user_id,
                trip_game_questions_left=questions_left - 1,
                exclude_categories=exclude_categories
            )
            return alice_request.response(
                d(TRIP_GAME_CHOOSE_THING, category=right_answer[0]),
                buttons=generate_answers_suggests(wrong_variables, right_answer)
            )
        return alice_request.response(
            d(TRIP_WRONG_ANSWER, category=payload.get('category')),
        )


    def register_handlers(self):
        self.dispatcher.register_request_handler(
            self.quiz_start_handle,
            state=TripGameStates.TRIP_GAME_START
        )
        self.dispatcher.register_request_handler(
            self.quiz_process_handle,
            state=TripGameStates.TRIP_GAME_QUIZ,
            request_type=RequestType.BUTTON_PRESSED
        )
