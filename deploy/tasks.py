from __future__ import absolute_import
from celery import task
from celery import shared_task
from common.email import sendmail
from deploy.models import DeployTask

@task
def add(x,y):
    print("%d + %d = %d" %(x,y,x+y))
    return x+y

@shared_task
def mul(x,y):
    print("%d * %d = %d" %(x,y,x*y))
    return x * y

@task
def sendemail_to_dev(id):
    subject = "请确认升级是否成功"
    deploy = DeployTask.objects.get(pk=id)
    module_name = deploy.project.module_name
    tag_version = deploy.tag_version
    message = "{}-{}已升级,请及时验证".format(module_name,tag_version)
    addr = ["{}@zhexinit.com".format(deploy.principal)]
    sendmail(subject,message,addr)
@task
def sendemail_partition_to_dev(id):
    subject = "部分节点已升级，请确认是否升级成功"
    deploy = DeployTask.objects.get(pk=id)
    module_name = deploy.project.module_name
    tag_version = deploy.tag_version
    message = "{}-{}已升级一个节点，请及时验证".format(module_name,tag_version)
    addr = ["{}@zhexinit.com".format(deploy.principal)]
    sendmail(subject,message,addr)

