include:
  - opg-collectd.service
  - opg-collectd.modules
  - opg-collectd.syslog
  - opg-collectd.ntpd
  - opg-collectd.write_graphite
  - opg-collectd.btrfs
  - bootstrap.groups

collectd:
  pkg.installed:
    - name: {{ collectd_settings.pkg }}
    {%- if collectd_settings.pkg_version is defined and collectd_settings.pkg_version %}
    - version: '{{ collectd_settings.pkg_version }}'
    {%- endif %}
  user.present:
    - home: /var/lib/collectd
    - shell: /bin/bash
    - groups:
      - wheel
    - require:
      - group: wheel

{{ collectd_settings.plugindirconfig }}:
  file.directory:
    - user: {{ collectd_settings.user }}
    - group: {{ collectd_settings.group }}
    - dir_mode: 755
    - file_mode: 644
    - makedirs: True
    - require_in:
      - service: collectd-service # set proper file mode before service runs

{{ collectd_settings.config }}:
  file.managed:
    - source: salt://opg-collectd/templates/collectd.conf
    - user: {{ collectd_settings.user }}
    - group: {{ collectd_settings.group }}
    - mode: 644
    - template: jinja
    - watch_in:
      - service: collectd-service
