transfer-pkg-jccharity-app-service:
  file.managed:
    - source: salt://jccharity-app-service/files/jccharity-app-service.tar.gz
    - name: /home/jcy/charity/jccharity-app-service/jccharity-app-service.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-jccharity-app-service:
  file.directory:
    - name: /home/jcy/charity/jccharity-app-service
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-jccharity-app-service:
  cmd.run:
    - name: tar -xzvf jccharity-app-service.tar.gz
    - cwd: /home/jcy/charity/jccharity-app-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-jccharity-app-service:
  file.absent:
    - name: /home/jcy/charity/jccharity-app-service/jccharity-app-service.tar.gz
    - require:
      - cmd: extract_pkg
start_service-jccharity-app-service:
  cmd.run:
    - name: sh start.sh jccharity-app-service
    - cwd: /home/jcy/charity/jccharity-app-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg