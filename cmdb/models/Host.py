from django.db import models
from cmdb.models.Cluster import Cluster
from cmdb.models.NodeGroup import NodeGroup

usage_type = (
    ("app","应用"),
    ("db","数据库"),
    ("mid","中间件"),
    ("plaform","平台")
)

class Host(models.Model):
    host_name = models.CharField(max_length=255,blank=False,null=False,verbose_name="主机DNS名称",unique=True)
    kernel = models.CharField(max_length=255,blank=True,null=True,verbose_name="系统内核")
    osrelease = models.CharField(max_length=255,blank=True,null=True,verbose_name="操作系统版本")
    os = models.CharField(max_length=255,blank=True,null=True,verbose_name="操作系统")
    cpu_nums = models.CharField(max_length=255,null=True,blank=True,verbose_name="cpu核数")
    memory = models.CharField(max_length=255,null=True,blank=True,verbose_name="内存大小")
    environment = models.CharField(max_length=255,blank=True,null=True,verbose_name="环境")
    cluster = models.ManyToManyField(Cluster,null=True,blank=True,verbose_name="集群",related_query_name="host")
    nodegroup = models.ForeignKey(NodeGroup,blank=True,null=True,verbose_name="saltstack主机组")
    host_usage = models.CharField(max_length=255,blank=True,null=True,verbose_name="主机用途",choices=usage_type)
    host_type = models.CharField(max_length=255,blank=True,null=True,verbose_name="主机类型")

    def __str__(self):
        return self.host_name
    class Meta:
        verbose_name = "主机"
        verbose_name_plural = verbose_name