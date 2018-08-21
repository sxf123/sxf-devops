from django.conf.urls import url
from common import views
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^logout/$',views.LogoutView.as_view(),name="logout")
]