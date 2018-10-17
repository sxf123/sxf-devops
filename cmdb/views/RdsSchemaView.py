from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from cmdb.forms.RdsSchemaForm import RdsSchemaSearchForm
from cmdb.models.RdsSchema import RdsSchema
from cmdb.forms.RdsSchemaForm import RdsSchemaAddForm
from cmdb.models.RdsInstance import RdsInstance
from django.forms import model_to_dict

class RdsSchemaSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_rdsschema",raise_exception=True))
    def get(self,request,*args,**kwargs):
        rdsschema_search_form = RdsSchemaSearchForm()
        rdsschema = RdsSchema.objects.all()
        self.context = {"rdsschema_search_form":rdsschema_search_form,"rdsschema":rdsschema}
        return render(request,"cmdb/rdsschema/rdsschema_list.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_rdsschema",raise_exception=True))
    def post(self,request,*args,**kwargs):
        rdsschema_search_form = RdsSchemaSearchForm(request.POST)
        if rdsschema_search_form.is_valid():
            search_schema_name = rdsschema_search_form.cleaned_data.get("search_schema_name")
            search_rdsinstance = rdsschema_search_form.cleaned_data.get("search_rdsinstance")
            if search_rdsinstance == "":
                rdsschema = RdsSchema.objects.filter(schema_name=search_schema_name)
                self.context = {"rdsschema":rdsschema,"rdsschema_search_form":rdsschema_search_form}
            else:
                rdsschema = RdsSchema.objects.filter(rdsinstance__id=search_rdsinstance).filter(schema_name=search_schema_name)
                self.context = {"rdsschema":rdsschema,"rdsschema_search_form":rdsschema_search_form}
        else:
            self.context = {"rdsschema_search_form":rdsschema_search_form,"errors":rdsschema_search_form.errors}
        return render(request,"cmdb/rdsschema/rdsschema_list.html",self.context)

class RdsSchemaAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_rdsschema",raise_exception=True))
    def get(self,request,*args,**kwargs):
        rdsschema_add_form = RdsSchemaAddForm()
        self.context = {"rdsschema_add_form":rdsschema_add_form}
        return render(request,"cmdb/rdsschema/rdsschema_add.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_rdsschema",raise_exception=True))
    def post(self,request,*args,**kwargs):
        rdsschema_add_form = RdsSchemaAddForm(request.POST)
        if rdsschema_add_form.is_valid():
            schema_name = rdsschema_add_form.cleaned_data.get("schema_name")
            instance_id = rdsschema_add_form.cleaned_data.get("rdsinstance")
            schema_desc = rdsschema_add_form.cleaned_data.get("schema_desc")
            rdsschema = RdsSchema(
                schema_name = schema_name,
                rdsinstance = RdsInstance.objects.get(pk=instance_id),
                schema_desc = schema_desc
            )
            rdsschema.save()
            return HttpResponseRedirect(reverse("rdsschema_list"))
        else:
            self.context = {"rdsschema_add_form":rdsschema_add_form,"errors":rdsschema_add_form.errors}
            return render(request,"cmdb/rdsschema/rdsschema_add.html",self.context)

class RdsSchemaUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_rdsschema",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        rdsschema = RdsSchema.objects.get(pk=id)
        rdsschema_dict = model_to_dict(rdsschema)
        rdsschema_update_form = RdsSchemaAddForm(rdsschema_dict)
        self.context = {"rdsschema_update_form":rdsschema_update_form}
        return render(request,"cmdb/rdsschema/rdsschema_update.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_rdsschema",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        rdsschema_update_form = RdsSchemaAddForm(request.POST)
        if rdsschema_update_form.is_valid():
            rdsschema = RdsSchema.objects.get(pk=id)
            rdsschema.schema_name = rdsschema_update_form.cleaned_data.get("schema_name")
            rdsschema.rdsinstanc = RdsInstance.objects.get(pk=rdsschema_update_form.cleaned_data.get("rdsinstance"))
            rdsschema.schema_desc = rdsschema_update_form.cleaned_data.get("schema_desc")
            rdsschema.save()
            return HttpResponseRedirect(reverse("rdsschema_list"))
        else:
            self.context = {"rdsschema_update_form":rdsschema_update_form,"errors":rdsschema_update_form.errors}
            return render(request,"cmdb/rdsschema/rdsschema_update.html",self.context)

class RdsSchemaDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.delete_rdsschema",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        rdsschema = RdsSchema.objects.get(pk=id)
        rdsschema.delete()
        return HttpResponseRedirect(reverse("rdsschema_list"))




