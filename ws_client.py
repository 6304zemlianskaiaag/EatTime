# ws_client.py
import asyncio
import websockets


async def listen():
    uri = "ws://localhost:8765"
    print(f"Подключение к {uri}...")

    async with websockets.connect(uri) as websocket:
        print("Подключено! Ожидание уведомлений...")
        while True:
            try:
                message = await websocket.recv()
                print(f"\n {message}")
            except websockets.exceptions.ConnectionClosed:
                print("Соединение закрыто")
                break


if __name__ == "__main__":
    asyncio.run(listen())