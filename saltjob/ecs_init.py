from saltjob.salt_http_api import SaltAPI
from saltjob.get_api_token import get_token
from devops.settings import SALT_REST_URL
from common.redis_conn import RedisConn
from devops.settings import REDIS_PORT,REDIS_HOST
import json

def ecs_init(tgt,func):
    data = {
        "client": "local",
        "tgt": tgt,
        "fun": "state.sls",
        "arg": func
    }
    token = get_token()
    salt_api_object = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_object.cmdrun()
    redisconn = RedisConn(REDIS_HOST,REDIS_PORT)
    key = "{}_{}".format(tgt,func)
    redisconn.set_key(key,json.dumps(res))
