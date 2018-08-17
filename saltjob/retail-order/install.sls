transfer-pkg-retail-order:
  file.managed:
    - source: salt://retail-order/files/retail-order.tar.gz
    - name: /home/jcy/retail/retail-order/retail-order.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-retail-order:
  file.directory:
    - name: /home/jcy/retail/retail-order
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-retail-order:
  cmd.run:
    - name: tar -xzvf retail-order.tar.gz
    - cwd: /home/jcy/retail/retail-order
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-retail-order:
  file.absent:
    - name: /home/jcy/retail/retail-order/retail-order.tar.gz
    - require:
      - cmd: extract_pkg
start_service-retail-order:
  cmd.run:
    - name: sh start.sh retail-order
    - cwd: /home/jcy/retail/retail-order
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg