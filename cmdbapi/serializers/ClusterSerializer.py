
from cmdb.models.Cluster import Cluster
from rest_framework import serializers

class ClusterGetSerializer(serializers.ModelSerializer):
    host = serializers.SerializerMethodField()
    def get_host(self,obj):
        temp = []
        for host in obj.host_set.all():
            temp.append(host.host_name)
        return temp
    class Meta:
        model = Cluster
        fields = ("id","cluster_name","cluster_type","cluster_desc","environment","host")

class ClusterEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ("id","cluster_name","cluster_type","cluster_desc","environment")
    def create(self,validated_data):
        return Cluster.objects.create(**validated_data)
    def update(self,instance,validated_data):
        instance.cluster_name = validated_data.get("cluster_name",instance.cluster_name)
        instance.cluster_type = validated_data.get("cluster_type",instance.cluster_type)
        instance.cluster_desc = validated_data.get("cluster_desc",instance.cluster_desc)
        instance.environment = validated_data.get("environment",instance.environment)
        instance.save()
        return instance