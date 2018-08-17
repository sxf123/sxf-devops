transfer-pkg-health-fitness-card-facadeimpl-cluster:
  file.managed:
    - source: salt://health-fitness-card-facadeimpl-cluster/files/health-fitness-card-facadeimpl-cluster.tar.gz
    - name: /home/jcy/health/health-fitness-card-facadeimpl-cluster/health-fitness-card-facadeimpl-cluster.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-health-fitness-card-facadeimpl-cluster:
  file.directory:
    - name: /home/jcy/health/health-fitness-card-facadeimpl-cluster
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-health-fitness-card-facadeimpl-cluster:
  cmd.run:
    - name: tar -xzvf health-fitness-card-facadeimpl-cluster.tar.gz
    - cwd: /home/jcy/health/health-fitness-card-facadeimpl-cluster
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-health-fitness-card-facadeimpl-cluster:
  file.absent:
    - name: /home/jcy/health/health-fitness-card-facadeimpl-cluster/health-fitness-card-facadeimpl-cluster.tar.gz
    - require:
      - cmd: extract_pkg
start_service-health-fitness-card-facadeimpl-cluster:
  cmd.run:
    - name: sh start.sh health-fitness-card-facadeimpl-cluster
    - cwd: /home/jcy/health/health-fitness-card-facadeimpl-cluster
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg