from cmdb.models.DomainName import DomainName
from rest_framework import serializers
from cmdb.models.IpPool import IpPool
from cmdb.models.ProjectModule import ProjectModule


class DomainNameSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(source = "ip.ip_address",allow_null=True,required=False)
    project_module = serializers.CharField(source = "project_module.module_name",allow_null=True,allow_blank=True,required=False)
    class Meta:
        model = DomainName
        fields = ("id","dns","ip","domain_type","project_module","project_module_url","environment")
    def get_ippool(self,ip_address):
        try:
            return IpPool.objects.get(ip_address=ip_address)
        except IpPool.DoesNotExist:
            return None
    def get_projectmodule(self,module_name):
        try:
            return ProjectModule.objects.get(module_name=module_name)
        except ProjectModule.DoesNotExist:
            return None
    def create(self,validated_data):
        # ip = IpPool.objects.get(ip_address=validated_data.get("ip").get("ip_address")) if validated_data.get("ip").get("ip_address") is not None else None
        # project_module = ProjectModule.objects.get(module_name=validated_data.get("project_module").get("module_name")) if validated_data.get("project_module").get("module_name") is not None else None
        ip = self.get_ippool(validated_data.get("ip").get("ip_address"))
        project_module = self.get_projectmodule(validated_data.get("project_module").get("module_name"))
        validated_data["ip"] = ip
        validated_data["project_module"] = project_module
        return DomainName.objects.create(**validated_data)
    def update(self,instance,validated_data):
        instance.dns = validated_data.get("dns",instance.dns)
        instance.domain_type = validated_data.get("domain_type",instance.domain_type)
        # instance.ip = IpPool.objects.get(ip_address=validated_data.get("ip",instance.ip).get("ip_address"))
        # instance.project_module = ProjectModule.objects.get(module_name=validated_data.get("project_module",instance.project_module).get("module_name")) if validated_data.get("project_module",instance.project_module).get("module_name") is not None else None
        instance.project_module_url = validated_data.get("project_module_url")
        instance.environment = validated_data.get("environment")
        instance.ip = self.get_ippool(validated_data.get("ip").get("ip_address"))
        instance.project_module = self.get_projectmodule(validated_data.get("project_module").get("module_name"))
        instance.save()
        return instance
