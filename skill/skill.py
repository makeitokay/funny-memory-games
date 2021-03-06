from aioalice import Dispatcher, get_new_configured_app
from aioalice.dispatcher import MemoryStorage
from aioalice.dispatcher.webhook import WebhookRequestHandler
from aiohttp import web

from skill import settings


class Skill:
    def __init__(self):
        self.dispatcher = Dispatcher(storage=MemoryStorage())

        self.app = get_new_configured_app(
            dispatcher=self.dispatcher, path=settings.WEBHOOK_URL_PATH
        )
        self.app.router.add_route(
            "*",
            settings.STRESS_TEST_URL_PATH,
            WebhookRequestHandler,
            name="stress_test_handler",
        )

        for handler_cls in settings.HANDLERS:
            handler = handler_cls(self.dispatcher)
            handler.register_handlers()

    def start(self):
        web.run_app(self.app, host=settings.WEBAPP_HOST, port=settings.WEBAPP_PORT)
