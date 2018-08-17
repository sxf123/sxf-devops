from rest_framework import serializers

class ManyRelationSerializer(serializers.StringRelatedField):
    def __init__(self,**kwargs):
        super(ManyRelationSerializer,self).__init__(**kwargs)
    def to_internal_value(self, data):
        return data