transfer-pkg-order-admin:
  file.managed:
    - source: salt://order-admin/files/order-admin.tar.gz
    - name: /home/jcy/order/order-admin/order-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-order-admin:
  file.directory:
    - name: /home/jcy/order/order-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-order-admin:
  cmd.run:
    - name: tar -xzvf order-admin.tar.gz
    - cwd: /home/jcy/order/order-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-order-admin:
  file.absent:
    - name: /home/jcy/order/order-admin/order-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-order-admin:
  cmd.run:
    - name: sh start.sh order-admin
    - cwd: /home/jcy/order/order-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg