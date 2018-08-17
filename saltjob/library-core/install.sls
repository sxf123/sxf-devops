transfer-pkg-library-core:
  file.managed:
    - source: salt://library-core/files/library-core.tar.gz
    - name: /home/jcy/library/library-core/library-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-library-core:
  file.directory:
    - name: /home/jcy/library/library-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-library-core:
  cmd.run:
    - name: tar -xzvf library-core.tar.gz
    - cwd: /home/jcy/library/library-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-library-core:
  file.absent:
    - name: /home/jcy/library/library-core/library-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-library-core:
  cmd.run:
    - name: sh start.sh library-core
    - cwd: /home/jcy/library/library-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg