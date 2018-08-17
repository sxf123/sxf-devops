from django.db import models
from cmdb.models.Database import Database

class DbSchema(models.Model):
    schema = models.CharField(max_length=255,null=False,blank=False,verbose_name="数据库名")
    url = models.CharField(max_length=255,null=True,blank=True,verbose_name="数据库地址")
    port = models.CharField(max_length=255,null=True,blank=True,verbose_name="端口")
    user = models.CharField(max_length=255,null=True,blank=True,verbose_name="用户名")
    password = models.CharField(max_length=255,null=True,blank=True,verbose_name="密码")
    instance = models.ForeignKey(Database,null=True,blank=True,verbose_name="数据库实例")

    def __str__(self):
        return self.schema
    class Meta:
        verbose_name_plural = "数据库"
        verbose_name = verbose_name_plural