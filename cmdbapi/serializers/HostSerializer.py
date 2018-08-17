from cmdb.models.Host import Host
from rest_framework import serializers
from cmdb.models.Cluster import Cluster
from cmdbapi.serializers.ManyRelationSerializer import ManyRelationSerializer


class HostGetSerializer(serializers.ModelSerializer):
    ippool_set = serializers.StringRelatedField(many=True,required=False)
    cluster = ManyRelationSerializer(many=True)
    class Meta:
        model = Host
        fields = ("id","host_name","kernel","os","osrelease","environment","ippool_set","cluster")
    def create(self,validated_data):
        host = Host.objects.create(
            host_name = validated_data.get("host_name"),
            kernel = validated_data.get("kernel"),
            os = validated_data.get("os"),
            osrelease = validated_data.get("osrelease"),
            environment = validated_data.get("environment"),
        )
        for cluster_name in validated_data.get("cluster"):
            host.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        return host
    def update(self,instance,validated_data):
        instance.host_name = validated_data.get("host_name",instance.host_name)
        instance.kernel = validated_data.get("kernel",instance.kernel)
        instance.os = validated_data.get("os",instance.os)
        instance.osrelease = validated_data.get("osrelease",instance.osrelease)
        instance.environment = validated_data.get("environment",instance.environment)
        instance.cluster.clear()
        for cluster_name in validated_data.get("cluster"):
            instance.cluster.add(Cluster.objects.get(cluster_name=cluster_name))
        instance.save()
        return instance