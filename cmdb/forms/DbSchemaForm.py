from django import forms
from django.forms import TextInput,Textarea,Select
from cmdb.models.Database import Database

class DbSchemaSearchForm(forms.Form):
    search_schema = forms.CharField(
        widget = TextInput(attrs={"id":"search_schema","class":"form-control","placeholder":"请输入database名称"}),
        required=False
    )
    search_instance = forms.CharField(
        widget = Select(attrs={"id":"search_instance","class":"form-control"})
    )
    def __init__(self,*args,**kwargs):
        super(DbSchemaSearchForm,self).__init__(*args,**kwargs)
        instance_choice = list(Database.objects.all().values_list("id","instance"))
        instance_choice.insert(0,("","请选择"))
        self.fields["search_instance"].widget.choices = instance_choice

class DbSchemaAddForm(forms.Form):
    schema = forms.CharField(
        widget = TextInput(attrs={"id":"schema","class":"form-control","placeholder":"请输入database名称"})
    )
    url = forms.CharField(
        widget = TextInput(attrs={"id":"url","class":"form-control","placeholder":"请输入连接地址"})
    )
    port = forms.CharField(
        widget = TextInput(attrs={"id":"port","class":"form-control","placeholder":"请输入端口"})
    )
    user = forms.CharField(
        widget = TextInput(attrs={"id":"user","class":"form-control","placeholder":"请输入用户名"}),
        required=False
    )
    password = forms.CharField(
        widget = TextInput(attrs={"id":"password","class":"form-control","placeholder":"请输入密码"}),
        required=False
    )
    instance = forms.CharField(
        widget = Select(attrs={"id":"instance","class":"form-control"})
    )
    def __init__(self,*args,**kwargs):
        super(DbSchemaAddForm,self).__init__(*args,**kwargs)
        instance_choice = list(Database.objects.all().values_list("id","instance"))
        instance_choice.insert(0,("","请选择"))
        self.fields["instance"].widget.choices = instance_choice
