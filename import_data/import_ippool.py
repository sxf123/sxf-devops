from cmdb.models.IpPool import IpPool
import os

def save_ippool(ip_model_dict):
    ip_address = ip_model_dict.get("ip_address")
    gateway = ip_model_dict.get("gateway")
    ip_segment = ip_model_dict.get("ip_segment")
    ip_type = ip_model_dict.get("ip_type")
    ippool = IpPool(ip_address=ip_address,gateway=gateway,ip_segment=ip_segment,ip_type=ip_type)
    ippool.save()

def get_ippool_fields():
    cwd = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(cwd,"ip_t.txt")
    with open(filename,"r",encoding="utf-8") as f:
        ippool_model_list = [i for i in f.readlines()]
        f.close()
    ippool_models_dict = []
    for i in ippool_model_list:
        ippool = {
            "ip_address":i.split(",")[0],
            "gateway": i.split(",")[1],
            "ip_segment": i.split(",")[2],
            "ip_type": i.split(",")[3].strip("\n")
        }
        ippool_models_dict.append(ippool)
    return ippool_models_dict