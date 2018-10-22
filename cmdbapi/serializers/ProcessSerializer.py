from rest_framework import serializers
from cmdb.models.EcsHost import EcsHost
from cmdb.models.Process import ProjectModule
from cmdb.models.Process import Process

class ProcessSerializer(serializers.ModelSerializer):
    projectmodule = serializers.CharField(source = "projectmodule.module_name",allow_blank=True)
    ecshost = serializers.CharField(source = "ecshost.minion_id",allow_blank=True)
    class Meta:
        model = Process
        fields = ("id","process_name","process_homepath","process_id","process_port","process_log","projectmodule","ecshost")
    def get_projectmodule(self,module_name):
        try:
            return ProjectModule.objects.get(module_name=module_name)
        except ProjectModule.DoesNotExist:
            return None
    def get_ecshost(self,minion_id):
        try:
            return EcsHost.objects.get(minion_id=minion_id)
        except EcsHost.DoesNotExist:
            return None
    def create(self, validated_data):
        projectmodule = self.get_projectmodule(validated_data.get("projectmodule").get("module_name"))
        ecshost = self.get_ecshost(validated_data.get("ecshost").get("minion_id"))
        validated_data["projectmodule"] = projectmodule
        validated_data["ecshost"] = ecshost
        return Process.objects.create(**validated_data)
    def update(self,instance,validate_data):
        instance.process_name = validate_data.get("process_name",instance.process_name)
        instance.process_homepath = validate_data.get("process_homepath",instance.process_homepath)
        instance.process_id = validate_data.get("process_id",instance.process_id)
        instance.process_port = validate_data.get("process_port",instance.process_port)
        instance.process_log = validate_data.get("process_log",instance.process_log)
        instance.projectmodule = self.get_projectmodule(validate_data.get("projectmodule").get("module_name"))
        instance.ecshost = self.get_ecshost(validate_data.get("ecshost").get("minion_id"))
        instance.save()
        return instance