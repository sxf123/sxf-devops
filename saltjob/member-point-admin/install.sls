transfer-pkg-member-point-admin:
  file.managed:
    - source: salt://member-point-admin/files/member-point-admin.tar.gz
    - name: /home/jcy/industry/member-point-admin/member-point-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-member-point-admin:
  file.directory:
    - name: /home/jcy/industry/member-point-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-member-point-admin:
  cmd.run:
    - name: tar -xzvf member-point-admin.tar.gz
    - cwd: /home/jcy/industry/member-point-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-member-point-admin:
  file.absent:
    - name: /home/jcy/industry/member-point-admin/member-point-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-member-point-admin:
  cmd.run:
    - name: sh start.sh member-point-admin
    - cwd: /home/jcy/industry/member-point-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg