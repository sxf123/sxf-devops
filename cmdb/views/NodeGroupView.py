from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.views import View
from django.contrib.auth.decorators import login_required
from cmdb.models.NodeGroup import NodeGroup
from cmdb.forms.NodeGroupForm import NodeGroupSearchForm,NodeGroupAddForm
from cmdb.models.Host import Host
from django.http import JsonResponse
import json
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator

class NodeGroupSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        nodegroup_search_form = NodeGroupSearchForm()
        nodegroup = NodeGroup.objects.all()
        self.context = {"nodegroup":nodegroup,"nodegroup_search_form":nodegroup_search_form}
        return render(request,"cmdb/nodegroup/nodegroup_list.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        nodegroup = request.POST["search_nodegroup"]
        host = request.POST["search_host"]
        host_nodegroup = Host.objects.select_related("nodegroup").get(host_name=host)
        nodegroup = NodeGroup.objects.get(nodegroup=host_nodegroup.nodegroup.nodegroup).get(nodegroup=nodegroup)
        nodegroup_dict = model_to_dict(nodegroup)
        return JsonResponse(json.dumps(nodegroup_dict),safe=False)

class NodeGroupAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        nodegroup_add_form = NodeGroupAddForm()
        self.context = {"nodegroup_add_form":nodegroup_add_form}
        return render(request,"cmdb/nodegroup/nodegroup_add.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        nodegroup_add_form = NodeGroupAddForm(request.POST)
        if nodegroup_add_form.is_valid():
            nodegroup_name = request.POST["nodegroup"]
            nodegroup = NodeGroup.objects.filter(nodegroup=nodegroup_name)
            if nodegroup.exists():
                self.context = {"nodegroup_add_form":nodegroup_add_form,"repeat_errors":"true"}
                return render(request,"cmdb/nodegroup/nodegroup_add.html",self.context)
            else:
                nodegroup_desc = request.POST["nodegroup_desc"]
                nodegroup = NodeGroup(nodegroup=nodegroup_name,nodegroup_desc=nodegroup_desc)
                nodegroup.save()
                return HttpResponsePermanentRedirect(reverse("nodegroup"))
        else:
            self.context = {"nodegroup_add_form":nodegroup_add_form,"errors":nodegroup_add_form.errors}
            return render(request,"cmdb/nodegroup/nodegroup_add.html",self.context)
class NodeGroupUpdateView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        nodegroup = NodeGroup.objects.get(pk=id)
        nodegroup_dict = model_to_dict(nodegroup)
        nodegroup_update_form = NodeGroupAddForm(nodegroup_dict)
        self.context = {"nodegroup_update_form":nodegroup_update_form}
        return render(request,"cmdb/nodegroup/nodegroup_update.html",self.context)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        nodegroup_update_form = NodeGroupAddForm(request.POST)
        if nodegroup_update_form.is_valid():
            nodegroup = NodeGroup.objects.get(pk=id)
            nodegroup.nodegroup = request.POST["nodegroup"]
            nodegroup.nodegroup_desc = request.POST["nodegroup_desc"]
            nodegroup.save()
            return HttpResponsePermanentRedirect(reverse("nodegroup"))
        else:
            self.context = {"nodegroup_update_form":nodegroup_update_form}
            return render(request,"cmdb/nodegroup/nodegroup_update.html",self.context)

class NodeGroupDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        nodegroup = NodeGroup.objects.get(pk=id)
        nodegroup.delete()
        return HttpResponsePermanentRedirect(reverse("nodegroup"))

class NodeGroupDetailView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        nodegroup_name = kwargs.get("nodegroup")
        nodegroup = NodeGroup.objects.get(nodegroup=nodegroup_name)
        host_list = nodegroup.host_set.all()
        self.context = {"host_list":host_list}
        return render(request,"cmdb/nodegroup/nodegroup_host_list.html",self.context)




