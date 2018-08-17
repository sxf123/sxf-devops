from django.db import models
from cmdb.models.Cluster import Cluster
from cmdb.models.Host import Host

class Database(models.Model):
    instance = models.CharField(max_length=255,blank=True,null=True,verbose_name="数据库实例名称",unique=True)
    db_type = models.CharField(max_length=255,blank=True,null=True,verbose_name="数据库类型")
    cluster = models.ForeignKey(Cluster,null=True,blank=True,verbose_name="集群")
    host = models.ForeignKey(Host,null=True,blank=True,verbose_name="主机")

    def __str__(self):
        return self.schema

    class Meta:
        verbose_name = "数据库实例"
        verbose_name_plural = verbose_name