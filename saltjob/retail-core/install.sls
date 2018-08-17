transfer-pkg-retail-core:
  file.managed:
    - source: salt://retail-core/files/retail-core.tar.gz
    - name: /home/jcy/retail/retail-core/retail-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-retail-core:
  file.directory:
    - name: /home/jcy/retail/retail-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-retail-core:
  cmd.run:
    - name: tar -xzvf retail-core.tar.gz
    - cwd: /home/jcy/retail/retail-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-retail-core:
  file.absent:
    - name: /home/jcy/retail/retail-core/retail-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-retail-core:
  cmd.run:
    - name: sh start.sh retail-core
    - cwd: /home/jcy/retail/retail-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg