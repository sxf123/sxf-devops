from rest_framework.response import Response
from rest_framework.views import APIView
from cmdbapi.serializers.ProcessSerializer import ProcessSerializer
from rest_framework import status
from cmdb.models.Process import Process

class ProcessList(APIView):
    def post(self,request,format=None):
        serializer = ProcessSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProcessUpdate(APIView):
    def get_object(self,pk):
        try:
            return Process.objects.get(pk=pk)
        except Process.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.data.get("id")
        process = self.get_object(id)
        if process is not None:
            serializer = ProcessSerializer(process,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})
