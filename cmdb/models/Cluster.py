from django.db import models

class Cluster(models.Model):
    cluster_name = models.CharField(max_length=255,null=False,blank=False,verbose_name="集群名称",unique=True)
    cluster_type = models.CharField(max_length=255,null=False,blank=False,verbose_name="集群类型")
    cluster_desc = models.CharField(max_length=255,null=False,blank=False,verbose_name="集群描述")
    environment = models.CharField(max_length=255,null=False,blank=False,verbose_name="环境")

    def __str__(self):
        return self.cluster_name
    class Meta:
        verbose_name = "集群"
        verbose_name_plural = verbose_name
        permissions = (
            ("scan_cluster","Can scan cluster info"),
            ("resource_manage","Can manage 资源"),
            ("project_manage","Can manage 项目"),
            ("ldap_add","Can add LDAP用户"),
            ("project_upgrade","Can upgrade 项目")
        )