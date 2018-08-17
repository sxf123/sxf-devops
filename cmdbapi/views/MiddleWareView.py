from rest_framework.response import Response
from rest_framework.views import APIView
from cmdbapi.serializers.MiddleWareSerializer import MiddleWareSerializer
from cmdb.models.MiddleWare import MiddleWare
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from saltjob.install_salt import run_state

class MiddleWareList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format = None):
        middleware = MiddleWare.objects.all()
        serializer = MiddleWareSerializer(middleware,many=True)
        return Response(serializer.data)
    def post(self,request,format = None):
        serializer = MiddleWareSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class MiddleWareDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return MiddleWare.objects.get(pk=pk)
        except MiddleWare.DoesNotExist:
            return None
    def get(self,request,pk,format=None):
        middleware = self.get_object(pk)
        if middleware is not None:
            serializer = MiddleWareSerializer(middleware)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})
    def put(self,request,pk,format=None):
        middleware = self.get_object(pk)
        if middleware is not None:
            serializer = MiddleWareSerializer(middleware,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"not found"})
    def delete(self,request,pk,format=None):
        middleware = self.get_object(pk)
        if middleware is not None:
            middleware.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class MiddleWareSearch(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,mid_name):
        try:
            return MiddleWare.objects.get(mid_name=mid_name)
        except MiddleWare.DoesNotExist:
            return None
    def post(self,request,format=None):
        mid_name = request.data.get("mid_name")
        middleware = self.get_object(mid_name)
        if middleware is not None:
            serializer = MiddleWareSerializer(middleware)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})

class MiddleWareDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,mid_name):
        try:
            return MiddleWare.objects.get(mid_name=mid_name)
        except MiddleWare.DoesNotExist:
            return None
    def post(self,request,format=None):
        mid_name = request.data.get("mid_name")
        middleware = self.get_object(mid_name)
        if middleware is not None:
            middleware.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})
class MiddleWareUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,mid_name):
        try:
            return MiddleWare.objects.get(mid_name=mid_name)
        except MiddleWare.DoesNotExist:
            return None
    def post(self,request,format=None):
        mid_name = request.data.get("mid_name")
        middleware = self.get_object(mid_name)
        if middleware is not None:
            serializer = MiddleWareSerializer(middleware,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})

class MiddleWareInstall(APIView):
    def post(self,request,format=None):
        tgt = request.data.get("target")
        tgt_type = request.data.get("target_type")
        res = run_state(tgt,tgt_type)
        return Response(res)

class MiddleWareUpdateWithId(APIView):
    def get_object(self,pk):
        try:
            return MiddleWare.objects.get(pk=pk)
        except MiddleWare.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.get("id")
        middleware = self.get_object(id)
        if middleware is not None:
            serializer = MiddleWareSerializer(middleware,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})
