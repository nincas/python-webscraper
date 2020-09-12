import redis
import sys

class RedisClient:
    client = None
    pubsub = None
    isSub = False

    def __init__(self): 
        self.client = redis.Redis(host='10.19.3.24', port=6379, password='Ccnkbq9V4KDVCyT5FfYpH7ZPhcvisYCf')

    def getClient(self):
        return self.client

    def subToKey(self, pattern):
        self.pubsub = self.client.pubsub()
        self.pubsub.subscribe(pattern)
        self.isSub = True
        return self

    def getSubMessage(self):
        message = self.pubsub.get_message()
        return message

    def publishValue(self, key, value):
        self.client.publish(key, value)