from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from deploy.forms import DeployForm
from deploy.models import DeployTask
from cmdb.models.ProjectModule import ProjectModule
from deploy.forms import DeploySearchForm
from common.email import sendmail
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
import time
from common.email import EmailThread

class DeployTaskSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_deploytask",raise_exception=True))
    def get(self,request,*args,**kwargs):
        deploy_search_form = DeploySearchForm()
        deploytask = DeployTask.objects.all()
        self.context = {"deploy_search_form":deploy_search_form,"deploytask":deploytask}
        return render(request,"deploy/deploytask_list.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_deploytask",raise_exception=True))
    def post(self,request,*args,**kwargs):
        deploy_search_form = DeploySearchForm(request.POST)
        if deploy_search_form.is_valid():
            module_name = deploy_search_form.cleaned_data.get("search_project_module")
            deploytask = DeployTask.objects.select_related("project").filter(project__id=module_name)
            self.context = {"deploy_search_form":deploy_search_form,"deploytask":deploytask}
            return render(request,"deploy/deploytask_list.html",self.context)
        else:
            self.context = {"deploy_search_form":deploy_search_form,"errors":deploy_search_form.errors}
            return render(request,"deploy/deploytask_list.html",self.context)

class DeployTaskView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.add_deploytask",raise_exception=True))
    def get(self,request,*args,**kwargs):
        deploy_form = DeployForm()
        self.context = {"deploy_form":deploy_form}
        return render(request,"deploy/deploy_add.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.add_deploytask",raise_exception=True))
    def post(self,request,*args,**kwargs):
        deploy_form = DeployForm(data = request.POST,files = request.FILES)
        if deploy_form.is_valid():
            project_id = deploy_form.cleaned_data.get("project")
            svn_path = deploy_form.cleaned_data.get("svn_path")
            principal = deploy_form.cleaned_data.get("principal")
            update_date = deploy_form.cleaned_data.get("update_date")
            update_project_id =deploy_form.cleaned_data.get("update_project")
            tag_date = deploy_form.cleaned_data.get("tag_date")
            tag_version = deploy_form.cleaned_data.get("tag_version")
            desc = deploy_form.cleaned_data.get("desc")
            bug_fix = deploy_form.cleaned_data.get("bug_fix")
            update_function = deploy_form.cleaned_data.get("update_function")
            solve_problem = deploy_form.cleaned_data.get("solve_problem")
            exist_risk = deploy_form.cleaned_data.get("exist_risk")
            rollback = deploy_form.cleaned_data.get("rollback")
            is_monitored = deploy_form.cleaned_data.get("is_monitored")
            instance = deploy_form.cleaned_data.get("instance")
            dbschema = deploy_form.cleaned_data.get("dbschema")
            need_test = deploy_form.cleaned_data.get("need_test")
            develop_person = deploy_form.cleaned_data.get("develop_person")
            monitored_person = deploy_form.cleaned_data.get("monitored_person")
            verify_person = deploy_form.cleaned_data.get("verify_person")
            sql_exec = deploy_form.cleaned_data.get("sql_exec")
            handle_person = deploy_form.cleaned_data.get("handle_person")
            deploy_type = deploy_form.cleaned_data.get("deploy_type")
            email_person = deploy_form.cleaned_data.get("email_person")
            now = time.strftime("%Y-%m-%d",time.localtime(time.time()))
            if str(update_date) != now or str(tag_date) != now:
                self.context = {"deploy_form":deploy_form,"date_error":"True"}
                return render(request,"deploy/deploy_add.html",self.context)
            else:
                deploy_task_list = DeployTask.objects.filter(project=project_id).filter(update_date=update_date)
                if len(deploy_task_list) < 3 and deploy_type == "common upgrade" or deploy_type == "bug fix":
                    deploy_task = DeployTask(
                        project = ProjectModule.objects.get(pk=project_id),
                        svn_path = svn_path,
                        principal = principal,
                        update_date = update_date,
                        update_project = ProjectModule.objects.get(pk=update_project_id),
                        tag_date = tag_date,
                        tag_version = tag_version,
                        desc = desc,
                        bug_fix = bug_fix,
                        update_function = update_function,
                        solve_problem = solve_problem,
                        exist_risk = exist_risk,
                        roll_back = rollback,
                        is_monitored = is_monitored,
                        develop_person = " ".join(develop_person),
                        monitored_person = " ".join(monitored_person),
                        verify_person = " ".join(verify_person),
                        need_test = need_test,
                        handle_person = handle_person,
                        deploy_type = deploy_type
                    )
                    deploy_task.save()
                    if need_test == "yes":
                        subject = "需要测试"
                        message = "<html><head><title></title></head><body><a>http://127.0.0.1:8000/deploy/task/examine/{}/</a></body></html>".format(deploy_task.id)
                        addr = ["{}@zhexinit.com".format(v) for v in verify_person]
                        for ep in email_person:
                            addr.append("{}@zhexinit.com".format(ep))
                        emailthread = EmailThread(subject,message,addr)
                        emailthread.start()
                    else:
                        subject = "需要升级"
                        message = deploy_task.project.module_name
                        addr = ["{}@zhexinit.com".format(handle_person)]
                        for ep in email_person:
                            addr.append("{}@zhexinit.com".format(ep))
                        emailthread = EmailThread(subject,message,addr)
                        emailthread.start()
                    return HttpResponsePermanentRedirect(reverse("deploy_task_list"))
                else:
                    self.context = {"deploy_form":deploy_form,"too_many_upgrade":"True"}
                    return render(request,"deploy/deploy_add.html",self.context)
        else:
            self.context = {"deploy_form":deploy_form,"errors":deploy_form.errors}
            return render(request,"deploy/deploy_add.html",self.context)

@csrf_exempt
@permission_required("deploy.examine_deploytask",raise_exception=True)
def test_pass(request,handle_person,project,tag_version):
    deploytask = DeployTask.objects.filter(project__module_name=project).filter(tag_version=tag_version)[0]
    subject = "测试通过，可以升级"
    message = "可以升级-{}-{}".format(deploytask.project.module_name,deploytask.tag_version)
    addr = ["{}@zhexinit.com".format(handle_person)]
    emailthread = EmailThread(subject,message,addr)
    emailthread.start()
    deploytask.is_test_pass = "yes"
    deploytask.save()
    return HttpResponseRedirect(reverse("deploy_task_list"))

@csrf_exempt
@permission_required("deploy.backspace_deploytask",raise_exception=True)
def backspace(request,principal,project,tag_version):
    deploytask = DeployTask.objects.filter(project__module_name=project).filter(tag_version=tag_version)[0]
    subject = "测试失败，不能升级"
    message = "不能升级-{}-{}".format(deploytask.project.module_name,deploytask.tag_version)
    addr = ["{}@zhexinit.com".format(principal)]
    emailthread = EmailThread(subject,message,addr)
    emailthread.start()
    deploytask.is_backspace = "yes"
    deploytask.save()
    return HttpResponseRedirect(reverse("deploy_task_list"))


class DeployTaskDelete(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.delete_deploytask",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        deploytask = DeployTask.objects.get(pk=id)
        deploytask.delete()
        return HttpResponseRedirect(reverse("deploy_task_list"))

class DeployTaskTransfer(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        pass
    def post(self,request,*args,**kwargs):
        pass

class DeployTaskExamine(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.examine_deploytask",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        deploytask = DeployTask.objects.get(pk=id)
        self.context = {"deploytask":deploytask}
        return render(request,"deploy/deploytask_info.html",self.context)

