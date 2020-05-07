import os

from skill.handlers import LoggingHandler, MainMenuHandler, ErrorHandler, UnknownCommandHandler, TripGameHandler

WEBHOOK_URL_PATH = '/webhook/'
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001

HANDLERS = [
    LoggingHandler,

    MainMenuHandler,
    TripGameHandler,

    ErrorHandler,
    UnknownCommandHandler,
]

ROOT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

LOGGER_NAME = 'skill'
LOGGING_PATH = os.path.join(ROOT_DIR_PATH, 'logs')

TRIP_GAME_QUESTIONS = 5