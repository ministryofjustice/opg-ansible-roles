Maintenance Role 
===============

This role is used to deploy a wordpress as in the vpc the ec2-app role

The app metadata is used to define the components of the maintenance stack.  The app metadata uses the same format as for the ec2-app, and is designed to use the ec2-app role with separate metadata to the application stacks.

Security
--------
The app is secured through the use of IAM profiles and security groups.  Load balancers, when required, are secured through the use of AWS security groups.

Variables
---------
- **wordpress_appdata**  A list of application components for maintenance stack. Default value **[]**


[Metadata details](../ec2-app/Readme.md)
