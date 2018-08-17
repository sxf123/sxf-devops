transfer-pkg-jccard-project-biz:
  file.managed:
    - source: salt://jccard-project-biz/files/jccard-project-biz.tar.gz
    - name: /home/jcy/jccard/jccard-project-biz/jccard-project-biz.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-jccard-project-biz:
  file.directory:
    - name: /home/jcy/jccard/jccard-project-biz
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-jccard-project-biz:
  cmd.run:
    - name: tar -xzvf jccard-project-biz.tar.gz
    - cwd: /home/jcy/jccard/jccard-project-biz
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-jccard-project-biz:
  file.absent:
    - name: /home/jcy/jccard/jccard-project-biz/jccard-project-biz.tar.gz
    - require:
      - cmd: extract_pkg
start_service-jccard-project-biz:
  cmd.run:
    - name: sh start.sh jccard-project-biz
    - cwd: /home/jcy/jccard/jccard-project-biz
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg