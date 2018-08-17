transfer-pkg-health-fitness-room-facadeimpl:
  file.managed:
    - source: salt://health-fitness-room-facadeimpl/files/health-fitness-room-facadeimpl.tar.gz
    - name: /home/jcy/health/health-fitness-room-facadeimpl/health-fitness-room-facadeimpl.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-health-fitness-room-facadeimpl:
  file.directory:
    - name: /home/jcy/health/health-fitness-room-facadeimpl
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-health-fitness-room-facadeimpl:
  cmd.run:
    - name: tar -xzvf health-fitness-room-facadeimpl.tar.gz
    - cwd: /home/jcy/health/health-fitness-room-facadeimpl
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-health-fitness-room-facadeimpl:
  file.absent:
    - name: /home/jcy/health/health-fitness-room-facadeimpl/health-fitness-room-facadeimpl.tar.gz
    - require:
      - cmd: extract_pkg
start_service-health-fitness-room-facadeimpl:
  cmd.run:
    - name: sh start.sh health-fitness-room-facadeimpl
    - cwd: /home/jcy/health/health-fitness-room-facadeimpl
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg