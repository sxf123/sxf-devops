from cmdb.models.NodeGroup import NodeGroup
from rest_framework import serializers

class NodeGroupSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField(many=True)
    class Meta:
        model = NodeGroup
        fields = ("id","nodegroup","nodegroup_desc","host")

class NodeGroupEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeGroup
        fields = ("id","nodegroup","nodegroup_desc")
    def create(self,validate_data):
        return NodeGroup.objects.create(**validate_data)
    def update(self,instance,validate_data):
        instance.nodegroup = validate_data.get("nodegroup",instance.nodegroup)
        instance.nodegroup_desc = validate_data.get("nodegroup_desc",instance.nodegroup_desc)
        instance.save()
        return instance