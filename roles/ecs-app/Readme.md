ecs-app Role 
============

This role is used to deploy an ECS based service to an ECS cluster.

[WIP] If the cluster does not exist, it will be created.

The app metadata is used to define the cluster, service and task definitions.  The app metadata uses the same format as for the ec2-app, with some new attributes to differentiate between ecs-app data and ec2-app data. The goal is to allow a single dict of applications which will be deployed using either role.

Security
--------
The ECS app is secured through the use of IAM profiles, in line with ECS supported features.  Load balancers, when required, are secured through the use of AWS security groups.

[Sample metadata](ecs-metadata.md)

Tasks
-----

* IAM profile and policies
* Security Groups
* ELB
* EFS storage (not implemented)
* ECS task
* ECS service


Status
------
Working to deploy ecs task and services.
Untested: ELB for ecs app, sg for ecs app