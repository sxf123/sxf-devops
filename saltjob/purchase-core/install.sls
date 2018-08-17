transfer-pkg-purchase-core:
  file.managed:
    - source: salt://purchase-core/files/purchase-core.tar.gz
    - name: /home/jcy/supply/purchase-core/purchase-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-purchase-core:
  file.directory:
    - name: /home/jcy/supply/purchase-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-purchase-core:
  cmd.run:
    - name: tar -xzvf purchase-core.tar.gz
    - cwd: /home/jcy/supply/purchase-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-purchase-core:
  file.absent:
    - name: /home/jcy/supply/purchase-core/purchase-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-purchase-core:
  cmd.run:
    - name: sh start.sh purchase-core
    - cwd: /home/jcy/supply/purchase-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg