#/bin/bash

PYENV_DIR=/opt/pyenv36/bin/activate
PROJ_DIR=/opt/zhexin_ops
UWSGI_FILE=${PROJ_DIR}/devops_prod_uwsgi.ini

if [[ $# -eq 0 ]];
then
    echo "usage: sh $0 start | stop"
fi

start() {
    source $PYENV_DIR
    pid=`ps -ef | grep devops_prod_uwsgi | grep -v grep | wc -l`
    if [[ $pid -gt 0 ]];
    then
        cd ${PROJ_DIR}
        uwsgi --stop ${PROJ_DIR}/devops.pid
    fi
    uwsgi --ini $UWSGI_FILE
}

stop() {
    source $PYENV_DIR
    pid=`ps -ef | grep devops_dev_uwsgi | wc -l`
    if [[ $pid -gt 0 ]];
    then
        cd ${PROJ_DIR}
        uwsgi --stop ${PROJ_DIR}/devops.pid
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