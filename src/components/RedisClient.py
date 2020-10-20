import redis
import sys

class RedisClient:
    client = None
    pubsub = None
    isSub = False
    host = '127.0.0.1'
    password = '' # Ccnkbq9V4KDVCyT5FfYpH7ZPhcvisYCf

    def __init__(self): 
        self.client = redis.Redis(host=self.host, port=6379, password=self.password)

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

    def setValue(self, key, value):
        self.client.set(key, value)