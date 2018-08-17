from rest_framework.views import APIView
from cmdb.models.Cluster import Cluster
from cmdbapi.serializers.ClusterSerializer import ClusterGetSerializer,ClusterEditSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ClusterList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        cluster = Cluster.objects.all()
        serializer = ClusterGetSerializer(cluster,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer = ClusterEditSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class ClusterDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Cluster.objects.get(pk=pk)
        except Cluster.DoesNotExist:
            return None
    def get(self,request,pk,format=None):
        cluster = self.get_object(pk)
        if cluster is not None:
            serializer = ClusterGetSerializer(cluster)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})
    def put(self,request,pk,format=None):
        cluster = self.get_object(pk)
        if cluster is not None:
            serializer = ClusterEditSerializer(cluster,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"not found"})
    def delete(self,request,pk,format=None):
        cluster = self.get_object(pk)
        if cluster is not None:
            cluster.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})
class ClusterSearch(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,cluster_name):
        try:
            return Cluster.objects.get(cluster_name=cluster_name)
        except Cluster.DoesNotExist:
            return None
    def post(self,request,format=None):
        cluster_name = request.data.get("cluster_name")
        cluster = self.get_object(cluster_name)
        if cluster is not None:
            serializer = ClusterGetSerializer(cluster)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})

class ClusterDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,cluster_name):
        try:
            return Cluster.objects.get(cluster_name=cluster_name)
        except Cluster.DoesNotExist:
            return None
    def post(self,request,format=None):
        cluster_name = request.data.get("cluster_name")
        cluster = self.get_object(cluster_name)
        if cluster is not None:
            cluster.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})
class ClusterUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,cluster_name):
        try:
            return Cluster.objects.get(cluster_name=cluster_name)
        except Cluster.DoesNotExist:
            return None
    def post(self,request,format=None):
        cluster_name = request.data.get("cluster_name")
        cluster = self.get_object(cluster_name)
        if cluster is not None:
            serializer = ClusterEditSerializer(cluster,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})
class ClusterUpdateWithId(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Cluster.objects.get(pk=pk)
        except Cluster.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.data.get("id")
        cluster = self.get_object(id)
        if cluster is not None:
            serializer = ClusterEditSerializer(cluster,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})
