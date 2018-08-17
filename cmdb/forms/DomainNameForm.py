from django import forms
from django.forms import TextInput,Select
from cmdb.forms.HostForm import env_type
from cmdb.models.ProjectModule import ProjectModule
from cmdb.models.IpPool import IpPool

domainname_type = (
    ("","请选择"),
    ("A","A"),
    ("CNAME","CNAME")
)


class DomainNameSearchForm(forms.Form):
    search_dns = forms.CharField(
        widget = TextInput(attrs={"id":"search_dns","class":"form-control","placeholder":"请输入dns域名"}),
        required=False
    )
    search_ip_address = forms.CharField(
        widget = Select(attrs={"id":"search_ip_address","class":"select2 form-control"},choices=env_type)
    )
    def __init__(self,*args,**kwargs):
        super(DomainNameSearchForm,self).__init__(*args,**kwargs)
        ip_choice = list(IpPool.objects.all().values_list("id","ip_address"))
        ip_choice.insert(0,("","请选择"))
        self.fields["search_ip_address"].widget.choices = ip_choice


class DomainNameAddForm(forms.Form):
    dns = forms.CharField(
        widget = TextInput(attrs={"id":"dns","class":"form-control","placeholder":"请输入dns域名"}),
    )
    domain_type = forms.CharField(
        widget = Select(attrs={"id":"domain_type","class":"form-control"},choices = domainname_type)
    )
    ip = forms.CharField(
        widget = Select(attrs={"id":"ip","class":"form-control select2"})
    )
    project_module = forms.CharField(
        widget = Select(attrs={"id":"project_module","class":"form-control"}),
        required=False
    )
    project_module_url = forms.CharField(
        widget = TextInput(attrs={"id":"project_module_url","class":"form-control","placeholder":"请输入项目模块访问地址"}),
        required=False
    )
    environment = forms.CharField(
        widget = Select(attrs={"id":"environment","class":"form-control"},choices=env_type),
        required=False
    )

    def __init__(self,*args,**kwargs):
        super(DomainNameAddForm,self).__init__(*args,**kwargs)
        projectmodule_choice = list(ProjectModule.objects.all().values_list("id","module_name"))
        projectmodule_choice.insert(0,("","请选择"))
        self.fields["project_module"].widget.choices = projectmodule_choice
        ip_choices = list(IpPool.objects.all().values_list("id","ip_address"))
        ip_choices.insert(0,("","请选择"))
        self.fields["ip"].widget.choices = ip_choices
