from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from deploy.forms import SqlUploadForm
from devops.settings import DEPLOY_UPLOAD_PATH
import os
from deploy.views.DeployTaskView import handle_uploaded_file
from deploy.models import SqlExecute
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import time
from django.contrib.auth.models import User
from deploy.forms import SqlExecuteSearchForm
from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
import shutil
from common.email import EmailThread

class SqlFile(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_sql",raise_exception=True))
    def get(self,request,*args,**kwargs):
        sqlexecute_search_form = SqlExecuteSearchForm()
        user = User.objects.get(username=request.user)
        if request.user.is_superuser:
            sqlexecute = SqlExecute.objects.all().order_by("-id")
        else:
            sqlexecute = SqlExecute.objects.filter(upload_person__username=request.user).order_by("-id")
        self.context = {"sqlexecute":sqlexecute,"sqlexecute_search_form":sqlexecute_search_form}
        return render(request,"deploy/sqlexecute_list.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_sql",raise_exception=True))
    def post(self,request,*args,**kwargs):
        sqlexecute_search_form = SqlExecuteSearchForm(request.POST)
        if sqlexecute_search_form.is_valid():
            upload_person = sqlexecute_search_form.cleaned_data.get("search_upload_person")
            return HttpResponseRedirect(reverse("sql_file_detail",kwargs={"upload_person":upload_person}))
        else:
            self.context = {"sqlexecute_search_form":sqlexecute_search_form,"errors":sqlexecute_search_form.errors}
            return render(request,"deploy/sqlexecute_list.html",self.context)

class SqlFileDetail(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.scan_sql",raise_exception=True))
    def get(self,request,*args,**kwargs):
        upload_person = kwargs.get("upload_person")
        sqlexecute = SqlExecute.objects.filter(upload_person__username=upload_person)
        self.context = {"sqlexecute":sqlexecute}
        return render(request,"deploy/sqlexecute_detail.html",self.context)

class SqlFileUpload(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.upload_sql",raise_exception=True))
    def get(self,request,*args,**kwargs):
        sql_upload_form = SqlUploadForm()
        self.context = {"sql_upload_form":sql_upload_form}
        return render(request,"deploy/sql_upload.html",self.context)
    @method_decorator(permission_required("deploy.upload_sql",raise_exception=True))
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        sql_upload_form = SqlUploadForm(request.POST)
        if sql_upload_form.is_valid():
            now = str(int(time.time()))
            user = User.objects.get(username=request.user)
            sqlupload_rdsinstance = sql_upload_form.cleaned_data.get("sqlupload_rdsinstance")
            for rds in sqlupload_rdsinstance:
                sqlupload_rdsschema = request.POST.getlist("sqlupload_{0}".format(rds))
                for schema in sqlupload_rdsschema:
                    sql_file = request.FILES.get("sqlupload_{0}".format(schema))
                    sqlexecute = SqlExecute(
                        rdsinstance = rds,
                        rdsschema = schema,
                        sqlfile = sql_file.name,
                        upload_person = user
                    )
                    sqlexecute.save()
                    sql_file_dir = os.path.join(os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"sql_file"),now),rds),schema)
                    sql_file_name = os.path.join(sql_file_dir,sql_file.name)
                    if not os.path.exists(sql_file_dir):
                        os.makedirs(sql_file_dir)
                    handle_uploaded_file(sql_file_name,sql_file)
            subject = "sql执行"
            message = "有SQL文件需要执行"
            addr = ['zhexin-ops@zhexinit.com']
            emailthread = EmailThread(subject,message,addr)
            emailthread.start()
            return HttpResponseRedirect(reverse("sql_file_list"))
        else:
            self.context = {"sql_upload_form":sql_upload_form,"errors":sql_upload_form.errors}
            return render(request,"deploy/sql_upload.html",self.context)

class SqlFileDelete(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("deploy.delete_sqlexecute",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        sqlexecute = SqlExecute.objects.get(pk=id)
        un_time = str(int(time.mktime(sqlexecute.upload_time.timetuple())))
        shutil.rmtree(os.path.join(os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"sql_file"),un_time),sqlexecute.rdsinstance),sqlexecute.rdsschema))
        sqlexecute.delete()
        return HttpResponseRedirect(reverse("sql_file_list"))
def sqlfile_download(request,id):
    sqlexecute = SqlExecute.objects.get(pk=id)
    un_time = str(int(time.mktime(sqlexecute.upload_time.timetuple())))
    sql_file_dir = os.path.join(os.path.join(os.path.join(os.path.join(DEPLOY_UPLOAD_PATH,"sql_file"),un_time),sqlexecute.rdsinstance),sqlexecute.rdsschema)
    sql_file = os.path.join(sql_file_dir, sqlexecute.sqlfile)
    file = open(sql_file,"rb")
    response = StreamingHttpResponse(file)
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = "attachment;filename={}".format(escape_uri_path(sqlexecute.sqlfile))
    return response

