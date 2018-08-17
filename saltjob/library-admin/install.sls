transfer-pkg-library-admin:
  file.managed:
    - source: salt://library-admin/files/library-admin.tar.gz
    - name: /home/jcy/library/library-admin/library-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-library-admin:
  file.directory:
    - name: /home/jcy/library/library-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-library-admin:
  cmd.run:
    - name: tar -xzvf library-admin.tar.gz
    - cwd: /home/jcy/library/library-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-library-admin:
  file.absent:
    - name: /home/jcy/library/library-admin/library-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-library-admin:
  cmd.run:
    - name: sh start.sh library-admin
    - cwd: /home/jcy/library/library-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg