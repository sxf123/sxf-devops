from cmdb.models.Host import Host
from cmdb.models.Cluster import Cluster
import os

def save_host(host_model_dict):
    host_name = host_model_dict.get("host_name")
    kernel = host_model_dict.get("kernel")
    osrelease = host_model_dict.get("osrelease")
    os = host_model_dict.get("os")
    host = Host(host_name=host_name,kernel=kernel,osrelease=osrelease,os=os)
    host.save()
def get_host_field():
    cwd = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(cwd,"host.txt")
    with open(filename,"r",encoding="utf-8") as f:
        host_model_list = [h for h in f.readlines()]
        f.close()
    host_model_dict = []
    for h in host_model_list:
        host = {
            "host_name": h.split(",")[0],
            "kernel": h.split(",")[1],
            "osrelease": h.split(",")[2],
            "os": h.split(",")[3]
        }
        host_model_dict.append(host)
    return host_model_dict