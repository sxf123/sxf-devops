transfer-pkg-operate-biz-web:
  file.managed:
    - source: salt://operate-biz-web/files/operate-biz-web.tar.gz
    - name: /home/jcy/operate/operate-biz-web/operate-biz-web.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-operate-biz-web:
  file.directory:
    - name: /home/jcy/operate/operate-biz-web
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-operate-biz-web:
  cmd.run:
    - name: tar -xzvf operate-biz-web.tar.gz
    - cwd: /home/jcy/operate/operate-biz-web
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-operate-biz-web:
  file.absent:
    - name: /home/jcy/operate/operate-biz-web/operate-biz-web.tar.gz
    - require:
      - cmd: extract_pkg
start_service-operate-biz-web:
  cmd.run:
    - name: sh start.sh operate-biz-web
    - cwd: /home/jcy/operate/operate-biz-web
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg