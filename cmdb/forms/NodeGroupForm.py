from django import forms
from django.forms import TextInput,Select,Textarea
from cmdb.models.Host import Host

class NodeGroupSearchForm(forms.Form):
    search_nodegroup = forms.CharField(
        widget = TextInput(attrs={"id":"nodegroup","class":"form-control","placeholder":"请输入主机组名称"})
    )
    search_host = forms.CharField(
        widget = Select(attrs={"id":"host_name","class":"form-control"})
    )

    def __init__(self,*args,**kwargs):
        super(NodeGroupSearchForm,self).__init__(*args,**kwargs)
        host_choice = list(Host.objects.all().values_list("id","host_name"))
        host_choice.insert(0,("","请选择"))
        self.fields["search_host"].widget.choices = host_choice

class NodeGroupAddForm(forms.Form):
    nodegroup = forms.CharField(
        widget = TextInput(attrs={"id":"nodegroup","class":"form-control","placeholder":"请输入主机组名称"})
    )
    nodegroup_desc = forms.CharField(
        widget = Textarea(attrs={"id":"nodegroup_desc","class":"form-control","placeholder":"请输入主机组描述"})
    )