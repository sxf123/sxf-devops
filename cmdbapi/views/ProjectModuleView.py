from cmdb.models.ProjectModule import ProjectModule
from cmdbapi.serializers.ProjectModuleSerializer import ProjectModuleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ProjectModuleList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        projectmodule = ProjectModule.objects.all()
        serializer = ProjectModuleSerializer(projectmodule,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer = ProjectModuleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class ProjectModuleDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return ProjectModule.objects.get(pk=pk)
        except ProjectModule.DoesNotExist:
            return None
    def get(self,request,pk,format=None):
        projectmodule = self.get_object(pk)
        if projectmodule is not None:
            serializer = ProjectModuleSerializer(projectmodule)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})
    def put(self,request,pk,format=None):
        projectmodule = self.get_object(pk)
        if projectmodule is not None:
            serializer = ProjectModuleSerializer(projectmodule,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"not found"})
    def delete(self,request,pk,format = None):
        projectmodule = self.get_object(pk)
        if projectmodule is not None:
            projectmodule.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class ProjectModuleSearch(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,module_name):
        try:
            return ProjectModule.objects.get(module_name=module_name)
        except ProjectModule.DoesNotExist:
            return None
    def post(self,request,format = None):
        module_name = request.data.get("module_name")
        projectmodule = self.get_object(module_name)
        if projectmodule is not None:
            serializer = ProjectModuleSerializer(projectmodule)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})

class ProjectModuleDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,module_name):
        try:
            return ProjectModule.objects.get(module_name=module_name)
        except ProjectModule.DoesNotExist:
            return None
    def post(self,request,format=None):
        module_name = request.data.get("module_name")
        projectmodule = self.get_object(module_name)
        if projectmodule is not None:
            projectmodule.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})
class ProjectModuleUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,module_name):
        try:
            return ProjectModule.objects.get(module_name=module_name)
        except ProjectModule.DoesNotExist:
            return None
    def post(self,request,format=None):
        module_name = request.data.get("module_name")
        projectmodule = self.get_object(module_name)
        if projectmodule is not None:
            serializer = ProjectModuleSerializer(projectmodule,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})

class ProjectModuleUpdateWithId(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return ProjectModule.objects.get(pk=pk)
        except ProjectModule.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.data.get("id")
        projectmodule = self.get_object(id)
        if projectmodule is not None:
            serializer = ProjectModuleSerializer(projectmodule,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})

