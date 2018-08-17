transfer-pkg-industry-edu-service:
  file.managed:
    - source: salt://industry-edu-service/files/industry-edu-service.tar.gz
    - name: /home/jcy/industry/industry-edu-service/industry-edu-service.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-industry-edu-service:
  file.directory:
    - name: /home/jcy/industry/industry-edu-service
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-industry-edu-service:
  cmd.run:
    - name: tar -xzvf industry-edu-service.tar.gz
    - cwd: /home/jcy/industry/industry-edu-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-industry-edu-service:
  file.absent:
    - name: /home/jcy/industry/industry-edu-service/industry-edu-service.tar.gz
    - require:
      - cmd: extract_pkg
start_service-industry-edu-service:
  cmd.run:
    - name: sh start.sh industry-edu-service
    - cwd: /home/jcy/industry/industry-edu-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg