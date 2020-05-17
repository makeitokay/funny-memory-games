from skill.handlers.handler import Handler


class ErrorHandler(Handler):
    async def handle(self, alice_request, e):
        self.logger.error("An error!", exc_info=e)
        return alice_request.response(
            "Произошла какая-то ошибка. Попробуй, пожалуйста, попозже!"
        )

    def register_handlers(self):
        self.dispatcher.register_errors_handler(self.handle)
