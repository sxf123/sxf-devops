transfer-pkg-order-gateway:
  file.managed:
    - source: salt://order-gateway/files/order-gateway.tar.gz
    - name: /home/jcy/order/order-gateway/order-gateway.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-order-gateway:
  file.directory:
    - name: /home/jcy/order/order-gateway
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-order-gateway:
  cmd.run:
    - name: tar -xzvf order-gateway.tar.gz
    - cwd: /home/jcy/order/order-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-order-gateway:
  file.absent:
    - name: /home/jcy/order/order-gateway/order-gateway.tar.gz
    - require:
      - cmd: extract_pkg
start_service-order-gateway:
  cmd.run:
    - name: sh start.sh order-gateway
    - cwd: /home/jcy/order/order-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg