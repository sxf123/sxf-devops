transfer-pkg-sysj-core:
  file.managed:
    - source: salt://sysj-core/files/sysj-core.tar.gz
    - name: /home/jcy/sysj/sysj-core/sysj-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-sysj-core:
  file.directory:
    - name: /home/jcy/sysj/sysj-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-sysj-core:
  cmd.run:
    - name: tar -xzvf sysj-core.tar.gz
    - cwd: /home/jcy/sysj/sysj-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-sysj-core:
  file.absent:
    - name: /home/jcy/sysj/sysj-core/sysj-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-sysj-core:
  cmd.run:
    - name: sh start.sh sysj-core
    - cwd: /home/jcy/sysj/sysj-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg