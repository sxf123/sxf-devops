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
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from datetime import datetime
from common.email import EmailThread
from common.redis_conn import RedisConn
from devops.settings import REDIS_HOST, REDIS_PORT
from deploy.views.UploadFileView import handle_uploaded_file
import os
from devops.settings import DEPLOY_UPLOAD_PATH
import shutil
import zipfile
from django.http import StreamingHttpResponse
from deploy.forms import TestReportUploadForm
from django.utils.encoding import escape_uri_path
from djcelery.models import PeriodicTask,IntervalSchedule
import json

class DeployTaskSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_deploytask", raise_exception=True))
    def get(self, request, *args, **kwargs):
        deploy_search_form = DeploySearchForm()
        username = str(request.user)
        user = User.objects.get(username=username)
        if request.user.is_superuser or user.groups.all()[0].name == "ops":
            deploytask = DeployTask.objects.all().order_by("-id")
        elif user.groups.all()[0].name == "test":
            deploytask = DeployTask.objects.filter(need_test="yes").filter(verify_person__contains=username).order_by("-id")
        else:
            deploytask = DeployTask.objects.filter(belong__username = str(request.user)).order_by("-id")
        self.context = {"deploy_search_form": deploy_search_form, "deploytask": deploytask}
        return render(request, "deploy/deploytask_list.html", self.context)

    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_deploytask", raise_exception=True))
    def post(self, request, *args, **kwargs):
        deploy_search_form = DeploySearchForm(request.POST)
        if deploy_search_form.is_valid():
            module_name_id = deploy_search_form.cleaned_data.get("search_project_module")
            module_name = ProjectModule.objects.get(pk=module_name_id).module_name
            return HttpResponseRedirect(reverse("deploy_task_detail",kwargs={"module_name":module_name}))
        else:
            self.context = {"deploy_search_form": deploy_search_form, "errors": deploy_search_form.errors}
            return render(request, "deploy/deploytask_list.html", self.context)

class DeployDetailView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_deploytask",raise_exception=True))
    def get(self,request,*args,**kwargs):
        module_name = kwargs.get("module_name")
        username = str(request.user)
        user = User.objects.get(username=username)
        if request.user.is_superuser:
            deploytask = DeployTask.objects.filter(project__module_name=module_name)
        elif user.groups.all()[0].name == "test":
            deploytask = DeployTask.objects.filter(project__module_name=module_name).filter(need_test="yes").filter(verify_person__contains=username)
        else:
            deploytask = DeployTask.objects.filter(project__module_name=module_name).filter(belong__username=username)
        self.context = {"deploytask_detail":deploytask}
        return render(request,"deploy/deploytask_detail.html",self.context)

class DeployTaskView(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.add_deploytask", raise_exception=True))
    def get(self, request, *args, **kwargs):
        deploy_form = DeployForm()
        self.context = {"deploy_form": deploy_form}
        return render(request, "deploy/deploy_add.html", self.context)

    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.add_deploytask", raise_exception=True))
    def post(self, request, *args, **kwargs):
        deploy_form = DeployForm(data=request.POST, files=request.FILES)
        if deploy_form.is_valid():
            project_id = deploy_form.cleaned_data.get("project")
            svn_path = deploy_form.cleaned_data.get("svn_path")
            principal = deploy_form.cleaned_data.get("principal")
            tag_date = deploy_form.cleaned_data.get("tag_date")
            tag_version = deploy_form.cleaned_data.get("tag_version")
            desc = deploy_form.cleaned_data.get("desc")
            bug_fix = deploy_form.cleaned_data.get("bug_fix")
            update_function = deploy_form.cleaned_data.get("update_function")
            solve_problem = deploy_form.cleaned_data.get("solve_problem")
            exist_risk = deploy_form.cleaned_data.get("exist_risk")
            rollback = deploy_form.cleaned_data.get("rollback")
            is_monitored = deploy_form.cleaned_data.get("is_monitored")
            rdsinstance = deploy_form.cleaned_data.get("rdsinstance")
            need_test = deploy_form.cleaned_data.get("need_test")
            develop_person = deploy_form.cleaned_data.get("develop_person")
            monitored_person = deploy_form.cleaned_data.get("monitored_person")
            verify_person = request.POST.getlist("verify_person")
            handle_person = deploy_form.cleaned_data.get("handle_person")
            deploy_type = deploy_form.cleaned_data.get("deploy_type")
            email_person = deploy_form.cleaned_data.get("email_person")
            upgrade_step = deploy_form.cleaned_data.get("upgrade_step")
            upgrade_partition = deploy_form.cleaned_data.get("upgrade_partition")
            deploytask = DeployTask.objects.filter(project__id=project_id).filter(tag_version=tag_version)
            if deploytask.exists():
                self.context = {"deploy_form": deploy_form, "upgrade_ticket_repeat": "True"}
                return render(request, "deploy/deploy_add.html", self.context)
            else:
                deploy_task = DeployTask(
                    project=ProjectModule.objects.get(pk=project_id),
                    svn_path=svn_path,
                    principal=principal,
                    tag_date=tag_date,
                    tag_version=tag_version,
                    desc=desc,
                    bug_fix=bug_fix,
                    update_function=update_function,
                    solve_problem=solve_problem,
                    exist_risk=exist_risk,
                    roll_back=rollback,
                    is_monitored=is_monitored,
                    develop_person=" ".join(develop_person),
                    monitored_person=" ".join(monitored_person),
                    need_test=need_test,
                    handle_person=handle_person,
                    deploy_type=deploy_type,
                    upgrade_step=upgrade_step,
                    email_person=" ".join(email_person),
                    belong = User.objects.get(username=str(request.user)),
                    upgrade_partition = upgrade_partition
                )
                module_name = deploy_task.project.module_name
                tag_version = deploy_task.tag_version
                if deploy_task.need_test == "yes":
                    deploy_task.verify_person = " ".join(verify_person)
                deploy_task.save()
                if len(rdsinstance) > 0:
                    deploy_task.is_sql_exec = "yes"
                    deploy_task.save()
                    for rds in rdsinstance:
                        rdsschema = request.POST.getlist(rds)
                        for schema in rdsschema:
                            sql_file = request.FILES.get(schema)
                            sql_file_dir = os.path.join(os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,module_name),tag_version),rds),schema)
                            sql_file_name = os.path.join(sql_file_dir,sql_file.name)
                            if not os.path.exists(sql_file_dir):
                                os.makedirs(sql_file_dir)
                            handle_uploaded_file(sql_file_name,sql_file)
                    dirname = os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,module_name),tag_version)
                    zipfilename = "{}-{}.zip".format(module_name, tag_version)
                    zip_dir(dirname,os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH, module_name), tag_version),zipfilename))
                    if deploy_task.need_test == "yes":
                        subject = "需要测试验证"
                        message = "{}-{}需要升级\nhttp://ops.zhexinit.com:81/deploy/task/examine/{}/".format(module_name,tag_version,deploy_task.id)
                        addr = ["{}@zhexinit.com".format(v) for v in deploy_task.verify_person.split()]
                        for e in email_person:
                            addr.append("{}@zhexinit.com".format(e))
                        emailthread = EmailThread(subject,message,addr)
                        emailthread.start()
                    else:
                        subject = "直接升级"
                        message = "{}-{}需要升级\nhttp://ops.zhexinit.com:81/deploy/task/examine/{}/".format(module_name,tag_version,deploy_task.id)
                        addr = ["{}@zhexinit.com".format(deploy_task.handle_person)]
                        for e in email_person:
                            addr.append("{}@zhexinit.com".format(e))
                        print(addr)
                        emailthread = EmailThread(subject,message,addr)
                        emailthread.start()
                    return HttpResponseRedirect(reverse("deploy_task_list"))
                else:
                    if deploy_task.need_test == "yes":
                        subject = "需要测试验证"
                        message = "{}-{}需要升级\nhttp://ops.zhexinit.com:81/deploy/task/examine/{}/".format(module_name,tag_version,deploy_task.id)
                        addr = ["{}@zhexinit.com".format(v) for v in deploy_task.verify_person.split()]
                        for e in deploy_task.email_person.split():
                            addr.append("{}@zhexinit.com".format(e))
                        emailthread = EmailThread(subject, message, addr)
                        emailthread.start()
                    else:
                        subject = "直接升级"
                        message = "{}-{}需要升级\nhttp://ops.zhexinit.com:81/deploy/task/examine/{}/".format(module_name,tag_version,deploy_task.id)
                        addr = ["{}@zhexinit.com".format(deploy_task.handle_person)]
                        for e in email_person:
                            addr.append("{}@zhexinit.com".format(e))
                        emailthread = EmailThread(subject, message, addr)
                        emailthread.start()
                    return HttpResponseRedirect(reverse("deploy_task_list"))
        else:
            self.context = {"deploy_form":deploy_form,"errors":deploy_form.errors}


