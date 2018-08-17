transfer-pkg-industry-officialsite-service:
  file.managed:
    - source: salt://industry-officialsite-service/files/industry-officialsite-service.tar.gz
    - name: /home/jcy/industry/industry-officialsite-service/industry-officialsite-service.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-industry-officialsite-service:
  file.directory:
    - name: /home/jcy/industry/industry-officialsite-service
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-industry-officialsite-service:
  cmd.run:
    - name: tar -xzvf industry-officialsite-service.tar.gz
    - cwd: /home/jcy/industry/industry-officialsite-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-industry-officialsite-service:
  file.absent:
    - name: /home/jcy/industry/industry-officialsite-service/industry-officialsite-service.tar.gz
    - require:
      - cmd: extract_pkg
start_service-industry-officialsite-service:
  cmd.run:
    - name: sh start.sh industry-officialsite-service
    - cwd: /home/jcy/industry/industry-officialsite-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg