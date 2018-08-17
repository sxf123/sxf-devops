transfer-pkg-report-admin:
  file.managed:
    - source: salt://report-admin/files/report-admin.tar.gz
    - name: /home/jcy/retail/report-admin/report-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-report-admin:
  file.directory:
    - name: /home/jcy/retail/report-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-report-admin:
  cmd.run:
    - name: tar -xzvf report-admin.tar.gz
    - cwd: /home/jcy/retail/report-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-report-admin:
  file.absent:
    - name: /home/jcy/retail/report-admin/report-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-report-admin:
  cmd.run:
    - name: sh start.sh report-admin
    - cwd: /home/jcy/retail/report-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg