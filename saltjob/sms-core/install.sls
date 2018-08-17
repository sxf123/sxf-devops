transfer-pkg-sms-core:
  file.managed:
    - source: salt://sms-core/files/sms-core.tar.gz
    - name: /home/jcy/sms/sms-core/sms-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-sms-core:
  file.directory:
    - name: /home/jcy/sms/sms-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-sms-core:
  cmd.run:
    - name: tar -xzvf sms-core.tar.gz
    - cwd: /home/jcy/sms/sms-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-sms-core:
  file.absent:
    - name: /home/jcy/sms/sms-core/sms-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-sms-core:
  cmd.run:
    - name: sh start.sh sms-core
    - cwd: /home/jcy/sms/sms-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg