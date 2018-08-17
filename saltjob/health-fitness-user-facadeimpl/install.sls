transfer-pkg-health-fitness-user-facadeimpl:
  file.managed:
    - source: salt://health-fitness-user-facadeimpl/files/health-fitness-user-facadeimpl.tar.gz
    - name: /home/jcy/health/health-fitness-user-facadeimpl/health-fitness-user-facadeimpl.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-health-fitness-user-facadeimpl:
  file.directory:
    - name: /home/jcy/health/health-fitness-user-facadeimpl
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-health-fitness-user-facadeimpl:
  cmd.run:
    - name: tar -xzvf health-fitness-user-facadeimpl.tar.gz
    - cwd: /home/jcy/health/health-fitness-user-facadeimpl
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-health-fitness-user-facadeimpl:
  file.absent:
    - name: /home/jcy/health/health-fitness-user-facadeimpl/health-fitness-user-facadeimpl.tar.gz
    - require:
      - cmd: extract_pkg
start_service-health-fitness-user-facadeimpl:
  cmd.run:
    - name: sh start.sh health-fitness-user-facadeimpl
    - cwd: /home/jcy/health/health-fitness-user-facadeimpl
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg