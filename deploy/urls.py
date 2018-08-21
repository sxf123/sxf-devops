from django.conf.urls import url
from deploy.views.DeployTaskView import DeployTaskView,DeployTaskSearchView,DeployTaskDelete,DeployTaskExamine
from deploy.views.UploadFileView import UploadFileView
from deploy.views.ScriptExecuteView import FileListView,FileExecuteView,FileDelete
from deploy.views.DeployTaskView import test_pass,backspace
from deploy.views.ScriptView import ScriptManageView,ScriptAddView,ScriptUpdateView,ScriptExecuteView,ScriptDeleteView,ScriptTransferView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r"^task/$",csrf_exempt(DeployTaskView.as_view()),name="deploy_task"),
    url(r"^task/list/$",csrf_exempt(DeployTaskSearchView.as_view()),name="deploy_task_list"),
    url(r"^task/delete/(?P<id>[0-9]+)/$",csrf_exempt(DeployTaskDelete.as_view()),name="deploy_task_delete"),
    url(r"^task/examine/(?P<id>[0-9]+)/$",csrf_exempt(DeployTaskExamine.as_view()),name="deploy_task_examine"),
    url(r"^task/test/pass/(?P<handle_person>(.*))/(?P<project>(.*))/(?P<tag_version>(.*))/$",test_pass,name="test_pass"),
    url(r"^task/back/(?P<principal>(.*))/(?P<project>(.*))/(?P<tag_version>(.*))/$",backspace,name="backspace"),
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
    url(r"^upload/file/delete/(?P<id>[0-9]+)/$",csrf_exempt(FileDelete.as_view()),name="delete_file")
]