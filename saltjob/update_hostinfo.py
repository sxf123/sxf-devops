from saltjob.salt_http_api import SaltAPI
from saltjob.get_api_token import get_token
from devops.settings import SALT_REST_URL
from cmdb.models.Host import Host
from devops.settings import GET_JAVA_PROCESS_SCRIPT
from cmdb.models.IpPool import IpPool

def update_host_info(hostname):
    token = get_token(hostname)
    data = {
        "tgt":hostname,
        "fun":"grains.items"
    }
    salt_api_object = SaltAPI(data,SALT_REST_URL,token)
    host_res = salt_api_object.cmdrun()["return"][0]
    host = Host.objects.get(host_name=hostname)
    host.kernel = host_res[hostname]["kernelrelease"]
    host.osrelease = host_res[hostname]["osrelease"]
    host.os = host_res[hostname]["kernel"]
    host.cpu_nums = host_res[hostname]["num_cpus"]
    host.memory = host_res[hostname]["mem_total"]
    host.host_type = host_res[hostname]["virtual"]
    host.save()

def update_host_cluster(hostname):
    token = get_token(hostname)
    data = {
        "tgt": hostname,
        "fun": "cmd.script",
        "arg": GET_JAVA_PROCESS_SCRIPT
    }
    salt_api_object = SaltAPI(data,SALT_REST_URL,token)
    modules = salt_api_object.cmdrun()["return"][0][hostname]["stdout"]
    module_list = [m.strip(".jar") for m in modules.split('\n')]
    return module_list

def update_host_ip(hostname):
    token = get_token(hostname)
    data = {
        "tgt": hostname,
        "fun": "grains.item",
        "arg": "ip4_interfaces"
    }
    salt_api_object = SaltAPI(data,SALT_REST_URL,token)
    ip_info_dict = salt_api_object.cmdrun()["return"][0][hostname]["ip4_interfaces"]
    for k,v in ip_info_dict.items():
        if k == "br0" or k == "eth0":
            if len(v) != 0:
                ip_info = v[0]
    gateway = "{}.1".format(".".join(ip_info.split(".")[0:3]))
    ip_segment = "{}.0/24".format(".".join(ip_info.split(".")[0:3]))
    ippool = IpPool.objects.filter(ip_address=ip_info)
    if not ippool.exists():
        IpPool.objects.create(
            ip_address=ip_info,
            ip_type = "local",
            gateway = gateway,
            ip_segment = ip_segment,
            host = Host.objects.get(host_name=hostname)
        )



