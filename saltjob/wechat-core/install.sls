transfer-pkg-wechat-core:
  file.managed:
    - source: salt://wechat-core/files/wechat-core.tar.gz
    - name: /home/jcy/wechat/wechat-core/wechat-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-wechat-core:
  file.directory:
    - name: /home/jcy/wechat/wechat-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-wechat-core:
  cmd.run:
    - name: tar -xzvf wechat-core.tar.gz
    - cwd: /home/jcy/wechat/wechat-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-wechat-core:
  file.absent:
    - name: /home/jcy/wechat/wechat-core/wechat-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-wechat-core:
  cmd.run:
    - name: sh start.sh wechat-core
    - cwd: /home/jcy/wechat/wechat-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg