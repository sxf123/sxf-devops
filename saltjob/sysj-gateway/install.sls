transfer-pkg-sysj-gateway:
  file.managed:
    - source: salt://sysj-gateway/files/sysj-gateway.tar.gz
    - name: /home/jcy/sysj/sysj-gateway/sysj-gateway.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-sysj-gateway:
  file.directory:
    - name: /home/jcy/sysj/sysj-gateway
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-sysj-gateway:
  cmd.run:
    - name: tar -xzvf sysj-gateway.tar.gz
    - cwd: /home/jcy/sysj/sysj-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-sysj-gateway:
  file.absent:
    - name: /home/jcy/sysj/sysj-gateway/sysj-gateway.tar.gz
    - require:
      - cmd: extract_pkg
start_service-sysj-gateway:
  cmd.run:
    - name: sh start.sh sysj-gateway
    - cwd: /home/jcy/sysj/sysj-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg