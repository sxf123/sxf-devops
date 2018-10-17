from django.forms import TextInput,Select,DateInput,FileInput,Textarea,SelectMultiple,ClearableFileInput
from django import forms
from cmdb.models.ProjectModule import ProjectModule
from django.contrib.auth.models import User
from saltjob import handle_script
from cmdb.models.RdsInstance import RdsInstance
from cmdb.models.RdsSchema import RdsSchema
from django.contrib.auth.models import Group

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
        widget = Select(attrs = {"id":"project","class":"form-control select2"})
    )
    svn_path = forms.CharField(
        widget = TextInput(attrs = {"id":"svn_path","class":"form-control","placeholder":"请输入svn地址"})
    )
    principal = forms.CharField(
        widget = Select(attrs = {"id":"principal","class":"form-control select2"})
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
    rdsinstance = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"rdsinstance","class":"form-control select2"}),
        required=False
    )
    develop_person = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"develop_person","class":"form-control select2"})
    )
    monitored_person = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"monitored_person","class":"form-control select2"})
    )
    need_test = forms.CharField(
        widget = Select(attrs = {"id":"need_test","class":"form-control select2"},choices=is_monitored_choice)
    )
    handle_person = forms.CharField(
        widget = Select(attrs = {"id":"handle_person","class":"form-control select2"})
    )
    deploy_type = forms.CharField(
        widget = Select(attrs = {"id":"deploy_type","class":"form-control"},choices=deploy_type_choice)
    )
    email_person = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"email_person","class":"form-control select2"})
    )
    upgrade_step = forms.CharField(
        widget = Textarea(attrs = {"id":"upgrade_step","class":"form-control","placeholder":"请输入升级步骤"})
    )
    upgrade_partition = forms.CharField(
        widget = Select(attrs = {"id":"is_upgrade_partition","class":"form-control"},choices=is_monitored_choice)
    )
    def __init__(self,*args,**kwargs):
        super(DeployForm,self).__init__(*args,**kwargs)
        project_choice = list(ProjectModule.objects.all().values_list("id","module_name"))
        project_choice.insert(0,("","请选择"))
        user_choice_queryset = User.objects.exclude(username="admin")
        user_choice = [(u.username, u.last_name) for u in user_choice_queryset]
        develop_group = Group.objects.get(name="develop")
        develop_person_queryset = develop_group.user_set.all()
        develop_person_choices = [(d.username,d.last_name) for d in develop_person_queryset]
        develop_person_choices.insert(0,("","请选择"))
        ops_group = Group.objects.get(name="ops")
        ops_group_queryset = ops_group.user_set.all()
        ops_group_choices = [(o.username,o.last_name) for o in ops_group_queryset]
        ops_group_choices.insert(0,("","请选择"))
        rdsinstance_choices = list(RdsInstance.objects.all().values_list("instance_name","instance_name"))
        self.fields["project"].widget.choices = project_choice
        self.fields["principal"].widget.choices = develop_person_choices
        self.fields["develop_person"].choices = develop_person_choices
        self.fields["monitored_person"].choices = ops_group_choices
        self.fields["handle_person"].widget.choices = ops_group_choices
        self.fields["email_person"].choices = user_choice
        self.fields["rdsinstance"].choices = rdsinstance_choices

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

# class SchemaSelectForm(forms.Form):
#     def __init__(self,*args,**kwargs):
#         rdsinstance_list = kwargs.pop("rdsinstance_list",None)
#         super(SchemaSelectForm,self).__init__(*args,**kwargs)
#         for rdsinstance in rdsinstance_list:
#             self.fields[rdsinstance] = forms.MultipleChoiceField(
#                 label=rdsinstance,
#                 widget = SelectMultiple(
#                     attrs = {"id":rdsinstance,"class":"form-control select2"}
#                 )
#             )
#             rdsschema_list = list(RdsSchema.objects.filter(rdsinstance__instance_name=rdsinstance).values_list("schema_name","schema_name"))
#             self.fields[rdsinstance].choices = rdsschema_list

# class SqlUploadForm(forms.Form):
#     def __init__(self,*args,**kwargs):
#         rdsschema = kwargs.pop("rdsschema",None)
#         super(SqlUploadForm,self).__init__(*args,**kwargs)
#         for rdsinstance,rdsschema_list in rdsschema.items():
#             for schema in rdsschema_list:
#                 self.fields[schema] = forms.FileField(
#                     label = "{}_{}".format(rdsinstance,schema),
#                     widget = FileInput(
#                         attrs = {"id":schema,"class":"file","data-show-preview":"false","data-show-upload":"false"},
#                     )
#                 )

class TestReportUploadForm(forms.Form):
    test_report = forms.FileField(
        widget = ClearableFileInput(attrs = {"id":"test_report","class":"file","data-show-preview":"false","data-show-upload":"false","multiple":True})
    )
    receiving_report = forms.FileField(
        widget = ClearableFileInput(attrs = {"id":"receiving_report","class":"file","data-show-preview":"false","data-show-upload":"false","multiple":True}),
        required=False
    )

class SchemaForm(forms.Form):
    def __init__(self,*args,**kwargs):
        rdsinstance = kwargs.pop("rdsinstance",None)
        super(SchemaForm,self).__init__(*args,**kwargs)
        self.fields[rdsinstance] = forms.MultipleChoiceField(
            label = rdsinstance,
            widget = SelectMultiple(
                attrs = {"id":rdsinstance,"class":"form-control select2"}
            )
        )
        rdsschema_list = list(RdsSchema.objects.filter(rdsinstance__instance_name=rdsinstance).values_list("schema_name","schema_name"))
        self.fields[rdsinstance].choices = rdsschema_list

class SqlExecuteSearchForm(forms.Form):
    search_upload_person = forms.CharField(
        widget = Select(attrs = {"id":"search_upload_person","class":"form-control select2"})
    )
    def __init__(self,*args,**kwargs):
        super(SqlExecuteSearchForm,self).__init__(*args,**kwargs)
        user = User.objects.all()
        user_choices = [(u.username,u.first_name + u.last_name) for u in user]
        user_choices.insert(0,("","请选择"))
        self.fields["search_upload_person"].widget.choices = user_choices
class SqlUploadForm(forms.Form):
    sqlupload_rdsinstance = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs = {"id":"sqlupload_rdsinstance","class":"form-control select2"})
    )
    def __init__(self,*args,**kwargs):
        super(SqlUploadForm,self).__init__(*args,**kwargs)
        rdsinstance_choices = list(RdsInstance.objects.all().values_list("instance_name", "instance_name"))
        self.fields["sqlupload_rdsinstance"].choices = rdsinstance_choices
