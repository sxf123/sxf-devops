transfer-pkg-pet-club-gateway:
  file.managed:
    - source: salt://pet-club-gateway/files/pet-club-gateway.tar.gz
    - name: /home/jcy/pet/pet-club-gateway/pet-club-gateway.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-pet-club-gateway:
  file.directory:
    - name: /home/jcy/pet/pet-club-gateway
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-pet-club-gateway:
  cmd.run:
    - name: tar -xzvf pet-club-gateway.tar.gz
    - cwd: /home/jcy/pet/pet-club-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-pet-club-gateway:
  file.absent:
    - name: /home/jcy/pet/pet-club-gateway/pet-club-gateway.tar.gz
    - require:
      - cmd: extract_pkg
start_service-pet-club-gateway:
  cmd.run:
    - name: sh start.sh pet-club-gateway
    - cwd: /home/jcy/pet/pet-club-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg