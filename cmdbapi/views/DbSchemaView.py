from rest_framework.response import Response
from rest_framework.views import APIView
from cmdbapi.serializers.DbSchemaSerializer import DbSchemaSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from cmdb.models.DbSchema import DbSchema

class DbSchemaList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        dbschema = DbSchema.objects.all()
        serializer = DbSchemaSerializer(dbschema,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer = DbSchemaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class DbSchemaDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return DbSchema.objects.get(pk=pk)
        except DbSchema.DoesNotExist:
            return None
    def get(self,request,pk,format=None):
        dbschema = self.get_object(pk)
        if dbschema is not None:
            serializer = DbSchemaSerializer(dbschema)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})

class DbSchemaSearch(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,schema):
        try:
            DbSchema.objects.get(schema=schema)
        except DbSchema.DoesNotExist:
            return None
    def post(self,request,format=None):
        schema = request.data.get("schema")
        dbschema = self.get_object(schema)
        if dbschema is not None:
            serializer = DbSchemaSerializer(dbschema)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})

class DbSchemaDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,schema):
        try:
            return DbSchema.objects.get(schema=schema)
        except DbSchema.DoesNotExist:
            return None
    def post(self,request,format=None):
        schema = request.data.get("schema")
        dbschema = self.get_object(schema)
        if dbschema is not None:
            dbschema.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class DbSchemaUpdateWithId(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return DbSchema.objects.get(pk=pk)
        except DbSchema.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.data.get("id")
        dbschema = self.get_object(id)
        if dbschema is not None:
            serializer = DbSchemaSerializer(dbschema,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})