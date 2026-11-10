# app/rabbit.py
import aio_pika
import json

async def publish_event(event_type: str, data: dict):
    # Подключаемся к RabbitMQ
    connection = await aio_pika.connect("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        # Отправляем сообщение в очередь "notifications"
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps({"event": event_type, "data": data}).encode()
            ),
            routing_key="notifications",
        )
    print(f"[RabbitMQ] Событие '{event_type}' отправлено в очередь")