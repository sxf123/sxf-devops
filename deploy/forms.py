from django.forms import TextInput,Select,DateInput,FileInput,Textarea,SelectMultiple
from django import forms
from cmdb.models.ProjectModule import ProjectModule
from django.contrib.auth.models import User
from saltjob import handle_script
from cmdb.models.Database import Database
from cmdb.models.DbSchema import DbSchema

is_monitored_choice = (
    ("","请选择"),
    ("yes","是"),
    ("no","否")
)

deploy_type_choice = (
    ("","请选择"),
    ("common upgrade","日常功能升级"),
    ("bug fix","问题修复")
)

class DeploySearchForm(forms.Form):
    search_project_module = forms.CharField(
        widget = Select(attrs = {"id":"search_project_module","class":"form-control select2"})
    )
    def __init__(self,*args,**kwargs):
        super(DeploySearchForm,self).__init__(*args,**kwargs)
        project_module_choices = list(ProjectModule.objects.all().values_list("id","module_name"))
        project_module_choices.insert(0,("","请选择"))
        self.fields["search_project_module"].widget.choices = project_module_choices

class DeployForm(forms.Form):
    project = forms.CharField(
        widget = Select(attrs = {"id":"project","class":"form-control"})
    )
    svn_path = forms.CharField(
        widget = TextInput(attrs = {"id":"svn_path","class":"form-control","placeholder":"请输入svn地址"})
    )
    principal = forms.CharField(
        widget = Select(attrs = {"id":"principal","class":"form-control"})
    )
    update_date = forms.DateField(
        widget = DateInput(attrs = {"id":"update_date","class":"form-control","placeholder":"请输入升级日期"})
    )
    update_project = forms.CharField(
        widget = Select(attrs = {"id":"update_project","class":"form-control"})
    )
    tag_date = forms.DateField(
        widget = DateInput(attrs = {"id":"tag_date","class":"form-control","placeholder":"请输入tag日期"})
    )
    tag_version = forms.CharField(
        widget = TextInput(attrs = {"id":"tag_version","class":"form-control","placeholder":"请输入tag版本"})
    )
    desc = forms.CharField(
        widget = Textarea(attrs = {"id":"desc","class":"form-control","placeholder":"请输入版本简要信息"})
    )
    bug_fix = forms.CharField(
        widget = TextInput(attrs = {"id":"bug_fix","class":"form-control","placeholder":"请输入修改的缺陷"})
    )
    update_function = forms.CharField(
        widget = TextInput(attrs = {"id":"update_function","class":"form-control","placeholder":"请输入新增功能"})
    )
    solve_problem = forms.CharField(
        widget = TextInput(attrs = {"id":"solve_problem","class":"form-control","placeholder":"请输入已解决的问题"})
    )
    exist_risk = forms.CharField(
        widget = TextInput(attrs = {"id":"exist_risk","class":"form-control","placeholder":"请输入可能存在的风险"})
    )
    rollback = forms.CharField(
        widget = TextInput(attrs = {"id":"rollback","class":"form-control","placeholder":"请输入出现问题回滚措施"})
    )
    is_monitored = forms.CharField(
        widget = Select(attrs = {"id":"is_monitored","class":"form-control"},choices = is_monitored_choice)
    )
    instance = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"instance","class":"form-control"}),
        required=False
    )
    dbschema = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"dbschema","class":"form-control"}),
        required=False
    )
    develop_person = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"develop_person","class":"form-control"})
    )
    monitored_person = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"monitored_person","class":"form-control"})
    )
    verify_person = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"verify_person","class":"form-control"})
    )
    sql_exec = forms.CharField(
        widget = Textarea(attrs = {"id":"sql_exec","class":"form-control","placeholder":"请输入需要执行的sql"})
    )
    need_test = forms.CharField(
        widget = Select(attrs = {"id":"need_test","class":"form-control"},choices=is_monitored_choice)
    )
    handle_person = forms.CharField(
        widget = Select(attrs = {"id":"handle_person","class":"form-control"})
    )
    deploy_type = forms.CharField(
        widget = Select(attrs = {"id":"deploy_type","class":"form-control"},choices=deploy_type_choice)
    )
    email_person = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"email_person","class":"form-control"})
    )
    def __init__(self,*args,**kwargs):
        super(DeployForm,self).__init__(*args,**kwargs)
        project_choice = list(ProjectModule.objects.all().values_list("id","module_name"))
        project_choice.insert(0,("","请选择"))
        user_choice = list(User.objects.all().values_list("username","username"))
        principal_choice = list(User.objects.all().values_list("username","username"))
        principal_choice.insert(0,("","请选择"))
        instance_choices = list(Database.objects.all().values_list("id","instance"))
        dbschema_choices = list(DbSchema.objects.all().values_list("id","schema"))
        self.fields["project"].widget.choices = project_choice
        self.fields["principal"].widget.choices = principal_choice
        self.fields["update_project"].widget.choices = project_choice
        self.fields["develop_person"].choices = user_choice
        self.fields["monitored_person"].choices = user_choice
        self.fields["verify_person"].choices = user_choice
        self.fields["instance"].choices = instance_choices
        self.fields["dbschema"].choices = dbschema_choices
        self.fields["handle_person"].widget.choices = principal_choice
        self.fields["email_person"].choices = user_choice

