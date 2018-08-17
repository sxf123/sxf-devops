transfer-pkg-operate-biz-service:
  file.managed:
    - source: salt://operate-biz-service/files/operate-biz-service.tar.gz
    - name: /home/jcy/operate/operate-biz-service/operate-biz-service.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-operate-biz-service:
  file.directory:
    - name: /home/jcy/operate/operate-biz-service
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-operate-biz-service:
  cmd.run:
    - name: tar -xzvf operate-biz-service.tar.gz
    - cwd: /home/jcy/operate/operate-biz-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-operate-biz-service:
  file.absent:
    - name: /home/jcy/operate/operate-biz-service/operate-biz-service.tar.gz
    - require:
      - cmd: extract_pkg
start_service-operate-biz-service:
  cmd.run:
    - name: sh start.sh operate-biz-service
    - cwd: /home/jcy/operate/operate-biz-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg