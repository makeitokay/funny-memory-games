from skill.handlers.handler import Handler


class UnknownCommandHandler(Handler):
    async def handle(self, alice_request):
        return alice_request.response("Прости, я не понимаю тебя. Попробуй еще раз!")

    def register_handlers(self):
        self.dispatcher.register_request_handler(self.handle, state="*")
