import asyncio
import websockets

async def run():
    async with websockets.connect("ws://localhost:8080/ws") as ws:
        await ws.send("hello")
        print(await ws.recv())

asyncio.run(run())
