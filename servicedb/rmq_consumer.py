import asyncio
import aio_pika
import os
import httpx
from json import dumps

EXCHANGE_NAME = os.getenv('EXCHANGE_NAME', 'exc_statement')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'statements')

RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD','guest')
RABBITMQ_USER = os.getenv('RABBITMQ_USER','guest')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT','5672')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST','127.0.0.1')
PREFETCH_COUNT = os.getenv('PREFETCH_COUNT',10)

async def consume():
    url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/'
    loop = asyncio.get_event_loop()

    connection = await aio_pika.connect_robust(
        url=url,
        loop=loop
    )

    async with connection:
        # Creating channel
        channel = await connection.channel()
        await channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC)
        await channel.set_qos(prefetch_count=PREFETCH_COUNT)

        # Declaring queue
        queue = await channel.declare_queue(QUEUE_NAME)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(ignore_processed=True):
                    str_message = message.body.decode()
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            url='http://localhost:8000/appeals/',
                            json=dumps(str_message)
                            )
                        if response.status_code == 200:
                            await message.reject()
                        
if __name__ == "__main__":
    asyncio.run(consume())