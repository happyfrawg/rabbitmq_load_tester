import pika

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

# Define the connection parameters with username and password
credentials = pika.PlainCredentials('user', 'bitnami')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

# Connect to RabbitMQ server
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the same queue as the producer
channel.queue_declare(queue='hello')

# Set up subscription on the queue
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
