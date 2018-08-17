from cmdb.models.ProjectModule import ProjectModule
from rest_framework import serializers
from cmdb.models.Project import Project
from cmdb.models.Cluster import Cluster
from cmdbapi.serializers.ManyRelationSerializer import ManyRelationSerializer

class ProjectModuleSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source = "project.name")
    cluster = ManyRelationSerializer(many=True)
    class Meta:
        model = ProjectModule
        fields = ("id","module_name","module_desc","service_type","git_url","project","cluster")
    def get_project(self,name):
        try:
            return Project.objects.get(name=name)
        except Project.DoesNotExist:
            return None
    def get_cluster(self,cluster_name):
        try:
            return Cluster.objects.get(cluster_name=cluster_name)
        except Cluster.DoesNotExist:
            return None
    def create(self, validated_data):
        project = self.get_project(validated_data.get("project").get("name"))
        projectmodule = ProjectModule.objects.create(
            module_name = validated_data.get("module_name"),
            module_desc = validated_data.get("module_desc"),
            service_type = validated_data.get("service_type"),
            git_url = validated_data.get("git_url"),
            project = project
        )
        for cluster_name in validated_data.get("cluster"):
            projectmodule.cluster.add(self.get_cluster(cluster_name))
        return projectmodule
    def update(self, instance, validated_data):
        instance.module_name = validated_data.get("module_name",instance.module_name)
        instance.module_desc = validated_data.get("module_desc",instance.module_desc)
        instance.service_type = validated_data.get("service_type",instance.service_type)
        instance.git_url = validated_data.get("git_url",instance.git_url)
        instance.project = self.get_project(validated_data.get("project").get("name"))
        instance.cluster.clear()
        for cluster_name in validated_data.get("cluster"):
            instance.cluster.add(self.get_cluster(cluster_name))
        return instance