@csrf_exempt
@permission_required("deploy.examine_deploytask", raise_exception=True)
def test_pass(request, module_name, tag_version):
    # deploytask = DeployTask.objects.filter(project__module_name=project).filter(tag_version=tag_version)[0]
    # subject = "测试通过，可以升级"
    # message = "可以升级-{}-{}".format(deploytask.project.module_name, deploytask.tag_version)
    # addr = ["{}@zhexinit.com".format(handle_person)]
    # emailthread = EmailThread(subject, message, addr)
    # emailthread.start()
    # deploytask.is_test_pass = "yes"
    # deploytask.save()
    return HttpResponseRedirect(reverse("test_report_upload",kwargs={"module_name":module_name,"tag_version":tag_version}))


@csrf_exempt
@permission_required("deploy.backspace_deploytask", raise_exception=True)
def backspace(request, principal, project, tag_version):
    deploytask = DeployTask.objects.filter(project__module_name=project).filter(tag_version=tag_version)[0]
    subject = "测试失败，不能升级"
    message = "不能升级-{}-{}".format(deploytask.project.module_name, deploytask.tag_version)
    addr = ["{}@zhexinit.com".format(principal)]
    emailthread = EmailThread(subject, message, addr)
    emailthread.start()
    deploytask.is_backspace = "yes"
    deploytask.save()
    return HttpResponseRedirect(reverse("deploy_task_list"))


class DeployTaskDelete(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.delete_deploytask", raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        deploytask = DeployTask.objects.get(pk=id)
        test_report_key = "{}_{}_test_report".format(deploytask.project.module_name,deploytask.tag_version)
        receiving_report_key = "{}_{}_receiving_report".format(deploytask.project.module_name,deploytask.tag_version)
        redisconn = RedisConn(REDIS_HOST,REDIS_PORT)
        if deploytask.is_sql_exec == "no" and deploytask.need_test == "no":
            deploytask.delete()
        elif deploytask.is_sql_exec == "no" and deploytask.need_test == "yes" and deploytask.is_test_pass == "no":
            deploytask.delete()
        elif deploytask.is_sql_exec == "no" and deploytask.need_test == "yes" and deploytask.is_test_pass == "yes":
            redisconn.del_key(test_report_key)
            redisconn.del_key(receiving_report_key)
            shutil.rmtree(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,deploytask.project.module_name),deploytask.tag_version))
            deploytask.delete()
        elif deploytask.is_sql_exec == "yes" and deploytask.need_test == "no":
            shutil.rmtree(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH, deploytask.project.module_name), deploytask.tag_version))
            deploytask.delete()
        elif deploytask.is_sql_exec == "yes" and deploytask.need_test == "yes" and deploytask.is_test_pass == "no":
            shutil.rmtree(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,deploytask.project.module_name),deploytask.tag_version))
            deploytask.delete()
        elif deploytask.is_sql_exec == "yes" and deploytask.need_test == "yes" and deploytask.is_test_pass == "yes":
            redisconn.del_key(test_report_key)
            redisconn.del_key(receiving_report_key)
            shutil.rmtree(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,deploytask.project.module_name),deploytask.tag_version))
            deploytask.delete()
        else:
            deploytask.delete()
        return HttpResponsePermanentRedirect(reverse("deploy_task_list"))


class DeployTaskExamine(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_deploytask", raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        deploytask = DeployTask.objects.get(pk=id)
        module_name = deploytask.project.module_name
        tag_version = deploytask.tag_version
        zip_file = "{}-{}.zip".format(module_name, tag_version)
        redisconn = RedisConn(REDIS_HOST,REDIS_PORT)
        test_report_key = "{}_{}_test_report".format(module_name,tag_version)
        receiving_report_key = "{}_{}_receiving_report".format(module_name,tag_version)
        if deploytask.need_test == "yes" and deploytask.is_test_pass == "yes":
            test_report_json = redisconn.get_key_no_json(test_report_key)
            receiving_report_json = redisconn.get_key_no_json(receiving_report_key)
            test_report = json.loads(test_report_json.decode("utf-8")) if test_report_json is not None else None
            receiving_report = json.loads(receiving_report_json.decode("utf-8")) if receiving_report_json is not None else None
        else:
            test_report = None
            receiving_report = None
        if deploytask.is_sql_exec == "yes" and deploytask.need_test == "no":
            self.context = {"zip_file": zip_file, "deploytask": deploytask}
        elif deploytask.is_sql_exec == "yes" and deploytask.need_test == "yes" and deploytask.is_test_pass == "no":
            self.context = {"zip_file":zip_file,"deploytask":deploytask,"test_report":test_report,"receiving_report":receiving_report}
        elif deploytask.is_sql_exec == "yes" and deploytask.need_test == "yes" and deploytask.is_test_pass == "yes":
            self.context = {"zip_file":zip_file,"deploytask":deploytask,"test_report":test_report,"receiving_report":receiving_report}
        elif deploytask.is_sql_exec == "no" and deploytask.need_test == "yes" and deploytask.is_test_pass == "yes":
            self.context = {"deploytask":deploytask,"test_report":test_report,"receiving_report":receiving_report}
        elif deploytask.is_sql_exec == "no" and deploytask.need_test == "yes" and deploytask.is_test_pass == "no":
            self.context = {"deploytask": deploytask}
        else:
            self.context = {"deploytask": deploytask}
        return render(request, "deploy/deploytask_info.html", self.context)


def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for dir in dirs:
                filelist.append(os.path.join(root, dir))
            for name in files:
                filelist.append(os.path.join(root, name))
    with zipfile.ZipFile(zipfilename, "w") as zf:
        for tar in filelist:
            arcname = tar[len(dirname):]
            zf.write(tar, arcname)


@login_required
@csrf_exempt
def sql_file_download(request, module_name, tag_version):
    filename = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH, module_name), tag_version),
                            "{}-{}.zip".format(module_name, tag_version))
    file = open(filename, "rb")
    response = StreamingHttpResponse(file)
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = "attachment;filename={}-{}.zip".format(module_name, tag_version)
    return response

@login_required
@csrf_exempt
def test_report_download(request,module_name,tag_version,test_report_filename):
    filename = os.path.join(os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,module_name),tag_version),"test_report"),test_report_filename)
    file = open(filename,"rb")
    response = StreamingHttpResponse(file)
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = "attachment;filename={}".format(escape_uri_path(test_report_filename))
    return response

@login_required
@csrf_exempt
def receiving_report_download(request,module_name,tag_version,receiving_report_filename):
    filename = os.path.join(os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,module_name),tag_version),"receiving_report"),receiving_report_filename)
    file = open(filename,"rb")
    response = StreamingHttpResponse(file)
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = "attachment;filename={}".format(escape_uri_path(receiving_report_filename))
    return response

class TestReportUploadView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        test_report_form = TestReportUploadForm()
        self.context = {"test_report_form":test_report_form}
        return render(request,"deploy/test_report_upload.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        module_name = kwargs.get("module_name")
        tag_version = kwargs.get("tag_version")
        test_report_form = TestReportUploadForm(request.POST,request.FILES)
        if test_report_form.is_valid():
            test_report = request.FILES.getlist("test_report")
            receiving_report = request.FILES.getlist("receiving_report")
            redisconn = RedisConn(REDIS_HOST,REDIS_PORT)
            test_report_dir = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,module_name),tag_version),"test_report")
            receiving_report_dir = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,module_name),tag_version),"receiving_report")
            if not os.path.exists(test_report_dir):
                os.makedirs(test_report_dir)
            if not os.path.exists(receiving_report_dir):
                os.makedirs(receiving_report_dir)
            test_report_filename_list = []
            test_report_filename_dict = {}
            receiving_report_filename_list = []
            receiving_report_filename_dict = {}
            test_report_key = "{0}_{1}_test_report".format(module_name,tag_version)
            receiving_report_key = "{0}_{1}_receiving_report".format(module_name,tag_version)
            for tr in test_report:
                test_report_filename = os.path.join(test_report_dir,tr.name)
                test_report_filename_list.append(tr.name)
                handle_uploaded_file(test_report_filename,tr)
            test_report_filename_dict["test_report_file_list"] = test_report_filename_list
            redisconn.set_key(test_report_key,json.dumps(test_report_filename_dict))
            if len(receiving_report) > 0:
                for rr in receiving_report:
                    receiving_report_filename = os.path.join(receiving_report_dir,rr.name)
                    receiving_report_filename_list.append(rr.name)
                    handle_uploaded_file(receiving_report_filename,rr)
                receiving_report_filename_dict["receiving_report_file_list"] = receiving_report_filename_list
                redisconn.set_key(receiving_report_key,json.dumps(receiving_report_filename_dict))
            deploytask = DeployTask.objects.filter(project__module_name=module_name).filter(tag_version=tag_version)[0]
            deploytask.is_test_pass = "yes"
            deploytask.save()
            subject = "测试通过，可以升级"
            message = "{0}-{1}-可以升级".format(module_name,tag_version)
            addr = ["{}@zhexinit.com".format(deploytask.handle_person)]
            emailthread = EmailThread(subject,message,addr)
            emailthread.start()
            return HttpResponseRedirect(reverse("deploy_task_list"))
        else:
            self.context = {"test_report_form":test_report_form,"errors":test_report_form.errors}
            return render(request,"deploy/test_report_upload.html",self.context)


@login_required
@permission_required("deploy.upgrade_deploytask",raise_exception=True)
def upgrade_deploytask(request,id):
    deploytask = DeployTask.objects.get(pk=id)
    deploytask.is_upgrade = "yes"
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    deploytask.upgrade_time = dt
    deploytask.save()
    subject = "升级成功"
    message = "{}-{}已经升级成功，如有问题请及时联系运维".format(deploytask.project.module_name,deploytask.tag_version)
    addr = ["{}@zhexinit.com".format(deploytask.principal)]
    for ep in deploytask.email_person.split():
        addr.append("{}@zhexinit.com".format(ep))
    addr.append("{}@zhexinit.com".format(deploytask.handle_person))
    emailthread = EmailThread(subject,message,addr)
    emailthread.start()
    periodictask = PeriodicTask(
        name = "sendemail_to_dev_{}_{}".format(deploytask.project.module_name,deploytask.tag_version),
        task = "deploy.tasks.sendemail_to_dev",
        args = [int(id)],
        interval = IntervalSchedule.objects.get(pk=2)
    )
    periodictask.save()
    return HttpResponseRedirect(reverse("deploy_task_list"))

