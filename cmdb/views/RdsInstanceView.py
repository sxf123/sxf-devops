from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required,permission_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from cmdb.forms.RdsInstanceForm import RdsInstanceSearchForm
from cmdb.models import RdsInstance
from cmdb.forms.RdsInstanceForm import RdsInstanceAddForm
from django.forms import model_to_dict

class RdsInstanceSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_rdsinstance",raise_exception=True))
    def get(self,request,*args,**kwargs):
        rds_search_form = RdsInstanceSearchForm()
        rdsinstance = RdsInstance.objects.all()
        self.context = {"rds_search_form":rds_search_form,"rdsinstance":rdsinstance}
        return render(request,"cmdb/rdsinstance/rdsinstance_list.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_rdsinstance",raise_exception=True))
    def post(self,request,*args,**kwargs):
        rds_search_form = RdsInstanceSearchForm(request.POST)
        if rds_search_form.is_valid():
            search_instance_name = rds_search_form.cleaned_data.get("search_instacnce_name")
            search_db_type = rds_search_form.cleaned_data.get("search_db_type")
            rdsinstance = RdsInstance.objects.filter(instance_name=search_instance_name).filter(db_type=search_db_type)
            self.context = {"rdsinstance":rdsinstance,"rds_search_form":rds_search_form}
            return render(request,"cmdb/rdsinstance/rdsinstance_list.html",self.context)
        else:
            self.context = {"rds_search_form":rds_search_form,"errors":rds_search_form.errors}
            return render(request,"cmdb/rdsinstance/rdsinstance_list.html",self.context)

class RdsInstanceAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_rdsinstance",raise_exception=True))
    def get(self,request,*args,**kwargs):
        rds_instance_add_form = RdsInstanceAddForm()
        self.context = {"rds_instance_add_form":rds_instance_add_form}
        return render(request,"cmdb/rdsinstance/rdsinstance_add.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_rdsinstance",raise_exception=True))
    def post(self,request,*args,**kwargs):
        rds_instance_add_form = RdsInstanceAddForm(request.POST)
        if rds_instance_add_form.is_valid():
            instance_name = rds_instance_add_form.cleaned_data.get("instance_name")
            instance_url = rds_instance_add_form.cleaned_data.get("instance_url")
            instance_port = rds_instance_add_form.cleaned_data.get("instance_port")
            db_type = rds_instance_add_form.cleaned_data.get("db_type")
            instance_desc = rds_instance_add_form.cleaned_data.get("instance_desc")
            rdsinstance = RdsInstance(
                instance_name = instance_name,
                instance_url = instance_url,
                instance_port = instance_port,
                db_type = db_type,
                instance_desc = instance_desc
            )
            rdsinstance.save()
            return HttpResponseRedirect(reverse("rdsinstance_list"))
        else:
            self.context = {"rds_instance_add_form":rds_instance_add_form,"errors":rds_instance_add_form.errors}
            return render(request,"cmdb/rdsinstance/rdsinstance_add.html",self.context)

class RdsInstanceUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_rdsinstance",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        rdsinstance = RdsInstance.objects.get(pk=id)
        rdsinstance_dict = model_to_dict(rdsinstance)
        rds_instance_update_form = RdsInstanceAddForm(rdsinstance_dict)
        self.context = {"rds_instance_update_form":rds_instance_update_form}
        return render(request,"cmdb/rdsinstance/rdsinstance_update.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_rdsinstance",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        rds_instance_update_form = RdsInstanceAddForm(request.POST)
        rdsinstance = RdsInstance.objects.get(pk=id)
        if rds_instance_update_form.is_valid():
            rdsinstance.instance_name = rds_instance_update_form.cleaned_data.get("instance_name")
            rdsinstance.instance_url = rds_instance_update_form.cleaned_data.get("instance_url")
            rdsinstance.instance_port = rds_instance_update_form.cleaned_data.get("instance_port")
            rdsinstance.db_type = rds_instance_update_form.cleaned_data.get("db_type")
            rdsinstance.instance_desc = rds_instance_update_form.cleaned_data.get("instance_desc")
            rdsinstance.save()
            return HttpResponseRedirect(reverse("rdsinstance_list"))
        else:
            self.context = {"rds_instance_update_form":rds_instance_update_form,"errors":rds_instance_update_form.errors}
            return render(request,"cmdb/rdsinstance/rdsinstance_update.html",self.context)

class RdsInstanceDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.delete_rdsinstance",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        rdsinstance = RdsInstance.objects.get(pk=id)
        rdsinstance.delete()
        return HttpResponseRedirect(reverse("rdsinstance_list"))