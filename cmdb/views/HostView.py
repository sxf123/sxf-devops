from django.shortcuts import render
from django.views.generic import View
from cmdb.forms.HostForm import HostSearchForm,HostAddForm
from cmdb.models.Host import Host
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from cmdb.models.Cluster import Cluster
from saltjob.update_hostinfo import update_host_info,update_host_cluster,update_host_ip
from saltjob.get_host_list import set_host,set_list,get_mid_list,del_host,del_mid_host
from django.db import connection
from cmdb.models.MiddleWare import MiddleWare
from django.contrib.auth.decorators import permission_required

class HostSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_host",raise_exception=True))
    def get(self,request,*args,**kwargs):
        host_search_form = HostSearchForm()
        host = Host.objects.all()
        self.context = {"host":host,"host_search_form":host_search_form}
        return render(request, "cmdb/host/host_list.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_host",raise_exception=True))
    def post(self,request,*args,**kwargs):
        host_search_form = HostSearchForm(request.POST)
        if host_search_form.is_valid():
            hostname = request.POST["hostname"]
            environment = request.POST["environment"]
            if hostname == "":
                host = Host.objects.filter(environment=environment)
            else:
                host = Host.objects.filter(host_name__contains=hostname).filter(environment=environment)
            self.context = {"host":host,"host_search_form":host_search_form}
            return render(request,"cmdb/host/host_detail.html",self.context)
        else:
            self.context = {"host_search_form":host_search_form,"errors":host_search_form.errors}
            return render(request,"cmdb/host/host_list.html",self.context)

class HostAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_host",raise_exception=True))
    def get(self,request,*args,**kwargs):
        host_add_form = HostAddForm()
        self.context = {"host_add_form":host_add_form}
        return render(request, "cmdb/host/host_add.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_host",raise_exception=True))
    def post(self,request,*args,**kwargs):
        host_add_form = HostAddForm(request.POST)
        if host_add_form.is_valid():
            hostname = request.POST["host_name"]
            host = Host.objects.filter(host_name=hostname)
            if host.exists():
                self.context = {"host_add_form":host_add_form,"repeat_errors":"true"}
                return render(request, "cmdb/host/host_add.html", self.context)
            else:
                kernel = request.POST["kernel"]
                osrelease = request.POST["osrelease"]
                operations = request.POST["os"]
                environment = request.POST["environment"]
                host_usage = request.POST["host_usage"]
                cluster_list = request.POST.getlist("cluster")
                host = Host(host_name=hostname,kernel=kernel,osrelease=osrelease,os=operations,environment=environment,host_usage=host_usage)
                host.save()
                for c in cluster_list:
                    host.cluster.add(c)
                if update_host_ip(hostname) == 0:
                    host.delete()
                    self.context = {"host_add_form": host_add_form,"minions_is_not_exist": "true"}
                    return render(request,"cmdb/host/host_add.html",self.context)
                elif update_host_ip(hostname) == 1:
                    if host.host_usage == "mid":
                        midware = request.POST.getlist("midware")
                        if len(midware) != 0:
                            for m in midware:
                                set_host(m,hostname)
                            set_list(hostname,midware)
                    return HttpResponsePermanentRedirect(reverse("host"))
        else:
            self.context = {"host_add_form":host_add_form,"errors":host_add_form.errors}
            return render(request, "cmdb/host/host_add.html", self.context)

class HostUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_host",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        host = Host.objects.get(pk=id)
        host_dict = model_to_dict(host)
        host_update_form = HostAddForm(host_dict)
        self.context = {"host_update_form":host_update_form}
        return render(request, "cmdb/host/host_update.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_host",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        host_update_form = HostAddForm(request.POST)
        if host_update_form.is_valid():
            host = Host.objects.get(pk=id)
            host.host_name = request.POST["host_name"]
            host.kernel = request.POST["kernel"]
            host.osrelease = request.POST["osrelease"]
            host.os = request.POST["os"]
            host.environment = request.POST["environment"]
            host.host_usage = request.POST["host_usage"]
            host.save()
            cluster_list = request.POST.getlist("cluster")
            for c in cluster_list:
                host.cluster.add(c)
            return HttpResponsePermanentRedirect(reverse("host"))
        else:
            self.context = {"host_update_form":host_update_form}
            return render(request, "cmdb/host/host_update.html", self.context)

class HostDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.delete_host",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        host = Host.objects.get(pk=id)
        hostname = host.host_name
        if host.host_usage == "mid":
            mid_list = get_mid_list(hostname)["middleware_list"]
            for m in mid_list:
                del_mid_host(m["name"],hostname)
        del_host(hostname)
        host.delete()
        return HttpResponsePermanentRedirect(reverse("host"))

class HostAppUpdateInfoView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        hostname = kwargs.get("hostname")
        update_host_info(hostname)
        host = Host.objects.get(host_name=hostname)
        module_list = update_host_cluster(hostname)
        if host.environment == "develop":
            host.cluster.clear()
            for m in module_list:
                if m != "":
                    cluster_name = "{}-cluster-dev".format(m)
                    host.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        elif host.environment == "test":
            host.cluster.clear()
            for m in module_list:
                if m != "":
                    cluster_name = "{}-cluster-test".format(m)
                    host.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        elif host.environment == "prepare":
            host.cluster.clear()
            for m in module_list:
                if m != "":
                    cluster_name = "{}-cluster-pre".format(m)
                    host.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        elif host.environment == "product":
            host.cluster.clear()
            for m in module_list:
                if m != "":
                    cluster_name = "{}-cluster-prod".format(m)
                    host.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        host.save()
        return HttpResponseRedirect(reverse("host"))

class HostMidUpdateInfoView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        hostname = kwargs.get("hostname")
        update_host_info(hostname)
        # host = Host.objects.get(host_name=hostname)
        # mid_list = get_mid_list(hostname)["middleware_list"]
        # if host.environment == "develop":
        #     host.cluster.clear()
        #     for mid in mid_list:
        #         cluster_name = "{}-cluster-dev".format(mid["name"])
        #         host.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        # elif host.environment == "test":
        #     host.cluster.clear()
        #     for mid in mid_list:
        #         cluster_name = "{}-cluster-test".format(mid["name"])
        #         host.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        # elif host.environment == "prepare":
        #     host.cluster.clear()
        #     for mid in mid_list:
        #         cluster_name = "{}-cluster-pre".format(mid["name"])
        #         host.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        # elif host.environment == "product":
        #     host.cluster.clear()
        #     for mid in mid_list:
        #         cluster_name = "{}-cluster-prod".format(mid["name"])
        #         host.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        # host.save()
        return HttpResponseRedirect(reverse("host"))

class HostDbUpdateInfoView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        hostname = kwargs.get("hostname")
        update_host_info(hostname)
        return HttpResponseRedirect(reverse("host"))

class HostProjectModuelView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        host = Host.objects.get(pk=id)
        sql = '''select ch.host_name,cc.cluster_name,cp.module_name,ci.ip_address from cmdb_host ch
                  inner join cmdb_host_cluster chc on ch.id=chc.host_id
                  inner join cmdb_cluster cc on chc.cluster_id=cc.id
                  inner join cmdb_projectmodule_cluster cpc on cc.id=cpc.cluster_id
                  inner join cmdb_projectmodule cp on cpc.projectmodule_id=cp.id
                  inner join cmdb_ippool ci on ci.host_id=ch.id
        '''
        with connection.cursor() as cursor:
            cursor.execute(sql+"where ch.id=%s",[int(id)])
            raw = cursor.fetchall()
        host_list = []
        for r in raw:
            host = {"hostname":r[0],"cluster_name":r[1],"module_name":r[2],"ip_address":r[3]}
            host_list.append(host)
        self.context = {"host_projectmodule_info":host_list}
        return render(request, "cmdb/host/host_projectmodule_info.html", self.context)

class HostMiddleWareView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        hostname = kwargs.get("hostname")
        mid_list = get_mid_list(hostname)["middleware_list"]
        middlewares = []
        for mid in mid_list:
            if mid["installed"] == "true":
                middleware = MiddleWare.objects.get(mid_name=mid["name"])
                middlewares.append(middleware)
        self.context = {"middlewares":middlewares}
        return render(request,"cmdb/host/host_middleware.html",self.context)



