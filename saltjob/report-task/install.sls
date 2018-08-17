transfer-pkg-report-task:
  file.managed:
    - source: salt://report-task/files/report-task.tar.gz
    - name: /home/jcy/retail/report-task/report-task.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-report-task:
  file.directory:
    - name: /home/jcy/retail/report-task
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-report-task:
  cmd.run:
    - name: tar -xzvf report-task.tar.gz
    - cwd: /home/jcy/retail/report-task
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-report-task:
  file.absent:
    - name: /home/jcy/retail/report-task/report-task.tar.gz
    - require:
      - cmd: extract_pkg
start_service-report-task:
  cmd.run:
    - name: sh start.sh report-task
    - cwd: /home/jcy/retail/report-task
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg