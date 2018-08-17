from cmdb.models.Project import Project
from rest_framework import serializers

class ProjectEditSerializer(serializers.ModelSerializer):
    projectmodule_set = serializers.StringRelatedField(many=True,required=False,allow_null=True)
    class Meta:
        model = Project
        fields = ("id","name","real_name","description","dev_leading","test_leading","proj_leading","ops_leading","projectmodule_set")
    def create(self,validated_data):
        return Project.objects.create(**validated_data)
    def update(self,instance,validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.real_name = validated_data.get("real_name",instance.real_name)
        instance.description = validated_data.get("description",instance.description)
        instance.dev_leading = validated_data.get("dev_leading",instance.dev_leading)
        instance.test_leading = validated_data.get("test_leading",instance.test_leading)
        instance.proj_leading = validated_data.get("proj_leading",instance.proj_leading)
        instance.ops_leading = validated_data.get("ops_leading",instance.ops_leading)
        instance.save()
        return instance