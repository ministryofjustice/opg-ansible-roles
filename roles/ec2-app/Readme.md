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
All node definitions are collected in a single list name ___app_data___
[Node metadata examples](node-metadata.md)

AWS services
------------

* dynamodb
    DynamoDB instances to support the application stack are created, with optional further indexes based on a yaml list named ___dynamodbs___ with each element in the list being a dict which defines the dynamodb instance.
* rds
    RDS instances are defined by a similarly named yaml list ___rds_dbs___
* s3
    S3 buckets are created based on the variable named ___s3_buckets___. All S3 buckets are encrypted.
* sns
    SNS topics are created based on the variable ___sns_topics___. Subscriptions to these topics are not managed by this role
* elasticache
    Elasticache instaces are created based on the variable ___elasticache_clusters___
    
[AWS resource metadata examples](aws-metadata.md)


#TODO
(/) Add cloudwatch metric to ELB
(x) Add cleanup for stale launch config objects
(/) elasticache testing
(x) task tagging to allow targeted runs


