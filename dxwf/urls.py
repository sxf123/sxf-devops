from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from dxwf.views import MavenProjSearchView,MavenProjAddView,MavenProjDeleteView,download_file

urlpatterns = [
    url(r"^mavenproj/$",csrf_exempt(MavenProjSearchView.as_view()),name="mavenproj"),
    url(r"^mavenproj/add/$",csrf_exempt(MavenProjAddView.as_view()),name="mavenproj_add"),
    url(r"^mavenproj/download/(.*)/$",download_file,name="download_file"),
    url(r"^mavenproj/delete/(?P<id>[0-9]+)/$",MavenProjDeleteView.as_view(),name="mvaenproj_delete")
]