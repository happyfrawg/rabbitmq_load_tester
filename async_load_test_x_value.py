#!/usr/bin/env python3
"""
Async RabbitMQ load script: publish 1 000 000 messages, then a STOP_MESSAGE.

• Uses aio-pika with the same credentials that work locally (user/bitnami).
• Publishes and consumes in parallel.
• Prints a progress line every 100k messages instead of every message.
"""

import asyncio
import aio_pika
from aio_pika import RobustConnection, Message, Channel, Queue

# ---------------------------------------------------------------------
RABBIT_URL   = "amqp://user:bitnami@localhost/"
QUEUE_NAME   = "test_queue"
STOP_MESSAGE = "STOP_MESSAGE"
TOTAL_MSGS   = 1_000_0
PROGRESS_EVERY = 100      # how often to show progress
# ---------------------------------------------------------------------


async def send_messages(channel: Channel) -> None:
    """Publish TOTAL_MSGS demo messages plus a STOP_MESSAGE."""
    for i in range(TOTAL_MSGS):
        body = f"Message {i}".encode()
        await channel.default_exchange.publish(
            Message(body=body),
            routing_key=QUEUE_NAME,
        )
        if (i + 1) % PROGRESS_EVERY == 0:
            print(f" [x] Sent {i + 1:,} messages")

    # Notify consumer to stop
    await channel.default_exchange.publish(
        Message(body=STOP_MESSAGE.encode()),
        routing_key=QUEUE_NAME,
    )
    print(" [x] Sent STOP_MESSAGE")


async def consume_messages(queue: Queue) -> None:
    """Consume until STOP_MESSAGE is received, then exit."""
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                body = message.body.decode()
                if body == STOP_MESSAGE:
                    print(" [x] Received STOP_MESSAGE – consumer exiting")
                    break


async def main() -> None:
    connection: RobustConnection = await aio_pika.connect_robust(RABBIT_URL)
    async with connection:
        channel: Channel = await connection.channel()
        queue: Queue = await channel.declare_queue(QUEUE_NAME, durable=False)

        await asyncio.gather(
            send_messages(channel),
            consume_messages(queue),
        )

if __name__ == "__main__":
    asyncio.run(main())
