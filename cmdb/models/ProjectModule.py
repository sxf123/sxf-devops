from django.db import models
from cmdb.models.Project import Project
from cmdb.models.Cluster import Cluster
from cmdb.models.DbSchema import DbSchema

class ProjectModule(models.Model):
    module_name = models.CharField(max_length=255,null=False,blank=False,verbose_name="模块名称",unique=True)
    module_desc = models.CharField(max_length=255,null=False,blank=False,verbose_name="模块描述")
    service_type = models.CharField(max_length=255,null=False,blank=False,verbose_name="服务")
    git_url = models.CharField(max_length=255,null=False,blank=False,verbose_name="git地址")
    project = models.ForeignKey(Project,null=False,blank=False,verbose_name="项目")
    db_schema = models.ForeignKey(DbSchema,null=True,blank=True,verbose_name="数据库")
    cluster = models.ManyToManyField(Cluster,null=True,blank=True,verbose_name="集群")

    def __str__(self):
        return self.module_name
    class Meta:
        verbose_name = "项目模块"
        verbose_name_plural = verbose_name