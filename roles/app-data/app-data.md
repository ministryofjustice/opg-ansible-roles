Custom `app_data` Metadata Examples
===================================

Normally we define our applications in the `app_data` variable in our group_vars something similar to below, however there
are cases when we need to define specific bits of application infrastructure for targets.


```yaml
# Will apply to all targets
app_data:
  - name: 'test'
    instance:
      type: 't2.medium'
      count: "1"
      volumes:
        - device_name: /dev/sda1
          volume_size: 50
          delete_on_termination: True
    sg: "{{ list-of-security-groups }}"
    server_sg:
      name: 'test-{{opg_data.stack}}'
      desc: 'Test instance access'
      client_sg: "test-client"
      ruleset:
        - proto: 'tcp'
          ports: '443,80'

  - name: asg-test
    asg:
      instance_type: "{{ opg_data.asg_instance_size | default('t2.small') }}"
      min: "{{ opg_data.asg_instance_count | default(1) }}"
      max: "{{ opg_data.asg_instance_count * 2 | default(2) }}"
      desired: "{{ opg_data.asg_instance_count | default(1) }}"
      subnets: "{{ private_subnets }}"
      wait_for_instances: "{{ opg_data.asg_wait_for_instances | default(True) }}"
      sg: "{{ shared_security_groups + opg_data.front_security_groups  }}"
      asg_sg:
        name: 'asg-test-{{ opg_data.stack }}'
        desc: 'test-asg access'
        client_sg: "test-elb"
        ruleset:
          - proto: 'tcp'
            ports: '443,80'
    elb:
      subnets: "{{ public_subnets }}"
      public_dns: "test-{{ opg_data.stack }}"
      connection_draining_timeout: "{{ opg_data.connection_drain_timeout | default(0) }}"
      listeners:
        - protocol: https
          load_balancer_port: 443
          instance_port: 443
          ssl_certificate_id: "{{ vpc.pub_ssl_cert_id }}"
          proxy_protocol: True
        - protocol: http
          load_balancer_port: 80
          instance_port: 80
      health_check:
        ping_protocol: https
        ping_port: 443
        ping_path: "/manage/elb"
        response_timeout: 5
        interval: 30
        unhealthy_threshold: "{{ opg_data.elb_health_check.unhealthy_threshold | default(2) }}"
        healthy_threshold: "{{ opg_data.elb_health_check.healthy_threshold | default(2) }}"
      sg:
        - "test-elb-{{ opg_data.stack }}"
        - "shared-security-group-{{ vpc_name }}"
      elb_sg:
        name: 'test-elb-{{ opg_data.stack }}'
        desc: 'test elb access'
        include_nat_gw: true
        ruleset:
          - proto: 'tcp'
            ports: '80,443'
            src: "{{ opg_data.frontend_src | default (opg_data.front_vpn_src) }}"
```

However we can now split the declaration above into sections and have them combined by the application at run time to
add targeted infrastructure, we now support `custom_app_instance_data` and `app_instance_data` variables along with the
existing use of `app_data`

*NB* There is an order of priority, from most to least significant this is `custom_app_instance_data`, `app_instance_data` and `app_data`.
Anything declared in a lesser priority block will be over-written if re-declared in a higher priority block

```yaml
# Will apply only when declared
custom_app_instance_data:
  - name: 'test'
    instance:
      type: 't2.medium'
      count: "1"
      volumes:
        - device_name: /dev/sda1
          volume_size: 50
          delete_on_termination: True
    sg: "{{ list-of-security-groups }}"
    server_sg:
      name: 'test-{{opg_data.stack}}'
      desc: 'Test instance access'
      client_sg: "test-client"
      ruleset:
        - proto: 'tcp'
          ports: '443,80'

# Will apply only when declared
app_instance_data:
  - name: asg-test
    asg:
      instance_type: "{{ opg_data.asg_instance_size | default('t2.small') }}"
      min: "{{ opg_data.asg_instance_count | default(1) }}"
      max: "{{ opg_data.asg_instance_count * 2 | default(2) }}"
      desired: "{{ opg_data.asg_instance_count | default(1) }}"
      subnets: "{{ private_subnets }}"
      wait_for_instances: "{{ opg_data.asg_wait_for_instances | default(True) }}"
      sg: "{{ shared_security_groups + opg_data.front_security_groups  }}"
      asg_sg:
        name: 'asg-test-{{ opg_data.stack }}'
        desc: 'test-asg access'
        client_sg: "test-elb"
        ruleset:
          - proto: 'tcp'
            ports: '443,80'
    elb:
      subnets: "{{ public_subnets }}"
      public_dns: "test-{{ opg_data.stack }}"
      connection_draining_timeout: "{{ opg_data.connection_drain_timeout | default(0) }}"
      listeners:
        - protocol: https
          load_balancer_port: 443
          instance_port: 443
          ssl_certificate_id: "{{ vpc.pub_ssl_cert_id }}"
          proxy_protocol: True
        - protocol: http
          load_balancer_port: 80
          instance_port: 80
      health_check:
        ping_protocol: https
        ping_port: 443
        ping_path: "/manage/elb"
        response_timeout: 5
        interval: 30
        unhealthy_threshold: "{{ opg_data.elb_health_check.unhealthy_threshold | default(2) }}"
        healthy_threshold: "{{ opg_data.elb_health_check.healthy_threshold | default(2) }}"
      sg:
        - "test-elb-{{ opg_data.stack }}"
        - "shared-security-group-{{ vpc_name }}"
      elb_sg:
        name: 'test-elb-{{ opg_data.stack }}'
        desc: 'test elb access'
        include_nat_gw: true
        ruleset:
          - proto: 'tcp'
            ports: '80,443'
            src: "{{ opg_data.frontend_src | default (opg_data.front_vpn_src) }}"
```

This will then create a structure as seen in the first construct under app_data to be consumed by the playbooks
