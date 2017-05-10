ec2-ami-base
================

An Ansible role, to create Ubuntu based AMI images for OPG

Requirements
------------

* ansible
* boto
* AWS environment variables

If using vi, this plugin is your friend: 
https://github.com/chase/vim-ansible-yaml.git

Installation
------------

    virtualenv venv
    . venv/bin/activate
    pip install --upgrade -r requirements.txt


Dependencies
------------

None.


Role Variables
--------------

This role doesn't contain any default variables, any missing variables in its
invocation should fail the execution of the play.


Example of a playbook consuming this role:

```


# vim: set ft=ansible
# role: ec2-ami-base/site.yml
---

# typical execution as:
# ansible-playbook -i ansible/ec2.py -e AMI_SERIAL=0001 -e KEY_NAME=xpto@example.org -e VPC_ID=xxxxxx -e VPC_SUBNET_ID=xxxxxxx site.yml

# expect warnings on duplicate dict keys at startup due to:
# http://stackoverflow.com/a/39712676

# fake hostgroup, only used for setting 'global' playbook variables across
# multiple hostgroup plays within the same playbook
- hosts: _setting_variables_only
  any_errors_fatal: true
  max_fail_percentage: 0
  vars:
    # common aliases block
    _common_security_groups: &common_security_groups
      region: &region 'eu-west-1'
      vpc_id: &vpc_id "{{ VPC_ID}}"
      # this is an ephemeral security group used only for baking the AMI
      sg_name: &sg_name 'bake_ami_ssh'

    _common_instances: &common_instances
      instance_type: &instance_type "t2.nano"
      # these should be set during ansible-plabook invocation
      # ansible-playbook -e KEY_NAME=xxxxx -e VPC_SUBNET_ID=yyyyy ....
      key_name: &key_name "{{ KEY_NAME }}"
      pubkey_filename: "{{ PUBKEY_FILENAME }}"
      vpc_subnet_id: &vpc_subnet_id  "{{ VPC_SUBNET_ID }}"
      security_groups: *sg_name
      region: *region
      assign_public_ip: yes
      ebs_optimized: false
      instance_tags: &instance_tags
        role: baking_ami
        ami_users_with_launch_permissions:
          user_ids:
            - 001780581745
            - 248804316466
            - 288342028542
            - 515688267891
            - 550790013665
            - 649098267436
      volumes:
        - device_name: /dev/sda1
          volume_size: 15
          volume_type: gp2
          delete_on_termination: true
      user_data: |
        #!/bin/sh
        # add python 2.7 as it could be missing from the base ami images
        apt-get update
        apt-get -y install python

    # variables consumed by role ec2-ami-base
    ec2_ami_base: &ec2_ami_base
      security_groups:
        - name: *sg_name
          region: *region
          vpc_id: *vpc_id
          ingress_rules:
            - from_port: 22
              to_port: 22
              cidr_ip: '0.0.0.0/0'
              proto: 'tcp'
          egress_rules:
            - cidr_ip: '0.0.0.0/0'
              proto: 'all'
      instances:
        - name: bake_ami_ubuntu_1404
          <<: *common_instances
          # Ubuntu AMIs available from:
          # https://cloud-images.ubuntu.com/locator/ec2/
          image: "{{ UBUNTU_1404_BASE_AMI |default('ami-9d8283fb') }}"
          # overwrite instance_tags
          instance_tags:
            <<: *instance_tags
            Name: bake_ami_ubuntu_1404
            os: 'ubuntu_1404'
          # this should be set during ansible-plabook invocation
          # ansible-playbook -e AMI_SERIAL=0001
            serial: '{{ AMI_SERIAL }}'

      # below is an example for baking additional images
      # additional instances to build below:
        - name: bake_ami_ubuntu_1604
          <<: *common_instances
          image: "{{ UBUNTU_1604_BASE_AMI |default('ami-a8d2d7ce') }}"
          instance_tags:
            <<: *instance_tags
            Name: bake_ami_ubuntu_1604
            os: 'ubuntu_1604'
      # this should be set during ansible-plabook invocation
      # ansible-playbook -e AMI_SERIAL=0001 ...
            serial: '{{ AMI_SERIAL }}'

      # Our role needs to execute tasks across different inventories (localhost
      # and newly provisioned/existing instances).
      # stages allows for spliting an ansible role into multiple execution
      # stages.
      # in this role, we need to create a set of EC2 instances (from localhost)
      # refresh the inventory and then provisioning the new instances.
      stages: []

# stages: sg_groups, create_instances, refresh-inventory
- hosts: 127.0.0.1
  any_errors_fatal: true
  max_fail_percentage: 0
  connection: local
  become: no
  vars:
    # variables consumed by role ec2-ami-base
    ec2_ami_base:
      <<: *ec2_ami_base
      stages:
        - create_sg_groups
        - create_keypair
        - create_instances
        - refresh_inventory
  roles:
    - ec2-ami-base

# stages: provision_instances, reboot_instances, test_instances
- hosts: tag_role_baking_ami
  any_errors_fatal: true
  max_fail_percentage: 0
  user: ubuntu
  become: yes
  vars:
    # variables consumed by role ec2-ami-base
    ec2_ami_base:
      <<: *ec2_ami_base
      stages:
        - provision_instances
        - reboot_instances
        - test_instances # uses GOSS
  roles:
    - ec2-ami-base

# stages: create_ami, destroy_baked_instances, delete_sg_groups
- hosts: 127.0.0.1
  any_errors_fatal: true
  max_fail_percentage: 0
  connection: local
  become: no
  vars:
    # variables consumed by role ec2-ami-base
    ec2_ami_base:
      <<: *ec2_ami_base
      stages:
        - create_ami
        - destroy_baked_instances
        - delete_keypair
        - delete_sg_groups
  roles:
    - ec2-ami-base

```


Example for execution:

    ansible-playbook -i ansible/ec2.py -e AMI_SERIAL=0001 -e KEY_NAME=xpto@example.org -e VPC_ID=xxxxxx -e VPC_SUBNET_ID=xxxxxxx site.yml


How does this work?
--------------------

The execution of the role is split into 'stages'. This is to work around 
ansible limitations on dealing with dynamic inventories.
For example, we would like to simply call a role with hosts: ec2_boxes, however
the inventory won't contain any hosts at time of invocation as the role will
be creating those roles itself.

By having 'stages' within a role, we can trigger all the different steps from
a single playbook run, by invoking the role with different parameters.

Stages:

- *create_sg_groups* -> creates the ephemeral EC2 Security Groups for ssh access
- *create_instances* -> launches the EC2 instances
- *refresh_inventory* -> updates the EC2 inventory with the new instances
- *provision_instances* -> provisions the EC2 instances
- *reboot_instances* -> reboots the EC2 instances
- *test_instances* -> tests the EC2 instances using GOSS (https://github.com/aelsabbahy/goss_)
- *create_ami* -> Creates an AMI from the ec2 instances
- *destroy_baked_instances* -> Removes the already baked instances
- *delete_sg_groups* -> Removes the security groups

Execution of the different stages is controlled by a dictionary variable, see the
`site.yml` file for an example:

    ec2_ami_base.stages: ['create_ami', 'destroy_baked_instances']


Development:
-------------

Have access to a AWS VPC configured with a jumphost.
Add your jumphost to your ~/.ssh/config file
Set your AWS credential variables
Set the required environment vars see `make check_vars`
then run: `make test`

you can control which ansible tags are executed by setting:

```export EXTRA_ANSIBLE_OPTIONS="--tags=bootstrap_new_ec2_instance,reboot_instances,test_instances"```


License
-------

MIT

