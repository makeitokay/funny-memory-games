from skill.texts.texts import get_dynamic_text as d, TRIP_GAME_CHOOSE_THING, TRIP_QUIZ_FINISH, TRIP_WRONG_ANSWER, \
    TRIP_GAME_END, SpeechText
from skill.states import TripGameStates
from skill.utils.trip_game_utils import generate_answers_suggests, get_random_locations, \
    get_random_questions
from skill.handlers.handler import Handler


class TripGameHandler(Handler):
    async def get_user_data(self, user_id):
        data = await self.dispatcher.storage.get_data(user_id)
        return data

    async def quiz_process_handle(self, alice_request):
        user_id = alice_request.session.user_id
        user_data = await self.get_user_data(user_id)
        payload = alice_request.request.payload or {}
        if payload.get('right') is not False:
            questions = user_data.get('trip_game_questions')
            self.logger.log(questions)
            if questions is None:
                questions = get_random_questions()
                await self.dispatcher.storage.update_data(user_id, trip_game_questions=questions)
            try:
                wrong_variables, right_answer = next(questions)
            except StopIteration:
                await self.dispatcher.storage.set_state(user_id, TripGameStates.TRIP_GAME_EXCURSION)
                return alice_request.response(TRIP_QUIZ_FINISH, buttons=['Да!'])
            suggests = generate_answers_suggests(wrong_variables, right_answer)
            # TODO: Saving suggests to user data storage is a bad idea
            await self.dispatcher.storage.update_data(user_id, trip_game_quiz_suggests=suggests)
            return alice_request.response(
                d(TRIP_GAME_CHOOSE_THING, category=right_answer[0]),
                buttons=suggests
            )
        suggests = user_data.get('trip_game_quiz_suggests')
        return alice_request.response(
            d(TRIP_WRONG_ANSWER, category=payload.get('category')),
            buttons=suggests
        )

    async def excursion_process_handle(self, alice_request):
        user_id = alice_request.session.user_id
        user_data = await self.get_user_data(user_id)
        locations = user_data.get('trip_game_locations')
        if locations is None:
            locations = get_random_locations()
            await self.dispatcher.storage.update_data(user_id, trip_game_locations=locations)
        try:
            current_location = next(locations)
        except StopIteration:
            await self.dispatcher.storage.set_state(user_id, TripGameStates.TRIP_GAME_END)
            return alice_request.response(TRIP_GAME_END, buttons=['Хочу в поход!', 'Главное меню'])

        text = SpeechText(current_location['text'])
        text.add_sound(current_location['sound'])

        return alice_request.response_big_image(
            text=text.text,
            tts=text.tts,
            image_id=current_location['image'],
            title=current_location['name'],
            description=current_location['text'],
            buttons=["Идём дальше!"]
        )

    def register_handlers(self):
        self.dispatcher.register_request_handler(
            self.quiz_process_handle,
            state=TripGameStates.TRIP_GAME_QUIZ
        )
        self.dispatcher.register_request_handler(
            self.excursion_process_handle,
            state=TripGameStates.TRIP_GAME_EXCURSION,
        )
