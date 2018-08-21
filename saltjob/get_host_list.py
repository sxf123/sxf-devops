from devops.settings import REDIS_HOST,REDIS_PORT
import redis
import traceback
import json

mid_dict = {
    "zookeeper":"3.4.10",
    "redis":"3.2.11",
    "nginx":"1.10.3"
}

def get_host_list(midware):
    r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
    res = r.smembers(midware)
    return res

def set_host(midware,host):
    r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
    r.sadd(midware,host)

def get_mid_list(tgt):
    r = redis.Redis(host = REDIS_HOST,port = REDIS_PORT)
    val = r.get(tgt).decode("utf-8").replace("'","\"")
    return json.loads(val)
def set_list(key,mid_list):
    tgt = key
    r = redis.Redis(host = REDIS_HOST,port = REDIS_PORT)
    midware_dict = {}
    midware_list = []
    for m in mid_list:
        m_dict = {"name":m,"installed":"false"}
        midware_list.append(m_dict)
    midware_dict["middleware_list"] = midware_list
    try:
        r.set(key,midware_dict)
    except Exception:
        traceback.print_exc()
def modify_list(key,midware):
    tgt = key
    r = redis.Redis(host = REDIS_HOST,port = REDIS_PORT)
    mid_list = []
    midware_dict = {}
    for k,v in mid_dict.items():
        if k == midware:
            m_dict = {"name":k,"installed":"true"}
            mid_list.append(m_dict)
        else:
            m_dict = {"name":k,"installed":"false"}
            mid_list.append(m_dict)
    midware_dict["middleware_list"] = mid_list
    try:
        r.set(key,midware_dict)
    except Exception:
        traceback.print_exc()
def del_host(key):
    tgt = key
    r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
    r.delete(key)
def del_mid_host(midware,host):
    r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
    r.srem(midware,host)
