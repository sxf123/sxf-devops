from django import forms
from django.forms import TextInput,Select,Textarea
from cmdb.forms.HostForm import env_type

cluster_type = (
    ("","请选择"),
    ("app","应用系统集群"),
    ("db","数据库集群"),
    ("middleware","中间件集群")
)

class ClusterSearchForm(forms.Form):
    search_cluster_name = forms.CharField(
        widget = TextInput(attrs={"id":"search_cluster_name","class":"form-control","placeholder":"请输入集群名称"}),
        required=False
    )
    search_cluster_type = forms.CharField(
        widget = Select(attrs={"id":"search_cluster_type","class":"form-control"},choices=cluster_type)
    )

class ClusterAddForm(forms.Form):
    cluster_name = forms.CharField(
        widget = TextInput(attrs={"id":"cluster_name","class":"form-control","placeholder":"请输入集群名称"})
    )
    cluster_type = forms.CharField(
        widget = Select(attrs={"id":"cluster_type","class":"form-control"},choices=cluster_type)
    )
    cluster_desc = forms.CharField(
        widget = Textarea(attrs={"id":"cluster_desc","class":"form-control"}),
        required=False
    )
    environment = forms.CharField(
        widget = Select(attrs={"id":"environment","class":"form-control"},choices=env_type)
    )