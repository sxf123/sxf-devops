from django import forms
from django.forms import Textarea,TextInput,Select
from cmdb.models.RdsInstance import RdsInstance

class RdsSchemaSearchForm(forms.Form):
    search_schema_name = forms.CharField(
        widget = TextInput(attrs = {"id":"search_schema_name","class":"form-control","placeholder":"请输入数据库名称"})
    )
    search_rdsinstance = forms.CharField(
        widget = Select(attrs = {"id":"search_rdsinstance","class":"form-control"}),
        required=False
    )

    def __init__(self,*args,**kwargs):
        super(RdsSchemaSearchForm,self).__init__(*args,**kwargs)
        rdsinstance_list = list(RdsInstance.objects.all().values_list("id","instance_name"))
        rdsinstance_list.insert(0,("","请选择"))
        self.fields["search_rdsinstance"].widget.choices = rdsinstance_list

class RdsSchemaAddForm(forms.Form):
    schema_name = forms.CharField(
        widget = TextInput(attrs = {"id":"schema_name","class":"form-control","placeholder":"请输入数据库名称"})
    )
    rdsinstance = forms.CharField(
        widget = Select(attrs = {"id":"rdsinstance","class":"form-control"})
    )
    schema_desc = forms.CharField(
        widget = Textarea(attrs = {"id":"schema_desc","class":"form-control","placeholder":"请输入数据库描述"})
    )

    def __init__(self,*args,**kwargs):
        super(RdsSchemaAddForm,self).__init__(*args,**kwargs)
        rdsinstance_list = list(RdsInstance.objects.all().values_list("id","instance_name"))
        rdsinstance_list.insert(0,("","请选择"))
        self.fields["rdsinstance"].widget.choices = rdsinstance_list

