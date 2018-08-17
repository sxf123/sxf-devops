import requests
from devops.settings import SALT_REST_URL,SALT_API_PASSWD,SALT_API_USER
import json

def get_token(hostname):
    data = {"username": SALT_API_USER,"password": SALT_API_PASSWD,"eauth": "pam"}
    headers = {"Accept":"application/json"}
    url = "{}/login".format(SALT_REST_URL)
    res = requests.post(url,headers=headers,data=data)
    if res.status_code == 200:
        return json.loads(res.text)["return"][0]["token"]
    else:
        return None

