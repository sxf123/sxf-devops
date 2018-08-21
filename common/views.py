from django.shortcuts import render
from django.views.generic import View
from common.forms import LoginForm
from django.contrib import auth
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    return render(request,'common/index.html')

class LoginView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        login_form = LoginForm()
        self.context = {"login_form":login_form}
        return render(request,"common/login.html",self.context)
    def post(self,request,*args,**kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponsePermanentRedirect(reverse("index"))
            else:
                self.context = {"login_form":login_form,"password_is_wrong":True}
                return render(request,"common/login.html",self.context)
        else:
            self.context = {"login_form":login_form,"errors":login_form.errors}
            return render(request,"common/login.html",self.context)
class LogoutView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        auth.logout(request)
        return HttpResponsePermanentRedirect(reverse("login"))

def permission_denied(request):
    return render(request,"common/403.html")



