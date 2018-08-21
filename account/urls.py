from django.conf.urls import url
from account.views import UserListView,UserAddView,UserUpdateView,GroupListView,GroupAddView,GroupUpdateView,UserDeleteView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r"^user/list/$",csrf_exempt(UserListView.as_view()),name="user_list"),
    url(r"^user/add/$",csrf_exempt(UserAddView.as_view()),name="user_add"),
    url(r"^user/update/(?P<id>[0-9]+)/$",csrf_exempt(UserUpdateView.as_view()),name="user_update"),
    url(r"^user/delete/(?P<id>[0-9]+)/$",csrf_exempt(UserDeleteView.as_view()),name="user_delete"),
    url(r"^group/list/$",csrf_exempt(GroupListView.as_view()),name="group_list"),
    url(r"^group/add/$",csrf_exempt(GroupAddView.as_view()),name="group_add"),
    url(r"^group/update/(?P<id>[0-9]+)/$",csrf_exempt(GroupUpdateView.as_view()),name="group_update")
]