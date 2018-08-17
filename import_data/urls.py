from django.conf.urls import url
from import_data import views

urlpatterns = [
    url(r"^project/$",views.import_data,name="import_project"),
    url(r"^ippool/$",views.import_ip,name="import_ippool"),
    url(r"^domainname/$",views.import_domain,name="import_domainname"),
    url(r"^host/$",views.import_host,name="import_host")
]