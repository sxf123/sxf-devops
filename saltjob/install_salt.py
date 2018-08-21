from saltjob.salt_http_api import SaltAPI
from devops.settings import SALT_REST_URL
from saltjob.get_api_token import get_token

def run_state(tgt,expr_form,midware):
    data = {
        "client":"local",
        "tgt":tgt,
        "fun":"state.sls",
        "arg":"{}".format(midware),
        "expr_form": expr_form,
        "kwargs": {
            "test": "True"
        }
    }

    token = get_token(tgt)
    salt_api_obj = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_obj.cmdrun()
    return res
