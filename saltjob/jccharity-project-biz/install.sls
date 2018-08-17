transfer-pkg-jccharity-project-biz:
  file.managed:
    - source: salt://jccharity-project-biz/files/jccharity-project-biz.tar.gz
    - name: /home/jcy/charity/jccharity-project-biz/jccharity-project-biz.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-jccharity-project-biz:
  file.directory:
    - name: /home/jcy/charity/jccharity-project-biz
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-jccharity-project-biz:
  cmd.run:
    - name: tar -xzvf jccharity-project-biz.tar.gz
    - cwd: /home/jcy/charity/jccharity-project-biz
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-jccharity-project-biz:
  file.absent:
    - name: /home/jcy/charity/jccharity-project-biz/jccharity-project-biz.tar.gz
    - require:
      - cmd: extract_pkg
start_service-jccharity-project-biz:
  cmd.run:
    - name: sh start.sh jccharity-project-biz
    - cwd: /home/jcy/charity/jccharity-project-biz
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg