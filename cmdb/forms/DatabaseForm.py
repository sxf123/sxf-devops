from django import forms
from django.forms import TextInput,Select
from cmdb.models.Cluster import Cluster
from cmdb.models.Host import Host

db_type = (
    ("","请选择"),
    ("mysql","MySQL"),
    ("oracle","Oracle"),
    ("postgresql","Postgresql")
)
class DatabaseSearchForm(forms.Form):
    search_schema = forms.CharField(
        widget = TextInput(attrs={"id":"search_schema","class":"form-control","placeholder":"请输入实例名称"}),
        required=False
    )
    search_db_type = forms.CharField(
        widget = Select(attrs={"id":"search_db_type","class":"form-control"},choices=db_type)
    )

class DatabaseAddForm(forms.Form):
    instance = forms.CharField(
        widget = TextInput(attrs={"id":"instance","class":"form-control","placeholder":"请输入实例名称"})
    )
    db_type = forms.CharField(
        widget = Select(attrs={"id":"db_type","class":"form-control"},choices=db_type)
    )
    cluster = forms.CharField(
        widget = Select(attrs={"id":"cluster","class":"form-control"}),required=False
    )
    host = forms.CharField(
        widget = Select(attrs={"id":"host","class":"form-control"}),
        required=False
    )
    def __init__(self,*args,**kwargs):
        super(DatabaseAddForm,self).__init__(*args,**kwargs)
        cluster_choices = list(Cluster.objects.all().values_list("id","cluster_name"))
        cluster_choices.insert(0,("","请选择"))
        host_choices = list(Host.objects.all().values_list("id","host_name"))
        host_choices.insert(0,("","请选择"))
        self.fields["cluster"].widget.choices = cluster_choices
        self.fields["host"].widget.choices = host_choices