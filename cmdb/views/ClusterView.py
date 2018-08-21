from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from cmdb.forms.ClusterForm import ClusterSearchForm,ClusterAddForm
from cmdb.models.Cluster import Cluster
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

class ClusterSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_cluster",raise_exception=True))
    def get(self,request,*args,**kwargs):
        cluster_search_form = ClusterSearchForm()
        cluster = Cluster.objects.all()
        self.context = {"cluster_search_form":cluster_search_form,"cluster":cluster}
        return render(request, "cmdb/cluster/cluster_list.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_cluster",raise_exception=True))
    def post(self,request,*args,**kwargs):
        cluster_search_form = ClusterSearchForm(request.POST)
        if cluster_search_form.is_valid():
            search_cluster_name = request.POST["search_cluster_name"]
            search_cluster_type = request.POST["search_cluster_type"]
            if search_cluster_name == "":
                cluster = Cluster.objects.filter(cluster_type=search_cluster_type)
            else:
                cluster = Cluster.objects.filter(cluster_name__contains=search_cluster_name).filter(cluster_type=search_cluster_type)
            self.context = {"cluster":cluster,"cluster_search_form":cluster_search_form}
            return render(request,"cmdb/cluster/cluster_detail.html",self.context)
        else:
            self.context = {"cluster_search_form":cluster_search_form,"errors":cluster_search_form.errors}
            return render(request,"cmdb/cluster/cluster_list.html",self.context)

class ClusterAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_cluster",raise_exception=True))
    def get(self,request,*args,**kwargs):
        cluster_add_form = ClusterAddForm()
        self.context = {"cluster_add_form":cluster_add_form}
        return render(request, "cmdb/cluster/cluster_add.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_cluster",raise_exception=True))
    def post(self,request,*args,**kwargs):
        cluster_add_form = ClusterAddForm(request.POST)
        if cluster_add_form.is_valid():
            cluster_name = request.POST["cluster_name"]
            cluster_type = request.POST["cluster_type"]
            cluster_desc = request.POST["cluster_desc"]
            environment = request.POST["environment"]
            cluster = Cluster.objects.filter(cluster_name = cluster_name)
            if cluster.exists():
                self.context = {"cluster_add_form":cluster_add_form,"repeat_errors":"true"}
                render(request, "cmdb/cluster/cluster_add.html", self.context)
            else:
                cluster = Cluster(cluster_name=cluster_name,cluster_type=cluster_type,cluster_desc=cluster_desc,environment=environment)
                cluster.save()
                return HttpResponsePermanentRedirect(reverse("cluster"))
        else:
            self.context = {"cluster_add_form":cluster_add_form,"cluster_add_errors":cluster_add_form.errors}
            return render(request, "cmdb/cluster/cluster_add.html", self.context)

class ClusterUpdateView(View):
    def __init__(self):
        context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_cluster",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        cluster = Cluster.objects.get(pk=id)
        cluster_dict = model_to_dict(cluster)
        cluster_update_form = ClusterAddForm(cluster_dict)
        self.context = {"cluster_update_form":cluster_update_form}
        return render(request,"cmdb/cluster/cluster_update.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_cluster",raise_exception=True))
    def post(self,request,*args,**kwargs):
        cluster_update_form = ClusterAddForm(request.POST)
        id = kwargs.get("id")
        if cluster_update_form.is_valid():
            cluster_name = request.POST["cluster_name"]
            cluster_type = request.POST["cluster_type"]
            cluster_desc = request.POST["cluster_desc"]
            environment = request.POST["environment"]
            cluster = Cluster.objects.get(pk=id)
            cluster.cluster_name = cluster_name
            cluster.cluster_type = cluster_type
            cluster.cluster_desc = cluster_desc
            cluster.environment = environment
            cluster.save()
            return HttpResponsePermanentRedirect(reverse("cluster"))
        else:
            self.context = {"cluster_update_form":cluster_update_form,"cluster_update_errors":cluster_update_form.errors}
            return render(request,"cmdb/cluster/cluster_update.html",self.context)

class ClusterDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.delete_cluster",raise_exception=True))
    def get(self,reqeust,*args,**kwargs):
        id = kwargs.get("id")
        cluster = Cluster.objects.get(pk=id)
        cluster.delete()
        return HttpResponsePermanentRedirect(reverse("cluster"))

class ClusterDetailView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        cluster_name = kwargs.get("cluster_name")
        cluster = Cluster.objects.get(cluster_name=cluster_name)
        host_list = cluster.host_set.all()
        self.context = {"host_list":host_list}
        return render(request,"cmdb/cluster/cluster_host.html",self.context)


