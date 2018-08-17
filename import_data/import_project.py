from cmdb.models.Project import Project
import os

def save_project(project_model_dict):
    name = project_model_dict.get("name")
    real_name = project_model_dict.get("real_name")
    description = project_model_dict.get("description")
    dev_leading = project_model_dict.get("dev_leading")
    test_leading = project_model_dict.get("test_leading")
    proj_leading = project_model_dict.get("proj_leading")
    ops_leading = project_model_dict.get("ops_leading")
    environment = project_model_dict.get("environment")
    project = Project(
        name=name,
        real_name=real_name,
        description=description,
        dev_leading=dev_leading,
        test_leading=test_leading,
        proj_leading=proj_leading,
        ops_leading=ops_leading,
        environment=environment
    )
    project.save()
def get_project_fields():
    cwd = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(cwd,"project.txt")
    with open(filename,"r",encoding="utf-8") as f:
        project_model_list = [p for p in f.readlines()]
        f.close()
    project_models_dict = []
    for p in project_model_list:
        project = {
            "name":p.split(",")[0],
            "real_name":p.split(",")[1],
            "description":p.split(",")[2],
            "dev_leading":p.split(",")[3],
            "test_leading":p.split(",")[4],
            "proj_leading":p.split(",")[5],
            "ops_leading":p.split(",")[6],
            "environment":p.split(",")[7].strip("\n")
        }
        project_models_dict.append(project)
    return project_models_dict

if __name__ == "__main__":
    project_models_dict_list = get_project_fields()
    for p in project_models_dict_list:
        save_project(**p)
