import pika

def establish_pika_connection():
    connection_params = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(connection_params)
    return connection

def publish_message(message):
    connection = establish_pika_connection()
    channel = connection.channel()
    channel.queue_declare(queue='my_queue')
    channel.basic_publish(exchange='', routing_key='my_queue', body=message)
    connection.close()
