import logging
import logging.handlers
import os

from skill import settings


class Logger:
    def __init__(self):
        self._logger = logging.getLogger(settings.LOGGER_NAME)
        self._logger.setLevel(logging.DEBUG)
        if not self._logger.handlers:
            filename = os.path.join(
                settings.LOGGING_PATH, f"{settings.LOGGER_NAME}.log"
            )
            handler = logging.handlers.TimedRotatingFileHandler(
                filename, when="midnight", backupCount=15
            )
            formatter = logging.Formatter("[%(asctime)s]  %(message)s")
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            self._logger.addHandler(handler)

    def log(self, msg):
        self._logger.debug(msg)

    def error(self, msg, exc_info):
        self._logger.error(msg, exc_info=exc_info)

    def log_request(self, alice_request):
        user_id = alice_request.session.user_id
        message = alice_request.request.command
        self.log(f'New request from {user_id[:16]} "{alice_request}"')
