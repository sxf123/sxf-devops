from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from cmdb.views.HostView import HostSearchView,HostAddView,HostUpdateView,HostDeleteView,HostAppUpdateInfoView,HostProjectModuelView,HostMidUpdateInfoView,HostMiddleWareView,HostDbUpdateInfoView
from cmdb.views.MiddlewareView import MiddlewareSearchView,MiddlewareAddView,MiddlewareUpdateView,MiddlewareDeleteView,MiddleWareInstall
from cmdb.views.ProjectView import ProjectSearchView,ProjectAddView,ProjectUpdateView,ProjectDeleteView
from cmdb.views.ProjectModuleView import ProjectModuleSearchView,ProjectModuleAddView,ProjectModuleUpdateView,ProjectModuleDeleteView,ProjectModuleDetailView,ProjectModuleConfigView,ProjectModuleUpdateInfo
from cmdb.views.ClusterView import ClusterSearchView,ClusterAddView,ClusterUpdateView,ClusterDeleteView,ClusterDetailView
from cmdb.views.IpPoolView import IpPoolSearchView,IpPoolAddView,IpPoolUpdateView,IpPoolDeleteView
from cmdb.views.DomainNameView import DomainNameSearchView,DomainNameAddView,DomainNameUpdateView,DomainNameDeleteView
from cmdb.views.DatabaseView import DatabaseSearchView,DatabaseAddView,DatabaseUpdateView,DatabaseDeleteView,DatabaseDetail
from cmdb.views.WebHook import WebHookTrigger
from cmdb.views.NodeGroupView import NodeGroupSearchView,NodeGroupAddView,NodeGroupUpdateView,NodeGroupDeleteView,NodeGroupDetailView
from cmdb.views.DbSchemaView import DbSchemaSearchView,DbSchemaAddView,DbSchemaUpdateView

urlpatterns = [
    url(r"^host/$",csrf_exempt(HostSearchView.as_view()),name="host"),
    url(r"^host/add/$",csrf_exempt(HostAddView.as_view()),name="host_add"),
    url(r"^host/update/(?P<id>[0-9]+)/$",csrf_exempt(HostUpdateView.as_view()),name="host_update"),
    url(r"^host/delete/(?P<id>[0-9]+)/$",csrf_exempt(HostDeleteView.as_view()),name="host_delete"),
    url(r"^hostinfo/app/update/(?P<hostname>(.*))/$",HostAppUpdateInfoView.as_view(),name="host_app_info_update"),
    url(r"^hostinfo/mid/update/(?P<hostname>(.*))/$",HostMidUpdateInfoView.as_view(),name="host_mid_info_update"),
    url(r"^hostinfo/db/update/(?P<hostname>(.*))/$",HostDbUpdateInfoView.as_view(),name="host_db_info_update"),
    url(r"^host/projectmodule/info/(?P<id>[0-9]+)/$",HostProjectModuelView.as_view(),name="host_projetmodule_info"),
    url(r"^host/middleware/info/(?P<hostname>(.*))/$",HostMiddleWareView.as_view(),name="host_middleware_info"),
    url(r"^middleware/$",csrf_exempt(MiddlewareSearchView.as_view()),name="middleware"),
    url(r"^middleware/add/$",csrf_exempt(MiddlewareAddView.as_view()),name="middleware_add"),
    url(r"^middleware/update/(?P<id>[0-9]+)/$",csrf_exempt(MiddlewareUpdateView.as_view()),name="middleware_update"),
    url(r"^middleware/delete/(?P<id>[0-9]+)/$",csrf_exempt(MiddlewareDeleteView.as_view()),name="middleware_delete"),
    url(r"^middleware/install/(?P<midware>(.*))/$",MiddleWareInstall.as_view(),name="middleware_install"),
    url(r"^middleware/install/$",csrf_exempt(MiddleWareInstall.as_view()),name="mid_install"),
    url(r"^project/$",csrf_exempt(ProjectSearchView.as_view()),name="project"),
    url(r"^project/add/$",csrf_exempt(ProjectAddView.as_view()),name="project_add"),
    url(r"^project/update/(?P<id>[0-9]+)/$",csrf_exempt(ProjectUpdateView.as_view()),name="project_update"),
    url(r"^project/delete/(?P<id>[0-9]+)/$",csrf_exempt(ProjectDeleteView.as_view()),name="project_delete"),
    url(r"^projectmodule/detail/(?P<name>(.*))/$",ProjectModuleDetailView.as_view(),name="project_detail"),
    url(r"^projectmodule/$",csrf_exempt(ProjectModuleSearchView.as_view()),name="projectmodule"),
    url(r"^projectmodule/add/$",csrf_exempt(ProjectModuleAddView.as_view()),name="projectmodule_add"),
    url(r"^projectmodule/update/(?P<id>[0-9]+)/$",csrf_exempt(ProjectModuleUpdateView.as_view()),name="projectmodule_update"),
    url(r"^projectmodule/delete/(?P<id>[0-9]+)/$",csrf_exempt(ProjectModuleDeleteView.as_view()),name="projectmodule_delete"),
    url(r"^projectmodule/config/(?P<id>[0-9]+)/$",ProjectModuleConfigView.as_view(),name="projectmodule_config"),
    url(r"^projectmodule/updateinfo/(?P<module_name>(.*))/$",ProjectModuleUpdateInfo.as_view(),name="projectmodule_update_info"),
    url(r"^cluster/$",csrf_exempt(ClusterSearchView.as_view()),name="cluster"),
    url(r"^cluster/add/$",csrf_exempt(ClusterAddView.as_view()),name="cluster_add"),
    url(r"^cluster/update/(?P<id>[0-9]+)/$",csrf_exempt(ClusterUpdateView.as_view()),name="cluster_update"),
    url(r"^cluster/delete/(?P<id>[0-9]+)/$",csrf_exempt(ClusterDeleteView.as_view()),name="cluster_delete"),
    url(r"^cluster/hostinfo/(?P<cluster_name>(.*))/$",ClusterDetailView.as_view(),name="cluster_host_info"),
    url(r"^ippool/$",csrf_exempt(IpPoolSearchView.as_view()),name="ippool"),
    url(r"^ippool/add/$",csrf_exempt(IpPoolAddView.as_view()),name="ippool_add"),
    url(r"^ippool/update/(?P<id>[0-9]+)/$",csrf_exempt(IpPoolUpdateView.as_view()),name="ippool_update"),
    url(r"^ippool/delete/(?P<id>[0-9]+)/$",csrf_exempt(IpPoolDeleteView.as_view()),name="ippool_delete"),
    url(r"^domainname/$",csrf_exempt(DomainNameSearchView.as_view()),name="domainname"),
    url(r"^domainname/add/$",csrf_exempt(DomainNameAddView.as_view()),name="domainname_add"),
    url(r"^domainname/update/(?P<id>[0-9]+)/$",csrf_exempt(DomainNameUpdateView.as_view()),name="domainname_update"),
    url(r"^domainname/delete/(?P<id>[0-9]+)/$",csrf_exempt(DomainNameDeleteView.as_view()),name="domainname_delete"),
    url(r"^database/$",csrf_exempt(DatabaseSearchView.as_view()),name="database"),
    url(r"^database/add/$",csrf_exempt(DatabaseAddView.as_view()),name="database_add"),
    url(r"^database/update/(?P<id>[0-9]+)/$",csrf_exempt(DatabaseUpdateView.as_view()),name="database_update"),
    url(r"^database/delete/(?P<id>[0-9]+)/$",csrf_exempt(DatabaseDeleteView.as_view()),name="database_delete"),
    url(r"^database/detail/(?P<instance>(.*))/$",DatabaseDetail.as_view(),name="database_detail"),
    url(r"^dbschema/$",csrf_exempt(DbSchemaSearchView.as_view()),name="dbschema"),
    url(r"^dbschema/add/$",csrf_exempt(DbSchemaAddView.as_view()),name="dbschema_add"),
    url(r"^dbschema/update/(?P<id>[0-9]+)/$",csrf_exempt(DbSchemaUpdateView.as_view()),name="dbschema_update"),
    url(r"^webhook/info/$",csrf_exempt(WebHookTrigger.as_view()),name="webhook_info"),
    url(r"^nodegroup/$",csrf_exempt(NodeGroupSearchView.as_view()),name="nodegroup"),
    url(r"^nodegroup/add/$",csrf_exempt(NodeGroupAddView.as_view()),name="nodegroup_add"),
    url(r"^nodegroup/update/(?P<id>[0-9]+)/$",csrf_exempt(NodeGroupUpdateView.as_view()),name="nodegroup_update"),
    url(r"^nodegroup/delete/(?P<id>[0-9]+)/$",csrf_exempt(NodeGroupDeleteView.as_view()),name="nodegroup_delete"),
    url(r"^nodegroup_detail/(?P<nodegroup>(.*))/host/$",NodeGroupDetailView.as_view(),name="nodegroup_detail")
]