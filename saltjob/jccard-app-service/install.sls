transfer-pkg-jccard-app-service:
  file.managed:
    - source: salt://jccard-app-service/files/jccard-app-service.tar.gz
    - name: /home/jcy/jccard/jccard-app-service/jccard-app-service.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-jccard-app-service:
  file.directory:
    - name: /home/jcy/jccard/jccard-app-service
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-jccard-app-service:
  cmd.run:
    - name: tar -xzvf jccard-app-service.tar.gz
    - cwd: /home/jcy/jccard/jccard-app-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-jccard-app-service:
  file.absent:
    - name: /home/jcy/jccard/jccard-app-service/jccard-app-service.tar.gz
    - require:
      - cmd: extract_pkg
start_service-jccard-app-service:
  cmd.run:
    - name: sh start.sh jccard-app-service
    - cwd: /home/jcy/jccard/jccard-app-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg