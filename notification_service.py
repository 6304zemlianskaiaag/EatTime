# notification_service.py
import asyncio
import json
import aio_pika
import websockets

# Хранилище подключенных клиентов
connected_clients = set()


async def websocket_handler(websocket):
    print(f"[WS] Клиент подключился: {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        print(f"[WS] Клиент отключился: {websocket.remote_address}")


async def rabbitmq_listener():
    # Подключаемся к RabbitMQ
    connection = await aio_pika.connect("amqp://guest:guest@localhost/")
    channel = await connection.channel()

    # Объявляем очередь
    queue = await channel.declare_queue("notifications", durable=True)

    print("[RabbitMQ] Ожидание сообщений...")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                body = json.loads(message.body.decode())
                print(f"[RabbitMQ] Получено событие: {body}")

                # Отправляем всем подключенным клиентам
                if connected_clients:
                    text = f"Уведомление: {body['event']} (ID брони: {body['data']['booking_id']})"
                    await asyncio.gather(*[client.send(text) for client in connected_clients])


async def main():
    # Запускаем WebSocket-сервер на порту 8765
    ws_server = await websockets.serve(websocket_handler, "localhost", 8765)
    print("=== Notification Service (WebSocket) запущен на ws://localhost:8765 ===")

    # Запускаем слушатель RabbitMQ
    await rabbitmq_listener()

    await ws_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())