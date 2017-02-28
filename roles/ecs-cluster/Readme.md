ecs-cluster Role 
================

This role is used to deploy one or more ECS clusters.  Each cluster is created with an EFS share that can be mounted on the cluster instances.

Variables
---------

* **ecs_cluster_list** list of ECS cluster names

Tasks
-----

* Create or destroy ecs clusters
* Create or destroy EFS filesystem for cluster

Usage
-----

````
  role:
    - ecs-cluster
````