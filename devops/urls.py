"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from common import views
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import handler403
from common.views import permission_denied

handler403 = permission_denied

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^common/',include('common.urls')),
    url(r'^cmdb/',include('cmdb.urls')),
    url(r'^project/',include('cmdb.urls_proj')),
    url(r'^accounts/login/$',views.LoginView.as_view(),name="login"),
    url(r'^dxwf/',include('dxwf.urls')),
    url(r'^api/',include('cmdbapi.urls')),
    url(r'^api-auth/',obtain_jwt_token),
    url(r'^import/',include('import_data.urls')),
    url(r'^jenkinsapi/',include('jenkinsapi.urls')),
    url(r'^deploy/',include('deploy.urls')),
    url(r'^account/',include('account.urls')),
    url(r'^ldap/',include('ldapmanage.urls'))
]
