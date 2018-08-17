transfer-pkg-face-gateway:
  file.managed:
    - source: salt://face-gateway/files/face-gateway.tar.gz
    - name: /home/jcy/face/face-gateway/face-gateway.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-face-gateway:
  file.directory:
    - name: /home/jcy/face/face-gateway
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-face-gateway:
  cmd.run:
    - name: tar -xzvf face-gateway.tar.gz
    - cwd: /home/jcy/face/face-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-face-gateway:
  file.absent:
    - name: /home/jcy/face/face-gateway/face-gateway.tar.gz
    - require:
      - cmd: extract_pkg
start_service-face-gateway:
  cmd.run:
    - name: sh start.sh face-gateway
    - cwd: /home/jcy/face/face-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg