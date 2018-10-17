from django.forms import Textarea,TextInput,SelectMultiple,Select
from django import forms
from zabbix.zabbix_api import get_template,get_groupname,login
from devops.settings import ZABBIX_URL,ZABBIX_URL_VPC,ZABBIX_USER,ZABBIX_PASSWORD

zapi = login(ZABBIX_URL,ZABBIX_USER,ZABBIX_PASSWORD)
zapivpc = login(ZABBIX_URL_VPC,ZABBIX_USER,ZABBIX_PASSWORD)

class EcsHostSearchForm(forms.Form):
    search_instance_id = forms.CharField(
        widget = TextInput(attrs = {"id":"search_instance_id","class":"form-control","placeholder":"请输入实例ID"})
    )

network_type_choice = (
    ("","请选择"),
    ("经典网络","经典网络"),
    ("专有网络","专有网络"),
)

class EcsHostAddForm(forms.Form):
    instance_id = forms.CharField(
        widget = TextInput(attrs = {"id":"instance_id","class":"form-control","placeholder":"请输入实例ID"})
    )
    desc = forms.CharField(
        widget = Textarea(attrs = {"id":"desc","class":"form-control","placeholder":"请输入主机描述"})
    )
    local_ip = forms.GenericIPAddressField(
        widget = TextInput(attrs = {"id":"local_ip","class":"form-control","placeholder":"请输入内网IP"})
    )
    internet_ip = forms.GenericIPAddressField(
        widget = TextInput(attrs = {"id":"internet_ip","class":"form-control","placeholder":"请输入外网IP"}),
        required = False
    )
    elastic_ip = forms.GenericIPAddressField(
        widget = TextInput(attrs = {"id":"elastic_ip","class":"form-control","placeholder":"请输入弹性IP"}),
        required = False
    )
    network_type = forms.CharField(
        widget = Select(attrs = {"id":"network_type","class":"form-control"},choices=network_type_choice)
    )
    minion_id = forms.CharField(
        widget = TextInput(attrs = {"id":"minion_id","class":"form-control","placeholder":"请输入minion_id"})
    )

class ZabbixAddForm(forms.Form):
    visible_name = forms.CharField(
        widget = TextInput(attrs = {"id":"visible_name","class":"form-control","placeholder":"请输入描述名称"})
    )
    hostname = forms.CharField(
        widget = TextInput(attrs = {"id":"hostname","class":"form-control","placeholder":"请输入主机名"})
    )
    ip = forms.CharField(
        widget = TextInput(attrs = {"id":"ip","class":"form-control","placeholder":"请输入主机IP"})
    )
    vpc = forms.CharField(
        widget = Select(attrs = {"id":"vpc","class":"form-control"},choices = (("","请选择"),("yes","专有网络"),("no","经典网络")))
    )
    templatename = forms.CharField(
        widget = Select(attrs = {"id":"templatename","class":"form-control select2"})
    )
    groupname = forms.CharField(
        widget = Select(attrs = {"id":"groupname","class":"form-control select2"})
    )
    def __init__(self,*args,**kwargs):
        network_type = kwargs.pop("network_type",None)
        super(ZabbixAddForm,self).__init__(*args,**kwargs)
        if network_type == "经典网络":
            template_list_choices = get_template(zapi)
            groupname_list_choices = get_groupname(zapi)
        elif network_type == "专有网络":
            template_list_choices = get_template(zapivpc)
            groupname_list_choices = get_template(zapivpc)
        self.fields["templatename"].widget.choices = template_list_choices
        self.fields["groupname"].widget.choices = groupname_list_choices