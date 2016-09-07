OPG Ansible Playbooks
---------------------

This repo has a collection fo ansible roles which can be used to provision AWS various resources used to support the OPG project.

AWS resources that can be created
---------------------------------
[awsvpc](roles/awsenv/Readme.md) - VPC with suitable security and infrastructure

[ec2-app](roles/ec2-app/Readme.md) - Instance of an application stack

**NOTES:**

There are various filters and modules which are bundled with the roles and are required for the roles to function correctly. Ensure you use the entire repo and provide suitable ansible configuration to include the _library_ and _filter_plugins_ directories.

The ansible roles make use of regular expressions for matching patterns in the name of the stack to allow the task logic to be used on multiple projects and stacks. This means there are some limitations imposed on the stack name that is used when provisioning.

1. All shared vpc stacks must have the string **'vpc'** in the name.  The stack names **'dev-vpc'** and **'prod-vpc'** should suffice and are preferred.
2. The string **'vpc'** may **NOT** be used in an application stack name, and is reserved for use as per point 1.
3. Application stack names should not cause regular expressions to match multiple values, eg having stacks named _aws-develop_ and _develop_ could lead to deletion or modification of incorrect infrastructure.
4. Stack names may not have spaces, and should instead use a **'-'** symbol in place of a space.

