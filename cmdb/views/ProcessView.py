from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from cmdb.models.Process import Process
from cmdb.forms.ProcessForm import ProcessSearchForm,ProcessAddForm
from cmdb.models.ProjectModule import ProjectModule
from cmdb.models.EcsHost import EcsHost
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

class ProcessList(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_process",raise_exception=True))
    def get(self,request,*args,**kwargs):
        process_search_form = ProcessSearchForm()
        process = Process.objects.all()
        self.context = {"process_search_form":process_search_form,"process":process}
        return render(request,"cmdb/process/process_list.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_process",raise_exception=True))
    def post(self,request,*args,**kwargs):
        process_search_form = ProcessSearchForm(request.POST)
        if process_search_form.is_valid():
            search_process_name = process_search_form.cleaned_data.get("search_process_name")
            search_ecshost = process_search_form.cleaned_data.get("search_ecshost")
            process = Process.objects.filter(process_name__contains=search_process_name).filter(ecshost__instance_id=search_ecshost)
            self.context = {"process":process,"process_search_form":process_search_form}
            return render(request,"cmdb/process/process_list.html",self.context)
        else:
            self.context = {"process_search_form":process_search_form,"errors":process_search_form.errors}
            return render(request,"cmdb/process/process_list.html",self.context)

class ProcessAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_process",raise_exception=True))
    def get(self,request,*args,**kwargs):
        process_add_form = ProcessAddForm()
        self.context = {"process_add_form":process_add_form}
        return render(request,"cmdb/process/process_add.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_process",raise_exception=True))
    def post(self,request,*args,**kwargs):
        process_add_form = ProcessAddForm(request.POST)
        if process_add_form.is_valid():
            process_name = process_add_form.cleaned_data.get("process_name")
            process_homepath = process_add_form.cleaned_data.get("process_homepath")
            process_id = process_add_form.cleaned_data.get("process_id")
            process_port = process_add_form.cleaned_data.get("process_port")
            process_log = process_add_form.cleaned_data.get("process_log")
            projectmodule = ProjectModule.objects.get(module_name=process_add_form.cleaned_data.get("projectmodule"))
            ecshost = EcsHost.objects.get(instance_id=process_add_form.cleaned_data.get("ecshost"))
            process = Process(
                process_name = process_name,
                process_homepath = process_homepath,
                process_id = process_id,
                process_port = process_port,
                process_log = process_log,
                projectmodule = projectmodule,
                ecshost = ecshost
            )
            process.save()
            return HttpResponseRedirect(reverse("process_list"))
        else:
            self.context = {"process_add_form":process_add_form,"errors":process_add_form.errors}
            return render(request,"cmdb/process/process_add.html",self.context)
class ProcessUpdate(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_process",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        process = Process.objects.get(pk=id)
        process_dict = model_to_dict(process)
        process_update_form = ProcessAddForm(process_dict)
        self.context = {"process_update_form":process_update_form}
        return render(request,"cmdb/process/process_update.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_process",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        process_update_form = ProcessAddForm(request.POST)
        if process_update_form.is_valid():
            process = Process.objects.get(pk=id)
            process.process_name = process_update_form.cleaned_data.get("process_name")
            process.process_homepath = process_update_form.cleaned_data.get("process_homepath")
            process.process_id = process_update_form.cleaned_data.get("process_id")
            process.process_port = process_update_form.cleaned_data.get("process_port")
            process.process_log = process_update_form.cleaned_data.get("process_log")
            process.projectmodule = ProjectModule.objects.get(module_name=process_update_form.cleaned_data.get("projectmodule"))
            process.ecshost = ProjectModule.objects.get(minion_id=process_update_form.cleaned_data.get("ecshost"))
            process.save()
            return HttpResponseRedirect(reverse("process_list"))
        else:
            self.context = {"process_update_form":process_update_form,"errors":process_update_form.errors}
            return render(request,"cmdb/process/process_update.html",self.context)

class ProcessDelete(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.delete_process",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        process = Process.objects.get(pk=id)
        process.delete()
        return HttpResponseRedirect(reverse("process_list"))

