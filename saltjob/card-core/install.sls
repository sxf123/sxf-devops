transfer-pkg-card-core:
  file.managed:
    - source: salt://card-core/files/card-core.tar.gz
    - name: /home/jcy/industry/card-core/card-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-card-core:
  file.directory:
    - name: /home/jcy/industry/card-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-card-core:
  cmd.run:
    - name: tar -xzvf card-core.tar.gz
    - cwd: /home/jcy/industry/card-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-card-core:
  file.absent:
    - name: /home/jcy/industry/card-core/card-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-card-core:
  cmd.run:
    - name: sh start.sh card-core
    - cwd: /home/jcy/industry/card-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg