transfer-pkg-supply-chain-gateway:
  file.managed:
    - source: salt://supply-chain-gateway/files/supply-chain-gateway.tar.gz
    - name: /home/jcy/supply/supply-chain-gateway/supply-chain-gateway.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-supply-chain-gateway:
  file.directory:
    - name: /home/jcy/supply/supply-chain-gateway
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-supply-chain-gateway:
  cmd.run:
    - name: tar -xzvf supply-chain-gateway.tar.gz
    - cwd: /home/jcy/supply/supply-chain-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-supply-chain-gateway:
  file.absent:
    - name: /home/jcy/supply/supply-chain-gateway/supply-chain-gateway.tar.gz
    - require:
      - cmd: extract_pkg
start_service-supply-chain-gateway:
  cmd.run:
    - name: sh start.sh supply-chain-gateway
    - cwd: /home/jcy/supply/supply-chain-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg