```
vpc:
  state: present
  ami: ami-123456
  cidr: 10.0.0.0/16
  aws_region: eu-west-1
  pub_ssl_cert_id: "arn:aws:iam::123456789:server-certificate/my-pub-ssl-cert"
  pvt_ssl_cert_id: "arn:aws:iam::123456789:server-certificate/my-pvt-ssl-cert"
  subnets:
    - name: private-1a
      address: 10.0.0.0/23
    - name: private-1b
      address: 10.0.2.0/23
    - name: private-1c
      address: 10.0.4.0/23
    - name: public-1a
      address: 10.0.6.0/23
    - name: public-1b
      address: 10.0.8.0/23
    - name: public-1c
      address: 10.0.10.0/23
  env_tags:
    Project: "{{ opg_data.project }}"
  security_groups:  #only groups with cidr rules go here
    - Name: jumphost
      description: "External access to jumphost"
      ruleset:
        - ports: '22'
          proto: tcp
          src:
            - 1.2.3.4/32
            - 5.6.7.8/32
    - Name: elb-monitoring
      description: "External monitoring"
      ruleset:
        - ports: '443'
          proto: tcp
          src:
            - 1.2.3.4/32
            - 5.6.7.8/32
    - Name: salt-master
      description: "Client access to salt master services"
      ruleset:
        - ports: '4505,4506'
          proto: tcp
    - Name: monitoring
      description: "monitoring security group"
      ruleset:
        - ports: '6379,9200,2003,2514,8003,5671'
          proto: tcp
        - ports: '2003,2514,8125'
          proto: udp

monitoring_instance:
  volumes:
    - device_name: /dev/sda1
      volume_size: 50
      delete_on_termination: True
    - device_name: /dev/xvdh
      volume_type: gp2
      volume_size: 150
      delete_on_termination: True
      encrypted: True
  instance_type: 'm4.large'
  sgs:
    - "default-{{ opg_data.stack }}"
    - "jumphost-client-{{ opg_data.stack }}"
    - "monitoring-{{ opg_data.stack }}"
    - "shared-services-{{ opg_data.stack }}"
  dns:
    - kibana
    - elasticsearch
    - graphite
    - grafana
    - sensu
```
