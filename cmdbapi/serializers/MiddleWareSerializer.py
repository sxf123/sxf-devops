from cmdb.models.MiddleWare import MiddleWare
from rest_framework import serializers

class MiddleWareSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiddleWare
        fields = ("id","mid_name","mid_type","mid_description","mid_version")
    def create(self, validated_data):
        return MiddleWare.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.mid_name = validated_data.get("mid_name",instance.mid_name)
        instance.mid_type = validated_data.get("mid_type",instance.mid_type)
        instance.mid_description = validated_data.get("mid_description",instance.mid_description)
        instance.mid_version = validated_data.get("mid_version",instance.mid_version)
        instance.save()
        return instance
