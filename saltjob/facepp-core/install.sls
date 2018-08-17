transfer-pkg-facepp-core:
  file.managed:
    - source: salt://facepp-core/files/facepp-core.tar.gz
    - name: /home/jcy/face/facepp-core/facepp-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-facepp-core:
  file.directory:
    - name: /home/jcy/face/facepp-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-facepp-core:
  cmd.run:
    - name: tar -xzvf facepp-core.tar.gz
    - cwd: /home/jcy/face/facepp-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-facepp-core:
  file.absent:
    - name: /home/jcy/face/facepp-core/facepp-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-facepp-core:
  cmd.run:
    - name: sh start.sh facepp-core
    - cwd: /home/jcy/face/facepp-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg