ecs-cluster Role 
================

This role is used to deploy one or more ECS clusters.

Variables
---------

* **ecs_cluster_list** list of ECS cluster names

Tasks
-----

* Create or destroy ecs clusters

Usage
-----

````
  role:
    - ecs-cluster
````