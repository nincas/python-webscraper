import websockets
import asyncio
from src.components.SocketServer import handler

# Start script of websocket
start_server = websockets.serve(handler, "localhost", 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()