from django.db import models
from cmdb.models.Host import Host

class IpPool(models.Model):
    ip_address = models.CharField(max_length=255,blank=False,null=False,verbose_name="ip地址",unique=True)
    gateway = models.CharField(max_length=255,blank=True,null=True,verbose_name="网关")
    ip_segment = models.CharField(max_length=255,blank=True,null=True,verbose_name="网段")
    ip_type = models.CharField(max_length=255,blank=True,null=True,verbose_name="IP地址类型")
    host = models.ForeignKey(Host,null=True,blank=True,verbose_name="主机")

    def __str__(self):
        return "{} : {}".format(self.ip_type,self.ip_address)
    class Meta:
        verbose_name = "ip地址信息"
        verbose_name_plural = verbose_name
        permissions = (
            ("scan_ippool","Can scan ippool info"),
        )