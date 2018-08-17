from rest_framework.response import Response
from rest_framework.views import APIView
from cmdb.models.Project import Project
from cmdbapi.serializers.ProjectSerializer import ProjectEditSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ProjectList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        project = Project.objects.all()
        serializer = ProjectEditSerializer(project,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer = ProjectEditSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class ProjectDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return None
    def get(self,request,pk,format=None):
        project = self.get_object(pk)
        if project is not None:
            serializer = ProjectEditSerializer(project)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})
    def put(self,request,pk,format=None):
        project = self.get_object(pk)
        if project is not None:
            serializer = ProjectEditSerializer(project,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"not found"})
    def delete(self,request,pk,format=None):
        project = self.get_object(pk)
        if project is not None:
            project.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class ProjectSearch(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,name):
        try:
            return Project.objects.get(name=name)
        except Project.DoesNotExist:
            return None
    def post(self,request,format=None):
        name = request.data.get("name")
        project = self.get_object(name)
        if project is not None:
            serializer = ProjectEditSerializer(project)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})

class ProjectDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,name):
        try:
            return Project.objects.get(name=name)
        except Project.DoesNotExist:
            return None
    def post(self,request,format=None):
        name = request.data.get("name")
        project = self.get_object(name)
        if project is not None:
            project.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})
class ProjectUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,name):
        try:
            return Project.objects.get(name=name)
        except Project.DoesNotExist:
            return None
    def post(self,request,format=None):
        name = request.data.get("name")
        project = self.get_object(name)
        if project is not None:
            serializer = ProjectEditSerializer(project,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})

class ProjectUpdateWithId(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.data.get("id")
        project = self.get_object(id)
        if project is not None:
            serializer = ProjectEditSerializer(project,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})