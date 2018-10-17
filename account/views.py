from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.views.generic import View
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from account.forms import UserSearchForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from account.forms import UserAddForm,UserUpdateForm
from account.forms import GroupSearchForm,GroupAddForm
from django.contrib.auth.decorators import permission_required

class UserListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        user_search_form = UserSearchForm()
        users = User.objects.all()
        self.context = {"user_search_form":user_search_form,"users":users}
        return render(request,"account/user_list.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        user_search_form = UserSearchForm(request.POST)
        if user_search_form.is_valid():
            username = user_search_form.cleaned_data.get("search_username")
            group = user_search_form.cleaned_data.get("search_group")
            if username == "" and group != "":
                group = Group.objects.get(pk=group)
                users = group.user_set.all()
                self.context = {"user_search_form":user_search_form,"users":users}
                return render(request,"account/user_detail.html",self.context)
            elif username != "" and group == "":
                users = User.objects.filter(username=username)
                self.context = {"user_search_form":user_search_form,"users":users}
                return render(request,"account/user_detail.html",self.context)
            elif username != "" and group != "":
                group = Group.objects.get(pk=group)
                users = group.user_set.filter(username=username)
                self.context = {"user_search_form":user_search_form,"users":users}
                return render(request,"account/user_detail.html",self.context)
            elif username == "" and group == "":
                users = User.objects.filter(username="")
                self.context = {"user_search_form":user_search_form,"users":users}
                return render(request,"account/user_detail.html",self.context)
        else:
            self.context = {"user_search_form":user_search_form,"errors":user_search_form.errors}
            return render(request,"account/user_list.html",self.context)

class UserAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.add_user",raise_exception=True))
    def get(self,request,*args,**kwargs):
        user_add_form = UserAddForm()
        self.context = {"user_add_form":user_add_form}
        return render(request,"account/user_add.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.add_user",raise_exception=True))
    def post(self,request,*args,**kwargs):
        user_add_form = UserAddForm(request.POST)
        if user_add_form.is_valid():
            username = user_add_form.cleaned_data.get("username")
            password = user_add_form.cleaned_data.get("password")
            first_name = user_add_form.cleaned_data.get("first_name")
            last_name = user_add_form.cleaned_data.get("last_name")
            email = user_add_form.cleaned_data.get("email")
            is_superuser = user_add_form.cleaned_data.get("is_superuser")
            is_staff = user_add_form.cleaned_data.get("is_staff")
            group = user_add_form.cleaned_data.get("group")
            user = User(
                username = username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                is_superuser = is_superuser,
                is_staff = is_staff
            )
            user.set_password(password)
            user.save()
            group = Group.objects.get(pk=group)
            user.groups.add(group)
            return HttpResponsePermanentRedirect(reverse("user_list"))
        else:
            print(user_add_form.cleaned_data)
            self.context = {"user_add_form":user_add_form,"errors":user_add_form.errors}
            return render(request,"account/user_add.html",self.context)

class UserUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.change_user",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        user = User.objects.get(pk=id)
        user_dict = model_to_dict(user)
        user_update_form = UserAddForm(user_dict)
        self.context = {"user_update_form":user_update_form}
        return render(request,"account/user_update.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.change_user",raise_exception=True))
    def post(self,request,*args,**kwargs):
        user_update_form = UserAddForm(request.POST)
        if user_update_form.is_valid():
            id = kwargs.get("id")
            user = User.objects.get(pk=id)
            user.username = user_update_form.cleaned_data.get("username")
            if user_update_form.cleaned_data.get("password") != "":
                user.set_password(user_update_form.cleaned_data.get("password"))
            user.first_name = user_update_form.cleaned_data.get("first_name")
            user.last_name = user_update_form.cleaned_data.get("last_name")
            user.email = user_update_form.cleaned_data.get("email")
            user.is_superuser = user_update_form.cleaned_data.get("is_superuser")
            user.is_staff = user_update_form.cleaned_data.get("is_staff")
            user.save()
            user.groups.clear()
            groups = Group.objects.filter(pk=user_update_form.cleaned_data.get("group"))
            print(groups)
            if len(groups) != 0:
                user.groups.add(groups[0])
            return HttpResponsePermanentRedirect(reverse("user_list"))
        else:
            self.context = {"user_update_form":user_update_form,"errors":user_update_form.errors}
            return render(request,"account/user_update.html",self.context)

class UserDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.delete_user",raise_exception=True))
    def get(self,reqeust,*args,**kwargs):
        id = kwargs.get("id")
        user = User.objects.get(pk=id)
        user.delete()
        return HttpResponsePermanentRedirect(reverse("user_list"))

class GroupListView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        group_search_form = GroupSearchForm()
        group_list = Group.objects.all()
        self.context = {"group_search_form":group_search_form,"group":group_list}
        return render(request,"account/group_list.html",self.context)
    def post(self,request,*args,**kwargs):
        group_search_form = GroupSearchForm(request.POST)
        if group_search_form.is_valid():
            name = group_search_form.cleaned_data.get("search_group_name")
            group = Group.objects.filter(name=name)
            self.context = {"group_search_form":group_search_form,"group":group}
            return render(request,"account/group_list.html",self.context)
        else:
            self.context = {"group_search_form":group_search_form,"errors":group_search_form.errors}
            return render(request,"account/group_list.html",self.context)
class GroupAddView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        group_add_form = GroupAddForm()
        self.context = {"group_add_form":group_add_form}
        return render(request,"account/group_add.html",self.context)
    def post(self,request,*args,**kwargs):
        group_add_form = GroupAddForm(request.POST)
        if group_add_form.is_valid():
            name = group_add_form.cleaned_data.get("name")
            permissions = group_add_form.cleaned_data.get("permissions")
            group = Group(name=name)
            group.save()
            for p in permissions:
                group.permissions.add(p)
                group.save()
            return HttpResponsePermanentRedirect(reverse("group_list"))
        else:
            self.context = {"group_add_form":group_add_form,"errors":group_add_form.errors}
            return render(request,"account/group_list.html",self.context)

class GroupUpdateView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        group = Group.objects.get(pk=id)
        group_dict = model_to_dict(group)
        group_update_form = GroupAddForm(group_dict)
        self.context = {"group_update_form":group_update_form}
        return render(request,"account/group_update.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        group = Group.objects.get(pk=id)
        group_update_form = GroupAddForm(request.POST)
        if group_update_form.is_valid():
            group.name = group_update_form.cleaned_data.get("name")
            group.permissions.clear()
            for p in group_update_form.cleaned_data.get("permissions"):
                group.permissions.add(p)
            group.save()
            return HttpResponsePermanentRedirect(reverse("group_list"))
        else:
            self.context = {"group_update_form":group_update_form,"errors":group_update_form.errors}
            return render(request,"account/group_update.html",self.context)

class GroupDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.delete_group",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        group = Group.objects.get(pk=id)
        group.delete()
        return HttpResponsePermanentRedirect(reverse("group_list"))




