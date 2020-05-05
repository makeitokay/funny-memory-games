from skill.handlers.handler import Handler
from aioalice.types import MediaButton, CardFooter, Image


class MainMenuHandler(Handler):
    async def handle(self, alice_request):
        return alice_request.response_items_list(
            'Вот альбом изображений',
            'Это текст заголовка, который будет над списком изображений',
            [
                {
                    "image_id": '1030494/ae247b496dbf582fa5da',
                    "title": None,
                    "description": "Описание картинки, которое тоже не обязательно",
                    "button": {
                        'text': 'Текст кнопки',
                        'url': 'https://github.com',
                        'payload': {'some': 'payload'}
                    }
                },
                {
                    "image_id": '1030494/ef2851808ff247bf5ad8',
                    "title": 'Заголовок картинки',
                    "description": None,
                    "button": MediaButton('Текст кнопки', 'https://google.ru', {'this_is': 'payload'})
                },
                Image('965417/5866b7a040d264f111c6',
                      'Заголовок изображения',
                      'Описание изображения',
                      MediaButton('Текст кнопки', None))
            ],
            CardFooter(
                'Текст футера (под списком изображений)',
                MediaButton('Текст кнопки', 'https://example.com')
            )
        )

    def register_handlers(self):
        self.dispatcher.register_request_handler(
            self.handle,
            func=lambda areq: areq.session.new
        )