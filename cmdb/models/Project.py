from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255,blank=False,null=False,verbose_name="名称")
    real_name = models.CharField(max_length=255,blank=True,null=True,verbose_name="汉字名称")
    description = models.CharField(max_length=255,blank=True,null=True,verbose_name="描述")
    dev_leading = models.CharField(max_length=255,blank=True,null=True,verbose_name="开发负责人")
    test_leading = models.CharField(max_length=255,blank=True,null=True,verbose_name="测试负责人")
    proj_leading = models.CharField(max_length=255,blank=True,null=True,verbose_name="项目负责人")
    ops_leading = models.CharField(max_length=255,blank=True,null=True,verbose_name="运维负责人")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name