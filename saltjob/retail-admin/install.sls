transfer-pkg-retail-admin:
  file.managed:
    - source: salt://retail-admin/files/retail-admin.tar.gz
    - name: /home/jcy/retail/retail-admin/retail-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-retail-admin:
  file.directory:
    - name: /home/jcy/retail/retail-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-retail-admin:
  cmd.run:
    - name: tar -xzvf retail-admin.tar.gz
    - cwd: /home/jcy/retail/retail-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-retail-admin:
  file.absent:
    - name: /home/jcy/retail/retail-admin/retail-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-retail-admin:
  cmd.run:
    - name: sh start.sh retail-admin
    - cwd: /home/jcy/retail/retail-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg