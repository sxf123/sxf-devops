from django import forms
from django.forms import TextInput,Select,Textarea

mid_type = (
    ("","请选择"),
    ("app_mid","应用中间件"),
    ("info_mid","消息中间件"),
    ("buf_mid","缓存中间件"),
    ("reb_mid","负载均衡中间件"),
    ("dis_mid","分布式中间件")
)

class MiddlewareAddForm(forms.Form):
    mid_name = forms.CharField(
        widget = TextInput(attrs={"id":"mid_name","class":"form-control","placeholder":"请输入中间件名称"})
    )
    mid_type = forms.CharField(
        widget = Select(attrs={"id":"mid_type","class":"form-control"},choices=mid_type)
    )
    mid_description = forms.CharField(
        widget = Textarea(attrs={"id":"mid_description","class":"form-control"}),
        required=False
    )
    mid_version = forms.CharField(
        widget = TextInput(attrs={"id":"mid_version","class":"form-control","placeholder":"请输入中间件版本"})
    )

class MiddlewareSearchForm(forms.Form):
    mid_search_name = forms.CharField(
        widget = TextInput(attrs={"id":"mid_search_name","class":"form-control","placeholder":"请输入中间件名称"})
    )
    mid_search_type = forms.CharField(
        widget = Select(attrs={"id":"mid_search_type","class":"form-control"},choices=mid_type)
    )