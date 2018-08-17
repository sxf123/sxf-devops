transfer-pkg-member-point-core:
  file.managed:
    - source: salt://member-point-core/files/member-point-core.tar.gz
    - name: /home/jcy/industry/member-point-core/member-point-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-member-point-core:
  file.directory:
    - name: /home/jcy/industry/member-point-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-member-point-core:
  cmd.run:
    - name: tar -xzvf member-point-core.tar.gz
    - cwd: /home/jcy/industry/member-point-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-member-point-core:
  file.absent:
    - name: /home/jcy/industry/member-point-core/member-point-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-member-point-core:
  cmd.run:
    - name: sh start.sh member-point-core
    - cwd: /home/jcy/industry/member-point-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg