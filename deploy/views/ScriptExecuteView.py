from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from deploy.models import UploadFile
from deploy.forms import FileListForm
from django.contrib.auth.models import User
from deploy.forms import FileExecuteForm
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from devops.settings import DEPLOY_UPLOAD_PATH
import os
import time
import shutil
import subprocess
from unrar import rarfile


class FileListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*ars,**kwargs):
        if request.user.is_superuser:
            upload_file_list = UploadFile.objects.all()
        else:
            upload_file_list = UploadFile.objects.filter(user__username=request.user)
        file_list_form = FileListForm()
        self.context = {"file_list_form":file_list_form,"upload_file_list":upload_file_list}
        return render(request,"deploy/upload_file_list.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        file_list_form = FileListForm(request.POST)
        if file_list_form.is_valid():
            upload_time = file_list_form.cleaned_data.get("upload_time")
            user = file_list_form.cleaned_data.get("user")
            if request.user.is_superuser:
                if user == "":
                    upload_file_list = UploadFile.objects.filter(upload_time__contains=upload_time)
                    self.context = {"file_list_form":file_list_form,"upload_file_list":upload_file_list}
                else:
                    upload_file_list = UploadFile.objects.filter(upload_time__contains=upload_time).filter(user=User.objects.get(pk=user))
                    self.context = {"file_list_form":file_list_form,"upload_file_list":upload_file_list}
            else:
                upload_file_list = UploadFile.objects.filter(upload_time__contains=upload_time).filter(user=User.objects.get(username=request.user))
                self.context = {"file_list_form":file_list_form,"upload_file_list":upload_file_list}
            return render(request,"deploy/upload_file_list.html",self.context)
        else:
            self.context = {"file_list_form":file_list_form,"errors":file_list_form.errors}
            return render(request,"deploy/upload_file_list.html",self.context)

class FileExecuteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        upload_file = UploadFile.objects.get(pk=id)
        upload_file_dict = model_to_dict(upload_file)
        file_execute_form = FileExecuteForm(upload_file_dict)
        self.context = {"file_execute_form":file_execute_form}
        return render(request,"deploy/execute_file.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        upload_file = UploadFile.objects.get(pk=id)
        sql_billing_file = upload_file.sql_billing_file
        sql_pay_file = upload_file.sql_pay_file
        jar_file = upload_file.jar_file
        timestamp = time.mktime(upload_file.upload_time.timetuple())
        if sql_billing_file is not None:
            file_name_billing = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"billing"),str(int(timestamp))),sql_billing_file)
            rar_billing_file = rarfile.RarFile(file_name_billing)
            rar_billing_file.extractall("/opt/billing/runfiles")
            billing_run_res = script_execute("/opt/runsql/billing_run.sh")
            # log_file_billing = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"billing"),str(int(timestamp))),"billing_run.log")
            # with open(log_file_billing,"w") as f:
            #     f.write(billing_run_res)
            #     f.close()
        else:
            billing_run_res = None
        if sql_pay_file is not None:
            file_name_pay = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"pay"),str(int(timestamp))),sql_pay_file)
            rar_pay_file = rarfile.RarFile(file_name_pay)
            rar_pay_file.extractall("/opt/pay/runfiles")
            pay_run_res = script_execute("/opt/runsql/pay_run.sh")
            # log_file_pay = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"pay"),str(int(timestamp))),"pay_run.log")
            # with open(log_file_pay,"w") as f:
            #     f.write(pay_run_res)
            #     f.close()
        else:
            pay_run_res = None
        if jar_file is not None:
            file_name_jar = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"jar"),str(int(timestamp))),jar_file)
            shutil.copyfile(file_name_jar,"/opt/transfile/jar/{}".format(file_name_jar))
            jar_run_res = script_execute("/opt/transfile/pscpfile.sh")
            # log_file_jar = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"jar"),str(int(timestamp))),"jar_run.log")
            # with open(log_file_jar,"w") as f:
            #     f.write(jar_run_res)
            #     f.close()
        else:
            jar_run_res = None
        self.context = {"billing_run_res":billing_run_res,"pay_run_res":pay_run_res,"jar_run_res":jar_run_res}
        return render(request,"deploy/file_run_res.html",self.context)

class FileDelete(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        upload_file = UploadFile.objects.get(pk=id)
        upload_file.delete()
        timestamp = str(int(time.mktime(upload_file.upload_time.timetuple())))
        if upload_file.sql_billing_file != None:
            billing_dir = os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"billing"),timestamp)
            shutil.rmtree(billing_dir)
        if upload_file.sql_pay_file != None:
            pay_dir = os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"pay"),timestamp)
            shutil.rmtree(pay_dir)
        if upload_file.jar_file != None:
            jar_dir = os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"jar"),timestamp)
            shutil.rmtree(jar_dir)
        return HttpResponseRedirect(reverse("execute_file_list"))

def script_execute(script_name):
    try:
        res = subprocess.check_output(["/bin/bash",script_name],stdout = subprocess.STDOUT,shell = False)
        return res
    except subprocess.CalledProcessError as exc:
        return exc.output


