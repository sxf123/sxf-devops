from django.forms import TextInput,SelectMultiple,Select,EmailInput,PasswordInput
from django import forms
from django.contrib.auth.models import Group,Permission

is_choice = (
    ("","请选择"),
    (True,"是"),
    (False,"否")
)

class UserSearchForm(forms.Form):
    search_username = forms.CharField(
        widget = TextInput(attrs = {"id":"search_username","class":"form-control","placeholder":"请输入用户名"}),
        required=False
    )
    search_group = forms.CharField(
        widget = Select(attrs = {"id":"search_group","class":"form-control"}),
        required=False
    )

    def __init__(self,*args,**kwargs):
        super(UserSearchForm,self).__init__(*args,**kwargs)
        group_choices = list(Group.objects.all().values_list("id","name"))
        group_choices.insert(0,("","请选择"))
        self.fields["search_group"].widget.choices = group_choices

class UserAddForm(forms.Form):
    username = forms.CharField(
        widget = TextInput(attrs = {"id":"username","class":"form-control","placeholder":"请输入用户名"})
    )
    password = forms.CharField(
        widget = PasswordInput(attrs = {"id":"password","class":"form-control","placeholder":"请输入密码"}),
        required = False
    )
    first_name = forms.CharField(
        widget = TextInput(attrs = {"id":"first_name","class":"form-control","placeholder":"请输入姓"})
    )
    last_name = forms.CharField(
        widget = TextInput(attrs = {"id":"last_name","class":"form-control","placeholder":"请输入名字"})
    )
    email = forms.CharField(
        widget = EmailInput(attrs = {"id":"email","class":"form-control","placeholder":"请输入邮箱"})
    )
    is_superuser = forms.CharField(
        widget = Select(attrs = {"id":"is_superuser","class":"form-control"},choices=is_choice)
    )
    is_staff = forms.CharField(
        widget = Select(attrs = {"id":"is_staff","class":"form-control"},choices=is_choice)
    )
    group = forms.CharField(
        widget = Select(attrs = {"id":"group","class":"form-control"})
    )
    def __init__(self,*args,**kwargs):
        super(UserAddForm,self).__init__(*args,**kwargs)
        group_choices = list(Group.objects.all().values_list("id","name"))
        group_choices.insert(0,("","请选择"))
        self.fields["group"].widget.choices = group_choices

class UserUpdateForm(UserAddForm):
    password = forms.CharField(
        widget = PasswordInput(attrs = {"id":"password","class":"form-control","placeholder":"请输入原密码"})
    )
    new_password = forms.CharField(
        widget = PasswordInput(attrs = {"id":"new_password","class":"form-control","placeholder":"请输入新密码"})
    )

class GroupSearchForm(forms.Form):
    search_group_name = forms.CharField(
        widget = TextInput(attrs = {"id":"search_group_name","class":"form-control","placeholder":"请输入组名称"})
    )

class GroupAddForm(forms.Form):
    name = forms.CharField(
        widget = TextInput(attrs = {"id":"name","class":"form-control","placeholder":"请输入组名称"})
    )
    permissions = forms.ModelMultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"permissions","class":"form-control select2"}),
        queryset = Permission.objects.all()
    )

