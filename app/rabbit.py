# app/rabbit.py
import aio_pika
import json
import pickle

async def publish_event(event_type: str, data: dict):
    connection = await aio_pika.connect("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()

        payload = {"event": event_type, "data": data}

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=pickle.dumps(payload)
            ),
            routing_key="notifications",
        )
    print(f"[RabbitMQ] Событие '{event_type}' отправлено в очередь")
