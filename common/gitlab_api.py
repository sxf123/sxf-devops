import requests
from devops.settings import GITLAB_URL,GITLAB_TOKEN

def get_project_id(project_name):
    endpoint = "/api/v4/projects?search={}".format(project_name)
    url = "{}{}".format(GITLAB_URL,endpoint)
    headers = {"PRIVATE-TOKEN":GITLAB_TOKEN}
    req = requests.get(url,headers = headers)
    req.encoding = "utf-8"
    return req.text[0]["name"]

def get_file_content(file_path,branch,project_id):
    endpoint = "/api/v4/projects/{}/repository/files".format(project_id)
    url = "{}{}{}/raw?ref={}".format(GITLAB_URL,endpoint,file_path,branch)
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    req = requests.get(url,headers = headers)
    req.encoding = "utf-8"
    return req.text

