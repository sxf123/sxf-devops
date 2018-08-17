from import_data.import_project import save_project,get_project_fields
from import_data.import_ippool import save_ippool,get_ippool_fields
from import_data.import_domainname import save_domainname,get_domainname_fields
from import_data.import_host import save_host,get_host_field
from django.http import HttpResponse

def import_data(request):
    project_models_dict_list = get_project_fields()
    for p in project_models_dict_list:
        save_project(p)
    return HttpResponse("import successfully")

def import_ip(request):
    ippool_models_dict_list = get_ippool_fields()
    for i in ippool_models_dict_list:
        save_ippool(i)
    return HttpResponse("import ippool successfully")

def import_domain(request):
    domainname_dict_list = get_domainname_fields()
    for d in domainname_dict_list:
        save_domainname(d)
    return HttpResponse("import domainname successfully")

def import_host(request):
    host_dict_list = get_host_field()
    for h in host_dict_list:
        save_host(h)
    return HttpResponse("import host successfully")


