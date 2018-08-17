import requests
from devops.settings import DISCONF_URL,DISCONF_USER,DISCONF_PASSWORD
import json

def config_list(appId,envId,version):
    session = requests.Session()
    log_endpoint = "/api/account/signin"
    data = {"name":DISCONF_USER,"password":DISCONF_PASSWORD,"remember":"1"}
    session.post(DISCONF_URL + log_endpoint,data=data)
    config_endpoint = "/api/web/config/list?appId={}&envId={}&version={}".format(appId,envId,version)
    req = session.get(DISCONF_URL + config_endpoint)
    res = json.loads(req.text).get("page").get("result")
    file_list = [r.get("key") for r in res]
    return file_list

def get_appId(appName):
    session = requests.Session()
    log_endpoint = "/api/account/signin"
    data = {"name":"admin","password":DISCONF_PASSWORD,"remember":"1"}
    session.post(DISCONF_URL + log_endpoint,data = data)
    app_endpoint = "/api/app/list"
    req = session.get(DISCONF_URL + app_endpoint)
    res = json.loads(req.text).get("page").get("result")
    appId = None
    for r in res:
        if appName == r.get("name"):
            appId = r.get("id")
            break
        else:
            continue
    return appId


