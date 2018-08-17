from rest_framework import serializers
from cmdb.models.DbSchema import DbSchema
from cmdb.models.Database import Database

class DbSchemaSerializer(serializers.ModelSerializer):
    instance = serializers.CharField(source = "instance.instance",allow_null=False)
    class Meta:
        model = DbSchema
        fields = ("id","schema","url","port","user","password","instance")
    def get_instance(self,instance):
        try:
            return Database.objects.get(instance=instance)
        except Database.DoesNotExist:
            return None
    def create(self,validated_data):
        instance = self.get_initial(validated_data.get("instance").get("instance"))
        validated_data["instance"] = instance
        return DbSchema.objects.create(**validated_data)
    def update(self,instance,validated_data):
        instance.schema = validated_data.get("schema",instance.schema)
        instance.url = validated_data.get("url",instance.url)
        instance.port = validated_data.get("port",instance.port)
        instance.user = validated_data.get("user",instance.user)
        instance.password = validated_data.get("password",instance.password)
        instance.instance = self.get_instance(validated_data.get("instance").get("instance"))
        instance.save()
        return instance