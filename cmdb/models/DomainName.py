from django.db import models
from cmdb.models.ProjectModule import ProjectModule
from cmdb.models.IpPool import IpPool

class DomainName(models.Model):
    dns = models.CharField(max_length=255,blank=False,null=False,verbose_name="域名地址")
    domain_type = models.CharField(max_length=255,blank=False,null=False,verbose_name="域名类型",default="A")
    ip = models.ForeignKey(IpPool,blank=False,null=False)
    project_module = models.OneToOneField(ProjectModule,blank=True,null=True,verbose_name="服务名称")
    project_module_url = models.CharField(max_length=255,blank=True,null=True,verbose_name="服务访问地址")
    environment = models.CharField(max_length=255,blank=True,null=True,verbose_name="环境")

    def __str__(self):
        return self.dns
    class Meta:
        verbose_name = "dns域名信息"
        verbose_name_plural = verbose_name
        permissions = (
            ("scan_domainname","Can scan domainname"),
        )