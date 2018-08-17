transfer-pkg-card-admin:
  file.managed:
    - source: salt://card-admin/files/card-admin.tar.gz
    - name: /home/jcy/industry/card-admin/card-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-card-admin:
  file.directory:
    - name: /home/jcy/industry/card-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-card-admin:
  cmd.run:
    - name: tar -xzvf card-admin.tar.gz
    - cwd: /home/jcy/industry/card-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-card-admin:
  file.absent:
    - name: /home/jcy/industry/card-admin/card-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-card-admin:
  cmd.run:
    - name: sh start.sh card-admin
    - cwd: /home/jcy/industry/card-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg