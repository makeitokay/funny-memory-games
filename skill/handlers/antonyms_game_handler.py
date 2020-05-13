from aioalice.dispatcher import SkipHandler

from skill.handlers.handler import Handler
from skill.states import AntonymsGameStates
from skill.texts import get_dynamic_text as d, ANTONYMS_GAME_END, ANTONYMS_RIGHT_ANSWER, ANTONYM_WRONG_ANSWER, \
    ANTONYM_DONT_KNOW, ANTONYM_NEXT_WORD, ANTONYMS_TIP_ALREADY_USED
from skill.utils.antonyms_game_utils import get_random_antonyms, get_tip_for_question
from skill.utils.utils import get_original_utterance


class AntonymsGameHandler(Handler):
    async def get_next_question(self, questions):
        try:
            return next(questions)[0]
        except StopIteration:
            return

    async def game_process_handle(self, alice_request):
        user_id = alice_request.session.user_id
        user_data = await self.dispatcher.storage.get_data(user_id)
        questions = user_data.get('antonyms_game_questions')
        answer = get_original_utterance(alice_request)

        if questions is None:
            questions = await get_random_antonyms()
            await self.dispatcher.storage.update_data(user_id, antonyms_game_questions=questions)

        # TODO: Bad condition
        if questions.current is None or answer == questions.current[1]:
            question = await self.get_next_question(questions)
            if question is None:
                await self.dispatcher.storage.set_state(user_id, AntonymsGameStates.ANTONYMS_GAME_END)
                suggests = ['Хочу отгадывать антонимы!', "Главное меню"]
                return alice_request.response(
                    ANTONYMS_GAME_END.text,
                    buttons=suggests,
                    tts=ANTONYMS_GAME_END.tts
                )
            await self.dispatcher.storage.update_data(user_id, antonyms_game_tip_used=False)
            suggests = ['Подсказка']
            return alice_request.response(
                d(ANTONYMS_RIGHT_ANSWER + ANTONYM_NEXT_WORD, next_question=question).text,
                buttons=suggests
            )

        if user_data.get('antonyms_game_tip_used') is True:
            suggests = ['Не знаю']
        else:
            suggests = ['Подсказка']

        return alice_request.response(
            ANTONYM_WRONG_ANSWER,
            buttons=suggests
        )

    async def dont_know_handle(self, alice_request):
        user_id = alice_request.session.user_id
        user_data = await self.dispatcher.storage.get_data(user_id)
        questions = user_data.get('antonyms_game_questions')
        if questions is None:
            raise SkipHandler

        current_question = questions.current
        next_question = await self.get_next_question(questions)
        if next_question is None:
            text = d(ANTONYM_DONT_KNOW + ANTONYMS_GAME_END,
                     question=current_question[0],
                     answer=current_question[1])
            suggests = ['Хочу отгадывать антонимы!', "Главное меню"]
            return alice_request.response(
                text.text,
                buttons=suggests,
                tts=text.tts
            )

        suggests = ['Подсказка']
        await self.dispatcher.storage.update_data(user_id, antonyms_game_tip_used=False)
        return alice_request.response(
            d(ANTONYM_DONT_KNOW + ANTONYM_NEXT_WORD,
              question=current_question[0],
              answer=current_question[1],
              next_question=next_question).text,
            buttons=suggests
        )

    async def get_tip_handle(self, alice_request):
        user_id = alice_request.session.user_id
        user_data = await self.dispatcher.storage.get_data(user_id)

        suggests = ['Не знаю']

        if user_data.get('antonyms_game_tip_used') is True:
            return alice_request.response(ANTONYMS_TIP_ALREADY_USED, buttons=suggests)

        questions = user_data.get('antonyms_game_questions')
        if questions is None:
            raise SkipHandler
        tip = await get_tip_for_question(questions.current)
        await self.dispatcher.storage.update_data(user_id, antonyms_game_tip_used=True)
        return alice_request.response(tip, buttons=suggests)

    def register_handlers(self):
        self.dispatcher.register_request_handler(
            self.dont_know_handle,
            state=AntonymsGameStates.ANTONYMS_GAME,
            contains=['не знаю']
        )
        self.dispatcher.register_request_handler(
            self.get_tip_handle,
            state=AntonymsGameStates.ANTONYMS_GAME,
            contains=['подсказка']
        )
        self.dispatcher.register_request_handler(
            self.game_process_handle,
            state=AntonymsGameStates.ANTONYMS_GAME
        )
