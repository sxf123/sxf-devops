from django import forms
from django.forms import TextInput,Select
from cmdb.models.Host import Host

ip_type = (
    ("","请选择"),
    ("local","内网IP"),
    ("internet","外网IP"),
    ("virtual","虚IP")
)

class IpSearchForm(forms.Form):
    search_ip_address = forms.CharField(
        widget = TextInput(attrs={"id":"search_ip_address","class":"form-control","placeholder":"请输入IP地址"}),
        required=False
    )

    search_ip_type = forms.CharField(
        widget = Select(attrs={"id":"search_ip_type","class":"form-control","placeholder":"请输入IP类型"},choices=ip_type)
    )

class IpAddForm(forms.Form):
    ip_address = forms.CharField(
        widget = TextInput(attrs={"id":"ip_address","class":"form-control","placeholder":"请输入IP地址"})
    )
    ip_type = forms.CharField(
        widget = Select(attrs={"id":"ip_type","class":"form-control"},choices=ip_type)
    )
    gateway = forms.CharField(
        widget = TextInput(attrs={"id":"gateway","class":"form-control","placeholder":"请输入网关"}),
        required = False
    )
    ip_segment = forms.CharField(
        widget = TextInput(attrs={"id":"ip_segment","class":"form-control","placeholder":"请输入所属网段"}),
        required = False
    )
    host = forms.CharField(
        widget = Select(attrs={"id":"host","class":"form-control"}),
        required = False
    )
    def __init__(self,*args,**kwargs):
        super(IpAddForm,self).__init__(*args,**kwargs)
        host_choice = list(Host.objects.all().values_list("id","host_name"))
        host_choice.insert(0,("","请选择"))
        self.fields["host"].widget.choices = host_choice

