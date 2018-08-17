transfer-pkg-industry-biz-web:
  file.managed:
    - source: salt://industry-biz-web/files/industry-biz-web.tar.gz
    - name: /home/jcy/industry/industry-biz-web/industry-biz-web.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-industry-biz-web:
  file.directory:
    - name: /home/jcy/industry/industry-biz-web
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-industry-biz-web:
  cmd.run:
    - name: tar -xzvf industry-biz-web.tar.gz
    - cwd: /home/jcy/industry/industry-biz-web
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-industry-biz-web:
  file.absent:
    - name: /home/jcy/industry/industry-biz-web/industry-biz-web.tar.gz
    - require:
      - cmd: extract_pkg
start_service-industry-biz-web:
  cmd.run:
    - name: sh start.sh industry-biz-web
    - cwd: /home/jcy/industry/industry-biz-web
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg