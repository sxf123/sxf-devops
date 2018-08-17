from saltjob.salt_http_api import SaltAPI
from devops.settings import SALT_REST_URL
from saltjob.get_api_token import get_token

def run_state(tgt,tgt_type,midware):
    data = {
        "client":"local",
        "tgt":tgt,
        "fun":"state.sls",
        "arg":"{}".format(midware),
        "tgt_type": tgt_type,
        "kwargs": {
            "test": "True"
        }
    }

    token = get_token(tgt)
    salt_api_obj = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_obj.cmdrun()
    return res
