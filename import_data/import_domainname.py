from cmdb.models.DomainName import DomainName
from cmdb.models.IpPool import IpPool
import os

def save_domainname(domainname_model_dict):
    dns = domainname_model_dict.get("dns")
    ip = IpPool.objects.get(ip_address=domainname_model_dict.get("ip"))
    domain_type = domainname_model_dict.get("domain_type")
    domainname = DomainName(dns=dns,domain_type=domain_type,ip=ip)
    domainname.save()

def get_domainname_fields():
    cwd = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(cwd,"dns_t.txt")
    with open(filename,"r",encoding="utf-8") as f:
        domainname_model_list = [d for d in f.readlines()]
        f.close()
    domainname_models_dict = []
    for d in domainname_model_list:
        print(d.split(","))
        domainname = {
            "dns":d.split(",")[0],
            "domain_type":d.split(",")[1],
            "ip":d.split(",")[2].strip("\n")
        }
        domainname_models_dict.append(domainname)
    return domainname_models_dict