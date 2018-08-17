from django.db import models
from django.utils import timezone

class MavenProj(models.Model):
    groupId = models.CharField(max_length=255,blank=False,null=False,verbose_name="groupId")
    artifactId = models.CharField(max_length=255,blank=False,null=False,verbose_name="artifactId")
    service_type = models.CharField(max_length=255,blank=False,null=False,verbose_name="service_type")
    create_time = models.DateTimeField(default=timezone.now,verbose_name="创建时间")

    def __str__(self):
        return self.artifactId
    class Meta:
        verbose_name = "maven项目"
        verbose_name_plural = verbose_name
