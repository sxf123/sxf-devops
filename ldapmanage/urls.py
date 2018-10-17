from django.conf.urls import url
from ldapmanage.views import ldap_add

urlpatterns = (
    url(r"^user/add/$",ldap_add,name="ldap_add"),
)