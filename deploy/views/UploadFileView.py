from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from deploy.forms import UploadFileForm
from devops.settings import DEPLOY_UPLOAD_PATH
from django.core.urlresolvers import reverse
import os
from deploy.models import UploadFile
from django.contrib.auth.models import User
import time
import uuid
from common.upload_file import UploadFileThread


class UploadFileView(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        token = str(uuid.uuid4())
        request.session["postToken"] = token
        upload_file_form = UploadFileForm()
        self.context = {"upload_file_form": upload_file_form, "postToken": token}
        return render(request, "deploy/upload_file.html", self.context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            sql_file_billing = upload_file_form.cleaned_data.get("sql_file_billing")
            sql_file_pay = upload_file_form.cleaned_data.get("sql_file_pay")
            jar_file = upload_file_form.cleaned_data.get("jar_file")
            upload_file = UploadFile(
                sql_billing_file=sql_file_billing.name if sql_file_billing is not None else None,
                sql_pay_file=sql_file_pay.name if sql_file_pay is not None else None,
                jar_file=jar_file.name if jar_file is not None else None,
                user=User.objects.get(username=request.user)
            )
            upload_file.save()
            timestamp = time.mktime(upload_file.upload_time.timetuple())
            if sql_file_billing is not None:
                billing_dir_name = os.path.join(os.path.join(DEPLOY_UPLOAD_PATH, "billing"), str(int(timestamp)))
                os.mkdir(billing_dir_name)
                file_name_billing = os.path.join(billing_dir_name, sql_file_billing.name)
                handle_uploaded_file(file_name_billing, sql_file_billing)
            if sql_file_pay is not None:
                pay_dir_name = os.path.join(os.path.join(DEPLOY_UPLOAD_PATH, "pay"), str(int(timestamp)))
                os.mkdir(pay_dir_name)
                file_name_pay = os.path.join(pay_dir_name, sql_file_pay.name)
                handle_uploaded_file(file_name_pay, sql_file_pay)
            if jar_file is not None:
                jar_dir_name = os.path.join(os.path.join(DEPLOY_UPLOAD_PATH, "jar"), str(int(timestamp)))
                os.mkdir(jar_dir_name)
                file_name_jar = os.path.join(jar_dir_name, jar_file.name)
                handle_uploaded_file(file_name_jar, jar_file)
            return HttpResponsePermanentRedirect(reverse("execute_file_list"))
        else:
            self.context = {"deploy_form": upload_file_form, "errors": upload_file_form.errors}
            return render(request, "deploy/upload_file.html", self.context)


def handle_uploaded_file(filename, f):
    with open(filename, "wb") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
