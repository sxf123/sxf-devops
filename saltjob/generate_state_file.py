from jinja2 import Template
import os
from devops.settings import DEFAUTL_LOGGER
import logging
import shutil

logger = logging.getLogger(DEFAUTL_LOGGER)

def create_state_dir(projectmodule):
    cwd = os.path.dirname(os.path.abspath(__file__))
    shutil.copytree(os.path.join(cwd,"state_tpl"),os.path.join(cwd,projectmodule))
    logger.info("copy dir successfully")
def write_yaml_file(yaml_dict,yaml_tpl_file,yaml_file):
    with open(yaml_tpl_file,"r") as fd:
        template = Template(fd.read())
    config_content = template.render(**yaml_dict)
    with open(yaml_file,"w") as fd:
        fd.write(config_content)