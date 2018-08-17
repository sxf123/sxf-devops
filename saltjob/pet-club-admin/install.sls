transfer-pkg-pet-club-admin:
  file.managed:
    - source: salt://pet-club-admin/files/pet-club-admin.tar.gz
    - name: /home/jcy/pet/pet-club-admin/pet-club-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-pet-club-admin:
  file.directory:
    - name: /home/jcy/pet/pet-club-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-pet-club-admin:
  cmd.run:
    - name: tar -xzvf pet-club-admin.tar.gz
    - cwd: /home/jcy/pet/pet-club-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-pet-club-admin:
  file.absent:
    - name: /home/jcy/pet/pet-club-admin/pet-club-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-pet-club-admin:
  cmd.run:
    - name: sh start.sh pet-club-admin
    - cwd: /home/jcy/pet/pet-club-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg