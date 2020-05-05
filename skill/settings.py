from skill.handlers import LoggingHandler, MainMenuHandler

WEBHOOK_URL_PATH = '/webhook/'
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001

HANDLERS = [
    LoggingHandler,
    MainMenuHandler
]
