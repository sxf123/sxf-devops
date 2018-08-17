transfer-pkg-operate-job-service:
  file.managed:
    - source: salt://operate-job-service/files/operate-job-service.tar.gz
    - name: /home/jcy/operate/operate-job-service/operate-job-service.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-operate-job-service:
  file.directory:
    - name: /home/jcy/operate/operate-job-service
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-operate-job-service:
  cmd.run:
    - name: tar -xzvf operate-job-service.tar.gz
    - cwd: /home/jcy/operate/operate-job-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-operate-job-service:
  file.absent:
    - name: /home/jcy/operate/operate-job-service/operate-job-service.tar.gz
    - require:
      - cmd: extract_pkg
start_service-operate-job-service:
  cmd.run:
    - name: sh start.sh operate-job-service
    - cwd: /home/jcy/operate/operate-job-service
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg