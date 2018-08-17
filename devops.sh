#/bin/bash

PYENV_DIR=/root/py36env/bin/activate
PROJ_DIR=/root/devops-dev/devops
UWSGI_FILE=/root/devops-dev/devops/devops_dev_uwsgi.ini

if [[ $# -eq 0 ]];
then
    echo "usage: sh $0 start | stop"
fi

start() {
    source $PYENV_DIR
    pid=`ps -ef | grep devosp_dev_uwsgi | grep -v grep | wc -l`
    if [[ $pid -gt 0 ]];
    then
        uwsgi --stop $PROJ_DIR/devops.pid
    fi
    uwsgi --ini $UWSGI_FILE
}

stop() {
    source $PYENV_DIR
    pid=`ps -ef | grep devops_dev_uwsgi | wc -l`
    if [[ $pid -gt 0 ]];
    then
        uwsgi --stop $PROJ_DIR/devops.pid
    fi
}

case "$1" in
    "start")
        start
        ;;
    "stop")
        stop
        ;;
esac