from django import forms
from django.forms import TextInput,Select

class JenkinsSearchForm(forms.Form):
    search_node_name = forms.CharField(
        widget = TextInput(attrs = {"id":"search_node_name","class":"form-control","placeholder":"请输入节点名称"})
    )

class JenkinsAddNodeForm(forms.Form):
    name = forms.CharField(
        widget = TextInput(attrs={"id":"node_name","class":"form-control","placeholder":"请输入节点名称"})
    )
    port = forms.CharField(
        widget = TextInput(attrs={"id":"node_port","class":"form-control","placeholder":"请输入节点端口"})
    )
    user = forms.CharField(
        widget = TextInput(attrs={"id":"node_user","class":"form-control","placeholder":"请输入节点用户"})
    )
    credentialsId = forms.CharField(
        widget = TextInput(attrs={"id":"credentialsId","class":"form-control","placeholder":"请输入credentialsId"})
    )
    host = forms.GenericIPAddressField(
        widget = TextInput(attrs={"id":"node_host","class":"form-control","placeholder":"请输入节点主机ip"})
    )
    javaPath = forms.CharField(
        widget = TextInput(attrs = {"id":"node_javaPath","class":"form-control","placeholder":"请输入节点Java路径"})
    )