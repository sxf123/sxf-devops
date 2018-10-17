from django.db import models

class SaltState(models.Model):
    fun_name = models.CharField(max_length=255,null=False,blank=False,verbose_name="state名称")
    fun_desc = models.CharField(max_length=255,null=True,blank=True,verbose_name="功能描述")
    state_dir = models.CharField(max_length=255,null=True,blank=True,verbose_name="state目录")

    def __str__(self):
        return self.fun_name
    class Meta:
        verbose_name = "saltstack state"
        verbose_name_plural = verbose_name