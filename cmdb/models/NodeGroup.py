from django.db import models

class NodeGroup(models.Model):
    nodegroup = models.CharField(max_length=255,blank=False,null=False,verbose_name="主机组名称")
    nodegroup_desc = models.CharField(max_length=255,blank=False,null=False,verbose_name="主机组描述")

    def __str__(self):
        return self.nodegroup
    class Meta:
        verbose_name_plural = "主机组"
        verbose_name = verbose_name_plural