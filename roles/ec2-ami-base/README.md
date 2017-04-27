opg-ansible-ami-base
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


Using `ansible-galaxy` localy you can install this role directly from github.
Use a `requirements.yml` as follows:

    # Install a role from GitHub
    - name: opg-ansible-ami-base
    src: https://github.com/ministryofjustice/opg-ansible-ami-base

We can install the role locally, using that `requirements.yml` file:

    ansible-galaxy install -r requirements.yml -p ./roles


Dependencies
------------

None.


Role Variables
--------------

This role doesn't contain any default variables, any missing variables in its
invocation should fail the execution of the play.


See `site.yml` for the required role properties.

Example:

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

    opg_ansible_ec2_ami_base.stages: ['create_ami', 'destroy_baked_instances']


Development:
-------------

Have access to a AWS VPC configured with a jumphost.
Add your jumphost to your ~/.ssh/config file
Set your AWS credential variables
Set the required environment vars see `make check_vars`
then run: `make test`

you can control which ansible tags are executed by setting:
    export EXTRA_ANSIBLE_OPTIONS="--tags=bootstrap_new_ec2_instance,reboot_instances,test_instances"


License
-------

MIT

