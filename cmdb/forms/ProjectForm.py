from django import forms
from django.forms import TextInput,Select,Textarea
from django.contrib.auth.models import User


class ProjectSearchForm(forms.Form):
    project_search_name = forms.CharField(
        widget = TextInput(attrs={"id":"project_search_name","class":"form-control","placeholder":"请输入项目名称"})
    )
class ProjectAddForm(forms.Form):
    name = forms.CharField(
        widget = TextInput(attrs = {"id":"project_name","class":"form-control","placeholder":"请输入项目名称"})
    )
    real_name = forms.CharField(
        widget = TextInput(attrs = {"id":"project_real_name","class":"form-control","placeholder":"请输入项目汉字名称"})
    )
    description = forms.CharField(
        widget = Textarea(attrs={"id":"project_description","class":"form-control","placeholder":"请输入项目描述"})
    )
    dev_leading = forms.CharField(
        widget = Select(attrs={"id":"dev_leading","class":"form-control"})
    )
    test_leading = forms.CharField(
        widget = Select(attrs={"id":"test_leading","class":"form-control"})
    )
    proj_leading = forms.CharField(
        widget = Select(attrs={"id":"proj_leaging","class":"form-control"})
    )
    ops_leading = forms.CharField(
        widget = Select(attrs={"id":"ops_leaging","class":"form-control"})
    )
    def __init__(self,*args,**kwargs):
        super(ProjectAddForm,self).__init__(*args,**kwargs)
        dev_leading_choice = list(User.objects.all().values_list("id","username"))
        dev_leading_choice.insert(0,("","请选择"))
        self.fields["dev_leading"].widget.choices = dev_leading_choice
        test_leading_choice = list(User.objects.all().values_list("id","username"))
        test_leading_choice.insert(0,("","请选择"))
        self.fields["test_leading"].widget.choices = test_leading_choice
        proj_leading_choice = list(User.objects.all().values_list("id","username"))
        proj_leading_choice.insert(0,("","请选择"))
        self.fields["proj_leading"].widget.choices = proj_leading_choice
        ops_leading_choice = list(User.objects.all().values_list("id","username"))
        ops_leading_choice.insert(0,("","请选择"))
        self.fields["ops_leading"].widget.choices = ops_leading_choice


