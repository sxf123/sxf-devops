transfer-pkg-health-gateway-api:
  file.managed:
    - source: salt://health-gateway-api/files/health-gateway-api.tar.gz
    - name: /home/jcy/health/health-gateway-api/health-gateway-api.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-health-gateway-api:
  file.directory:
    - name: /home/jcy/health/health-gateway-api
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-health-gateway-api:
  cmd.run:
    - name: tar -xzvf health-gateway-api.tar.gz
    - cwd: /home/jcy/health/health-gateway-api
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-health-gateway-api:
  file.absent:
    - name: /home/jcy/health/health-gateway-api/health-gateway-api.tar.gz
    - require:
      - cmd: extract_pkg
start_service-health-gateway-api:
  cmd.run:
    - name: sh start.sh health-gateway-api
    - cwd: /home/jcy/health/health-gateway-api
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg