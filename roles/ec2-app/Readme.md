ec2app Role
===========

This role will deploy a full application stack to a shared AWS VPC.  An application stack comprises the following components:
- application nodes
- IAM profiles
- security groups
- dynamodb, rds, elasticache, s3

All components are optional, and are deployed based on the presence of suitable metadata being available to the playbooks.


application node
----------------

An application node deploys the infrastructure for a single component/micro service of the application stack. Each component requires one or more of the following infrastructure:
- EC2 instance
- Auto Scaling Group & Launch Configuration
- Internal or External ELB
- Route53 DNS private and public records
- Node specific security groups

Each node is defined with a yaml dict which can define a variety of different node configurations.

[Node metadata examples](node-metadata.md)

#TODO
- Add cloudwatch metric to ELB (/)
- Add cleanup for launch config
- elasticache testing
- task tagging to allow targeted runs


