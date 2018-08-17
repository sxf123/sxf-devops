transfer-pkg-logistics-passageway:
  file.managed:
    - source: salt://logistics-passageway/files/logistics-passageway.tar.gz
    - name: /home/jcy/supply/logistics-passageway/logistics-passageway.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-logistics-passageway:
  file.directory:
    - name: /home/jcy/supply/logistics-passageway
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-logistics-passageway:
  cmd.run:
    - name: tar -xzvf logistics-passageway.tar.gz
    - cwd: /home/jcy/supply/logistics-passageway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-logistics-passageway:
  file.absent:
    - name: /home/jcy/supply/logistics-passageway/logistics-passageway.tar.gz
    - require:
      - cmd: extract_pkg
start_service-logistics-passageway:
  cmd.run:
    - name: sh start.sh logistics-passageway
    - cwd: /home/jcy/supply/logistics-passageway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg