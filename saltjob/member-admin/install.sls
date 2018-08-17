transfer-pkg-member-admin:
  file.managed:
    - source: salt://member-admin/files/member-admin.tar.gz
    - name: /home/jcy/industry/member-admin/member-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-member-admin:
  file.directory:
    - name: /home/jcy/industry/member-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-member-admin:
  cmd.run:
    - name: tar -xzvf member-admin.tar.gz
    - cwd: /home/jcy/industry/member-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-member-admin:
  file.absent:
    - name: /home/jcy/industry/member-admin/member-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-member-admin:
  cmd.run:
    - name: sh start.sh member-admin
    - cwd: /home/jcy/industry/member-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg