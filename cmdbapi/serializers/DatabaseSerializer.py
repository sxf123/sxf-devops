from rest_framework import serializers
from cmdb.models.Database import Database
from cmdb.models.Cluster import Cluster
from cmdb.models.Host import Host

class DatabaseSerializer(serializers.ModelSerializer):
    cluster_name = serializers.CharField(source = "cluster.cluster_name",allow_null=True)
    host_name = serializers.CharField(source = "host.host_name",allow_null=True)
    class Meta:
        model = Database
        fields = ("id","instance","db_type","cluster_name","host_name")
    def get_cluster(self,cluster_name):
        try:
            return Cluster.objects.get(cluster_name=cluster_name)
        except Cluster.DoesNotExist:
            return None
    def get_host(self,host_name):
        try:
            return Host.objects.get(host_name=host_name)
        except Host.DoesNotExist:
            return None
    def create(self, validated_data):
        cluster = self.get_cluster(validated_data.get("cluster").get("cluster_name"))
        host = self.get_host(validated_data.get("host").get("host_name"))
        validated_data["cluster"] = cluster
        validated_data["host"] = host
        return Database.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.instance = validated_data.get("instance",instance.instance)
        instance.db_type = validated_data.get("db_type",instance.db_type)
        instance.cluster = self.get_cluster(validated_data.get("cluster").get("cluster_name"))
        instance.host = self.get_host(validated_data.get("host").get("host_name"))
        instance.save()
        return instance