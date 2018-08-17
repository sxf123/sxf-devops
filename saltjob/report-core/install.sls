transfer-pkg-report-core:
  file.managed:
    - source: salt://report-core/files/report-core.tar.gz
    - name: /home/jcy/retail/report-core/report-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-report-core:
  file.directory:
    - name: /home/jcy/retail/report-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-report-core:
  cmd.run:
    - name: tar -xzvf report-core.tar.gz
    - cwd: /home/jcy/retail/report-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-report-core:
  file.absent:
    - name: /home/jcy/retail/report-core/report-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-report-core:
  cmd.run:
    - name: sh start.sh report-core
    - cwd: /home/jcy/retail/report-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg