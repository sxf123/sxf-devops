from django.conf.urls import url
from jenkinsapi.views import JenkinsSearchNode,JekinsAddNode
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r"^node/list/$",JenkinsSearchNode.as_view(),name="jenkins_search_node"),
    url(r"^node/add/$",csrf_exempt(JekinsAddNode.as_view()),name="jenkins_add_node")
]