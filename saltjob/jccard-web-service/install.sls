transfer-pkg-jccard-web-service:
  file.managed:
    - source: salt://jccard-web-service/files/jccard-web-service.tar.gz
    - name: /home/jcy/jccard/jccard-web-service/jccard-web-service.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-jccard-web-service:
  file.directory:
    - name: /home/jcy/jccard/jccard-web-service
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-jccard-web-service:
  cmd.run:
    - name: tar -xzvf jccard-web-service.tar.gz
    - cwd: /home/jcy/jccard/jccard-web-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-jccard-web-service:
  file.absent:
    - name: /home/jcy/jccard/jccard-web-service/jccard-web-service.tar.gz
    - require:
      - cmd: extract_pkg
start_service-jccard-web-service:
  cmd.run:
    - name: sh start.sh jccard-web-service
    - cwd: /home/jcy/jccard/jccard-web-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg