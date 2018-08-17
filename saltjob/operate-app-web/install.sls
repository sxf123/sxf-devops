transfer-pkg-operate-app-web:
  file.managed:
    - source: salt://operate-app-web/files/operate-app-web.tar.gz
    - name: /home/jcy/operate/operate-app-web/operate-app-web.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-operate-app-web:
  file.directory:
    - name: /home/jcy/operate/operate-app-web
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-operate-app-web:
  cmd.run:
    - name: tar -xzvf operate-app-web.tar.gz
    - cwd: /home/jcy/operate/operate-app-web
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-operate-app-web:
  file.absent:
    - name: /home/jcy/operate/operate-app-web/operate-app-web.tar.gz
    - require:
      - cmd: extract_pkg
start_service-operate-app-web:
  cmd.run:
    - name: sh start.sh operate-app-web
    - cwd: /home/jcy/operate/operate-app-web
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg