from saltjob.salt_http_api import SaltAPI
from devops.settings import SALT_REST_URL
from saltjob.get_api_token import get_token
from devops.settings import DNS_CONF_FILE,DNS_SERVER

def append_domainname(dns,domainname_type,ip_address):
    token=get_token(DNS_SERVER)
    dns_record = "{}     IN     {}     {}".format(dns,domainname_type,ip_address)
    data = {
        "client":"local",
        "tgt":DNS_SERVER,
        "fun":"file.append",
        "arg":[DNS_CONF_FILE,dns_record],
    }
    salt_api_obj = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_obj.cmdrun()
    return res

def sed_domainname(srcstr,deststr):
    token = get_token(DNS_SERVER)
    data = {
        "client":"local",
        "tgt":DNS_SERVER,
        "fun":"file.sed",
        "arg":[DNS_CONF_FILE,srcstr,deststr]
    }
    salt_api_obj = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_obj.cmdrun()
    return res

def comment_domainname(regex_str):
    token = get_token(DNS_SERVER)
    data = {
        "client":"local",
        "tgt":DNS_SERVER,
        "fun":"file.comment",
        "arg":[DNS_CONF_FILE,regex_str]
    }
    salt_api_obj = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_obj.cmdrun()
    return res

def reload_bind():
    token = get_token(DNS_SERVER)
    data = {
        "client":"local",
        "tgt":DNS_SERVER,
        "fun":"cmd.run",
        "arg":"systemctl restart named"
    }
    salt_api_obj = SaltAPI(data,SALT_REST_URL,token)
    res = salt_api_obj.cmdrun()
    return res

