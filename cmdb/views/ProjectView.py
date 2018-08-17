from django.shortcuts import render
from django.views.generic import View
from cmdb.forms.ProjectForm import ProjectSearchForm,ProjectAddForm
from cmdb.models.Project import Project
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict

class ProjectSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        project_search_form = ProjectSearchForm()
        project = Project.objects.all()
        self.context = {"project_search_form":project_search_form,"project":project}
        return render(request, "cmdb/project/project_list.html", self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        project_search_form = ProjectSearchForm(request.POST)
        if project_search_form.is_valid():
            project_search_name = request.POST["project_search_name"]
            project = Project.objects.filter(name__contains=project_search_name)
            self.context = {"project":project,"project_search_form":project_search_form}
            return render(request,"cmdb/project/project_detail.html",self.context)
        else:
            self.context = {"project_search_form":project_search_form,"errors":project_search_form.errors}
            return render(request,"cmdb/project/project_list.html",self.context)
class ProjectAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        project_add_form = ProjectAddForm()
        self.context = {"project_add_form":project_add_form}
        return render(request, "cmdb/project/project_add.html", self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        project_add_form = ProjectAddForm(request.POST)
        if project_add_form.is_valid():
            name = request.POST["name"]
            project = Project.objects.filter(name=name)
            real_name = request.POST["real_name"]
            description = request.POST["description"]
            dev_leading = request.POST["dev_leading"]
            test_leading = request.POST["test_leading"]
            proj_leading = request.POST["proj_leading"]
            ops_leading = request.POST["ops_leading"]
            project = Project(name = name,real_name=real_name,description = description,dev_leading = dev_leading,test_leading = test_leading,proj_leading = proj_leading,ops_leading = ops_leading)
            project.save()
            return HttpResponsePermanentRedirect(reverse("project"))
        else:
            self.context = {"project_add_form":project_add_form,"project_add_errors":project_add_form.errors}
            return render(request, "cmdb/project/project_add.html", self.context)
class ProjectUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        project = Project.objects.get(pk=id)
        project_dict = model_to_dict(project)
        project_update_form = ProjectAddForm(project_dict)
        self.context = {"project_update_form":project_update_form}
        return render(request, "cmdb/project/project_update.html", self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        project_updata_form = ProjectAddForm(request.POST)
        if project_updata_form.is_valid():
            project = Project.objects.get(pk=id)
            project.name = request.POST["name"]
            project.real_name = request.POST["real_name"]
            project.description = request.POST["description"]
            project.devleading = request.POST["dev_leading"]
            project.test_leading = request.POST["test_leading"]
            project.proj_leaging = request.POST["proj_leading"]
            project.ops_leading = request.POST["ops_leading"]
            project.save()
            return HttpResponsePermanentRedirect(reverse("project"))
        else:
            self.context = {"project_update_form":project_updata_form,"project_update_errors":project_updata_form.errors}
            print(project_updata_form.errors)
            return render(request, "cmdb/project/project_update.html", self.context)

class ProjectDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        project = Project.objects.get(pk=id)
        project.delete()
        return HttpResponsePermanentRedirect(reverse("project"))
