transfer-pkg-warehouse-core:
  file.managed:
    - source: salt://warehouse-core/files/warehouse-core.tar.gz
    - name: /home/jcy/supply/warehouse-core/warehouse-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-warehouse-core:
  file.directory:
    - name: /home/jcy/supply/warehouse-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-warehouse-core:
  cmd.run:
    - name: tar -xzvf warehouse-core.tar.gz
    - cwd: /home/jcy/supply/warehouse-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-warehouse-core:
  file.absent:
    - name: /home/jcy/supply/warehouse-core/warehouse-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-warehouse-core:
  cmd.run:
    - name: sh start.sh warehouse-core
    - cwd: /home/jcy/supply/warehouse-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg