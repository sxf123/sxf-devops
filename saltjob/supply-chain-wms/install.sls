transfer-pkg-supply-chain-wms:
  file.managed:
    - source: salt://supply-chain-wms/files/supply-chain-wms.tar.gz
    - name: /home/jcy/supply/supply-chain-wms/supply-chain-wms.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-supply-chain-wms:
  file.directory:
    - name: /home/jcy/supply/supply-chain-wms
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-supply-chain-wms:
  cmd.run:
    - name: tar -xzvf supply-chain-wms.tar.gz
    - cwd: /home/jcy/supply/supply-chain-wms
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-supply-chain-wms:
  file.absent:
    - name: /home/jcy/supply/supply-chain-wms/supply-chain-wms.tar.gz
    - require:
      - cmd: extract_pkg
start_service-supply-chain-wms:
  cmd.run:
    - name: sh start.sh supply-chain-wms
    - cwd: /home/jcy/supply/supply-chain-wms
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg