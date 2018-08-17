from django import forms
from django.forms import TextInput,Select

service_type = (
    ("","请选择"),
    ("jc-provider","dubbo服务"),
    ("jc-consumer","接口服务")
)

class MavenProjSearchForm(forms.Form):
    search_artifactId = forms.CharField(
        widget = TextInput(attrs={"id":"search_artifact","class":"form-control","placeholder":"请输入artifactId"})
    )
    search_service_type = forms.CharField(
        widget = Select(attrs={"id":"search_service_type","class":"form-control"},choices=service_type)
    )

class MavenProjAddForm(forms.Form):
    groupId = forms.CharField(
        widget = TextInput(attrs={"id":"groupId","class":"form-control","placeholder":"请输入groupId"})
    )
    artifactId = forms.CharField(
        widget = TextInput(attrs={"id":"artifactId","class":"form-control","placeholder":"请输入artifatId"})
    )
    service_type = forms.CharField(
        widget = Select(attrs={"id":"service_type","class":"form-control"},choices=service_type)
    )