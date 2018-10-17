from django.db import models

class RdsInstance(models.Model):
    instance_name = models.CharField(max_length=255,null=False,blank=False,verbose_name="实例名称")
    instance_url = models.CharField(max_length=255,null=False,blank=False,verbose_name="实例地址")
    instance_port = models.CharField(max_length=255,null=False,blank=False,verbose_name="实例端口")
    db_type = models.CharField(max_length=255,null=True,blank=False,verbose_name="数据库类型")
    instance_desc = models.CharField(max_length=255,null=True,blank=True,verbose_name="实例描述")

    def __str__(self):
        return self.instance_name
    class Meta:
        verbose_name = "rds实例"
        verbose_name_plural = verbose_name
        permissions = (
            ("scan_rdsinstance","Can scan RDS实例"),
        )