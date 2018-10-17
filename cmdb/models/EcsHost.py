from django.db import models

class EcsHost(models.Model):
    instance_id = models.CharField(max_length=255,null=False,blank=False,verbose_name="ECS实例ID")
    hostname = models.CharField(max_length=255,null=True,blank=True,verbose_name="主机名")
    desc = models.CharField(max_length=255,null=True,blank=True,verbose_name="主机描述")
    local_ip = models.CharField(max_length=255,null=True,blank=True,verbose_name="内网IP")
    internet_ip = models.CharField(max_length=255,null=True,blank=True,verbose_name="公网IP")
    elastic_ip = models.CharField(max_length=255,null=True,blank=True,verbose_name="弹性IP")
    network_type = models.CharField(max_length=255,null=True,blank=True,verbose_name="网络类型")
    cpu_nums = models.CharField(max_length=255,null=True,blank=True,verbose_name="CPU配置")
    memory = models.CharField(max_length=255,null=True,blank=True,verbose_name="内存配置")
    brand = models.CharField(max_length=255,null=True,blank=True,verbose_name="带宽配置")
    minion_id = models.CharField(max_length=255,null=True,blank=True,verbose_name="saltstack minion_id")

    def __str__(self):
        return self.minion_id
    class Meta:
        verbose_name = "ECS主机"
        verbose_name_plural = verbose_name
        permissions = (
            ("scan_ecshost","Can scan ECS主机"),
        )
