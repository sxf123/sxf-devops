transfer-pkg-library-gateway:
  file.managed:
    - source: salt://library-gateway/files/library-gateway.tar.gz
    - name: /home/jcy/retail/library-gateway/library-gateway.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-library-gateway:
  file.directory:
    - name: /home/jcy/retail/library-gateway
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-library-gateway:
  cmd.run:
    - name: tar -xzvf library-gateway.tar.gz
    - cwd: /home/jcy/retail/library-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-library-gateway:
  file.absent:
    - name: /home/jcy/retail/library-gateway/library-gateway.tar.gz
    - require:
      - cmd: extract_pkg
start_service-library-gateway:
  cmd.run:
    - name: sh start.sh library-gateway
    - cwd: /home/jcy/retail/library-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg