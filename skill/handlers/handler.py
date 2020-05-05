from abc import ABC, abstractmethod

from skill.logger import Logger


class Handler(ABC):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.logger = Logger().logger

    @abstractmethod
    def register_handlers(self):
        pass
