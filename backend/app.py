import asyncio

from tornado.web import Application
from config import TORNADO_PORT
from utils.rabbitmq import rmq_channel
from handlers.appeal_handler import MainHandler
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    filename='server.log'
                    )

async def main():
    application = Application([(r"/", MainHandler)])
    application.listen(TORNADO_PORT)
    logging.info(f'Server started on {TORNADO_PORT} port.')
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(f'Server stoped.')
    finally:
        if rmq_channel.is_open: 
            rmq_channel.close()
