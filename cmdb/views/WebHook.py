from django.http import JsonResponse
from django.views.generic import View
import json

class WebHookTrigger(View):
    def post(self,request,*args,**kwargs):
        task = request.body
        print(json.loads(task))
        return JsonResponse(json.loads(task))