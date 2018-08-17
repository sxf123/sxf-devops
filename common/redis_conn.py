import redis
import json

class RedisConn(object):
    def __init__(self,redis_host,redis_port):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_conn = redis.Redis(host=redis_host,port=redis_port)

    def set_key(self,key,val):
        return self.redis_conn.set(key,val)
    def get_key(self,key):
        s = self.redis_conn.get(key).decode("utf-8")
        return json.loads(s)