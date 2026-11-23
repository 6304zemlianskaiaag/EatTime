# notification_service.py
import asyncio
import json
import pickle
import aio_pika
import websockets

connected_clients = set()
async def websocket_handler(websocket):
    print(f"[WS] Клиент подключился: {websocket.remote_address}")
   # print(f" {websocket.__dict__}")
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
    connection = await aio_pika.connect("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    queue = await channel.declare_queue("notifications", durable=True)

    print("[RabbitMQ] Ожидание сообщений...")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                body = pickle.loads(message.body)
                print(f"[RabbitMQ] Получено событие: {body}")

                if connected_clients:
                    text = f"Уведомление: {body['event']} (ID брони: {body['data']['booking_id']})"
                    for client in connected_clients:
                        await client.send(text)


async def main():
    ws_server = await websockets.serve(websocket_handler, "localhost", 8765)
    print(" Notification Service запущен на ws://localhost:8765")
    await rabbitmq_listener()
    await ws_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())