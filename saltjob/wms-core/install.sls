transfer-pkg-wms-core:
  file.managed:
    - source: salt://wms-core/files/wms-core.tar.gz
    - name: /home/jcy/supply/wms-core/wms-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-wms-core:
  file.directory:
    - name: /home/jcy/supply/wms-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-wms-core:
  cmd.run:
    - name: tar -xzvf wms-core.tar.gz
    - cwd: /home/jcy/supply/wms-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-wms-core:
  file.absent:
    - name: /home/jcy/supply/wms-core/wms-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-wms-core:
  cmd.run:
    - name: sh start.sh wms-core
    - cwd: /home/jcy/supply/wms-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg