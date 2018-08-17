import requests
import json
import traceback

class SaltAPI(object):
    def __init__(self,data,url,token):
        self.data = data
        self.token = token
        self.headers = {"Accept":"application/json"}
        self.url = url
        self.headers.update({"X-Auth-Token":token})
    def cmdrun(self,client="local"):
        self.data["client"] = client
        req = requests.post(self.url,headers=self.headers,json=self.data,verify=False)
        context = req.text
        return json.loads(context)
    def wheelrun(self,client="wheel"):
        self.data["client"] = client
        req = requests.post(self.url,headers=self.headers,json=self.data,verify=False)
        context = req.text
        return json.loads(context)
    def runnerrun(self,client="runner"):
        self.data["client"] = client
        req = requests.post(self.url,headers=self.headers,json=self.data,verify=False)
        context = req.text
        return json.loads(context)

