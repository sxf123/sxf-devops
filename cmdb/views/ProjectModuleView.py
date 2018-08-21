from django.shortcuts import render
from cmdb.forms.ProjectModuleForm import ProjectModuleSearchForm,ProjectModuleAddForm
from cmdb.models.ProjectModule import ProjectModule
from django.views.generic import View
from django.forms.models import model_to_dict
from cmdb.models.Project import Project
from cmdb.models.Cluster import Cluster
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from saltjob.generate_state_file import write_yaml_file,create_state_dir
import os
from common.disconf_api import config_list,get_appId
from django.contrib.auth.decorators import permission_required

class ProjectModuleSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_projectmodule",raise_exception=True))
    def get(self,request,*args,**kwargs):
        projectmodule_search_form = ProjectModuleSearchForm()
        projectmodule = ProjectModule.objects.all()
        self.context = {"projectmodule_search_form":projectmodule_search_form,"projectmodule":projectmodule}
        return render(request, "cmdb/projectmodule/projectmodule_list.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_projectmodule",raise_exception=True))
    def post(self,request,*args,**kwargs):
        projectmodule_search_form = ProjectModuleSearchForm(request.POST)
        if projectmodule_search_form.is_valid():
            search_module_name = request.POST["search_module_name"]
            search_proj_name = request.POST["search_proj_name"]
            if search_module_name == "":
                projectmodule = ProjectModule.objects.filter(project=search_proj_name)
            else:
                projectmodule = ProjectModule.objects.filter(module_name__contains=search_module_name).filter(project=search_proj_name)
            self.context = {"projectmodule_search_form":projectmodule_search_form,"projectmodule":projectmodule}
            return render(request,"cmdb/projectmodule/projectmodule_detail.html",self.context)
        else:
            self.context = {"projectmoudle_search_form":projectmodule_search_form,"errors":projectmodule_search_form.errors}
            return render(request,"cmdb/projectmodule/projectmodule_list.html",self.context)
class ProjectModuleAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_projectmodule",raise_exception=True))
    def get(self,request,*args,**kwargs):
        projectmodule_add_form = ProjectModuleAddForm()
        self.context = {"projectmodule_add_form":projectmodule_add_form}
        return render(request, "cmdb/projectmodule/projectmodule_add.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_projectmodule",raise_exception=True))
    def post(self,request,*args,**kwargs):
        projectmodule_add_form = ProjectModuleAddForm(request.POST)
        if projectmodule_add_form.is_valid():
            module_name = request.POST["module_name"]
            module_desc = request.POST["module_desc"]
            module_service_type = request.POST["service_type"]
            module_git_url = request.POST["git_url"]
            module_project_id = request.POST["project"]
            module_cluster_list = request.POST.getlist("cluster")
            if module_project_id == "":
                module_project = None
            else:
                module_project = Project.objects.get(pk=module_project_id)
            projectmodule = ProjectModule(
                module_name = module_name,
                module_desc = module_desc,
                service_type = module_service_type,
                git_url = module_git_url,
                project = module_project
            )
            projectmodule.save()
            for c in module_cluster_list:
                projectmodule.cluster.add(c)
            projectmodule.save()
            name = module_project.name.split("-")[0]
            yaml_dict = {"projectmodule":module_name,"project":name}
            create_state_dir(module_name)
            cwd = os.path.dirname(os.path.abspath(__file__))
            init_tpl = os.path.join(os.path.join(os.path.dirname(os.path.dirname(cwd)),"saltjob"),"init.json.j2")
            install_tpl = os.path.join(os.path.join(os.path.dirname(os.path.dirname(cwd)),"saltjob"),"install.json.j2")
            init_file = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.dirname(cwd)),"saltjob"),module_name),"init.sls")
            install_file = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.dirname(cwd)),"saltjob"),module_name),"install.sls")
            write_yaml_file(yaml_dict,init_tpl,init_file)
            write_yaml_file(yaml_dict,install_tpl,install_file)
            return HttpResponsePermanentRedirect(reverse("projectmodule"))
        else:
            self.context = {"projectmodule_add_form":projectmodule_add_form,"project_add_errors":projectmodule_add_form.errors}
            return render(request, "cmdb/projectmodule/projectmodule_add.html", self.context)
class ProjectModuleUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_projectmodule",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        projectmodule = ProjectModule.objects.get(pk=id)
        projectmodule_dict = model_to_dict(projectmodule)
        # print(projectmodule_dict["module_service_type"])
        projectmodule_update_form = ProjectModuleAddForm(projectmodule_dict)
        self.context = {"projectmodule_update_form":projectmodule_update_form}
        return render(request, "cmdb/projectmodule/projectmodule_update.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_projectmodule",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        projectmodule_update_form = ProjectModuleAddForm(request.POST)
        if projectmodule_update_form.is_valid():
            module_name = request.POST["module_name"]
            module_desc = request.POST["module_desc"]
            module_service_type = request.POST["service_type"]
            module_git_url = request.POST["git_url"]
            module_project_id = request.POST["project"]
            if module_project_id == "":
                module_project = None
            else:
                module_project = Project.objects.get(pk=module_project_id)
            module_cluster_list = request.POST.getlist("cluster")
            projectmodule = ProjectModule.objects.get(pk=id)
            projectmodule.module_name = module_name
            projectmodule.module_desc = module_desc
            projectmodule.service_type = module_service_type
            projectmodule.git_url = module_git_url
            projectmodule.project = module_project
            projectmodule.cluster.clear()
            for c in module_cluster_list:
                projectmodule.cluster.add(c)
            projectmodule.save()
            return HttpResponsePermanentRedirect(reverse("projectmodule"))
        else:
            self.context = {"projectmodule_update_form":projectmodule_update_form,"projectmodule_update_errors":projectmodule_update_form.errors}
            return render(request, "cmdb/projectmodule/projectmodule_update.html", self.context)

class ProjectModuleDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.delete_projectmodule",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        projectmodule = ProjectModule.objects.get(pk=id)
        projectmodule.delete()
        return HttpResponsePermanentRedirect(reverse("projectmodule"))

class ProjectModuleDetailView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        name = kwargs.get("name")
        projectmoudle = ProjectModule.objects.select_related("project").filter(project__name=name)
        self.context = {"projectmodule":projectmoudle}
        return render(request,"cmdb/project/projectmodule_detail.html",self.context)

class ProjectModuleUpdateInfo(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        module_name = kwargs.get("module_name")
        projectmodule = ProjectModule.objects.get(module_name=module_name)
        cluster_list = ["{}-cluster-dev".format(module_name),"{}-cluster-test".format(module_name),"{}-cluster-pre".format(module_name),"{}-cluster-prod".format(module_name)]
        for cluster_name in cluster_list:
            projectmodule.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        projectmodule.save()
        return HttpResponsePermanentRedirect(reverse("projectmodule"))

class ProjectModuleConfigView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        projectmodule = ProjectModule.objects.get(pk=id)
        appName = projectmodule.module_name
        project = projectmodule.project
        appId = get_appId(appName)
        file_list = config_list(appId,"1","1.0.0")
        self.context = {"file_list":file_list,"module_name":appName,"environment":project.environment}
        return render(request,"cmdb/projectmodule/config_list.html",self.context)






