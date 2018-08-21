from django.db import models
from cmdb.models.ProjectModule import ProjectModule
from django.contrib.auth.models import User

class DeployTask(models.Model):
    project = models.ForeignKey(ProjectModule,null=False,blank=False,verbose_name="项目名称",related_name="project_module_name")
    svn_path = models.CharField(max_length=255,null=False,blank=False,verbose_name="svn地址")
    principal = models.CharField(max_length=255,null=False,blank=False,verbose_name="负责人")
    update_date = models.DateField(auto_now=False,auto_now_add=False,verbose_name="更新日期")
    update_project = models.ForeignKey(ProjectModule,null=False,blank=False,verbose_name="更新项目",related_name="update_project")
    tag_date = models.DateField(auto_now=False,auto_now_add=False,verbose_name="tag日期")
    tag_version = models.CharField(max_length=255,null=False,blank=False,verbose_name="tag版本")
    desc = models.TextField(max_length=255,null=False,blank=False,verbose_name="版本简要说明")
    bug_fix = models.CharField(max_length=255,null=True,blank=True,verbose_name="修改的缺陷")
    update_function = models.CharField(max_length=255,null=True,blank=True,verbose_name="新增功能")
    solve_problem = models.CharField(max_length=255,null=True,blank=True,verbose_name="已解决的问题")
    exist_risk = models.CharField(max_length=255,null=True,blank=True,verbose_name="已存在的风险")
    roll_back = models.CharField(max_length=255,null=False,blank=False,verbose_name="出现问题回滚措施")
    is_monitored = models.CharField(max_length=255,null=False,blank=False,verbose_name="新上线功能是否可监控")
    develop_person = models.CharField(max_length=255,null=False,blank=False,verbose_name="版本开发人员")
    monitored_person = models.CharField(max_length=255,null=False,blank=False,verbose_name="升级后监控人员")
    verify_person = models.CharField(max_length=255,null=False,blank=False,verbose_name="升级后功能验证人员")
    need_test = models.CharField(max_length=255,null=True,blank=False,verbose_name="是否需要测试")
    is_test_pass = models.CharField(max_length=255,null=True,blank=False,default="no",verbose_name="是否测试通过")
    is_examine_pass = models.CharField(max_length=255,null=True,blank=False,default="no",verbose_name="是否审核通过")
    handle_person = models.CharField(max_length=255,null=True,blank=False,verbose_name="升级操作人员")
    is_backspace = models.CharField(max_length=255,null=True,blank=False,default="no",verbose_name="是否被回退")
    deploy_type = models.CharField(max_length=255,null=True,blank=False,default="common upgrade",verbose_name="升级类型")
    create_time = models.DateField(auto_now=True,verbose_name="工单创建时间")

    def __str__(self):
        return "{}-{}-{}".format(self.project,self.tag_version,self.tag_date)
    class Meta:
        verbose_name = "升级任务"
        verbose_name_plural = verbose_name
        permissions = (
            ("scan_deploytask","Can scan deploytask info"),
            ("examine_deploytask","Can examine deploytask"),
            ("backspace_deploytask","Can backspace deploytask")
        )

class Script(models.Model):
    script_name = models.CharField(max_length=255,null=False,blank=False,verbose_name="脚本名称")
    script_type = models.CharField(max_length=255,null=False,blank=False,verbose_name="脚本类型")
    script_content = models.TextField(null=False,blank=False,verbose_name="脚本内容")
    script_dir = models.CharField(max_length=255,null=False,blank=False,verbose_name="脚本路径")
    def __str__(self):
        return self.script_name
    class Meta:
        verbose_name = "脚本"
        verbose_name_plural = verbose_name
        permissions = (
            ("scan_script","Can scan script info"),
            ("execute_script","Can execute script"),
            ("transfer_script","Can transfer script")
        )

class UploadFile(models.Model):
    sql_billing_file = models.CharField(max_length=255,null=True,blank=True,verbose_name="billing sql文件")
    sql_pay_file = models.CharField(max_length=255,null=True,blank=True,verbose_name="pay sql 文件")
    jar_file = models.CharField(max_length=255,null=True,blank=True,verbose_name="jar 文件")
    upload_time = models.DateTimeField(auto_now_add=True,verbose_name="上传时间")
    user = models.ForeignKey(User,null=True,blank=True,verbose_name="上传文件用户")

    def __str__(self):
        return self.upload_time
    class Meta:
        verbose_name = "文件上传执行"
        verbose_name_plural = verbose_name
