from django.db import models
from cmdb.models.RdsInstance import RdsInstance

class RdsSchema(models.Model):
    schema_name = models.CharField(max_length=255,null=False,blank=True,verbose_name="schema名称")
    rdsinstance = models.ForeignKey(RdsInstance,null=True,blank=True,verbose_name="rds实例")
    schema_desc = models.CharField(max_length=255,null=True,blank=True,verbose_name="schema描述")

    def __str__(self):
        return self.schema_name

    class Meta:
        verbose_name = "数据库schema"
        verbose_name_plural = verbose_name
        permissions = (
            ("scan_rdsschema","Can scan rdsschema"),
        )