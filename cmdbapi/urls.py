from django.conf.urls import url
from cmdbapi.views.ClusterView import ClusterList,ClusterDetail,ClusterSearch,ClusterDelete,ClusterUpdateWithId
from cmdbapi.views.HostView import HostList,HostDetail,HostSearch,HostDelete,HostUpdateWithId
from cmdbapi.views.ProjectView import ProjectList,ProjectDetail,ProjectSearch,ProjectDelete,ProjectUpdateWithId
from cmdbapi.views.ProjectModuleView import ProjectModuleList,ProjectModuleDetail,ProjectModuleSearch,ProjectModuleDelete,ProjectModuleUpdateWithId
from cmdbapi.views.MiddleWareView import MiddleWareList,MiddleWareDetail,MiddleWareSearch,MiddleWareDelete,MiddleWareUpdateWithId,MiddleWareInstall
from cmdbapi.views.DatabaseView import DatabaseDetail,DatabaseList,DatabaseSearch,DatabaseDelete,DatabaseUpdateWithId
from cmdbapi.views.DomainNameView import DomainNameList,DomainNameDetail,DomainNameSearch,DomainNameDelet,DomainNameUpdateWithId
from cmdbapi.views.IpPoolView import IpPoolList,IpPoolDetail,IpPollSearch,IpPoolDelete,IpPoolUpdateWithId
from cmdbapi.views.UserInfoView import UserInfo
from cmdbapi.views.NodeGroupView import NodeGroupSearch,NodeGroupDetail,NodeGroupList,NodeGroupUpdate,NodeGroupUpdateWithId,NodeGroupDelete
from cmdbapi.views.DbSchemaView import DbSchemaList,DbSchemaSearch,DbSchemaDetail,DbSchemaDelete,DbSchemaUpdateWithId

urlpatterns = [
    url(r'^cluster/list/$',ClusterList.as_view(),name="cluster_list_api"),
    url(r"^cluster/(?P<pk>[0-9]+)/$",ClusterDetail.as_view(),name="cluster_detail_api"),
    url(r"^cluster/search/$",ClusterSearch.as_view(),name="cluster_search_api"),
    url(r"^cluster/delete/$",ClusterDelete.as_view(),name="cluster_delete_api"),
    url(r"^cluster/update/$",ClusterUpdateWithId.as_view(),name="cluster_update_api"),
    url(r"^host/list/$",HostList.as_view(),name="host_list_api"),
    url(r"^host/(?P<pk>[0-9]+)/$",HostDetail.as_view(),name="host_detail_api"),
    url(r"^host/search/$",HostSearch.as_view(),name="host_search_api"),
    url(r"^host/delete/$",HostDelete.as_view(),name="host_delete_api"),
    url(r"^host/update/$",HostUpdateWithId.as_view(),name="host_update_api"),
    url(r"^project/list/$",ProjectList.as_view(),name="project_list_api"),
    url(r"^project/(?P<pk>[0-9]+)/$",ProjectDetail.as_view(),name="project_list_api"),
    url(r"^project/search/$",ProjectSearch.as_view(),name="project_search_api"),
    url(r"^project/delete/$",ProjectDelete.as_view(),name="project_delete_api"),
    url(r"^project/update/$",ProjectUpdateWithId.as_view(),name="project_update_api"),
    url(r"^projectmodule/list/$",ProjectModuleList.as_view(),name="projectmodule_list_api"),
    url(r"^projectmodule/(?P<pk>[0-9]+)/$",ProjectModuleDetail.as_view(),name="projectmodule_detail_api"),
    url(r"^projectmodule/search/$",ProjectModuleSearch.as_view(),name="projectmodule_search_api"),
    url(r"^projectmodule/delete/$",ProjectModuleDelete.as_view(),name="projectmodule_delete_api"),
    url(r"^projectmodule/update/$",ProjectModuleUpdateWithId.as_view(),name="projectmodule_update_api"),
    url(r"^middleware/list/$",MiddleWareList.as_view(),name="middleware_list_api"),
    url(r"^middleware/(?P<pk>[0-9]+)/$",MiddleWareDetail.as_view(),name="middleware_detail_api"),
    url(r"^middleware/search/$",MiddleWareSearch.as_view(),name="middleware_search_api"),
    url(r"^middleware/delete/$",MiddleWareDelete.as_view(),name="middleware_delete_api"),
    url(r"^middleware/update/$",MiddleWareUpdateWithId.as_view(),name="middleware_update_api"),
    url(r"^middleware/install/$",MiddleWareInstall.as_view(),name="middleware_install_api"),
    url(r"^database/list/$",DatabaseList.as_view(),name="database_list_api"),
    url(r"^database/(?P<pk>[0-9]+)/$",DatabaseDetail.as_view(),name="database_detail_api"),
    url(r"^database/search/$",DatabaseSearch.as_view(),name="database_search_api"),
    url(r"^database/delete/$",DatabaseDelete.as_view(),name="database_delete_api"),
    url(r"^database/update/$",DatabaseUpdateWithId.as_view(),name="database_update_api"),
    url(r"^dbschema/list/$",DbSchemaList.as_view(),name="dbschema_list_api"),
    url(r"^dbschema/(?P<pk>[0-9]+)/$",DbSchemaDetail.as_view(),name="dbschema_detail_api"),
    url(r"^dbschema/search/$",DbSchemaSearch.as_view(),name="dbschema_search_api"),
    url(r"^dbschema/delete/$",DbSchemaDelete.as_view(),name="dbschema_delete_api"),
    url(r"^dbschema/update/$",DbSchemaUpdateWithId.as_view(),name="dbschema_update_api"),
    url(r"^domainname/list/$",DomainNameList.as_view(),name="domainname_list_api"),
    url(r"^domainname/(?P<pk>[0-9]+)/$",DomainNameDetail.as_view(),name="domainname_detail_api"),
    url(r"^domainname/search/$",DomainNameSearch.as_view(),name="domainname_search_api"),
    url(r"^domainname/delete/$",DomainNameDelet.as_view(),name="domainname_delete_api"),
    url(r"^domainname/update/$",DomainNameUpdateWithId.as_view(),name="domainname_update_api"),
    url(r"^ippool/list/$",IpPoolList.as_view(),name="ippool_list_api"),
    url(r"^ippool/(?P<pk>[0-9]+)/$",IpPoolDetail.as_view(),name="ippool_detail_api"),
    url(r"^ippool/search/$",IpPollSearch.as_view(),name="ippool_search_api"),
    url(r"^ippool/delete/$",IpPoolDelete.as_view(),name="ippool_delete_api"),
    url(r"^ippool/update/$",IpPoolUpdateWithId.as_view(),name="ippool_update_api"),
    url(r"^user/info/$",UserInfo.as_view(),name="user_info_api"),
    url(r"^nodegroup/list/$",NodeGroupList.as_view(),name="nodegroup_list_api"),
    url(r"^nodegroup/(?P<pk>[0-9]+)/$",NodeGroupDetail.as_view(),name="nodegroup_detail_api"),
    url(r"^nodegroup/search/$",NodeGroupSearch.as_view(),name="nodegroup_search_api"),
    url(r"^nodegroup/delete/$",NodeGroupDelete.as_view(),name="nodegroup_delete_api"),
    url(r"^nodegroup/update/$",NodeGroupUpdateWithId.as_view(),name="nodegroup_update_api"),
]