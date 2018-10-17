from django import forms
from django.forms import TextInput,Select
from cmdb.models.EcsHost import EcsHost
from cmdb.models.ProjectModule import ProjectModule

class ProcessSearchForm(forms.Form):
    search_process_name = forms.CharField(
        widget = TextInput(attrs = {"id":"search_process_name","class":"form-control","placeholder":"请输入进程名称"})
    )
    search_ecshost = forms.CharField(
        widget = Select(attrs = {"id":"search_ecshost","class":"form-control select2"})
    )
    def __init__(self,*args,**kwargs):
        super(ProcessSearchForm,self).__init__(*args,**kwargs)
        ecshost_choices = list(EcsHost.objects.all().values_list("instance_id","minion_id"))
        ecshost_choices.insert(0,("","ECS主机"))
        self.fields["search_ecshost"].widget.choices = ecshost_choices

class ProcessAddForm(forms.Form):
    process_name = forms.CharField(
        widget = TextInput(attrs = {"id":"process_name","class":"form-control","placeholder":"请输入进程名称"})
    )
    process_homepath = forms.CharField(
        widget = TextInput(attrs = {"id":"process_homepath","class":"form-control","placeholder":"请输入进程home目录"})
    )
    process_id = forms.CharField(
        widget = TextInput(attrs = {"id":"process_id","class":"form-control","placeholder":"请输入进程ID"})
    )
    process_port = forms.CharField(
        widget = TextInput(attrs = {"id":"process_port","class":"form-control","placeholder":"请输入进程端口"})
    )
    process_log = forms.CharField(
        widget = TextInput(attrs = {"id":"process_log","class":"form-control","placeholder":"请输入进程启动日志"})
    )
    projectmodule = forms.CharField(
        widget = Select(attrs = {"id":"projectmodule","class":"form-control select2"})
    )
    ecshost = forms.CharField(
        widget = Select(attrs = {"id":"ecshost","class":"form-control select2"})
    )
    def __init__(self,*args,**kwargs):
        super(ProcessAddForm,self).__init__(*args,**kwargs)
        projectmodule_choices = list(ProjectModule.objects.all().values_list("module_name","module_name"))
        projectmodule_choices.insert(0,("","模块"))
        ecshost_choices = list(EcsHost.objects.all().values_list("instance_id","minion_id"))
        ecshost_choices.insert(0,("","ECS主机"))
        self.fields["projectmodule"].widget.choices = projectmodule_choices
        self.fields["ecshost"].widget.choices = ecshost_choices