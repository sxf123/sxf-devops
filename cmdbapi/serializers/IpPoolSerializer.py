from rest_framework import serializers
from cmdb.models.IpPool import IpPool
from cmdb.models.Host import Host

class IpPoolSerializer(serializers.ModelSerializer):
    host = serializers.CharField(source = "host.host_name",default = None)
    class Meta:
        model = IpPool
        fields = ("id","ip_address","gateway","ip_segment","ip_type","host")
    def get_host(self,host_name):
        try:
            return Host.objects.get(host_name=host_name)
        except Host.DoesNotExist:
            return None
    def create(self, validated_data):
        # host = Host.objects.get(host_name=validated_data.get("host").get("host_name")) if validated_data.get("host").get("host_name") is not None else None
        host = self.get_host(validated_data.get("host").get("host_name"))
        validated_data["host"] = host
        return IpPool.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.ip_address = validated_data.get("ip_address",instance.ip_address)
        instance.gateway = validated_data.get("gateway",instance.gateway)
        instance.ip_segment = validated_data.get("ip_segment",instance.ip_segment)
        instance.ip_type = validated_data.get("ip_type",instance.ip_type)
        # instance.host = Host.objects.get(host_name=validated_data.get("host").get("host_name")) if validated_data.get("host").get("host_name") is not None else None
        instance.host = self.get_host(validated_data.get("host").get("host_name"))
        instance.save()
        return instance
