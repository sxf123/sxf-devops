from django import forms
from django.forms import TextInput,Select,MultipleChoiceField,SelectMultiple
from cmdb.models.Cluster import Cluster
from saltjob.get_host_list import get_host_list,get_mid_list
from cmdb.models.MiddleWare import MiddleWare
from cmdb.models.Host import usage_type
env_type = (
        ("","请选择"),
        ("develop","研发环境"),
        ("test","测试环境"),
        ("prepare","预发环境"),
        ("product","生产环境"),
        ("operation","运维环境")
    )
class HostSearchForm(forms.Form):
    hostname = forms.CharField(
        widget = TextInput(attrs={"id":"input_hostname","class":"form-control","placeholder":"主机名称"}),
        required=False
    )
    environment = forms.CharField(
        widget = Select(attrs={"id":"select_env","class":"form-control"},choices=env_type)
    )

class HostAddForm(forms.Form):
    host_name = forms.CharField(
        widget = TextInput(attrs={"id":"hostname","class":"form-control","placeholder":"主机名称"}),
    )
    kernel = forms.CharField(
        widget = TextInput(attrs={"id":"kernel","class":"form-control","placeholder":"内核"}),
    )
    osrelease = forms.CharField(
        widget = TextInput(attrs={"id":"osrelease","class":"form-control","placeholder":"操作系统版本"}),
    )
    os = forms.CharField(
        widget = TextInput(attrs={"id":"os","class":"form-control","placeholder":"操作系统"})
    )
    environment = forms.CharField(
        widget = Select(attrs={"id":"environment","class":"form-control"},choices=env_type)
    )
    cluster = forms.ModelMultipleChoiceField(
        widget = forms.SelectMultiple(attrs={"id":"cluster","class":"form-control select2"}),
        required = False,
        queryset = Cluster.objects.all()
    )
    host_usage = forms.CharField(
        widget = Select(attrs={"id":"host_usage","class":"form-control"},choices=usage_type)
    )
    midware = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={"id":"midware","class":"form-control select2"}),
        required=False,
    )
    def __init__(self,*args,**kwargs):
        super(HostAddForm,self).__init__(*args,**kwargs)
        # cluster_choice = list(Cluster.objects.all().values_list("id","cluster_name"))
        middleware_choice = list(MiddleWare.objects.all().values_list("mid_name","mid_name"))
        # self.fields["cluster"].choices = cluster_choice
        self.fields["midware"].choices = middleware_choice

class HostSelectForm(forms.Form):
    host_name = forms.CharField(
        widget = Select(attrs={"id":"select_host","class":"form-control select2"})
    )
    def __init__(self,*args,**kwargs):
        midware = kwargs.pop("midware",None)
        super(HostSelectForm,self).__init__(*args,**kwargs)
        host_list = list(get_host_list(midware))
        host_choice = []
        for i in range(0,len(host_list)):
            for h in get_mid_list(host_list[i])["middleware_list"]:
                if h["name"] == midware and h["installed"] == "false":
                    host_choice.append((host_list[i],host_list[i]))
        host_choice.insert(0,("","请选择"))
        self.fields["host_name"].widget.choices = host_choice