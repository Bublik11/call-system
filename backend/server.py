import re
import json
import asyncio
import tornado.web
import tornado.escape

from dataclasses import dataclass
from tornado.options import define, options


define('port', default=8080, help='port to listen on')


@dataclass
class Appeal:
    surname: str
    name: str
    patronymic: str
    phone_number: str
    message: str
    phone: int | None = None

    # Валидатор для пост обработки данных, в случае если данные не коректны вызывается ошибка
    def __post_init__(self):
        if not re.fullmatch(r'^\+7[\d]{10}$', self.phone_number):
            raise TypeError()
        else:
            self.phone = int(self.phone_number[2:])


class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        # устанавливаем заголовки по умолчанию
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST')

    def get(self):
        # меняем и отправляем код 404 - не найдено
        self.send_error(status_code=404)

    def options(self, *args):
        # Чтобы избежать CORS Policy в ответ на запрос отправляем статус 200
        self.set_status(200)
        self.finish()


class MainHandler(BaseHandler):
    def post(self):
        try:
            obj: dict = json.loads(self.request.body.decode('utf-8'))
            obj = Appeal(**obj)
            self.set_status(status_code=201)
        except:
            self.set_status(status_code=400)
        finally:
            self.finish()


async def main():
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(options.port)
    print(f'# Server started on {options.port} port.')
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