class UploadFileForm(forms.Form):
    sql_file_billing = forms.FileField(
        widget = FileInput(attrs = {"id":"sql_file_billing","class":"file","data-show-preview":"false","data-show-upload":"false"}),
        required = False
    )
    sql_file_pay = forms.FileField(
        widget = FileInput(attrs = {"id":"sql_file_pay","class":"file","data-show-preview":"false","data-show-upload":"false"}),
        required = False
    )
    jar_file = forms.FileField(
        widget = FileInput(attrs = {"id":"jar_file","class":"file","data-show-preview":"false","data-show-upload":"false"}),
        required = False
    )
    upload_desc = forms.CharField(
        widget = Textarea(attrs = {"id":"upload_desc","class":"form-control","placeholder":"请输入上线详细信息"})
    )

script_type_choice = (
    ("","请选择"),
    (".py","python"),
    (".sh","shell")
)

class ScriptSearchForm(forms.Form):
    search_script_name = forms.CharField(
        widget = TextInput(attrs = {"id":"search_script_name","class":"form-control","placeholder":"请输入脚本名称"})
    )
    search_script_type = forms.CharField(
        widget = Select(attrs = {"id":"search_script_type","class":"form-control"},choices=script_type_choice)
    )

class ScriptAddForm(forms.Form):
    script_name = forms.CharField(
        widget = TextInput(attrs = {"id":"script_name","class":"form-control","placeholder":"请输入脚本名称"})
    )
    script_type = forms.CharField(
        widget = Select(attrs = {"id":"script_type","class":"form-control"},choices=script_type_choice)
    )
    script_content = forms.CharField(
        widget = Textarea(attrs = {"id":"script_content","class":"form-control","placeholder":"请输入脚本内容"})
    )
    script_dir = forms.CharField(
        widget = TextInput(attrs = {"id":"script_dir","class":"form-control","placeholder":"请输入脚本路径"})
    )

class HostSelectForm(forms.Form):
    hostname = forms.CharField(
        widget = Select(attrs = {"id":"hostname","class":"form-control select2"})
    )
    def __init__(self,*args,**kwargs):
        super(HostSelectForm,self).__init__(*args,**kwargs)
        hostname_choices = [(m,m) for m in handle_script.get_minions()]
        hostname_choices.insert(0,("","请选择"))
        self.fields["hostname"].widget.choices = hostname_choices

class MinionSelectForm(forms.Form):
    minions = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"minions","class":"form-control select2"})
    )

    def __init__(self,*args,**kwargs):
        super(MinionSelectForm,self).__init__(*args,**kwargs)
        minions_choices = [(m,m) for m in handle_script.get_minions()]
        self.fields["minions"].choices = minions_choices

class FileListForm(forms.Form):
    upload_time = forms.DateField(
        widget = DateInput(attrs = {"id":"upload_time","class":"form-control","placeholder":"请输入上传日期"})
    )
    user = forms.CharField(
        widget = Select(attrs = {"id":"user","class":"form-control"}),
        required = False
    )
    def __init__(self,*args,**kwargs):
        super(FileListForm,self).__init__(*args,**kwargs)
        user_choices = list(User.objects.all().values_list("id","username"))
        user_choices.insert(0,("","请选择"))
        self.fields["user"].widget.choices = user_choices

class FileExecuteForm(forms.Form):
    sql_billing_file = forms.CharField(
        widget = TextInput(attrs = {"id":"billing_file","class":"form-control"})
    )
    sql_pay_file = forms.CharField(
        widget = TextInput(attrs = {"id":"pay_file","class":"form-control"})
    )
    jar_file = forms.CharField(
        widget = TextInput(attrs = {"id":"jar_file","class":"form-control"})
    )
    def __init__(self,*args,**kwargs):
        super(FileExecuteForm,self).__init__(*args,**kwargs)
        self.fields["sql_billing_file"].widget.attrs["readonly"] = True
        self.fields["sql_pay_file"].widget.attrs["readonly"] = True
        self.fields["jar_file"].widget.attrs["readonly"] = True