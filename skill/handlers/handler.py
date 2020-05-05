from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    @abstractmethod
    def register_handlers(self):
        pass
