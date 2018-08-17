transfer-pkg-wechat-gateway:
  file.managed:
    - source: salt://wechat-gateway/files/wechat-gateway.tar.gz
    - name: /home/jcy/wechat/wechat-gateway/wechat-gateway.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-wechat-gateway:
  file.directory:
    - name: /home/jcy/wechat/wechat-gateway
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-wechat-gateway:
  cmd.run:
    - name: tar -xzvf wechat-gateway.tar.gz
    - cwd: /home/jcy/wechat/wechat-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-wechat-gateway:
  file.absent:
    - name: /home/jcy/wechat/wechat-gateway/wechat-gateway.tar.gz
    - require:
      - cmd: extract_pkg
start_service-wechat-gateway:
  cmd.run:
    - name: sh start.sh wechat-gateway
    - cwd: /home/jcy/wechat/wechat-gateway
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg