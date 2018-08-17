transfer-pkg-supply-print:
  file.managed:
    - source: salt://supply-print/files/supply-print.tar.gz
    - name: /home/jcy/supply/supply-print/supply-print.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-supply-print:
  file.directory:
    - name: /home/jcy/supply/supply-print
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-supply-print:
  cmd.run:
    - name: tar -xzvf supply-print.tar.gz
    - cwd: /home/jcy/supply/supply-print
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-supply-print:
  file.absent:
    - name: /home/jcy/supply/supply-print/supply-print.tar.gz
    - require:
      - cmd: extract_pkg
start_service-supply-print:
  cmd.run:
    - name: sh start.sh supply-print
    - cwd: /home/jcy/supply/supply-print
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg