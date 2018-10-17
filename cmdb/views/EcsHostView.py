from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from cmdb.models.EcsHost import EcsHost
from cmdb.forms.EcsHostForm import EcsHostSearchForm,EcsHostAddForm
from django.forms import model_to_dict
from saltjob.update_ecshost_info import scan_ecshost
from saltjob.ecs_init import ecs_init
from common.redis_conn import RedisConn
from devops.settings import REDIS_HOST,REDIS_PORT
from django.http import JsonResponse
import json
from cmdb.models.SaltState import SaltState
from jenkinsapi.jenkinsapi import create_node
from jenkinsapi.forms import JenkinsAddNodeForm
from cmdb.forms.EcsHostForm import ZabbixAddForm
from zabbix.zabbix_api import add_host,get_visible_name,get_hostname
from zabbix.zabbix_api import login
from devops.settings import ZABBIX_URL,ZABBIX_URL_VPC,ZABBIX_USER,ZABBIX_PASSWORD

zapi = login(ZABBIX_URL,ZABBIX_USER,ZABBIX_PASSWORD)
zapivpc = login(ZABBIX_URL_VPC,ZABBIX_USER,ZABBIX_PASSWORD)

class EcsHostSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_ecshost",raise_exception=True))
    def get(self,request,*args,**kwargs):
        ecshost_search_form = EcsHostSearchForm()
        ecshost = EcsHost.objects.all()
        self.context = {"ecshost":ecshost,"ecshost_search_form":ecshost_search_form}
        return render(request,"cmdb/ecshost/ecshost_list.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_ecshost",raise_exception=True))
    def post(self,request,*args,**kwargs):
        ecshost_search_form = EcsHostSearchForm(request.POST)
        if ecshost_search_form.is_valid():
            search_instance_id = ecshost_search_form.cleaned_data.get("search_instance_id")
            ecshost = EcsHost.objects.filter(instance_id__contains=search_instance_id)
            self.context = {"ecshost":ecshost,"ecshost_search_form":ecshost_search_form}
        else:
            self.context = {"ecshost_search_form":ecshost_search_form,"errors":ecshost_search_form.errors}
        return render(request,"cmdb/ecshost/ecshost_list.html",self.context)

class EcsHostAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_ecshost",raise_exception=True))
    def get(self,request,*args,**kwargs):
        ecshost_add_form = EcsHostAddForm()
        self.context = {"ecshost_add_form":ecshost_add_form}
        return render(request,"cmdb/ecshost/ecshost_add.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_ecshost",raise_exception=True))
    def post(self,request,*args,**kwargs):
        ecshost_add_form = EcsHostAddForm(request.POST)
        if ecshost_add_form.is_valid():
            instance_id = ecshost_add_form.cleaned_data.get("instance_id")
            hostname = ecshost_add_form.cleaned_data.get("hostname")
            desc = ecshost_add_form.cleaned_data.get("desc")
            local_ip = ecshost_add_form.cleaned_data.get("local_ip")
            internet_ip = ecshost_add_form.cleaned_data.get("internet_ip")
            elastic_ip = ecshost_add_form.cleaned_data.get("elastic_ip")
            network_type = ecshost_add_form.cleaned_data.get("network_type")
            minion_id = ecshost_add_form.cleaned_data.get("minion_id")
            if EcsHost.objects.filter(instance_id=instance_id).exists():
                self.context = {"ecshost_add_form":ecshost_add_form,"ecshost_repeat":"True"}
                return render(request,"cmdb/ecshost/ecshost_add.html",self.context)
            else:
                ecshost = EcsHost(
                    instance_id = instance_id,
                    hostname = hostname,
                    desc = desc,
                    local_ip = local_ip,
                    internet_ip = internet_ip,
                    elastic_ip = elastic_ip,
                    network_type = network_type,
                    minion_id = minion_id
                )
                ecshost.save()
                return HttpResponseRedirect(reverse("ecshost_list"))
        else:
            self.context = {"ecshost_add_form":ecshost_add_form,"errors":ecshost_add_form.errors}
            return render(request,"cmdb/ecshost/ecshost_add.html",self.context)

class EcsHostUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_ecshost",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        ecshost = EcsHost.objects.get(pk=id)
        ecshost_dict = model_to_dict(ecshost)
        ecshost_update_form = EcsHostAddForm(ecshost_dict)
        self.context = {"ecshost_update_form":ecshost_update_form}
        return render(request,"cmdb/ecshost/ecshost_update.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_ecshost",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        ecshost_update_form = EcsHostAddForm(request.POST)
        if ecshost_update_form.is_valid():
            ecshost = EcsHost.objects.get(pk=id)
            ecshost.instance_id = ecshost_update_form.cleaned_data.get("instance_id")
            ecshost.hostname = ecshost_update_form.cleaned_data.get("hostname")
            ecshost.desc = ecshost_update_form.cleaned_data.get("desc")
            ecshost.local_ip = ecshost_update_form.cleaned_data.get("local_ip")
            ecshost.internet_ip = ecshost_update_form.cleaned_data.get("internet_ip")
            ecshost.elastic_ip = ecshost_update_form.cleaned_data.get("elastic_ip")
            ecshost.network_type = ecshost_update_form.cleaned_data.get("network_type")
            ecshost.minion_id = ecshost_update_form.cleaned_data.get("minion_id")
            ecshost.save()
            return HttpResponseRedirect(reverse("ecshost_list"))
        else:
            self.context = {"ecshost_update_form":ecshost_update_form,"errors":ecshost_update_form.errors}
            return render(request,"cmdb/ecshost/ecshost_update.html",self.context)

class EcsHostDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.delete_ecshost",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        ecshost = EcsHost.objects.get(pk=id)
        ecshost.delete()
        return HttpResponseRedirect(reverse("ecshost_list"))

class EcsHostScanInfoView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        minion_id = kwargs.get("minion_id")
        scan_ecshost(minion_id)
        return HttpResponseRedirect(reverse("ecshost_list"))

class EcsHostInitView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        ecshost = EcsHost.objects.get(pk=id)
        redisconn = RedisConn(REDIS_HOST,REDIS_PORT)
        func_dict = redisconn.get_key_no_json("{}_init_func".format(ecshost.minion_id))
        if func_dict is not None:
            func_list = [k for k,v in json.loads(func_dict)["func_list"].items() if v == "true"]
            saltstate = SaltState.objects.exclude(fun_name__in=func_list)
        else:
            saltstate = SaltState.objects.all()
        self.context = {"func_list":saltstate,"minion_id":ecshost.minion_id}
        return render(request,"cmdb/ecshost/select_func.html",self.context)
    def post(self,request,):
        target = request.POST.get("tgt")
        func_list = request.POST.getlist("func_list")
        for func in func_list:
            ecs_init(target,func)
        func_dict = {func:"true" for func in func_list}
        redisconn = RedisConn(REDIS_HOST,REDIS_PORT)
        key = "{}_init_func".format(target)
        value = {"func_list":func_dict}
        redisconn.set_key(key,json.dumps(value))
        return JsonResponse({"message":"initial success"})

class EcsHostInitResView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        target = kwargs.get("target")
        key = "{}_init_func".format(target)
        redisconn = RedisConn(REDIS_HOST,REDIS_PORT)
        func_list = redisconn.get_key(key)["func_list"]
        install_res = {}
        for func in func_list:
            res_key = "{}_{}".format(target,func)
            install_res[func] = redisconn.get_key(res_key)
        self.context = {"install_res":install_res,"target":target}
        return render(request,"cmdb/ecshost/ecshost_init_res.html",self.context)

class JenkinsAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        ecshost = EcsHost.objects.get(pk=id)
        minion_id = ecshost.minion_id
        form_dict={"name":minion_id,"port":"22181","user":"jenkins","javaPath":"/opt/java/bin/java"}
        jenkins_add_node_form = JenkinsAddNodeForm(form_dict)
        self.context = {"jenkins_add_node_form":jenkins_add_node_form}
        return render(request,"jenkins/node/node_add.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        jenkins_add_node_form = JenkinsAddNodeForm(request.POST)
        if jenkins_add_node_form.is_valid():
            name = jenkins_add_node_form.cleaned_data.get("name")
            port = jenkins_add_node_form.cleaned_data.get("port")
            user = jenkins_add_node_form.cleaned_data.get("user")
            credentialsId = jenkins_add_node_form.cleaned_data.get("credentialsId")
            host = jenkins_add_node_form.cleaned_data.get("host")
            javaPath = jenkins_add_node_form.cleaned_data.get("javaPath")
            if create_node(port,user,credentialsId,host,javaPath,name) == 1:
                return HttpResponseRedirect(reverse("ecshost_list"))
            elif create_node(port,user,credentialsId,host,javaPath,name) == 0:
                self.context = {"jenkins_add_node_form":jenkins_add_node_form,"errors":"true"}
        else:
            self.context = {"jenkins_add_node_form":jenkins_add_node_form,"errors":jenkins_add_node_form.errors}
            return render(request,"jenkins/node/node_add.html",self.context)
class ZabbixAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        ecshost = EcsHost.objects.get(pk=id)
        form_dict = {"hostname":ecshost.minion_id,"ip":ecshost.local_ip}
        zabbix_add_form = ZabbixAddForm(form_dict,network_type=ecshost.network_type)
        self.context = {"zabbix_add_form":zabbix_add_form}
        return render(request,"zabbix/zabbix_add_node.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        ecshost = EcsHost.objects.get(pk=id)
        zabbix_add_form = ZabbixAddForm(request.POST,network_type=ecshost.network_type)
        if zabbix_add_form.is_valid():
            visible_name = zabbix_add_form.cleaned_data.get("visible_name")
            hostname = zabbix_add_form.cleaned_data.get("hostname")
            ip = zabbix_add_form.cleaned_data.get("ip")
            templateid = zabbix_add_form.cleaned_data.get("templatename")
            groupid = zabbix_add_form.cleaned_data.get("groupname")
            vpc = zabbix_add_form.cleaned_data.get("vpc")
            if vpc == "yes":
                hostname_list = get_hostname(zapivpc)
                visible_name_list = get_hostname(zapivpc)
                if visible_name in visible_name_list and hostname not in hostname_list:
                    self.context = {"zabbix_add_form":zabbix_add_form,"visible_name_repeat":"true"}
                    return render(request,"zabbix/zabbix_add_node.html",self.context)
                elif visible_name not in visible_name and hostname in hostname_list:
                    self.context = {"zabbix_add_form":zabbix_add_form,"host_name_repeat":"true"}
                    return render(request,"zabbix/zabbix_add_node.html",self.context)
                elif visible_name in visible_name and hostname in hostname_list:
                    self.context = {"zabbix_add_form":zabbix_add_form,"host_name_repeat":"true","visible_name_repeat":"true"}
                    return render(request,"zabbix/zabbix_add_node.html",self.context)
                else:
                    add_host(zapivpc,hostname,groupid,ip,0,templateid,visible_name)
                    return HttpResponseRedirect(reverse("ecshost_list"))
            elif vpc == "no":
                hostname_list = get_hostname(zapi)
                visible_name_list = get_hostname(zapivpc)
                if visible_name in visible_name_list and hostname not in hostname_list:
                    self.context = {"zabbix_add_form":zabbix_add_form,"visible_name_repeat":"true"}
                    return render(request, "zabbix/zabbix_add_node.html", self.context)
                elif visible_name not in visible_name_list and hostname in hostname_list:
                    self.context = {"zabbix_add_form":zabbix_add_form,"hostname_name_repeat":"true"}
                    return render(request, "zabbix/zabbix_add_node.html", self.context)
                elif visible_name in visible_name_list and hostname in hostname_list:
                    self.context = {"zabbix_add_form":zabbix_add_form,"host_name_repeat":"true","visible_name_repeat":"true"}
                    return render(request, "zabbix/zabbix_add_node.html", self.context)
                else:
                    add_host(zapi,hostname,groupid,ip,0,templateid,visible_name)
                    return HttpResponseRedirect(reverse("ecshost_list"))
        else:
            self.context = {"zabbix_add_form":zabbix_add_form,"errors":zabbix_add_form.errors}
            return render(request,"zabbix/zabbix_add_node.html",self.context)
