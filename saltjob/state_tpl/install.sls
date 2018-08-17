transfer-pkg-projectmodule:
  file.managed:
    - source: salt://projectmodule/files/projectmodule.tar.gz
    - name: /home/jcy/project/projectmodule/projectmodule.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-projectmodule:
  file.directory:
    - name: /home/jcy/project/projectmodule
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-projectmodule:
  cmd.run:
    - name: tar -xzvf projectmodule.tar.gz
    - cwd: /home/jcy/project/projectmodule
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-projectmodule:
  file.absent:
    - name: /home/jcy/project/projectmodule/projectmodule.tar.gz
    - require:
      - cmd: extract_pkg
start_service-projectmodule:
  cmd.run:
    - name: sh start.sh  rojectmodule
    - cwd: /home/jcy/project/projectmodule
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg