transfer-pkg-logistics-core:
  file.managed:
    - source: salt://logistics-core/files/logistics-core.tar.gz
    - name: /home/jcy/supply/logistics-core/logistics-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-logistics-core:
  file.directory:
    - name: /home/jcy/supply/logistics-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-logistics-core:
  cmd.run:
    - name: tar -xzvf logistics-core.tar.gz
    - cwd: /home/jcy/supply/logistics-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-logistics-core:
  file.absent:
    - name: /home/jcy/supply/logistics-core/logistics-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-logistics-core:
  cmd.run:
    - name: sh start.sh logistics-core
    - cwd: /home/jcy/supply/logistics-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg