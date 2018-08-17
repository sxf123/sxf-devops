transfer-pkg-cargo-core:
  file.managed:
    - source: salt://cargo-core/files/cargo-core.tar.gz
    - name: /home/jcy/supply/cargo-core/cargo-core.tar.gz
    - user: jcy
    - group: jcy
    - mode: 644
    - makedirs: True
change_owner-cargo-core:
  file.directory:
    - name: /home/jcy/supply/cargo-core
    - user: jcy
    - group: jcy
    - mode: 744
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: transfer-pkg
extract_pkg-cargo-core:
  cmd.run:
    - name: tar -xzvf cargo-core.tar.gz
    - cwd: /home/jcy/supply/cargo-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
remove_pkg-cargo-core:
  file.absent:
    - name: /home/jcy/supply/cargo-core/cargo-core.tar.gz
    - require:
      - cmd: extract_pkg
start_service-cargo-core:
  cmd.run:
    - name: sh start.sh cargo-core
    - cwd: /home/jcy/supply/cargo-core
    - runas: jcy
    - require:
      - file: transfer-pkg
      - file: change_owner
      - cmd: extract_pkg