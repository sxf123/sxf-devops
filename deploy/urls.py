from django.conf.urls import url
from deploy.views.DeployTaskView import DeployTaskView,DeployTaskSearchView,DeployTaskDelete,DeployTaskExamine
from deploy.views.UploadFileView import UploadFileView
from deploy.views.ScriptExecuteView import FileListView,FileExecuteView,FileDelete,ExecuteResView
from deploy.views.DeployTaskView import test_pass,backspace,sql_file_download,test_report_download,receiving_report_download
from deploy.views.DeployTaskView import TestReportUploadView
from deploy.views.DeployTaskView import DeployDetailView
from deploy.views.DeployTaskView import upgrade_success_deploytask
from deploy.views.DeployTaskView import upgrade_failure_deploytask,upgrade_partition_deploytask,upgrade_continue_deploytask
from deploy.views.ScriptView import ScriptManageView,ScriptAddView,ScriptUpdateView,ScriptExecuteView,ScriptDeleteView,ScriptTransferView
from deploy.views.DBFileView import SchemaView,VerifyPersonView
from deploy.views.DeployTaskView import upgrade_deploytask
from deploy.views.SqlExecuteView import SqlFileUpload,SqlFile,SqlFileDelete,SqlFileDetail,sqlfile_download
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r"^task/$",csrf_exempt(DeployTaskView.as_view()),name="deploy_task"),
    url(r"^task/list/$",csrf_exempt(DeployTaskSearchView.as_view()),name="deploy_task_list"),
    url(r"^task/detail/(?P<module_name>(.*))/$",csrf_exempt(DeployDetailView.as_view()),name="deploy_task_detail"),
    url(r"^task/delete/(?P<id>[0-9]+)/$",csrf_exempt(DeployTaskDelete.as_view()),name="deploy_task_delete"),
    url(r"^task/examine/(?P<id>[0-9]+)/$",csrf_exempt(DeployTaskExamine.as_view()),name="deploy_task_examine"),
    url(r"^task/test/pass/(?P<module_name>(.*))/(?P<tag_version>(.*))/$",test_pass,name="test_pass"),
    url(r"^task/back/(?P<principal>(.*))/(?P<project>(.*))/(?P<tag_version>(.*))/$",backspace,name="backspace"),
    url(r"^task/download/sql/file/(?P<module_name>(.*))/(?P<tag_version>(.*))/$",sql_file_download,name="download_sql"),
    url(r"^task/test/report/upload/(?P<module_name>(.*))/(?P<tag_version>(.*))/$",csrf_exempt(TestReportUploadView.as_view()),name="test_report_upload"),
    url(r"^task/test/report/download/(?P<module_name>(.*))/(?P<tag_version>(.*))/(?P<test_report_filename>(.*))/$",test_report_download,name="test_report_download"),
    url(r"^task/receiving/report/download/(?P<module_name>(.*))/(?P<tag_version>(.*))/(?P<receiving_report_filename>(.*))/$",receiving_report_download,name="receiving_report_download"),
    url(r"^task/rdsschema/select/$",csrf_exempt(SchemaView.as_view()),name="schema"),
    url(r"^task/verifyperson/select/$",csrf_exempt(VerifyPersonView.as_view()),name="verify_person"),
    url(r"^task/upgrade/(?P<id>[0-9]+)/$",upgrade_deploytask,name="upgrade_deploytask"),
    url(r"^task/upgrade/success/(?P<id>[0-9]+)/$",upgrade_success_deploytask,name="upgrade_success"),
    url(r"^task/upgrade/failure/(?P<id>[0-9]+)/$",upgrade_failure_deploytask,name="upgrade_failure"),
    url(r"^task/upgrade/partition/(?P<module_name>(.*))/(?P<tag_version>(.*))/$",upgrade_partition_deploytask,name="upgrade_partition"),
    url(r"^task/upgrade/continue/(?P<module_name>(.*))/(?P<tag_version>(.*))/$",upgrade_continue_deploytask,name="upgrade_continue"),
    url(r"^scripts/$",csrf_exempt(ScriptManageView.as_view()),name="script_manage"),
    url(r"^scripts/add/$",csrf_exempt(ScriptAddView.as_view()),name="script_add"),
    url(r"^scripts/delete/(?P<id>[0-9]+)/$",csrf_exempt(ScriptDeleteView.as_view()),name="script_delete"),
    url(r"^scripts/update/(?P<id>[0-9]+)/$",csrf_exempt(ScriptUpdateView.as_view()),name="script_update"),
    url(r"^scripts/execute/(?P<id>[0-9]+)/$",csrf_exempt(ScriptExecuteView.as_view()),name="minion_select"),
    url(r"^scripts/execute/$",csrf_exempt(ScriptExecuteView.as_view()),name="script_execute"),
    url(r"^scripts/transfer/(?P<id>[0-9]+)/$",csrf_exempt(ScriptTransferView.as_view()),name="minions_select"),
    url(r"^upload/file/$",csrf_exempt(UploadFileView.as_view()),name="upload_file"),
    url(r"^upload/file/list/$",csrf_exempt(FileListView.as_view()),name="execute_file_list"),
    url(r"^upload/file/execute/(?P<id>[0-9]+)/$",csrf_exempt(FileExecuteView.as_view()),name="execute_file"),
    url(r"^upload/file/delete/(?P<id>[0-9]+)/$",csrf_exempt(FileDelete.as_view()),name="delete_file"),
    url(r"^execute/file/res/(?P<id>[0-9]+)/$",csrf_exempt(ExecuteResView.as_view()),name="execute_file"),
    url(r"^sql/upload/$",csrf_exempt(SqlFileUpload.as_view()),name="sql_upload"),
    url(r"^sql/upload/list/$",csrf_exempt(SqlFile.as_view()),name="sql_file_list"),
    url(r"^sql/upload/detail/(?P<upload_person>(.*))/$",csrf_exempt(SqlFileDetail.as_view()),name="sql_file_detail"),
    url(r"^sql/upload/delete/(?P<id>[0-9]+)/$",csrf_exempt(SqlFileDelete.as_view()),name="sql_file_delete"),
    url(r"^sql/upload/download/(?P<id>[0-9]+)/$",sqlfile_download,name="sql_file_download")
]