from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ldapmanage.forms import LdapAddForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from devops.settings import BASE_DIR
import os
import subprocess
from django.contrib.auth.decorators import permission_required
from common.redis_conn import RedisConn
from devops.settings import REDIS_HOST,REDIS_PORT


inputFile = os.path.join(os.path.join(BASE_DIR,"ldapmanage"),"uidNumber.txt")
ldap_add_script = os.path.join(os.path.join(BASE_DIR,"ldapmanage"),"ldap_add.sh")

def uidNumbers():
    redisconn = RedisConn(REDIS_HOST,REDIS_PORT)
    key = "uidNumber"
    uidNumber = redisconn.get_key(key)
    redisconn.set_key(key,int(uidNumber) + 1)
    return uidNumber


@login_required
@csrf_exempt
@permission_required("cmdb.add_ldap",raise_exception=True)
def ldap_add(request):
    if request.method == "GET":
        ldap_add_form = LdapAddForm()
        context = {"ldap_add_form":ldap_add_form}
        return render(request,"ldapmanage/ldap_add.html",context)
    elif request.method == "POST":
        ldap_add_form = LdapAddForm(request.POST)
        if ldap_add_form.is_valid():
            job_number = ldap_add_form.cleaned_data.get("job_number")
            name = ldap_add_form.cleaned_data.get("name")
            username = ldap_add_form.cleaned_data.get("username")
            email = ldap_add_form.cleaned_data.get("email")
            ou = ldap_add_form.cleaned_data.get("ou")
            first_department = ldap_add_form.cleaned_data.get("first_department")
            second_department = ldap_add_form.cleaned_data.get("second_department")
            uidNumber = uidNumbers()
            if second_department != "":
                result = shell(str(job_number),name,username,email,ou,first_department,second_department,str(uidNumber))
            else:
                result = shell(str(job_number),name,username,email,ou,first_department,"/",str(uidNumber))
            code = result.returncode
            stderr = (result.stderr).decode(encoding="gb2312",errors="strict")
            stdout = (result.stdout).decode(encoding="gb2312",errors="strict")
            context = {}
            return render(request,"ldapmanage/run.html",locals())
        else:
            context = {"ldap_add_form":ldap_add_form,"errors":ldap_add_form.errors}
            return render(request,"",context)
def shell(job_number,name,username,email,ou,first_department,second_department,uidNumber):
    cmd = "{} {} {} {} {} {} {} {}".format(job_number,name,username,email,ou,first_department,second_department,uidNumber)
    result = subprocess.run("/bin/bash {} {}".format(ldap_add_script,cmd),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    return result
