from django.shortcuts import render
from django.views.generic import View
from jenkinsapi.jenkinsapi import get_node,create_node
from jenkinsapi.forms import JenkinsSearchForm,JenkinsAddNodeForm
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class JenkinsSearchNode(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        jenkins_search_form = JenkinsSearchForm()
        node_list = get_node()
        self.context = {"jenkins_search_form":jenkins_search_form,"node_list":node_list}
        return render(request,"jenkins/node/node_list.html",self.context)
    def post(self,request,*args,**kwargs):
        pass


class JekinsAddNode(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        jenkins_add_node_form = JenkinsAddNodeForm()
        self.context = {"jenkins_add_node_form":jenkins_add_node_form}
        return render(request,"jenkins/node/node_add.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        jenkins_add_node_form = JenkinsAddNodeForm(request.POST)
        if jenkins_add_node_form.is_valid():
            name = request.POST["name"]
            port = request.POST["port"]
            user = request.POST["user"]
            credentialsId = request.POST["credentialsId"]
            host = request.POST["host"]
            javaPath = request.POST["javaPath"]
            if create_node(port,user,credentialsId,host,javaPath,name) == 1:
                return HttpResponsePermanentRedirect(reverse("jenkins_search_node"))
            elif create_node(port,user,credentialsId,host,javaPath,name) == 0:
                self.context = {"jekins_add_node_form":jenkins_add_node_form,"errors":"true"}
                return render(request,"jenkins/node/node_add.html",)
        else:
            self.context = {"jenkins_add_node_form":jenkins_add_node_form,"errors":jenkins_add_node_form.errors}
            return render(request,"jenkins/node/node_add.html",self.context)
