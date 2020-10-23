import asyncio
import json
import logging
import websockets
from websockets import WebSocketClientProtocol
import redis
import socket
from .RedisClientAsync import RedisClientAsync
from time import sleep

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO)

class SocketServer:
    PORT = 3003
    FORMAT = 'utf-8'
    SERVER = socket.gethostbyname(socket.gethostname())
    CLIENTS = set()
    SUBSCRIBERS = {}
    STATE = {"value": {} }
    ALLOWED_ORIGINS = [
        '127.0.0.1'
    ]
    
    # Register socket user on list
    async def register(self, ws: WebSocketClientProtocol) -> None:
        self.CLIENTS.add(ws)
        self.SUBSCRIBERS[ws.remote_address] = ws;
        logging.info(f'{ws.remote_address} connects')




    # Remove socket user on list
    async def unregister(self, ws: WebSocketClientProtocol) -> None:
        self.CLIENTS.remove(ws)
        del self.SUBSCRIBERS[ws.remote_address]
        logging.info(f'{ws.remote_address} disconnects')



    # Broadcaster
    async def send_to_clients(self, message: str) -> None:
        if self.CLIENTS:
            await asyncio.wait([client.send(message) for client in self.CLIENTS])



    # Main handler/entry point
    async def ws_handler(self, ws: WebSocketClientProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)




    # Distributor function handles all messages and publish events
    async def distribute(self, ws: WebSocketClientProtocol) -> None:
        async for message in ws:
            msg = json.loads(message)
            logging.info(msg)
            if msg:
                client = await RedisClientAsync().main()
                ch = await client.subToKey('btc-value-' + msg['source'])
                pubsub = await ch.getChannels()
                while await pubsub.wait_message():
                    msg = await pubsub.get()
                    # sleep(0.2)
                    if msg:
                        await self.SUBSCRIBERS[ws.remote_address].send(msg.decode(self.FORMAT))
                        #await ws.send(msg.decode(self.FORMAT))



    # Starting function to run the server
    def start(self):
        logging.info(f'Server has started. {self.SERVER}@{self.PORT}')
        startServer = websockets.serve(self.ws_handler, self.SERVER, self.PORT)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(startServer)
        loop.run_forever()