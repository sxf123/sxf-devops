transfer-pkg-industry-biz-service:
  file.managed:
    - source: salt://industry-biz-service/files/industry-biz-service.tar.gz
    - name: /home/jcy/industry/industry-biz-service/industry-biz-service.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-industry-biz-service:
  file.directory:
    - name: /home/jcy/industry/industry-biz-service
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-industry-biz-service:
  cmd.run:
    - name: tar -xzvf industry-biz-service.tar.gz
    - cwd: /home/jcy/industry/industry-biz-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-industry-biz-service:
  file.absent:
    - name: /home/jcy/industry/industry-biz-service/industry-biz-service.tar.gz
    - require:
      - cmd: extract_pkg
start_service-industry-biz-service:
  cmd.run:
    - name: sh start.sh industry-biz-service
    - cwd: /home/jcy/industry/industry-biz-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg