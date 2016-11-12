ecs-app Role 
============

This role is used to deploy an ECS based service to an ECS cluster.

If the cluster does not exist, it will be created.

The app metadata is used to define the cluster, service and task definitions.

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