@login_required
def upgrade_success_deploytask(request,id):
    deploytask = DeployTask.objects.get(pk=id)
    deploytask.is_upgrade_success = "yes"
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    deploytask.upgrade_success_time = dt
    deploytask.save()
    periodictask = PeriodicTask.objects.get(name="sendemail_to_dev_{}_{}".format(deploytask.project.module_name,deploytask.tag_version))
    periodictask.enabled = 0
    periodictask.save()
    return HttpResponseRedirect(reverse("deploy_task_list"))

@login_required
def upgrade_failure_deploytask(request,id):
    deploytask = DeployTask.objects.get(pk=id)
    deploytask.is_upgrade_failure = "yes"
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    deploytask.upgrade_failure_time = dt
    deploytask.save()
    try:
        periodictask = PeriodicTask.objects.get(name="sendemail_partition_to_dev_{}_{}".format(deploytask.project.module_name,deploytask.tag_version))
        periodictask.enabled = 0
        periodictask.save()
    except PeriodicTask.DoesNotExist:
        periodictask_success = PeriodicTask.objects.get(name="sendemail_to_dev_{}_{}".format(deploytask.project.module_name,deploytask.tag_version))
        periodictask_success.enabled = 0
        periodictask_success.save()
    subject = "升级失败"
    message = "{}-{}升级失败".format(deploytask.project.module_name,deploytask.tag_version)
    addr = ["{}@zhexinit.com".format(deploytask.handle_person)]
    for ep in deploytask.email_person.split():
        addr.append("{}@zhexinit.com".format(ep))
    emailthreadd = EmailThread(subject,message,addr)
    emailthreadd.start()
    return HttpResponseRedirect(reverse("deploy_task_list"))

@login_required
@permission_required("deploy.upgrade_partition",raise_exception=True)
def upgrade_partition_deploytask(request,module_name,tag_version):
    deploytask = DeployTask.objects.filter(project__module_name=module_name).filter(tag_version=tag_version)[0]
    deploytask.is_upgrade_partition = "yes"
    deploytask.save()
    subject = "已升级一个节点"
    message = "{}-{}已升级一个节点，请及时验证".format(module_name,tag_version)
    addr = ["{}@zhexinit.com".format(deploytask.principal)]
    for ep in deploytask.email_person.split():
        addr.append("{}@zhexinit.com".format(ep))
    addr.append("{}@zhexinit.com".format(deploytask.handle_person))
    emailthread = EmailThread(subject,message,addr)
    emailthread.start()
    periodictask = PeriodicTask(
        name = "sendemail_partition_to_dev_{}_{}".format(module_name,tag_version),
        task = "deplpy.tasks.sendemail_partition_to_dev",
        args = [deploytask.id],
        interval = IntervalSchedule.objects.get(pk=2)
    )
    periodictask.save()
    return HttpResponseRedirect(reverse("deploy_task_list"))

@permission_required("deploy.upgrade_continue",raise_exception=True)
@login_required
def upgrade_continue_deploytask(request,module_name,tag_version):
    deploytask = DeployTask.objects.filter(project__module_name=module_name).filter(tag_version=tag_version)[0]
    deploytask.is_upgrade_continue = "yes"
    deploytask.save()
    subject = "继续升级"
    message = "{}-{}验证成功，可以继续升级".format(module_name,tag_version)
    addr = ["{}@zhexinit.com".format(deploytask.handle_person)]
    emailthread = EmailThread(subject,message,addr)
    emailthread.start()
    periodictask = PeriodicTask.objects.get(name="sendemail_partition_to_dev_{}_{}".format(module_name,tag_version))
    periodictask.enabled = 0
    periodictask.save()
    return HttpResponseRedirect(reverse("deploy_task_list"))


