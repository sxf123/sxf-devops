from django.shortcuts import render
from django.views.generic import View
from cmdb.models.DbSchema import DbSchema
from cmdb.forms.DbSchemaForm import DbSchemaSearchForm
from cmdb.forms.DbSchemaForm import DbSchemaAddForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json
from django.core.serializers import serialize
from cmdb.models.Database import Database
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import permission_required

class DbSchemaSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_dbschema",raise_exception=True))
    def get(self,request,*args,**kwargs):
        dbschema_search_form = DbSchemaSearchForm()
        dbschema = DbSchema.objects.all()
        self.context = {"dbschema":dbschema,"dbschema_search_form":dbschema_search_form}
        return render(request,"cmdb/database/dbschema_list.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_dbschema",raise_exception=True))
    def post(self,request,*args,**kwargs):
        search_schema = request.POST["search_schema"]
        search_instance = request.POST["search_instance"]
        dbschema = DbSchema.objects.select_related("instance").filter(schema=search_schema).filter(instance__id=search_instance)
        return JsonResponse(json.loads(serialize("json",dbschema)),safe=False)

class DbSchemaAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_dbschema",raise_exception=True))
    def get(self,request,*args,**kwargs):
        dbschema_add_form = DbSchemaAddForm()
        self.context = {"dbschema_add_form":dbschema_add_form}
        return render(request,"cmdb/database/dbschema_add.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_dbschema",raise_exception=True))
    def post(self,request,*args,**kwargs):
        dbschema_add_form = DbSchemaAddForm(request.POST)
        if dbschema_add_form.is_valid():
            schema = request.POST["schema"]
            dbschema = DbSchema.objects.filter(schema=schema)
            if dbschema.exists():
                self.context = {"dbschema_add_form":dbschema_add_form,"repeat_errors":"true"}
                return render(request,"cmdb/database/dbschema_add.html",self.context)
            else:
                url = request.POST["url"]
                port = request.POST["port"]
                user = request.POST["user"]
                password = request.POST["password"]
                instance_id = request.POST["instance"]
                if instance_id == "":
                    database = None
                else:
                    database = Database.objects.get(pk=instance_id)
                dbschema = DbSchema(schema=schema,url=url,port=port,user=user,password=password,instance=database)
                dbschema.save()
                return HttpResponsePermanentRedirect(reverse("dbschema"))
        else:
            self.context = {"dbschema_add_form":dbschema_add_form,"errors":dbschema_add_form.errors}
            return render(request,"cmdb/database/dbschema_add.html",self.context)

class DbSchemaUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_dbschema",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        dbschema = DbSchema.objects.get(pk=id)
        dbschema_dict = model_to_dict(dbschema)
        dbschema_update_form = DbSchemaAddForm(dbschema_dict)
        self.context = {"dbschema_update_form":dbschema_update_form}
        return render(request,"cmdb/database/dbschema_update.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_dbschema",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        dbschema_update_form = DbSchemaAddForm(request.POST)
        dbschema = DbSchema.objects.get(pk=id)
        if dbschema_update_form.is_valid():
            dbschema.schema = request.POST["schema"]
            dbschema.url = request.POST["url"]
            dbschema.port = request.POST["port"]
            dbschema.user = request.POST["user"]
            dbschema.password = request.POST["password"]
            instance_id = request.POST["instance"]
            if instance_id == "":
                database = None
            else:
                database = Database.objects.get(pk=instance_id)
            dbschema.instance = database
            dbschema.save()
            return HttpResponsePermanentRedirect(reverse("dbschema"))
        else:
            self.context = {"dbschema_update_form":dbschema_update_form,"errors":dbschema_update_form.errors}
            return render(request,"cmdb/database/dbschema_update.html",self.context)




