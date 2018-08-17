from rest_framework.views import APIView
from rest_framework.response import Response
from cmdb.models.IpPool import IpPool
from cmdbapi.serializers.IpPoolSerializer import IpPoolSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class IpPoolList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        ippool = IpPool.objects.all()
        serializer = IpPoolSerializer(ippool,many=True)
        return Response(serializer.data)
    def post(self,request,format = None):
        serializer = IpPoolSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class IpPoolDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return IpPool.objects.get(pk=pk)
        except IpPool.DoesNotExist:
            return None
    def get(self,request,pk,format=None):
        ippool = self.get_object(pk)
        if ippool is not None:
            serializer = IpPoolSerializer(ippool)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})
    def put(self,request,pk,format=None):
        ippool = self.get_object(pk)
        if ippool is not None:
            serializer = IpPoolSerializer(ippool,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"not found"})
    def delete(self,request,pk,format = None):
        ippool = self.get_object(pk)
        if ippool is not None:
            ippool.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class IpPollSearch(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,ip_address):
        try:
            return IpPool.objects.get(ip_address=ip_address)
        except IpPool.DoesNotExist:
            return None
    def post(self,request,format=None):
        ip_address = request.data.get("ip_address")
        ippool = self.get_object(ip_address)
        if ippool is not None:
            serializer = IpPoolSerializer(ippool)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})

class IpPoolDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,ip_address):
        try:
            return IpPool.objects.get(ip_address=ip_address)
        except IpPool.DoesNotExist:
            return None
    def post(self,request,format=None):
        ip_address = request.data.get("ip_address")
        ippool = self.get_object(ip_address)
        if ippool is not None:
            ippool.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})
class IpPoolUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,ip_address):
        try:
            return IpPool.objects.get(ip_address=ip_address)
        except IpPool.DoesNotExist:
            return None
    def post(self,request,format=None):
        ip_address = request.data.get("ip_address")
        ippool = self.get_object(ip_address)
        if ippool is not None:
            serializer = IpPoolSerializer(ippool,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})

class IpPoolUpdateWithId(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return IpPool.objects.get(pk=pk)
        except IpPool.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.data.get("id")
        ippool = self.get_object(id)
        if ippool is not None:
            serializer = IpPoolSerializer(ippool,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})
