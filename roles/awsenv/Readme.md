Role awsenv
============

This role will deploy a VPC with shared services using the following components:
- VPC
- shared public and private subnets (1 per AZ)
- Shared NAT gateway for internet access
- DHCP options and route tables as required
- Required security groups for basic network connectivity

The main configuration of the VPC is controlled by a dict variable named ___vpc___ . Some variables have sane defaults and do not need to be declared in the main dict.

[Example metadata](vpc-metadata.md)

Shared services provide access to the environment for:
- configuration management using a single salt master
- monitoring using standard ELK stack with elastic beats
- share jumphost for ssh access

Each of the shared services is configured with suitable IAM profiles and policies; and security groups to provide access from all instances within the VPC.

Shared services
---------------
Various monitoring services are provided via docker containers which are controlled with docker-compose.  The configuration is delivered via salt.  These playbooks are for provisioning only. The configuration management is handled via other automation tools.
  

#TODO
(/) Update Readme in line with ec2-app role

(x) Move monitoring and salt server creation out and use ec2app to deploy.

(x) Review complex variables and consider custom filters for the task.
