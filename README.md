OPG Ansible Playbooks
---------------------

This repo has a collection fo anisble roles which can be used to provision AWS various resources used to support the OPG project.

AWS resources that can be created
---------------------------------
VPC - VPC with suitable security and infrastructure
ec2_app - 


variable data
-------------
core data structure

opg_data:
  role:
  project:
  stack:
  domain:
  environment:

app:
  name: 
  instance:
    bootstrap_branch:
    has_docker:
    ami:
  elb:
    listeners:
    health_check:
  iam:
      
      