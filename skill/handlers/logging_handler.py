from aioalice.dispatcher import SkipHandler

from skill.handlers.handler import Handler


class LoggingHandler(Handler):
    async def handle(self, alice_request):
        self.logger.debug('New request! %r', alice_request)
        raise SkipHandler

    def register_handlers(self):
        self.dispatcher.register_request_handler(self.handle)
