{% from "opg-collectd/map.jinja" import collectd_settings with context %}

include:
  - opg-collectd

{{ collectd_settings.plugindirconfig }}/syslog.conf:
  file.managed:
    - source: salt://opg-collectd/templates/syslog.conf
    - user: {{ collectd_settings.user }}
    - group: {{ collectd_settings.group }}
    - mode: 644
    - template: jinja
    - watch_in:
      - service: collectd-service
