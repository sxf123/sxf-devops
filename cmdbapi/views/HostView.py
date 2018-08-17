from rest_framework.views import APIView
from cmdb.models.Host import Host
from cmdbapi.serializers.HostSerializer import HostGetSerializer
from cmdbapi.serializers.IpPoolSerializer import IpPoolSerializer
from cmdb.models.IpPool import IpPool
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class HostList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        host = Host.objects.all()
        serializer = HostGetSerializer(host,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer = HostGetSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class HostDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Host.objects.get(pk=pk)
        except Host.DoesNotExist:
            return None
    def get(self,request,pk,format=None):
        host = self.get_object(pk)
        if host is not None:
            serializer = HostGetSerializer(host)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})
    def put(self,request,pk,format=None):
        host = self.get_object(pk)
        if host is not None:
            serializer = HostGetSerializer(host,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"not found"})
    def delete(self,request,pk,format=None):
        host = self.get_object(pk)
        if host is not None:
            host.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class HostSearch(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,host_name):
        try:
            return Host.objects.get(host_name=host_name)
        except Host.DoesNotExist:
            return None
    def post(self,request,format=None):
        host_name = request.data.get("host_name")
        host = self.get_object(host_name)
        if host is not None:
            serializer = HostGetSerializer(host)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})

class HostDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,host_name):
        try:
            return Host.objects.get(host_name=host_name)
        except Host.DoesNotExist:
            return None
    def post(self,request,format=None):
        host_name = request.data.get("host_name")
        host = self.get_object(host_name)
        if host is not None:
            host.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class HostUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,host_name):
        try:
            return Host.objects.get(host_name=host_name)
        except Host.DoesNotExist:
            return None
    def post(self,request,format=None):
        host_name = request.data.get("host_name")
        host = self.get_object(host_name)
        if host is not None:
            serializer = HostEditSerializer(host,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})

class HostUpdateWithId(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Host.objects.get(pk=pk)
        except Host.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.data.get("id")
        host = self.get_object(id)
        if host is not None:
            serializer = HostGetSerializer(host,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})
