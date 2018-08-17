transfer-pkg-order-core:
  file.managed:
    - source: salt://order-core/files/order-core.tar.gz
    - name: /home/jcy/order/order-core/order-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-order-core:
  file.directory:
    - name: /home/jcy/order/order-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-order-core:
  cmd.run:
    - name: tar -xzvf order-core.tar.gz
    - cwd: /home/jcy/order/order-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-order-core:
  file.absent:
    - name: /home/jcy/order/order-core/order-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-order-core:
  cmd.run:
    - name: sh start.sh order-core
    - cwd: /home/jcy/order/order-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg