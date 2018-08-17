transfer-pkg-facepp-agent:
  file.managed:
    - source: salt://facepp-agent/files/facepp-agent.tar.gz
    - name: /home/jcy/face/facepp-agent/facepp-agent.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-facepp-agent:
  file.directory:
    - name: /home/jcy/face/facepp-agent
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-facepp-agent:
  cmd.run:
    - name: tar -xzvf facepp-agent.tar.gz
    - cwd: /home/jcy/face/facepp-agent
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-facepp-agent:
  file.absent:
    - name: /home/jcy/face/facepp-agent/facepp-agent.tar.gz
    - require:
      - cmd: extract_pkg
start_service-facepp-agent:
  cmd.run:
    - name: sh start.sh facepp-agent
    - cwd: /home/jcy/face/facepp-agent
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg