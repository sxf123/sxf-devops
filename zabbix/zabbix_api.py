from pyzabbix import ZabbixAPI
import traceback

def login(url,username,password):
    zapi = ZabbixAPI(url)
    zapi.login(user=username,password=password)
    return zapi

def get_visible_name(zapi):
    hostids = zapi.host.get()
    visible_name_list = [h["name"] for h in hostids["result"]]
    return visible_name_list

def get_hostname(zapi):
    hostnames = ZabbixAPI.do_request(zapi,"host.get")
    hostname_list = [h["name"] for h in hostnames["result"]]
    return hostname_list

def get_template(zapi):
    templates = ZabbixAPI.do_request(zapi,"template.get")
    template_list = [(t["templateid"],t["host"]) for t in templates["result"]]
    template_list.insert(0,("","请选择"))
    return template_list

def get_groupname(zapi):
    groups = ZabbixAPI.do_request(zapi,"hostgroup.get")
    group_list = [(g["groupid"],g["name"]) for g in groups["result"]]
    group_list.insert(0,("","请选择"))
    return group_list

def get_groupid(zapi,groupname):
    groupid = ZabbixAPI.do_request(zapi,"hostgroup.get",params={"filter":{"name":groupname}})
    try:
        return groupid["resutl"][0]["groupid"]
    except KeyError as e:
        add_group = ZabbixAPI.do_request(zapi,"hostgroup.create",params={"name":groupname})
        return add_group["result"]["groupids"][0]

def get_templateid(zapi,templatename):
    templateid = ZabbixAPI.do_request(zapi,"template.get",params={"filter": {"host": templatename}})
    try:
        return templateid["result"][0]["templateid"]
    except KeyError as e:
        return None


def add_host(zapi,hostname,groupid,ip,status,templateid,visible_name):
    param = {
        "host": hostname,
        "name": visible_name,
        "groups": [
            {
                "groupid": groupid,
            }
        ],
        "templates": templateid,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050",
                "status": status
            }
        ]
    }
    try:
        ZabbixAPI.do_request(zapi,"host.create",params=param)
    except Exception as e:
        traceback.print_exc()


