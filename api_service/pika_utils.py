import pika
import uuid
import json


class RabbitMQProducer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = json.loads(body)

    def call(self, stock_ticker, user_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        message = json.dumps(
            {'stock_ticker': stock_ticker, 'user_id': user_id})
        self.channel.basic_publish(
            exchange='',
            routing_key='stock_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message
        )

        while self.response is None:
            self.connection.process_data_events()

        return self.response


def get_stock_data(stock_ticker, user_id):
    producer = RabbitMQProducer()
    response = producer.call(stock_ticker, user_id)
    return response
