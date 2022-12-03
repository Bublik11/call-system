import re
import asyncio
import tornado.web
import tornado.escape

from typing import Optional
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
    phone: Optional[int] = None

    # Валидатор для пост обработки данных, в случае если данные не коректны вызывается ошибка
    def __post_init__(self):
        if not re.fullmatch(r'^\+7[\d]{10}$', self.phone_number):
            raise TypeError()
        else:
            self.phone = int(self.phone_number[2:])


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            obj = {}
            for key, value in self.request.arguments.items():
                obj[key] = value[0].decode("utf-8")
            obj = Appeal(**obj)
            self.write('Ваш запрос успешно отправлен!')
        except TypeError:
            self.send_error(status_code=400)


async def main():
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(options.port)
    print(f'# Server started on {options.port} port.')
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
