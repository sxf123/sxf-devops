from saltjob.salt_http_api import SaltAPI
from devops.settings import SALT_REST_URL
from saltjob.get_api_token import get_token

def transfer_script(tgt,script_dir,script_name):
    data = {
        "tgt": tgt,
        "fun": "cp.get_file",
        "arg": [
            "salt://scripts/{}".format(script_name),
            "{}/{}".format(script_dir,script_name)
        ],
        "expr_form": "list"
    }
    token = get_token()
    salt_api_object = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_object.cmdrun()["return"][0]
    return res

def execute_script(tgt,script_name,args=[]):
    data = {
        "tgt": tgt,
        "fun": "cmd.script",
        "arg": [
            "salt://scripts/{}".format(script_name),
            " ".join(args)
        ]
    }
    token = get_token()
    salt_api_object = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_object.cmdrun()
    return res

def get_minions():
    data = {
        "tgt": "*",
        "fun": "key.list_all",
    }
    token = get_token()
    salt_api_object = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_object.wheelrun()["return"][0]["data"]["return"]["minions"]
    return res
