Examples
========

1. EC2 instance with no ELB or ASG

  This configuration would be suitable for a db cluster

```
  - name: 'mongodb'
    instance:
      type: 'm3.medium'
      volumes:
        - encrypted: true
          volume_type: 'io1'
          volume_size: 50
          iops: 100
          device_name: '/dev/sdh'
          delete_on_termination: True
      count: 3
    sg: "{{ shared_security_groups + ['mongodb-client-' + opg_data.stack, 'mongodb-server-' + opg_data.stack] }}"
    server_sg:
      name: 'mongodb-server-{{ opg_data.stack }}'
      desc: 'mongodb server access'
      client_sg: "mongodb-client"
      ruleset:
        - proto: 'tcp'
          ports: '27017'
```

2. Scaling group with ELB

```
  - name: simple-node
    asg:
      instance_type: 't2.small'
      min: 1
      max: 1
      desired: 1
      subnets: "{{ private_subnets }}"
      sg: "{{ shared_security_groups }}"
```

3. Node with Scaling Group and ELB

```
  - name: full-example
    asg:
      instance_type: 't2.small'
      min: 1
      max: 1
      desired: 1
      subnets: "{{ private_subnets }}"
      sg: "{{ shared_security_groups + ['example-' + opg_data.stack, 'mongodb-client-' + opg_data.stack] }}"
      asg_sg:
        name: 'full-example-{{ opg_data.stack }}'
        desc: 'full-example server access'
        client_sg: "full-example-elb"
        ruleset:
          - proto: 'tcp'
            ports: '443'
    elb:
      subnets: "{{ private_subnets }}"
      private_dns: "full-example.{{ opg_data.stack }}"
      type: internal
      listeners:
        - protocol: https
          load_balancer_port: 443
          instance_port: 443
          ssl_certificate_id: "{{ vpc.ssl_cert_id }}"
          proxy_protocol: True
      health_check:
        ping_protocol: tcp
        ping_port: 443
        response_timeout: 5
        interval: 30
        unhealthy_threshold: 2
        healthy_threshold: 2
      sg:
        - "shared-services-{{ vpc_name }}"
        - "full-example-elb-{{ opg_data.stack }}"
      elb_sg:
        name: 'full-example-elb-{{ opg_data.stack }}'
        desc: 'full-example elb access'
        client_sg: "full-example-client"
        ruleset:
          - proto: 'tcp'
            ports: '443'
```
