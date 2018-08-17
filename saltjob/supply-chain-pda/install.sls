transfer-pkg-supply-chain-pda:
  file.managed:
    - source: salt://supply-chain-pda/files/supply-chain-pda.tar.gz
    - name: /home/jcy/supply/supply-chain-pda/supply-chain-pda.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-supply-chain-pda:
  file.directory:
    - name: /home/jcy/supply/supply-chain-pda
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-supply-chain-pda:
  cmd.run:
    - name: tar -xzvf supply-chain-pda.tar.gz
    - cwd: /home/jcy/supply/supply-chain-pda
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-supply-chain-pda:
  file.absent:
    - name: /home/jcy/supply/supply-chain-pda/supply-chain-pda.tar.gz
    - require:
      - cmd: extract_pkg
start_service-supply-chain-pda:
  cmd.run:
    - name: sh start.sh supply-chain-pda
    - cwd: /home/jcy/supply/supply-chain-pda
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg