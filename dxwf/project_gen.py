#-*- coding: utf-8 -*-
import os
import shutil
from devops.settings import DEFAUTL_LOGGER
import logging
import tarfile
from devops.settings import DXWF_PKG_DIR
import subprocess

logger = logging.getLogger(DEFAUTL_LOGGER)

config_list = [
    "dubbo.properties",
    "jdbc.properties",
    "redis.properties",
    "sso.properties",
    "url.properties"
]

def list_files(path,files):
    for filename in os.listdir(path):
        if os.path.isdir("{}/{}".format(path,filename)):
            list_files("{}/{}".format(path,filename),files)
        else:
            files.append("{}/{}".format(path,filename))
    return files

def get_dirs(files):
    for i in range(len(files)):
        dir = files[i].rstrip(files[i].split("/")[-1]).rstrip("/")
        files[i] = dir
    return files

def gen_project(service,groupId, artifactId):
    cwd = DXWF_PKG_DIR
    shutil.copytree(os.path.join(cwd,service),os.path.join(cwd,artifactId))
    dirs = get_dirs(list_files(os.path.join(cwd,artifactId),[]))
    path_pre_dirs = []
    path_post_dirs = []
    for d in dirs:
        if "com/jcgroup/demo" in d:
            path_pre = os.path.join(cwd,d.split("demo")[0])+":"+d.split("demo")[1].lstrip("/").split("/")[0]
            path_pre_dirs.append(path_pre)
    print(path_pre_dirs)
    for p in set(path_pre_dirs):
        dir_name = "/".join(artifactId.split("-")[1:-1])
        os.makedirs(p+"demo/"+dir_name)
        shutil.move(p.split(":")[0]+"demo/"+p.split(":")[1],p+"demo/"+dir_name)
        shutil.move(p.split(":")[0]+"demo",p.split(":")[0]+"/"+groupId.split(".")[-1])
    files = list_files(os.path.join(cwd,artifactId),[])
    for filename in files:
        if filename.split("/")[-1] == "pom.xml":
            modify_pom(filename,groupId,artifactId)
        elif filename.split("/")[-1].split(".")[1] == "java":
            modify_java(filename,groupId)
        elif filename.split("/")[-1] == "disconf.properties":
            modify_disconf(filename,artifactId)
        elif filename.split("/")[-1] == "dubbo.properties":
            modify_dubbo(filename,groupId,artifactId)
        elif filename.split("/")[-1] == "disconf.xml":
            modify_disconf_xml(filename,groupId)
        elif filename.split("/")[-1] == "application.properties":
            modify_application(filename,artifactId)
        elif filename.split("/")[-1] == "log4j.xml":
            modify_log4j(filename,groupId)
    for file in files:
        if file.split("/")[-1] in config_list:
            shutil.copy(file,os.path.join(os.path.join(cwd,artifactId),"config"))
    os.chdir(cwd)
    subprocess.check_call(["tar","-czvf","{}.tar.gz".format(artifactId),artifactId],shell=False)

def modify_pom(pomfile,groupId,artifactId):
    with open(pomfile,"r",encoding="utf-8") as f:
        pom_list = f.readlines()
        f.close()
    for p in range(len(pom_list)):
        if "com.jcgroup.demo" in pom_list[p]:
            p_re = pom_list[p].replace("com.jcgroup.demo",groupId)
            pom_list[p] = p_re
        elif "jc-consumer" in pom_list[p]:
            p_re = pom_list[p].replace("jc-consumer",artifactId)
            pom_list[p] = p_re
            # print(pom_list[p])
    with open(pomfile,"w") as f:
        pom_str = "".join(pom_list)
        f.write(pom_str)
        f.close()

def modify_java(javafile,groupId):
    with open(javafile,"r",encoding="utf-8") as f:
        java_list = f.readlines()
        f.close()
    for j in range(len(java_list)):
        if "com.jcgroup.demo" in java_list[j]:
            j_re = java_list[j].replace("com.jcgroup.demo",groupId)
            java_list[j] = j_re
    with open(javafile,"w") as f:
        java_str = "".join(java_list)
        f.write(java_str)
        f.close()
def modify_disconf(disconf_file,artifactId):
    with open(disconf_file,"r",encoding="utf-8")  as f:
        disconf_list = f.readlines()
        f.close()
    for d in range(len(disconf_list)):
        if "disconf.conf_server_host" in disconf_list[d]:
            d_re = disconf_list[d].replace(disconf_list[d].split("=")[1],"10.100.246.23:8000")
            disconf_list[d] = d_re
        elif "disconf.app" in disconf_list[d]:
            d_re = disconf_list[d].replace(disconf_list[d].split("=")[1],artifactId)
            disconf_list[d] = d_re
        elif "disconf.user_define_download_dir" in disconf_list[d]:
            d_re = disconf_list[d].replace(disconf_list[d].split("/")[-1],artifactId)
            disconf_list[d] = d_re
    with open(disconf_file,"w") as f:
        disconf_str = "".join(disconf_list)
        f.write(disconf_str)
        f.close()
def modify_dubbo(dubbo_file,groupId,artifactId):
    with open(dubbo_file,"r",encoding="utf-8") as f:
        dubbo_list = f.readlines()
        f.close()
    for d in range(len(dubbo_list)):
        if "dubbo.application.name" in dubbo_list[d]:
            d_re = dubbo_list[d].replace(dubbo_list[d].split("=")[1].rstrip("\n"),artifactId)
            dubbo_list[d] = d_re
        elif "dubbo.registry.address" in dubbo_list[d]:
            d_re = dubbo_list[d].replace(dubbo_list[d].split("=")[1].rstrip("\n"),"10.100.243.14:2181")
            dubbo_list[d] = d_re
        elif "dubbo.annotation.package" in dubbo_list[d]:
            d_re = dubbo_list[d].replace(dubbo_list[d].split("=")[1].rstrip("\n"),groupId)
            dubbo_list[d] = d_re
    with open(dubbo_file,"w") as f:
        dubbo_str = "".join(dubbo_list)
        f.write(dubbo_str)
        f.close()
def modify_application(application_file,artifactId):
    with open(application_file,"r",encoding="utf-8") as f:
        application_list = f.readlines()
        f.close()
    for a in range(len(application_list)):
        if "spring.applicationname" in application_list[a]:
            a_re = application_list[a].replace(application_list[a].split("=")[1].rstrip("\n"),artifactId)
            application_list[a] = a_re
    with open(application_file,"w") as f:
        application_str = "".join(application_list)
        f.write(application_str)
        f.close()
def modify_disconf_xml(disconf_xml_file,groupId):
    with open(disconf_xml_file,"r",encoding="utf-8") as f:
        disconf_xml_list = f.readlines()
        f.close()
    for d in range(len(disconf_xml_list)):
        if "com.jcgroup.demo" in disconf_xml_list[d]:
            d_re = disconf_xml_list[d].replace("com.jcgroup.demo",groupId)
            disconf_xml_list[d] = d_re
    with open(disconf_xml_file,"w") as f:
        disconf_xml_str = "".join(disconf_xml_list)
        f.write(disconf_xml_str)
        f.close()
def modify_log4j(log4j_file,groupId):
    with open(log4j_file,"r",encoding="utf-8") as f:
        log4j_list = f.readlines()
        f.close()
    for l in range(len(log4j_list)):
        if "com.jcgroup.demo" in log4j_list[l]:
            l_re = log4j_list[l].replace("com.jcgroup.demo",groupId)
            log4j_list[l] = l_re
    with open(log4j_file,"w") as f:
        log4j_str = "".join(log4j_list)
        f.write(log4j_str)
        f.close()
def tarpackage(files,artifactId):
    tar = tarfile.open("{}.tar.gz".format(artifactId),"w:gz")
    for filename in files:
        tar.add(filename)
    tar.close()
def remove_proj(artifactId):
    cwd = os.path.dirname(os.path.abspath(__file__))
    os.remove(os.path.join(cwd,"{}.tar.gz".format(artifactId)))
    shutil.rmtree(os.path.join(cwd,artifactId))


