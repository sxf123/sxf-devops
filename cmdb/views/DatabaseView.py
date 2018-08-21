from django.shortcuts import render
from django.views.generic import View
from cmdb.forms.DatabaseForm import DatabaseSearchForm,DatabaseAddForm
from cmdb.models.Database import Database
from cmdb.models.Cluster import Cluster
from cmdb.models.Host import Host
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from cmdb.models.DbSchema import DbSchema
from django.contrib.auth.decorators import permission_required

class DatabaseSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_database",raise_exception=True))
    def get(self,request,*args,**kwargs):
        database_search_form = DatabaseSearchForm()
        database = Database.objects.all()
        self.context = {"database_search_form":database_search_form,"database":database}
        return render(request,"cmdb/database/database_list.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_database",raise_exception=True))
    def post(self,request,*args,**kwargs):
        database_search_form = DatabaseSearchForm(request.POST)
        if database_search_form.is_valid():
            search_schema = request.POST["search_schema"]
            search_db_type = request.POST["search_db_type"]
            if search_schema == "":
                database = Database.objects.filter(db_type=search_db_type)
            else:
                database = Database.objects.filter(instance=search_schema).filter(db_type=search_db_type)
            self.context = {"database":database,"database_search_form":database_search_form}
            return render(request,"cmdb/database/database_detail.html",self.context)
        else:
            self.context = {"database_search_form":database_search_form,"errors":database_search_form.errors}
            return render(request,"cmdb/database/database_list.html",self.context)
class DatabaseAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_database",raise_exception=True))
    def get(self,request,*args,**kwargs):
        database_add_form = DatabaseAddForm()
        self.context = {"database_add_form":database_add_form}
        return render(request,"cmdb/database/database_add.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_database",raise_exception=True))
    def post(self,request,*args,**kwargs):
        database_add_form = DatabaseAddForm(request.POST)
        if database_add_form.is_valid():
            instance = request.POST["instance"]
            database = Database.objects.filter(instance=instance)
            if database.exists():
                self.context = {"database_add_form":database_add_form,"repeat_errors":"true"}
                return render(request,"cmdb/database/database_add.html",self.context)
            else:
                db_type = request.POST["db_type"]
                cluster_id = request.POST["cluster"]
                host_id = request.POST["host"]
                if cluster_id == "":
                    cluster = None
                else:
                    cluster = Cluster.objects.get(pk=cluster_id)
                if host_id == "":
                    host = None
                else:
                    host = Host.objects.get(pk=host_id)
                database = Database(instance=instance,db_type=db_type,cluster=cluster,host=host)
                database.save()
                return HttpResponsePermanentRedirect(reverse("database"))
        else:
            self.context = {"database_add_form":database_add_form,"database_add_errors":database_add_form.errors}
            return render(request,"cmdb/database/database_add.html",self.context)

class DatabaseUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_database",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        database = Database.objects.get(pk=id)
        database_dict = model_to_dict(database)
        database_update_form = DatabaseAddForm(database_dict)
        self.context = {"database_update_form":database_update_form}
        return render(request,"cmdb/database/database_update.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_database",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        database_update_form = DatabaseAddForm(request.POST)
        database = Database.objects.get(pk=id)
        if database_update_form.is_valid():
            database.instance = request.POST["instance"]
            database.db_type = request.POST["db_type"]
            cluster_id = request.POST["cluster"]
            if cluster_id == "":
                cluster = None
            else:
                cluster = Cluster.objects.get(pk=cluster_id)
            database.cluster = cluster
            host_id = request.POST["host"]
            if host_id == "":
                host = None
            else:
                host = Host.objects.get(pk=host_id)
            database.host = host
            database.save()
            return HttpResponsePermanentRedirect(reverse("database"))
        else:
            self.context = {"database_update_form":database_update_form,"database_update_errors":database_update_form.errors}
            return render(request,"cmdb/database/database_update.html",self.context)

class DatabaseDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.delete_database",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        database = Database.objects.get(pk=id)
        database.delete()
        return HttpResponsePermanentRedirect(reverse("database"))

class DatabaseDetail(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        instance = kwargs.get("instance")
        dbschema_list = DbSchema.objects.select_related("instance").filter(instance__instance=instance)
        self.context = {"dbschema_list":dbschema_list}
        return render(request,"cmdb/database/dbschema_detail.html",self.context)

