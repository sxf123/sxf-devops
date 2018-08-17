transfer-pkg-operate-auction-service:
  file.managed:
    - source: salt://operate-auction-service/files/operate-auction-service.tar.gz
    - name: /home/jcy/operate/operate-auction-service/operate-auction-service.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-operate-auction-service:
  file.directory:
    - name: /home/jcy/operate/operate-auction-service
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-operate-auction-service:
  cmd.run:
    - name: tar -xzvf operate-auction-service.tar.gz
    - cwd: /home/jcy/operate/operate-auction-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-operate-auction-service:
  file.absent:
    - name: /home/jcy/operate/operate-auction-service/operate-auction-service.tar.gz
    - require:
      - cmd: extract_pkg
start_service-operate-auction-service:
  cmd.run:
    - name: sh start.sh operate-auction-service
    - cwd: /home/jcy/operate/operate-auction-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg