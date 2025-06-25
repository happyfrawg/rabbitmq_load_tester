#!/usr/bin/env python3
"""
Asynchronous send-and-consume demo for RabbitMQ using aio-pika.

• Connects with the same credentials as your working pika examples
  (user/bitnami on localhost:5672, vhost “/”).
• Declares/uses the existing queue “test_queue”.
• Sends 100 messages plus a special “STOP_MESSAGE”.
• Consumes from the same queue until it receives the stop message,
  then exits cleanly and closes the connection.
"""

import asyncio
import aio_pika

# ----------------------------------------------------------------------
# Connection settings – change only if you really need to.
# ----------------------------------------------------------------------
RABBIT_URL = "amqp://user:bitnami@localhost/"       # <- local broker
QUEUE_NAME = "test_queue"
STOP_MESSAGE = "STOP_MESSAGE"


async def send_messages(channel: aio_pika.Channel) -> None:
    """Publish 100 demo messages and one stop message."""
    for i in range(100):
        body = f"Message {i}".encode()
        await channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=QUEUE_NAME,
        )
        print(f" [x] Sent: Message {i}")

    # Tell the consumer to stop.
    await channel.default_exchange.publish(
        aio_pika.Message(body=STOP_MESSAGE.encode()),
        routing_key=QUEUE_NAME,
    )


async def consume_messages(queue: aio_pika.Queue) -> None:
    """Consume until STOP_MESSAGE is received, then break."""
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                body = message.body.decode()
                print(f" [x] Received: {body}")
                if body == STOP_MESSAGE:
                    break


async def main() -> None:
    # Robust connection automatically handles reconnects/back-off.
    connection: aio_pika.RobustConnection = await aio_pika.connect_robust(RABBIT_URL)

    async with connection:
        channel: aio_pika.Channel = await connection.channel()
        queue: aio_pika.Queue = await channel.declare_queue(QUEUE_NAME, durable=False)

        # Run sender and consumer concurrently.
        await asyncio.gather(
            send_messages(channel),
            consume_messages(queue),
        )

if __name__ == "__main__":
    asyncio.run(main())
