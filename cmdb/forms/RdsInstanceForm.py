from django.forms import Textarea,TextInput,Select
from django import forms

db_type_choice = (
    ("","请选择"),
    ("mysql","MySQL"),
    ("oracle","Oracle"),
    ("postgresql","PostgreSQL")
)

class RdsInstanceSearchForm(forms.Form):
    search_instance_name = forms.CharField(
        widget = TextInput(attrs = {"id":"search_instance_name","class":"form-control",})
    )
    search_db_type = forms.CharField(
        widget = Select(attrs = {"id":"search_db_type","class":"form-control"},choices = db_type_choice)
    )

class RdsInstanceAddForm(forms.Form):
    instance_name = forms.CharField(
        widget = TextInput(attrs = {"id":"instance_name","class":"form-control","placeholder":"请输入实例名称"})
    )
    instance_url = forms.CharField(
        widget = TextInput(attrs = {"id":"instance_url","class":"form-control","placeholder":"请输入实例地址"})
    )
    instance_port = forms.CharField(
        widget = TextInput(attrs = {"id":"instance_port","class":"form-control","placeholder":"请输入实例地址"})
    )
    db_type = forms.CharField(
        widget = Select(attrs = {"id":"db_type","class":"form-control"},choices = db_type_choice)
    )
    instance_desc = forms.CharField(
        widget = Textarea(attrs = {"id":"instance_desc","class":"form-control","placeholder":"请输入实例描述"})
    )
