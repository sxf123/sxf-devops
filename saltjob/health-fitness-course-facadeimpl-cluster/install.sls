transfer-pkg-health-fitness-course-facadeimpl-cluster:
  file.managed:
    - source: salt://health-fitness-course-facadeimpl-cluster/files/health-fitness-course-facadeimpl-cluster.tar.gz
    - name: /home/jcy/health/health-fitness-course-facadeimpl-cluster/health-fitness-course-facadeimpl-cluster.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-health-fitness-course-facadeimpl-cluster:
  file.directory:
    - name: /home/jcy/health/health-fitness-course-facadeimpl-cluster
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-health-fitness-course-facadeimpl-cluster:
  cmd.run:
    - name: tar -xzvf health-fitness-course-facadeimpl-cluster.tar.gz
    - cwd: /home/jcy/health/health-fitness-course-facadeimpl-cluster
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-health-fitness-course-facadeimpl-cluster:
  file.absent:
    - name: /home/jcy/health/health-fitness-course-facadeimpl-cluster/health-fitness-course-facadeimpl-cluster.tar.gz
    - require:
      - cmd: extract_pkg
start_service-health-fitness-course-facadeimpl-cluster:
  cmd.run:
    - name: sh start.sh health-fitness-course-facadeimpl-cluster
    - cwd: /home/jcy/health/health-fitness-course-facadeimpl-cluster
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg