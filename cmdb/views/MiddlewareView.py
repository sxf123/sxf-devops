from django.shortcuts import render
from django.views.generic import View
from cmdb.models.MiddleWare import MiddleWare
from cmdb.forms.MiddlewareForm import MiddlewareSearchForm,MiddlewareAddForm
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from saltjob.install_salt import run_state
from cmdb.forms.HostForm import HostSelectForm
from saltjob.get_host_list import modify_list
from django.contrib.auth.decorators import permission_required

class MiddlewareSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_middleware",raise_exception=True))
    def get(self,request,*args,**kwargs):
        middleware_search_form = MiddlewareSearchForm()
        middleware = MiddleWare.objects.all()
        self.context = {"middleware":middleware,"middleware_search_form":middleware_search_form}
        return render(request, "cmdb/middleware/middleware_list.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_middleware",raise_exception=True))
    def post(self,request,*args,**kwargs):
        middleware_search_form = MiddlewareSearchForm()
        if middleware_search_form.is_valid():
            mid_search_name = request.POST["mid_search_form"]
            mid_search_type = request.POST["mid_search_type"]
            middleware = MiddleWare.objects.filter(mid_name=mid_search_name).filter(mid_type=mid_search_type)
            self.context = {"middleware":middleware,"middleware_search_form":middleware_search_form}
            return render(request,"cmdb/middleware/middleware_detail.html",self.context)
        else:
            self.context = {"middleware_search_form":middleware_search_form,"errors":middleware_search_form.errors}
            return render(request,"cmdb/middleware/middleware_list.html",self.context)

class MiddlewareAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_middleware",raise_exception=True))
    def get(self,request,*args,**kwargs):
        middleware_add_form = MiddlewareAddForm()
        self.context = {"middleware_add_form":middleware_add_form}
        return render(request, "cmdb/middleware/middleware_add.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_middleware",raise_exception=True))
    def post(self,request,*args,**kwargs):
        middleware_add_form = MiddlewareAddForm(request.POST)
        if middleware_add_form.is_valid():
            mid_name = request.POST["mid_name"]
            middleware = MiddleWare.objects.filter(mid_name=mid_name)
            if middleware.exists():
                self.context = {"middleware_add_form":middleware_add_form,"repeat_errors":"true"}
                return render(request, "cmdb/middleware/middleware_add.html", self.context)
            else:
                mid_type = request.POST["mid_type"]
                mid_description = request.POST["mid_description"]
                mid_version = request.POST["mid_version"]
                middleware = MiddleWare(mid_name=mid_name,mid_type=mid_type,mid_description=mid_description,mid_version=mid_version)
                middleware.save()
                return HttpResponsePermanentRedirect(reverse("middleware"))
        else:
            self.context = {"middleware_add_form":middleware_add_form,"errors":middleware_add_form.errors}
            return render(request, "cmdb/middleware/middleware_add.html", self.context)
class MiddlewareUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_middleware",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        middleware = MiddleWare.objects.get(pk=id)
        middleware_dict = model_to_dict(middleware)
        middleware_update_form = MiddlewareAddForm(middleware_dict)
        self.context = {"middleware_update_form":middleware_update_form}
        return render(request, "cmdb/middleware/middleware_update.html", self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_middleware",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        middleware_update_form = MiddlewareAddForm(request.POST)
        if middleware_update_form.is_valid():
            middleware = MiddleWare.objects.get(pk=id)
            middleware.mid_name = request.POST["mid_name"]
            middleware.mid_type = request.POST["mid_type"]
            middleware.mid_description = request.POST["mid_description"]
            middleware.mid_version = request.POST["mid_version"]
            middleware.save()
            return HttpResponsePermanentRedirect(reverse("middleware"))
        else:
            self.context = {"middleware_update_form":middleware_update_form,"middleware_update_errors":middleware_update_form.errors}
            return render(request, "cmdb/middleware/middleware_update.html", self.context)

class MiddlewareDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.delete_middleware",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        middleware = MiddleWare.objects.get(pk=id)
        middleware.delete()
        return HttpResponsePermanentRedirect(reverse("middleware"))

class MiddleWareInstall(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        midware = kwargs.get("midware")
        host_select_form = HostSelectForm(midware=midware)
        self.context = {"host_select_form":host_select_form,"middleware":midware}
        return render(request,"cmdb/middleware/host_select.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        tgt = request.POST["target"]
        midware = request.POST["midware"]
        expr_form = request.POST["expr_form"]
        resp = run_state(tgt,expr_form,midware)
        modify_list(tgt,midware)
        self.context = {"install_res":resp}
        return JsonResponse(self.context)





