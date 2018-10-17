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
from django.contrib.auth.decorators import permission_required
import os
import time
import shutil
import subprocess
import zipfile
from django.http import JsonResponse
from common.redis_conn import RedisConn
from devops.settings import REDIS_PORT,REDIS_HOST
import json
import chardet

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
    @method_decorator(permission_required("deploy.execute_file",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        upload_file = UploadFile.objects.get(pk=id)
        upload_file_dict = model_to_dict(upload_file)
        file_execute_form = FileExecuteForm(upload_file_dict)
        self.context = {"file_execute_form":file_execute_form,"upload_file":upload_file}
        return render(request,"deploy/execute_file.html",self.context)
    def post(self,request,*args,**kwargs):
        id = request.POST["id"]
        upload_file = UploadFile.objects.get(pk=id)
        sql_billing_file = upload_file.sql_billing_file
        sql_pay_file = upload_file.sql_pay_file
        jar_file = upload_file.jar_file
        timestamp = time.mktime(upload_file.upload_time.timetuple())
        if sql_billing_file is not None:
            file_name_billing = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"billing"),str(int(timestamp))),sql_billing_file)
            unzip_file(file_name_billing,"/opt/billing/runfiles")
            billing_run_res = str(script_execute("/opt/runsql/billing_run.sh"),encoding="utf-8")
            redis_conn = RedisConn(REDIS_HOST,REDIS_PORT)
            key = "billing_{}".format(upload_file.id)
            val = {"id":str(upload_file.id),"timestamp":str(timestamp),"result":billing_run_res}
            redis_conn.set_key(key,json.dumps(val))
        if sql_pay_file is not None:
            file_name_pay = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"pay"),str(int(timestamp))),sql_pay_file)
            unzip_file(file_name_pay,"/opt/pay/runfiles")
            pay_run_res = str(script_execute("/opt/runsql/pay_run.sh"),encoding="utf-8")
            redis_conn = RedisConn(REDIS_HOST,REDIS_PORT)
            key = "pay_{}".format(upload_file.id)
            val = {"id":str(upload_file.id),"timestamp":str(timestamp),"result":pay_run_res}
            redis_conn.set_key(key,json.dumps(val))
        if jar_file is not None:
            file_name_jar = os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"jar"),str(int(timestamp))),jar_file)
            shutil.copy(file_name_jar,"/opt/transfile/jar/")
            jar_run_res = str(script_execute("/opt/transfile/pscpfile.sh"),encoding="utf-8")
            redis_conn = RedisConn(REDIS_HOST,REDIS_PORT)
            key = "jar_{}".format(upload_file.id)
            val = {"id":str(upload_file.id),"timestamp":str(timestamp),"result":jar_run_res}
            redis_conn.set_key(key,json.dumps(val))
        self.context = {"id":id,"message":"execute success"}
        return JsonResponse(self.context)
class ExecuteResView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        upload_file = UploadFile.objects.get(pk=id)
        redis_conn = RedisConn(REDIS_HOST,REDIS_PORT)
        if upload_file.sql_billing_file is not None:
            key = "billing_{}".format(id)
            billing_run_res = redis_conn.get_key(key)["result"].split("\n")
        else:
            billing_run_res = None
        if upload_file.sql_pay_file is not None:
            key = "pay_{}".format(id)
            pay_run_res = redis_conn.get_key(key)["result"].split("\n")
        else:
            pay_run_res = None
        if upload_file.jar_file is not None:
            key = "jar_{}".format(id)
            jar_run_res = redis_conn.get_key(key)["result"].split("\n")
        else:
            jar_run_res = None
        self.context = {"upload_file":upload_file,"billing_run_res":billing_run_res,"pay_run_res":pay_run_res,"jar_run_res":jar_run_res}
        return render(request,"deploy/file_run_res.html",self.context)

class FileDelete(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        upload_file = UploadFile.objects.get(pk=id)
        upload_file.delete()
        timestamp = str(int(time.mktime(upload_file.upload_time.timetuple())))
        redis_conn = RedisConn(REDIS_HOST,REDIS_PORT)
        if upload_file.sql_billing_file != None:
            billing_dir = os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"billing"),timestamp)
            shutil.rmtree(billing_dir)
            key = "billing_{}".format(upload_file.id)
            redis_conn.del_key(key)
        if upload_file.sql_pay_file != None:
            pay_dir = os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"pay"),timestamp)
            shutil.rmtree(pay_dir)
            key = "pay_{}".format(id)
            redis_conn.del_key(key)
        if upload_file.jar_file != None:
            jar_dir = os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"jar"),timestamp)
            shutil.rmtree(jar_dir)
            key = "jar_{}".format(id)
            redis_conn.del_key(key)
        return HttpResponseRedirect(reverse("execute_file_list"))

def script_execute(script_name):
    try:
        res = subprocess.check_output(["/bin/bash",script_name],stderr = subprocess.STDOUT,shell = False)
        return res
    except subprocess.CalledProcessError as exc:
        return exc.output

def unzip_file(zip_file,path):
    zip = zipfile.ZipFile(zip_file,"r")
    for z in zip.namelist():
        sencoding = chardet.detect(zip.read(z))
        data = zip.read(z).decode(sencoding["encoding"])
        with open("{}/{}".format(path,z),"w") as f:
            f.write(data)
            f.close()
    zip.close()
    # try:
    #     subprocess.check_call("unzip {} -d {}".format(zip_file,path),stderr=subprocess.STDOUT,shell=True)
    # except subprocess.CalledProcessError as e:
    #     return e.output
    #


