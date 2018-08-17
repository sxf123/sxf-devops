from rest_framework.response import Response
from rest_framework.views import APIView
from cmdbapi.serializers.DomainNameSerializer import DomainNameSerializer
from cmdb.models.DomainName import DomainName
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from common.append_dns import append_domainname
from common.append_dns import sed_domainname
from common.append_dns import comment_domainname

class DomainNameList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        domainname = DomainName.objects.all()
        serializer = DomainNameSerializer(domainname,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer = DomainNameSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            dns = serializer.data.get("dns").split(".")[0]
            domain_type = serializer.data.get("domain_type")
            ip_address = serializer.data.get("ip")
            append_domainname(dns,domain_type,ip_address)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class DomainNameDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return DomainName.objects.get(pk=pk)
        except DomainName.DoesNotExist:
            return None
    def get(self,request,pk,format=None):
        domainname = self.get_object(pk)
        if domainname is not None:
            serializer = DomainNameSerializer(domainname)
            return Response(serializer.data)
        else:
            return Response({"detail":"not found"})
    def put(self,request,pk,format=None):
        domainname = self.get_object(pk)
        srcstr = "{}                       IN    {}    {}".format(domainname.dns,domainname.domain_type,domainname.ip.ip_address)
        if domainname is not None:
            serializer = DomainNameSerializer(domainname,data = request.data)
            if serializer.is_valid():
                serializer.save()
                deststr = "{}                       IN    {}    {}".format(serializer.data.get("dns"),serializer.data.get("domain_type"),serializer.data.get("ip"))
                sed_domainname(srcstr,deststr)
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"not found"})
    def delete(self,request,pk,format=None):
        domainname = self.get_object(pk)
        if domainname is not None:
            domainname.delete()
            comment_domainname(domainname.dns)
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class DomainNameSearch(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,dns):
        try:
            return DomainName.objects.get(dns=dns)
        except DomainName.DoesNotExist:
            return None
    def post(self,request,format=None):
        dns = request.data.get("dns")
        domainname = self.get_object(dns)
        if domainname is not None:
            serializer = DomainNameSerializer(domainname)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        else:
            return Response({"detail":"not found"})

class DomainNameDelet(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,dns):
        try:
            return DomainName.objects.get(dns=dns)
        except DomainName.DoesNotExist:
            return None
    def post(self,request,format=None):
        dns = request.data.get("dns")
        domainname = self.get_object(dns)
        if domainname is not None:
            domainname.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail":"not found"})

class DomainNameUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,dns):
        try:
            return DomainName.objects.get(dns=dns)
        except DomainName.DoesNotExist:
            return None
    def post(self,request,format=None):
        dns = request.data.get("dns")
        domainname = self.get_object(dns)
        if domainname is not None:
            serializer = DomainNameSerializer(domainname,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})

class DomainNameUpdateWithId(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return DomainName.objects.get(pk=pk)
        except DomainName.DoesNotExist:
            return None
    def post(self,request,format=None):
        id = request.data.get("id")
        domainname = self.get_object(id)
        if domainname is not None:
            serializer = DomainNameSerializer(domainname,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"not found"})