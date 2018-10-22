from rest_framework.response import Response
from rest_framework.views import APIView
from cmdbapi.serializers.ProcessSerializer import ProcessSerializer
from rest_framework import status
from cmdb.models.Process import Process
from cmdb.models.EcsHost import EcsHost

class ProcessList(APIView):
    def get(self,request,format=None):
        process = Process.objects.all()
        serializer = ProcessSerializer(process,many=True)
        return Response(serializer.data)
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

class ProcessDetail(APIView):
    def post(self,request,format=None):
        process_name = request.data.get("process_name")
        process_id = request.data.get("porcess_id")
        ecshost = request.data.get("ecshost")
        process = Process.objects.filter(process_name=process_name).filter(process_id=process_id).filter(ecshost__minion_id=ecshost)[0]
        if process.exists():
            serializer = ProcessSerializer(process)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})
