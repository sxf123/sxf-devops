from django.views.generic import View
from django.http import JsonResponse
from cmdb.models.RdsSchema import RdsSchema
from django.contrib.auth.models import Group

class SchemaView(View):
    def __init__(self):
        self.context = {}
    def post(self,request,*args,**kwargs):
        rdsinstance = request.POST.get("rdsinstance")
        rdsschema = list(RdsSchema.objects.filter(rdsinstance__instance_name=rdsinstance).values_list("schema_name","schema_name"))
        rdsschema_list = []
        for r in rdsschema:
            rdsschem_dict = {"id":r[0],"text":r[1]}
            rdsschema_list.append(rdsschem_dict)
        return JsonResponse({"rdsschema":rdsschema_list})

class VerifyPersonView(View):
    def __init__(self):
        self.context = {}
    def post(self,request,*args,**kwargs):
        need_test = request.POST.get("need_test")
        group = Group.objects.get(name="test")
        # verify_person = list(group.user_set.all().values_list("username","username"))
        verify_persons = group.user_set.all()
        verify_person = [(v.username,v.first_name + v.last_name) for v in verify_persons]
        verify_person_list = []
        for v in verify_person:
            verify_person_dict = {"id":v[0], "text":v[1]}
            verify_person_list.append(verify_person_dict)
        return JsonResponse({"verify_person":verify_person_list})
