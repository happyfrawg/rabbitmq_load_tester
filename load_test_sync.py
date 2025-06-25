import pika
import time
import threading

# Define the connection parameters with username and password
credentials = pika.PlainCredentials('user', 'bitnami')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

# Function to send messages
def send_messages(num_messages, interval):
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='test_queue')

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

# Callback function for message consumption
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

# Function to consume messages
def consume_messages():
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='test_queue')

    channel.basic_consume(queue='test_queue',
                          on_message_callback=callback,
                          auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

# Define the number of messages and the interval between each message
num_messages = 1000
interval = 0.0001  # 10 milliseconds

# Start the producer thread
producer_thread = threading.Thread(target=send_messages, args=(num_messages, interval))
producer_thread.start()

# Wait for the producer thread to finish
producer_thread.join()


time.sleep(10)
# Start the consumer thread
consumer_thread = threading.Thread(target=consume_messages)
consumer_thread.start()

# Optionally, wait for the consumer thread to finish
consumer_thread.join()
