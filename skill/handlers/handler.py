from abc import ABC, abstractmethod

from skill.logger import Logger


class Handler(ABC):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.logger = Logger()

    async def save_suggests(self, user_id, suggests):
        return await self.dispatcher.storage.update_data(user_id, last_suggests=suggests)

    @abstractmethod
    def register_handlers(self):
        pass
