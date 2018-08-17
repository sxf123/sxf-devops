transfer-pkg-logistics-gateway:
  file.managed:
    - source: salt://logistics-gateway/files/logistics-gateway.tar.gz
    - name: /home/jcy/supply/logistics-gateway/logistics-gateway.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-logistics-gateway:
  file.directory:
    - name: /home/jcy/supply/logistics-gateway
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-logistics-gateway:
  cmd.run:
    - name: tar -xzvf logistics-gateway.tar.gz
    - cwd: /home/jcy/supply/logistics-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-logistics-gateway:
  file.absent:
    - name: /home/jcy/supply/logistics-gateway/logistics-gateway.tar.gz
    - require:
      - cmd: extract_pkg
start_service-logistics-gateway:
  cmd.run:
    - name: sh start.sh logistics-gateway
    - cwd: /home/jcy/supply/logistics-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg