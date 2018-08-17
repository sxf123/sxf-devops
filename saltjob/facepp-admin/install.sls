transfer-pkg-facepp-admin:
  file.managed:
    - source: salt://facepp-admin/files/facepp-admin.tar.gz
    - name: /home/jcy/face/facepp-admin/facepp-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-facepp-admin:
  file.directory:
    - name: /home/jcy/face/facepp-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-facepp-admin:
  cmd.run:
    - name: tar -xzvf facepp-admin.tar.gz
    - cwd: /home/jcy/face/facepp-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-facepp-admin:
  file.absent:
    - name: /home/jcy/face/facepp-admin/facepp-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-facepp-admin:
  cmd.run:
    - name: sh start.sh facepp-admin
    - cwd: /home/jcy/face/facepp-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg