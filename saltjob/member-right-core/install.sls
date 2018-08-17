transfer-pkg-member-right-core:
  file.managed:
    - source: salt://member-right-core/files/member-right-core.tar.gz
    - name: /home/jcy/industry/member-right-core/member-right-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-member-right-core:
  file.directory:
    - name: /home/jcy/industry/member-right-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-member-right-core:
  cmd.run:
    - name: tar -xzvf member-right-core.tar.gz
    - cwd: /home/jcy/industry/member-right-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-member-right-core:
  file.absent:
    - name: /home/jcy/industry/member-right-core/member-right-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-member-right-core:
  cmd.run:
    - name: sh start.sh member-right-core
    - cwd: /home/jcy/industry/member-right-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg