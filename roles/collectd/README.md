###collectd


Ansible role to install collectd

####Example metadata

```yaml

collectd:
  FQDNLookup: true
  plugins:
    default: 
        - battery
        - cpu
        - entropy
        - load
        - memory
        - swap
        - users
    enable: false
    syslog:
      loglevel: info
    network:
      host: 'logstash'
      port: 25826
      securitylevel: 'Encrypt'
      username: 'user'
      password: 'password'
    ntpd:
      host: localhost
      port: 123
      ReverseLookups: 'false'
    write_graphite:
      host: graphite-host
      port: "2003"
      prefix: "collectd"
      postfix: ""
      protocol: "tcp"
      logsenderrors: false
      escapecharacter: "_"
      separateinstances: true
      storerates: true
      alwaysappendds: false
    statsd:
      host: localhost
      port: 8125
    python:
      Globals: true
      ModulePath: "/usr/share/collectd/modules"
      LogTraces: true
      Interactive: false
      modules:
        - name: module_name
          variables:
            var1: value1
            var2: value2
```