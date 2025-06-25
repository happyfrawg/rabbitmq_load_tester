import pika

# Define the connection parameters with username and password
credentials = pika.PlainCredentials('user', 'bitnami')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

# Connect to RabbitMQ server
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='hello')

# Publish a message to the queue
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")
connection.close()
