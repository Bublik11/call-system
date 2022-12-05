import pika

RABBIT_HOST = "localhost"
RABBIT_QUEUE = "appeal"

rmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
rmq_channel = rmq_connection.channel()
