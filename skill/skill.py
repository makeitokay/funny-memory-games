from aioalice import Dispatcher, get_new_configured_app
from aioalice.dispatcher import MemoryStorage
from aiohttp import web

import ssl

from skill import settings


class Skill:
    def __init__(self):
        self.dispatcher = Dispatcher(storage=MemoryStorage())
        self.app = get_new_configured_app(dispatcher=self.dispatcher, path=settings.WEBHOOK_URL_PATH)

        for handler_cls in settings.HANDLERS:
            handler = handler_cls(self.dispatcher)
            handler.register_handlers()

        self.ssl_context = None
        if not settings.DEBUG:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.load_cert_chain('data/certs/cert.pem', 'data/certs/key.pem')

    def start(self):
        web.run_app(
            self.app,
            host=settings.WEBAPP_HOST,
            port=settings.WEBAPP_PORT,
            ssl_context=self.ssl_context
        )
