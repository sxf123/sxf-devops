from devops.settings import DEFAUTL_LOGGER
import logging

logger = logging.Logger(DEFAUTL_LOGGER)

def add_nodegroup(conf_file,nodegroup,host_list):
    with open(conf_file,"a") as f:
        nodegroup_str = "  {}: 'L@{}'\n".format(nodegroup,",".join(host_list))
        f.write(nodegroup_str)
        f.close()

def add_host(conf_file,nodegroup,host_name):
    with open(conf_file,"r",encoding="utf-8") as f:
        nodegroup_list = f.readlines()
        f.close()
    for i in range(len(nodegroup_list)):
        if nodegroup in nodegroup_list[i]:
            host_list = nodegroup_list[i].split(":")[1].lstrip(" 'L@").rstrip("'\n").split(",")
            host_list.append(host_name)
            nodegroup_list[i] = "{}: 'L@{}'\n".format(nodegroup_list[i].split(":")[0],",".join(host_list))
            break
    with open(conf_file,"w") as f:
        nodegroup_list = "".join(nodegroup_list)
        f.write(nodegroup_list)
        f.close()

if __name__ == "__main__":
    add_nodegroup("nodegroup.conf","dev-app-test",["host1","host2"])