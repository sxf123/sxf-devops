transfer-pkg-goods-core:
  file.managed:
    - source: salt://goods-core/files/goods-core.tar.gz
    - name: /home/jcy/goods/goods-core/goods-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-goods-core:
  file.directory:
    - name: /home/jcy/goods/goods-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-goods-core:
  cmd.run:
    - name: tar -xzvf goods-core.tar.gz
    - cwd: /home/jcy/goods/goods-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-goods-core:
  file.absent:
    - name: /home/jcy/goods/goods-core/goods-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-goods-core:
  cmd.run:
    - name: sh start.sh goods-core
    - cwd: /home/jcy/goods/goods-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg