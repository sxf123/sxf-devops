from jenkins import Jenkins
from devops.settings import JENKINS_URL,JENKINS_TOKEN,JENKINS_USER
import jenkins

def get_server():
    server = Jenkins(JENKINS_URL,JENKINS_USER,JENKINS_TOKEN)
    return server

def get_node():
    server = get_server()
    return server.get_nodes()

def create_node(port,user,credentialsId,host,javaPath,name):
    server = get_server()
    params = {
        "port": port,
        "user": user,
        "credentialsId": credentialsId,
        "host": host,
        "javaPaht": javaPath
    }
    try:
        server.create_node(
            name,
            nodeDescription=name,
            remoteFS="/opt/jenkins",
            exclusive=True,
            launcher=jenkins.LAUNCHER_SSH,
            launcher_params=params
        )
        return 1
    except jenkins.JenkinsException as e:
        print(e)
        return 0

def search_node():
    server = get_server()
    return server.get_nodes(0)