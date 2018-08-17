transfer-pkg-retail-gateway:
  file.managed:
    - source: salt://retail-gateway/files/retail-gateway.tar.gz
    - name: /home/jcy/retail/retail-gateway/retail-gateway.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-retail-gateway:
  file.directory:
    - name: /home/jcy/retail/retail-gateway
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-retail-gateway:
  cmd.run:
    - name: tar -xzvf retail-gateway.tar.gz
    - cwd: /home/jcy/retail/retail-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-retail-gateway:
  file.absent:
    - name: /home/jcy/retail/retail-gateway/retail-gateway.tar.gz
    - require:
      - cmd: extract_pkg
start_service-retail-gateway:
  cmd.run:
    - name: sh start.sh retail-gateway
    - cwd: /home/jcy/retail/retail-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg