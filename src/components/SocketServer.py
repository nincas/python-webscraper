import asyncio
import json
import logging
import websockets
from websockets import WebSocketClientProtocol
import redis
import socket
from .RedisClientAsync import RedisClientAsync

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO)

class SocketServer:
    PORT = 6789
    FORMAT = 'utf-8'
    SERVER = socket.gethostbyname(socket.gethostname())
    clients = set()
    STATE = {"value": {} }
    # client = RedisClient()
    # pubsub = client.subToKey('btc-value')
    ALLOWED_ORIGINS = [
        '127.0.0.1'
    ]
    
    async def register(self, ws: WebSocketClientProtocol) -> None:
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketClientProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketClientProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketClientProtocol) -> None:
        async for message in ws:
            msg = json.loads(message)
            logging.info(msg)
            if msg:
                client = await RedisClientAsync().main()
                ch = await client.subToKey('btc-value')
                pubsub = await ch.getChannels()
                while await pubsub.wait_message():
                    msg = await pubsub.get()
                    if msg:
                        await self.send_to_clients(msg.decode(self.FORMAT))

    # Starting function to run the server
    def start(self):
        logging.info(f'Server has started.')
        startServer = websockets.serve(self.ws_handler, self.SERVER, self.PORT)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(startServer)
        loop.run_forever()