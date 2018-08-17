from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        user = request.user
        return Response({"roles":["{}".format(user)],"name":"{}".format(user),"avatar":""})