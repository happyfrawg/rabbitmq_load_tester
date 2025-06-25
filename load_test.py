import pika
import time

# Define the connection parameters with username and password
credentials = pika.PlainCredentials('user', 'bitnami')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

# Connect to RabbitMQ server
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='test_queue')

# Define the number of messages and the interval between each message
num_messages = 100000
interval = 0.0001  # 10 milliseconds

# Send messages
start_time = time.time()
for i in range(num_messages):
    message = f'Message {i}'
    channel.basic_publish(exchange='',
                          routing_key='test_queue',
                          body=message)
    time.sleep(interval)

end_time = time.time()
elapsed_time = end_time - start_time
print(f" [x] Sent {num_messages} messages in {elapsed_time:.2f} seconds")

connection.close()
