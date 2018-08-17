transfer-pkg-member-core:
  file.managed:
    - source: salt://member-core/files/member-core.tar.gz
    - name: /home/jcy/industry/member-core/member-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-member-core:
  file.directory:
    - name: /home/jcy/industry/member-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-member-core:
  cmd.run:
    - name: tar -xzvf member-core.tar.gz
    - cwd: /home/jcy/industry/member-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-member-core:
  file.absent:
    - name: /home/jcy/industry/member-core/member-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-member-core:
  cmd.run:
    - name: sh start.sh member-core
    - cwd: /home/jcy/industry/member-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg