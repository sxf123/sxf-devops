from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from deploy.forms import ScriptSearchForm
from deploy.models import Script
from deploy.forms import ScriptAddForm
from django.forms import model_to_dict
from devops.settings import DEPLOY_UPLOAD_PATH
from django.core.urlresolvers import reverse
import os
from deploy.forms import HostSelectForm
from saltjob.handle_script import execute_script
from deploy.forms import MinionSelectForm
from saltjob.handle_script import transfer_script
from django.contrib.auth.decorators import permission_required


class ScriptManageView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_script",raise_exception=True))
    def get(self,request,*args,**kwargs):
        script_search_form = ScriptSearchForm()
        script_list = Script.objects.all()
        self.context = {"script_search_form":script_search_form,"script_list":script_list}
        return render(request,"deploy/script_list.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_script",raise_exception=True))
    def post(self,request,*args,**kwargs):
        script_search_form = ScriptSearchForm(request.POST)
        if script_search_form.is_valid():
            search_script_name = script_search_form.cleaned_data.get("search_script_name")
            search_script_type = script_search_form.cleaned_data.get("search_script_type")
            script_list = Script.objects.filter(script_name=search_script_name).filter(script_type=search_script_type)
            self.context = {"script_search_form":script_search_form,"script_list":script_list}
            return render(request,"deploy/script_detail.html",self.context)
        else:
            self.context = {"script_search_form":script_search_form,"errors":script_search_form.errors}
            return render(request,"deploy/script_detail.html",self.context)
class ScriptAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.add_script",raise_exception=True))
    def get(self,request,*args,**kwargs):
        script_add_form = ScriptAddForm()
        self.context = {"script_add_form":script_add_form}
        return render(request,"deploy/script_add.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.add_script",raise_exception=True))
    def post(self,request,*args,**kwargs):
        script_add_form = ScriptAddForm(request.POST)
        if script_add_form.is_valid():
            script_name = script_add_form.cleaned_data.get("script_name")
            script_type = script_add_form.cleaned_data.get("script_type")
            script_content = script_add_form.cleaned_data.get("script_content")
            script_dir = script_add_form.cleaned_data.get("script_dir")
            print(script_content)
            script = Script(
                script_name = script_name,
                script_type = script_type,
                script_content = script_content,
                script_dir = script_dir
            )
            script.save()
            filename = os.path.join(DEPLOY_UPLOAD_PATH,script_name)
            with open(filename,"w") as f:
                f.write(script_content.replace("\r\n","\n"))
                f.close()
            return HttpResponsePermanentRedirect(reverse("script_manage"))
        else:
            self.context = {"script_add_form":script_add_form,"errors":script_add_form.errors}
            return render(request,"deploy/script_add.html",self.context)

class ScriptUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.change_script",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        script = Script.objects.get(pk=id)
        script_dict = model_to_dict(script)
        script_update_form = ScriptAddForm(script_dict)
        self.context = {"script_update_form":script_update_form}
        return render(request,"deploy/script_update.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.change_script",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        script = Script.objects.get(pk=id)
        script_update_form = ScriptAddForm(request.POST)
        if script_update_form.is_valid():
            script.script_name = script_update_form.cleaned_data.get("script_name")
            script.script_type = script_update_form.cleaned_data.get("script_type")
            script.script_content = script_update_form.cleaned_data.get("script_content")
            script.script_dir = script_update_form.cleaned_data.get("script_dir")
            script.save()
            filename = os.path.join(DEPLOY_UPLOAD_PATH,script_update_form.cleaned_data.get("script_name"))
            with open(filename,"w") as f:
                f.write(script_update_form.cleaned_data.get("script_content").replace("\r\n","\n"))
                f.close()
            return HttpResponsePermanentRedirect(reverse("script_manage"))
        else:
            self.context = {"script_update_form":script_update_form,"errors":script_update_form.errors}
            return render(request,"deploy/script_update.html",self.context)

class ScriptDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.delete_script",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        script = Script.objects.get(pk=id)
        script.delete()
        filename = os.path.join(DEPLOY_UPLOAD_PATH,script.script_name)
        os.remove(filename)
        return HttpResponsePermanentRedirect(reverse("script_manage"))

class ScriptExecuteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        script = Script.objects.get(pk=id)
        minion_select_form = HostSelectForm()
        self.context = {"minion_select_form":minion_select_form,"script":script}
        return render(request,"deploy/minion_select.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        script = Script.objects.get(pk=id)
        script_name = script.script_name
        minion_select_form = HostSelectForm(request.POST)
        if minion_select_form.is_valid():
            target = minion_select_form.cleaned_data.get("hostname")
            execute_res = execute_script(target,script_name)
            self.context = {"minion_select_form":minion_select_form,"execute_res":execute_res}
            return render(request,"deploy/minion_select.html",self.context)
        else:
            self.context = {"minion_select_form":minion_select_form,"errors":minion_select_form.errors}
            return render(request,"deploy/minion_select.html",self.context)

class ScriptTransferView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        script = Script.objects.get(pk=id)
        minions_select_form = MinionSelectForm()
        self.context = {"minions_select_form":minions_select_form,"script":script}
        return render(request,"deploy/minions_select.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        script = Script.objects.get(pk=id)
        script_name = script.script_name
        script_dir = script.script_dir
        minions_select_form = MinionSelectForm(request.POST)
        print(minions_select_form)
        if minions_select_form.is_valid():
            targets = minions_select_form.cleaned_data.get("minions")
            transfer_res = transfer_script(targets,script_dir,script_name)
            self.context = {"transfer_res":transfer_res,"minions_select_form":minions_select_form}
            print(transfer_res)
            return render(request,"deploy/minions_select.html",self.context)
        else:
            self.context = {"minions_select_form":minions_select_form}
            return render(request,"deploy/minions_select.html",self.context)