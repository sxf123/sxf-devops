from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from dxwf.forms import MavenProjSearchForm,MavenProjAddForm
from dxwf.models import MavenProj
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from dxwf.project_gen import gen_project
import os
from django.http import StreamingHttpResponse
from dxwf.project_gen import remove_proj

class MavenProjSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        mavenproj_search_form = MavenProjSearchForm()
        mavenproj = MavenProj.objects.all()
        self.context = {"mavenproj_search_form":mavenproj_search_form,"mavenproj":mavenproj}
        return render(request,"dxwf/mavenproj_list.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        search_artifactId = request.POST["search_artifactId"]
        search_service_type = request.POST["search_service_type"]
        mavenproj = MavenProj.objects.filter(artifactId=search_artifactId).filter(service_type=search_service_type)
        return JsonResponse(json.loads(serialize("json",mavenproj)),safe=False)

class MavenProjAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        mavenproj_add_form = MavenProjAddForm()
        self.context = {"mavenproj_add_form":mavenproj_add_form}
        return render(request,"dxwf/mavenproj_add.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        mavenproj_add_form = MavenProjAddForm(request.POST)
        if mavenproj_add_form.is_valid():
            groupId = request.POST["groupId"]
            artifactId = request.POST["artifactId"]
            service_type = request.POST["service_type"]
            mavenproj = MavenProj.objects.filter(artifactId=artifactId)
            if mavenproj.exists():
                self.context = {"mavenproj_add_form":mavenproj_add_form,"repeat_errors":"true"}
                return render(request,"dxwf/mavenproj_add.html",self.context)
            else:
                mavenproj = MavenProj(groupId=groupId,artifactId=artifactId,service_type=service_type)
                mavenproj.save()
                gen_project(service_type,groupId,artifactId)
                return HttpResponsePermanentRedirect(reverse("mavenproj"))
        else:
            self.context = {"mavenproj_add_form":mavenproj_add_form,"mavenproj_add_errors":mavenproj_add_form.errors}
            return render(request,"dxwf/mavenproj_add.html",self.context)

class MavenProjDeleteView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        mvnproj = MavenProj.objects.get(pk=id)
        artifactId = mvnproj.artifactId
        mvnproj.delete()
        remove_proj(artifactId)
        return HttpResponsePermanentRedirect(reverse("mavenproj"))
def readFile(filename,chunk_size=512):
    with open(filename,"rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
@login_required
def download_file(request,artifactId):
    mavenproj = MavenProj.objects.get(artifactId=artifactId)
    filename = "{}.tar.gz".format(artifactId)
    path = os.path.dirname(os.path.abspath(__file__))
    response = StreamingHttpResponse(readFile(os.path.join(path,filename)))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=%s' % filename
    return response