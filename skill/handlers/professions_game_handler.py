from skill.handlers.handler import Handler
from skill.states import ProfessionsGameStates
from skill.texts import get_dynamic_text as d, PROFESSIONS_GAME_END
from skill.utils.professions_game_utils import get_random_professions
from skill.utils.utils import get_original_utterance


class ProfessionsGameHandler(Handler):
    async def check_answer_handle(self, alice_request):
        user_id = alice_request.session.user_id
        user_data = await self.dispatcher.storage.get_data(user_id)
        questions = user_data.get('professions_game_questions')
        answer = get_original_utterance(alice_request)

        text = "Запомни: "
        if questions.current['name'].lower() in answer and answer != "не знаю":
            text = "Правильно!"

        suggests = ['Идём дальше!']
        await self.dispatcher.storage.set_state(user_id, ProfessionsGameStates.PROFESSIONS_GO_NEXT)
        current = questions.current
        if current.get('image') is not None:
            return alice_request.response_big_image(
                text=text + current['description'],
                image_id=current['image'],
                title=current['name'],
                description=current['description'],
                buttons=suggests
            )

    async def go_next_handle(self, alice_request):
        user_id = alice_request.session.user_id
        user_data = await self.dispatcher.storage.get_data(user_id)

        questions = user_data.get('professions_game_questions')
        if questions is None:
            questions = await get_random_professions()
            await self.dispatcher.storage.update_data(user_id, professions_game_questions=questions)

        try:
            question = next(questions)
        except StopIteration:
            await self.dispatcher.storage.set_state(user_id, ProfessionsGameStates.PROFESSIONS_GAME_END)
            professions = ", ".join([p['name'].lower() for p in questions.saved])
            suggests = ['Хочу отгадывать профессии!', "Главное меню"]
            text = d(PROFESSIONS_GAME_END, professions=professions)
            return alice_request.response(
                text.text,
                buttons=suggests,
                tts=text.tts
            )
        suggests = ['Не знаю']
        await self.dispatcher.storage.set_state(user_id, ProfessionsGameStates.PROFESSIONS_CHECK_ANSWER)
        return alice_request.response(
            f"Кто {question['question']}?",
            buttons=suggests
        )

    def register_handlers(self):
        self.dispatcher.register_request_handler(
            self.check_answer_handle,
            state=ProfessionsGameStates.PROFESSIONS_CHECK_ANSWER
        )
        self.dispatcher.register_request_handler(
            self.go_next_handle,
            state=ProfessionsGameStates.PROFESSIONS_GO_NEXT
        )
