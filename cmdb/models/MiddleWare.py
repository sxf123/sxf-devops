from django.db import models
from cmdb.models.Cluster import Cluster

class MiddleWare(models.Model):
    mid_name = models.CharField(max_length=255,blank=False,null=False,verbose_name="名称",unique=True)
    mid_type = models.CharField(max_length=255,blank=True,null=True,verbose_name="中间件类型")
    mid_description = models.CharField(max_length=255,blank=True,null=True,verbose_name="描述")
    mid_version = models.CharField(max_length=255,blank=True,null=True,verbose_name="版本")

    def __str__(self):
        return self.mid_name

    class Meta:
        verbose_name = "中间件"
        verbose_name_plural = verbose_name
        permissions = (
            ("scan_middleware","Can scan middleware info"),
        )
