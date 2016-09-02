OPG Ansible Playbooks
---------------------

This repo has a collection fo ansible roles which can be used to provision AWS various resources used to support the OPG project.

AWS resources that can be created
---------------------------------
[awsvpc](roles/awsenv/Readme.md) - VPC with suitable security and infrastructure
[ec2-app](roles/ec2-app/Readme.md) - Instance of an application stack

**Note:**
There are various filters and modules which are bundled with the roles and are required for the roles to function correctly.
