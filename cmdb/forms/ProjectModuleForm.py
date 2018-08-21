from django import forms
from django.forms import TextInput,Select
from cmdb.models.Project import Project
from cmdb.models.Database import Database
from cmdb.models.Cluster import Cluster

service_type = (
    ("","请选择"),
    ("dubbo","dubbo服务"),
    ("admin","b端接口"),
    ("gateway","c端接口"),
    ("web","前端")
)

class ProjectModuleSearchForm(forms.Form):
    search_module_name = forms.CharField(
        widget = forms.TextInput(attrs={"id":"search_module_name","class":"form-control","placeholder":"请输入模块名称"}),
        required=False
    )
    search_proj_name = forms.CharField(
        widget = forms.Select(attrs={"id":"search_proj_name","class":"form-control"})
    )
    def __init__(self,*args,**kwargs):
        super(ProjectModuleSearchForm,self).__init__(*args,**kwargs)
        project_choice = list(Project.objects.all().values_list("id","real_name"))
        project_choice.insert(0,("","请选择"))
        self.fields["search_proj_name"].widget.choices = project_choice

class ProjectModuleAddForm(forms.Form):
    module_name = forms.CharField(
        widget = forms.TextInput(attrs={"id":"module_name","class":"form-control","placeholder":"请输入模块名称"})
    )
    module_desc = forms.CharField(
        widget = forms.TextInput(attrs={"id":"module_desc","class":"form-control","placeholder":"请输入模块描述"}),
        required=False
    )
    service_type = forms.CharField(
        widget = forms.Select(attrs={"id":"module_service_type","class":"form-control"},choices=service_type)
    )
    git_url = forms.CharField(
        widget = forms.TextInput(attrs={"id":"module_git_url","class":"form-control","placeholder":"请输入git地址"}),
        required = False
    )
    project = forms.CharField(
        widget = forms.Select(attrs={"id":"module_project","class":"form-control"}),
        required = False
    )
    cluster = forms.ModelMultipleChoiceField(
        widget = forms.SelectMultiple(attrs={"id":"module_cluster","class":"form-control select2"}),
        required = False,
        queryset = Cluster.objects.all()
    )
    def __init__(self,*args,**kwargs):
        super(ProjectModuleAddForm,self).__init__(*args,**kwargs)
        module_project_choice = list(Project.objects.all().values_list("id","name"))
        module_project_choice.insert(0,("","请选择"))
        # module_cluster_choices = list(Cluster.objects.all().values_list("id","cluster_name"))
        self.fields["project"].widget.choices = module_project_choice
        # self.fields["cluster"].choices = module_cluster_choices

