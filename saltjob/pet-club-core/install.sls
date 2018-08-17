transfer-pkg-pet-club-core:
  file.managed:
    - source: salt://pet-club-core/files/pet-club-core.tar.gz
    - name: /home/jcy/pet/pet-club-core/pet-club-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-pet-club-core:
  file.directory:
    - name: /home/jcy/pet/pet-club-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-pet-club-core:
  cmd.run:
    - name: tar -xzvf pet-club-core.tar.gz
    - cwd: /home/jcy/pet/pet-club-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-pet-club-core:
  file.absent:
    - name: /home/jcy/pet/pet-club-core/pet-club-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-pet-club-core:
  cmd.run:
    - name: sh start.sh pet-club-core
    - cwd: /home/jcy/pet/pet-club-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg