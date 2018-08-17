from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.views.generic import View
from cmdb.forms.DomainNameForm import DomainNameSearchForm,DomainNameAddForm
from cmdb.models.DomainName import DomainName
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from cmdb.models.ProjectModule import ProjectModule
from cmdb.models.IpPool import IpPool
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from common.append_dns import append_domainname
from common.append_dns import sed_domainname
from common.append_dns import comment_domainname
class DomainNameSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        domainname_search_form = DomainNameSearchForm()
        domainname = DomainName.objects.all()
        self.context = {"domainname_search_form":domainname_search_form,"domainname":domainname}
        return render(request, "cmdb/domainname/domainname_list.html", self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        domainname_search_form = DomainNameSearchForm(request.POST)
        if domainname_search_form.is_valid():
            search_dns = request.POST["search_dns"]
            search_ip_address = request.POST["search_ip_address"]
            if search_dns == "":
                domainname = DomainName.objects.filter(ip=search_ip_address)
            else:
                domainname = DomainName.objects.filter(dns__contains = search_dns).filter(ip=search_ip_address)
            self.context = {"domainname":domainname,"domainname_search_form":domainname_search_form}
            return render(request,"cmdb/domainname/domainname_detail.html",self.context)
        else:
            self.context = {"domainname_search_form":domainname_search_form,"errors":domainname_search_form.errors}
            return render(request,"cmdb/domainname/domainname_list.html",self.context)

class DomainNameAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        domainname_add_form = DomainNameAddForm()
        self.context = {"domainname_add_form":domainname_add_form}
        return render(request,"cmdb/domainname/domainname_add.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        domainname_add_form = DomainNameAddForm(request.POST)
        if domainname_add_form.is_valid():
            dns = request.POST["dns"]
            domain_type = request.POST["domain_type"]
            ip_id = request.POST["ip"]
            project_module_id = request.POST["project_module"]
            project_module_url = request.POST["project_module_url"]
            environment = request.POST["environment"]
            if project_module_id == "":
                project_module = None
            else:
                project_module = ProjectModule.objects.get(pk=project_module_id)
            ippool = IpPool.objects.get(pk=ip_id)
            domainname = DomainName.objects.filter(dns=dns).filter(project_module=project_module)
            if domainname.exists():
                self.context = {"domainname_add_form":domainname_add_form,"repeat_errors":"true"}
                return render(request,"cmdb/domainname/domainname_add.html",self.context)
            else:
                domainname = DomainName(dns=dns,domain_type=domain_type,ip=ippool,project_module=project_module,environment=environment,project_module_url=project_module_url)
                domainname.save()
                append_domainname(dns.split(".")[0],domain_type,ippool.ip_address)
                return HttpResponsePermanentRedirect(reverse("domainname"))
        else:
            self.context = {"domainname_add_form":domainname_add_form,"domainname_add_errors":domainname_add_form.errors}
            return render(request,"cmdb/domainname/domainname_add.html",self.context)


class DomainNameUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        domainname = DomainName.objects.get(pk=id)
        domainname_dict = model_to_dict(domainname)
        domainname_update_form = DomainNameAddForm(domainname_dict)
        self.context = {"domainname_update_form":domainname_update_form}
        return render(request,"cmdb/domainname/domainname_update.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        domainname_update_form = DomainNameAddForm(request.POST)
        if domainname_update_form.is_valid():
            domainname = DomainName.objects.get(pk=id)
            srcstr = "{}     IN     {}     {}".format(domainname.dns.split(".")[0], domainname.domain_type,domainname.ip.ip_address)
            domainname.dns = request.POST["dns"]
            domainname.domain_type = request.POST["domain_type"]
            ip_id = request.POST["ip"]
            domainname.ip = IpPool.objects.get(pk=ip_id)
            project_module_id = request.POST["project_module"]
            if project_module_id == "":
                domainname.project_module = None
            else:
                domainname.project_module = ProjectModule.objects.get(pk=project_module_id)
            domainname.project_module_url = request.POST["project_module_url"]
            domainname.environment = request.POST["environment"]
            domainname.save()
            deststr = "{}     IN     {}     {}".format(domainname.dns.split(".")[0],domainname.domain_type,domainname.ip.ip_address)
            sed_domainname(srcstr,deststr)
            return HttpResponsePermanentRedirect(reverse("domainname"))
        else:
            self.context = {"domainname_update_form":domainname_update_form,"domainname_update_errors":domainname_update_form.errors}
            print(self.context)
            return render(request,"cmdb/domainname/domainname_update.html",self.context)

class DomainNameDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        domainname = DomainName.objects.get(pk=id)
        domainname.delete()
        res = comment_domainname(domainname.dns.split(".")[0])
        print(res)
        return HttpResponsePermanentRedirect(reverse("domainname"))

