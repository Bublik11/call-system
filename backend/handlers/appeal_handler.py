import json
import logging
from tornado.web import RequestHandler
from utils.appeal_data import Appeal, ValidatePhoneError
from utils.rabbitmq import RABBIT_QUEUE, rmq_channel


rmq_channel.queue_declare(queue=RABBIT_QUEUE)

class BaseHandler(RequestHandler):
    """Базовый класс обработчика запросов"""

    def set_default_headers(self):
        # устанавливаем заголовки по умолчанию
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "OPTIONS, GET, POST")

    def get(self):
        # меняем и отправляем код 404 - не найдено, так как принимаем
        # только post запросы
        self.send_error(status_code=404)

    def options(self, *args):
        # чтобы избежать CORS Policy в ответ на запрос отправляем статус 200
        self.set_status(200)
        self.finish()


class MainHandler(BaseHandler):
    """Основной обработчик запроса обращения"""

    def post(self):
        try:
            new_appeal = Appeal(**json.loads(self.request.body.decode("utf-8")))
            rmq_channel.basic_publish(
                exchange="", routing_key=RABBIT_QUEUE, body=str(new_appeal)
            )
            self.set_status(status_code=200)
        except TypeError:
            self.set_status(status_code=400, reason='Transmitted data error.')
        except ValidatePhoneError:
            self.set_status(status_code=400, reason='Transmitted data error.\nThe phone number entered is incorrect.')
        except Exception as e:
            self.set_status(status_code=503, reason='Service is unavailable. The server is currently unable to process your request.')
            logging.error(e)
        finally:
            logging.info(self._reason)
            self.finish()
