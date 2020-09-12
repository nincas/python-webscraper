import asyncio
import json
import logging
import websockets
import redis
from .RedisClient import RedisClient

logging.basicConfig()

STATE = {"value": {} }

USERS = set()

# client = redis.Redis(host='10.19.3.24', port=6379, password='Ccnkbq9V4KDVCyT5FfYpH7ZPhcvisYCf')
# pubsub = client.pubsub()
# pubsub.subscribe('btc-value')
client = RedisClient()
pubsub = client.subToKey('btc-value')

def state_event():
    return json.dumps({"type": "btc", **STATE['value']})


def users_event():
    return json.dumps({"type": "users", "value": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def handler(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    await websocket.send(users_event())
    try:
        while True:
            message = pubsub.getSubMessage();
            if message and not message['data'] == 1: 
                print(message['data'].decode('utf-8'))
                jstr = json.loads(message['data'].decode('utf-8'))
                STATE['value'] = jstr
                await notify_state()
    finally:
        await unregister(websocket)


