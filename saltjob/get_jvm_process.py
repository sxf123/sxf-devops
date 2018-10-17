from saltjob.get_api_token import get_token
from saltjob.salt_http_api import SaltAPI
from devops.settings import GET_JAVA_PROCESS_SCRIPT
from devops.settings import SALT_REST_URL

def get_jvm_pid(tgt):
    token = get_token()
    data = {
        "tgt": tgt,
        "fun": "cmd.script",
        "arg": GET_JAVA_PROCESS_SCRIPT
    }
    salt_api_object = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_object.cmdrun()["return"][0][tgt]["stdout"].split("\n")
    return res