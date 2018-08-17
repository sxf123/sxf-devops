transfer-pkg-supply-task:
  file.managed:
    - source: salt://supply-task/files/supply-task.tar.gz
    - name: /home/jcy/supply/supply-task/supply-task.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-supply-task:
  file.directory:
    - name: /home/jcy/supply/supply-task
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-supply-task:
  cmd.run:
    - name: tar -xzvf supply-task.tar.gz
    - cwd: /home/jcy/supply/supply-task
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-supply-task:
  file.absent:
    - name: /home/jcy/supply/supply-task/supply-task.tar.gz
    - require:
      - cmd: extract_pkg
start_service-supply-task:
  cmd.run:
    - name: sh start.sh supply-task
    - cwd: /home/jcy/supply/supply-task
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg