import pika
import json
import logging
from django.core.management.base import BaseCommand
from stocks.views import StockView

logger = logging.getLogger(__name__)

def on_request(ch, method, properties, body):
    message = json.loads(body)
    stock_code = message['stock_ticker']
    user_id = message['user_id']
    logger.info(f"Received message with stock_code: {stock_code}")

    view = StockView()
    json_response, response_status = view.get_stock_data(stock_code)

    response_message = json.dumps({"response": json_response, "status": response_status})
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=response_message
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info(f"Processed and sent response: {response_message}")

class Command(BaseCommand):
    help = 'Runs the RabbitMQ consumer'

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='stock_queue')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='stock_queue', on_message_callback=on_request)

        self.stdout.write(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
