transfer-pkg-jccharity-web-service:
  file.managed:
    - source: salt://jccharity-web-service/files/jccharity-web-service.tar.gz
    - name: /home/jcy/charity/jccharity-web-service/jccharity-web-service.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-jccharity-web-service:
  file.directory:
    - name: /home/jcy/charity/jccharity-web-service
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-jccharity-web-service:
  cmd.run:
    - name: tar -xzvf jccharity-web-service.tar.gz
    - cwd: /home/jcy/charity/jccharity-web-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-jccharity-web-service:
  file.absent:
    - name: /home/jcy/charity/jccharity-web-service/jccharity-web-service.tar.gz
    - require:
      - cmd: extract_pkg
start_service-jccharity-web-service:
  cmd.run:
    - name: sh start.sh jccharity-web-service
    - cwd: /home/jcy/charity/jccharity-web-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg