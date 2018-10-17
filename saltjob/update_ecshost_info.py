from saltjob.get_api_token import get_token
from saltjob.salt_http_api import SaltAPI
from devops.settings import SALT_REST_URL
from cmdb.models.EcsHost import EcsHost

def scan_ecshost(minion_id):
    token = get_token()
    data = {
        "tgt": minion_id,
        "fun": "grains.items"
    }
    salt_api_object = SaltAPI(data,SALT_REST_URL,token)
    host_res = salt_api_object.cmdrun()["return"][0]
    ecshost = EcsHost.objects.get(minion_id=minion_id)
    ecshost.hostname = host_res[minion_id]["nodename"]
    ecshost.cpu_nums = host_res[minion_id]["num_cpus"]
    ecshost.memory = host_res[minion_id]["mem_total"]
    ecshost.save()
