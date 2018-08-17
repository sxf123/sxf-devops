from django.contrib import admin
from cmdb.models.Host import Host
from cmdb.models.Cluster import Cluster
from cmdb.models.ProjectModule import ProjectModule
from cmdb.models.Project import Project
from cmdb.models.Database import Database
from cmdb.models.DomainName import DomainName
from cmdb.models.IpPool import IpPool
from cmdb.models.MiddleWare import MiddleWare

admin.site.register(Host)
admin.site.register(Cluster)
admin.site.register(ProjectModule)
admin.site.register(Project)
admin.site.register(Database)
admin.site.register(DomainName)
admin.site.register(IpPool)
admin.site.register(MiddleWare)