transfer-pkg-logistics-admin:
  file.managed:
    - source: salt://logistics-admin/files/logistics-admin.tar.gz
    - name: /home/jcy/supply/logistics-admin/logistics-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-logistics-admin:
  file.directory:
    - name: /home/jcy/supply/logistics-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-logistics-admin:
  cmd.run:
    - name: tar -xzvf logistics-admin.tar.gz
    - cwd: /home/jcy/supply/logistics-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-logistics-admin:
  file.absent:
    - name: /home/jcy/supply/logistics-admin/logistics-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-logistics-admin:
  cmd.run:
    - name: sh start.sh logistics-admin
    - cwd: /home/jcy/supply/logistics-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg