from django.db import models
from cmdb.models.EcsHost import EcsHost
from cmdb.models.ProjectModule import ProjectModule

class Process(models.Model):
    process_name = models.CharField(max_length=255,null=False,blank=False,verbose_name="java进程名称")
    process_homepath = models.CharField(max_length=255,null=True,blank=True,verbose_name="进程HOME目录")
    process_id = models.CharField(max_length=255,null=True,blank=True,verbose_name="进程ID")
    process_port = models.CharField(max_length=255,null=True,blank=True,verbose_name="进程端口")
    process_log = models.CharField(max_length=255,null=True,blank=True,verbose_name="进程启动日志")
    projectmodule = models.ForeignKey(ProjectModule,null=True,blank=True,verbose_name="所属模块")
    ecshost = models.ForeignKey(EcsHost,null=True,blank=True,verbose_name="所属主机")

    def __str__(self):
        return self.process_name

    class Meta:
        verbose_name = "进程"
        verbose_name_plural = verbose_name
        permissions = (
            ("scan_process","Can scan 进程"),
        )