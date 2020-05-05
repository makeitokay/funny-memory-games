import os
import logging, logging.handlers

from skill import settings


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(settings.LOGGER_NAME)
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            filename = os.path.join(settings.LOGGING_PATH, f'{settings.LOGGER_NAME}.log')
            handler = logging.handlers.TimedRotatingFileHandler(filename, when='midnight', backupCount=15)
            formatter = logging.Formatter(
                u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s'
            )
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            self.logger.addHandler(handler)
