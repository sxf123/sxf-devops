from django.forms import ModelForm,TextInput,PasswordInput,Select
from django.contrib.auth.models import User,Group
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = TextInput(attrs={"id":"user","placeholder":u"用户名称","class":"form-control","style":"border: 1px solid rgba(255, 255, 255, 0.1);background: rgba(0, 0, 0, 0.1);border-radius: 5px;color: #fff;height: 50px;"}),
        error_messages = {"required":"用户名不能为空"}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "pwd", "placeholder": u"密码","class":"form-control","style":"border: 1px solid rgba(255, 255, 255, 0.1);background: rgba(0, 0, 0, 0.1);border-radius: 5px;color: #fff;height: 50px;"}),
        error_messages={'required': u"密码不能为空"}
    )
