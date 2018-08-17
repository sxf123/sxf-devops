transfer-pkg-wechat-admin:
  file.managed:
    - source: salt://wechat-admin/files/wechat-admin.tar.gz
    - name: /home/jcy/wechat/wechat-admin/wechat-admin.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-wechat-admin:
  file.directory:
    - name: /home/jcy/wechat/wechat-admin
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-wechat-admin:
  cmd.run:
    - name: tar -xzvf wechat-admin.tar.gz
    - cwd: /home/jcy/wechat/wechat-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-wechat-admin:
  file.absent:
    - name: /home/jcy/wechat/wechat-admin/wechat-admin.tar.gz
    - require:
      - cmd: extract_pkg
start_service-wechat-admin:
  cmd.run:
    - name: sh start.sh wechat-admin
    - cwd: /home/jcy/wechat/wechat-admin
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg