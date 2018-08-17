transfer-pkg-health-system-api:
  file.managed:
    - source: salt://health-system-api/files/health-system-api.tar.gz
    - name: /home/jcy/health/health-system-api/health-system-api.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-health-system-api:
  file.directory:
    - name: /home/jcy/health/health-system-api
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-health-system-api:
  cmd.run:
    - name: tar -xzvf health-system-api.tar.gz
    - cwd: /home/jcy/health/health-system-api
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-health-system-api:
  file.absent:
    - name: /home/jcy/health/health-system-api/health-system-api.tar.gz
    - require:
      - cmd: extract_pkg
start_service-health-system-api:
  cmd.run:
    - name: sh start.sh health-system-api
    - cwd: /home/jcy/health/health-system-api
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg