import asyncio
import json
import aioredis

class RedisClientAsync:
    client = None
    pubsub = None
    isSub = False
    channel = None
    host = '10.19.3.24'
    password = 'Ccnkbq9V4KDVCyT5FfYpH7ZPhcvisYCf'

    async def main(self):
        self.client = await aioredis.create_redis_pool(address=(self.host, 6379), password=self.password)
        return self

    def getClient(self):
        return self.client

    async def subToKey(self, pattern):
        self.channel = pattern
        self.pubsub = await self.client.subscribe(pattern)
        self.isSub = True
        return self

    async def getChannels(self):
        return self.client.channels[self.channel]

    async def publishValue(self, key, value):
        await self.client.publish(key, value)