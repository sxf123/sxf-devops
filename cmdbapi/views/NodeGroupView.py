from rest_framework.views import APIView
from cmdb.models.NodeGroup import NodeGroup
from cmdbapi.serializers.NodeGroupSerializer import NodeGroupEditSerializer,NodeGroupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class NodeGroupList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        nodegroup = NodeGroup.objects.all()
        serializer = NodeGroupSerializer(nodegroup,many=True)
        return Response(serializer.data)
    def post(self,reqeust,format=None):
        serializer = NodeGroupEditSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
class NodeGroupDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return NodeGroup.objects.get(pk=pk)
        except NodeGroup.DoesNotExist:
            return None
    def get(self,request,pk,format=None):
        nodegroup = self.get_object(pk)
        if nodegroup is not None:
            serializer = NodeGroupSerializer(nodegroup)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})

class NodeGroupSearch(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,nodegroup):
        try:
            return NodeGroup.objects.get(nodegroup=nodegroup)
        except NodeGroup.DoesNotExist:
            return None
    def post(self,request,format=None):
        nodegroup_name = request.data.get("nodegroup")
        nodegroup = self.get_object(nodegroup_name)
        if nodegroup is not None:
            serializer = NodeGroupSerializer(nodegroup)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})
class NodeGroupDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,nodegroup):
        try:
            return NodeGroup.objects.get(nodegroup=nodegroup)
        except NodeGroup.DoesNotExist:
            return None
    def post(self,request,format=None):
        nodegroup_name = request.data.get("nodegroup")
        nodegroup = self.get_object(nodegroup_name)
        if nodegroup is not None:
            nodegroup.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})
class NodeGroupUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,nodegroup):
        try:
            return NodeGroup.objects.get(nodegroup=nodegroup)
        except NodeGroup.DoesNotExist:
            return None
    def post(self,request,format=None):
        nodegroup_name = request.data.get("nodegroup")
        nodegroup = self.get_object(nodegroup_name)
        if nodegroup is not None:
            nodegroup.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        return Response({"detail":"not found"})

class NodeGroupUpdateWithId(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return NodeGroup.objects.get(pk=pk)
        except NodeGroup.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.data.get("id")
        nodegroup = self.get_object(id)
        if nodegroup is not None:
            serializer = NodeGroupEditSerializer(nodegroup,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})
