transfer-pkg-supply-chain-admin:
  file.managed:
    - source: salt://supply-chain-admin/files/supply-chain-admin.tar.gz
    - name: /home/jcy/supply/supply-chain-admin/supply-chain-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-supply-chain-admin:
  file.directory:
    - name: /home/jcy/supply/supply-chain-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-supply-chain-admin:
  cmd.run:
    - name: tar -xzvf supply-chain-admin.tar.gz
    - cwd: /home/jcy/supply/supply-chain-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-supply-chain-admin:
  file.absent:
    - name: /home/jcy/supply/supply-chain-admin/supply-chain-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-supply-chain-admin:
  cmd.run:
    - name: sh start.sh supply-chain-admin
    - cwd: /home/jcy/supply/supply-chain-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg