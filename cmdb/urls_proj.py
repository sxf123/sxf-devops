from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from cmdb.views.ProjectView import ProjectSearchView,ProjectAddView,ProjectDeleteView,ProjectUpdateView
from cmdb.views.ProjectModuleView import ProjectModuleDetailView,ProjectModuleSearchView,ProjectModuleAddView,ProjectModuleUpdateView,ProjectModuleDeleteView,ProjectModuleConfigView,ProjectModuleUpdateInfo
from cmdb.views.ProcessView import ProcessList,ProcessAdd,ProcessUpdate,ProcessDelete

urlpatterns = [
    url(r"^list/$",csrf_exempt(ProjectSearchView.as_view()),name="project"),
    url(r"^add/$",csrf_exempt(ProjectAddView.as_view()),name="project_add"),
    url(r"^update/(?P<id>[0-9]+)/$",csrf_exempt(ProjectUpdateView.as_view()),name="project_update"),
    url(r"^delete/(?P<id>[0-9]+)/$",csrf_exempt(ProjectDeleteView.as_view()),name="project_delete"),
    url(r"^projectmodule/detail/(?P<name>(.*))/$",ProjectModuleDetailView.as_view(),name="project_detail"),
    url(r"^projectmodule/$",csrf_exempt(ProjectModuleSearchView.as_view()),name="projectmodule"),
    url(r"^projectmodule/add/$",csrf_exempt(ProjectModuleAddView.as_view()),name="projectmodule_add"),
    url(r"^projectmodule/update/(?P<id>[0-9]+)/$",csrf_exempt(ProjectModuleUpdateView.as_view()),name="projectmodule_update"),
    url(r"^projectmodule/delete/(?P<id>[0-9]+)/$",csrf_exempt(ProjectModuleDeleteView.as_view()),name="projectmodule_delete"),
    url(r"^projectmodule/config/(?P<id>[0-9]+)/$",ProjectModuleConfigView.as_view(),name="projectmodule_config"),
    url(r"^projectmodule/updateinfo/(?P<module_name>(.*))/$",ProjectModuleUpdateInfo.as_view(),name="projectmodule_update_info"),
    url(r"^process/list/$",csrf_exempt(ProcessList.as_view()),name="process_list"),
    url(r"^process/add/$",csrf_exempt(ProcessAdd.as_view()),name="process_add"),
    url(r"^process/update/(?P<id>[0-9]+)/$",csrf_exempt(ProcessUpdate.as_view()),name="process_update"),
    url(r"^process/delete/(?P<id>[0-9]+)/$",csrf_exempt(ProcessDelete.as_view()),name="process_delete")
]