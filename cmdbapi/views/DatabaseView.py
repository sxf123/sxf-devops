from rest_framework.response import Response
from rest_framework.views import APIView
from cmdbapi.serializers.DatabaseSerializer import DatabaseSerializer
from cmdb.models.Database import Database
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class DatabaseList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        database = Database.objects.all()
        serializer = DatabaseSerializer(database,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer = DatabaseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class DatabaseDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Database.objects.get(pk=pk)
        except Database.DoesNotExist:
            return None
    def get(self,request,pk,format=None):
        database = self.get_object(pk)
        if database is not None:
            serializer = DatabaseSerializer(database)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})
    def put(self,request,pk,format=None):
        database = self.get_object(pk)
        if database is not None:
            serializer = DatabaseSerializer(database,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"not found"})
    def delete(self,request,pk,format=None):
        database = self.get_object(pk)
        if database is not None:
            database.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class DatabaseSearch(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,schema):
        try:
            return Database.objects.get(schema=schema)
        except Database.DoesNotExist:
            return None
    def post(self,request,format=None):
        schema = request.data.get("schema")
        database = self.get_object(schema)
        if database is not None:
            serializer = DatabaseSerializer(database)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})

class DatabaseDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,schema):
        try:
            return Database.objects.get(schema=schema)
        except Database.DoesNotExist:
            return None
    def post(self,request,format=None):
        schema = request.data.get("schema")
        database = self.get_object(schema)
        if database is not None:
            database.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class DatabaseUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,schema):
        try:
            return Database.objects.get(schema=schema)
        except Database.DoesNotExist:
            return None
    def post(self,request,format=None):
        schema = request.data.get("schema")
        database = self.get_object(schema)
        if database is not None:
            serializer = DatabaseSerializer(database,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})
class DatabaseUpdateWithId(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Database.objects.get(pk=pk)
        except Database.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.data.get("id")
        database = self.get_object(id)
        if database is not None:
            serializer = DatabaseSerializer(database,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})

