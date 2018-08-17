from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.views.generic import View
from cmdb.models.IpPool import IpPool
from cmdb.forms.IpPoolForm import IpSearchForm,IpAddForm
from cmdb.models.Host import Host
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class IpPoolSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        ippool = IpPool.objects.all()
        search_ippool_form = IpSearchForm()
        self.context = {"ippool":ippool,"search_ippool_form":search_ippool_form}
        return render(request, "cmdb/ippool/ippool_list.html", self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        ippool_search_form = IpSearchForm(request.POST)
        if ippool_search_form.is_valid():
            search_ip_address = request.POST["search_ip_address"]
            search_ip_type = request.POST["search_ip_type"]
            if search_ip_address == "":
                ippool = IpPool.objects.filter(ip_type=search_ip_type)
            else:
                ippool = IpPool.objects.filter(ip_address__contains=search_ip_address).filter(ip_type=search_ip_type)
            self.context = {"ippool":ippool,"ippool_search_form":ippool_search_form}
            return render(request,"cmdb/ippool/ippool_detail.html",self.context)
        else:
            self.context = {"ippool_search_form":ippool_search_form,"errors":ippool_search_form.errors}
            return render(request,"cmdb/ippool/ippool_list.html",self.context)
class IpPoolAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        ippool_add_form = IpAddForm()
        self.context = {"ippool_add_form":ippool_add_form}
        return render(request,"cmdb/ippool/ippool_add.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        ippool_add_form = IpAddForm(request.POST)
        if ippool_add_form.is_valid():
            ip_address = request.POST["ip_address"]
            ip_type = request.POST["ip_type"]
            gateway = request.POST["gateway"]
            ip_segment = request.POST["ip_segment"]
            host_id = request.POST["host"]
            ip = IpPool.objects.filter(ip_address = ip_address)
            if ip.exists():
                self.context = {"ippool_add_form":ippool_add_form,"repeat_errors":"true"}
                return render(request,"cmdb/ippool/ippool_add.html",self.context)
            else:
                if host_id == "":
                    host = None
                else:
                    host = Host.objects.get(pk=host_id)
                ippool = IpPool(ip_address=ip_address,ip_type=ip_type,gateway=gateway,ip_segment=ip_segment,host=host)
                ippool.save()
                return HttpResponsePermanentRedirect(reverse("ippool"))
        else:
            self.context = {"ippool_add_form":ippool_add_form,"ippool_add_errors":ippool_add_form.errors}
            return render(request,"cmdb/ippool/ippool_add.html",self.context)

class IpPoolUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        ippool = IpPool.objects.get(pk=id)
        ippool_dict = model_to_dict(ippool)
        ippool_update_form = IpAddForm(ippool_dict)
        self.context = {"ippool_update_form":ippool_update_form}
        return render(request,"cmdb/ippool/ippool_update.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        ippool_update_form = IpAddForm(request.POST)
        if ippool_update_form.is_valid():
            ip_address = request.POST["ip_address"]
            ip_type = request.POST["ip_type"]
            gateway = request.POST["gateway"]
            ip_segment = request.POST["ip_segment"]
            host_id = request.POST["host"]
            if host_id == "":
                host = None
            else:
                host = Host.objects.get(pk=host_id)
            ippool = IpPool.objects.get(pk=id)
            ippool.ip_address = ip_address
            ippool.ip_type = ip_type
            ippool.gateway = gateway
            ippool.ip_segment = ip_segment
            ippool.host = host
            ippool.save()
            return HttpResponsePermanentRedirect(reverse("ippool"))
        else:
            self.context = {"ippool_update_form":ippool_update_form,"ippool_update_errors":ippool_update_form.errors}
            return render(request,"cmdb/ippool/ippool_update.html",self.context)

class IpPoolDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        ippool = IpPool.objects.get(pk=id)
        ippool.delete()
        return HttpResponsePermanentRedirect(reverse("ippool"))
