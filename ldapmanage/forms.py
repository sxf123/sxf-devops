from django.forms import TextInput,Select,EmailInput
from django import forms

ldap_ou = (
    ("","请选择"),
    ("BeijingBranch", "北京分公司"),
    ("CEOoffice","CEO办公室"),
    ("SettlementCenter","结算中心"),
    ("GameDistributionDivision","游戏发行事业部"),
    ("InnovationCooperationDept","创新合作部"),
    ("AgentBusinessDept","网盟事业部"),
    ("FinanceDept","财务部"),
    ("WirelessBusinessDept","无线事业部"),
    ("ProductRDCenter","产品研发中心"),
    ("IMD","综合管理部"),
    ("HRDepartment1","人力资源一部"),
    ("FinancialBusinessDept","金融事业部"),
    ("GameMerchandizeDivision","衍生品事业部"),
    ("StrategicDevelopmentDept","战略发展部"),
    ("OverseasBusinessDivision","海外事业部"),
    ("InteractiveEntertainmentDivision","互动娱乐事业部"),
    ("CreativeContentDivision","创意内容事业部"),
    ("HRDepartment2","人力资源二部"),
    ("HRDepartment3","人力资源三部"),
    ("MinistryofLaw","法务部"),
    ("AdministrationDept","行政部"),
    ("people","外部人员")
)

ldap_o = (
    ("","请选择"),
    ("北京分公司", "北京分公司"),
    ("CEO办公室", "CEO办公室"),
    ("结算中心", "结算中心"),
    ("游戏发行事业部", "游戏发行事业部"),
    ("创新合作部", "创新合作部"),
    ("网盟事业部", "网盟事业部"),
    ("财务部", "财务部"),
    ("无线事业部", "无线事业部"),
    ("产品研发中心", "产品研发中心"),
    ("综合管理部", "综合管理部"),
    ("人力资源一部", "人力资源一部"),
    ("金融事业部", "金融事业部"),
    ("衍生品事业部", "衍生品事业部"),
    ("战略发展部", "战略发展部"),
    ("海外事业部", "海外事业部"),
    ("互动娱乐事业部", "互动娱乐事业部"),
    ("创意内容事业部", "创意内容事业部"),
    ("人力资源二部", "人力资源二部"),
    ("人力资源三部","人力资源三部"),
    ("法务部", "法务部"),
    ("行政部", "行政部"),
    ("外部人员", "外部人员")
)

class LdapAddForm(forms.Form):
    job_number = forms.CharField(
        widget = TextInput(attrs = {"id":"job_number","class":"form-control","placeholder":"请输入员工工号"})
    )
    name = forms.CharField(
        widget = TextInput(attrs = {"id":"name","class":"form-control","placeholder":"请输入姓名"})
    )
    username = forms.CharField(
        widget = TextInput(attrs = {"id":"email","class":"form-control","placeholder":"请输入姓名全拼"})
    )
    email = forms.CharField(
        widget = EmailInput(attrs = {"id":"email","class":"form-control","placeholder":"请输入邮箱地址"})
    )
    ou = forms.CharField(
        widget = Select(attrs = {"id":"ou","class":"form-control select2"},choices = ldap_ou)
    )
    first_department = forms.CharField(
        widget = Select(attrs = {"id":"first_department","class":"form-control select2"},choices=ldap_o)
    )
    second_department = forms.CharField(
        widget = TextInput(attrs = {"id":"second_department","class":"form-control","placeholder":"请输入组织二级部门"}),
        required = False
    )