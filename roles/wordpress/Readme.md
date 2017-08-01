Wordpress Role 
==============

This role is used to deploy a wordpress instance on the vpc via the ec2-app role, the role is activated via a vpc defined boolean variable `has_wordpress_help`

The app metadata is used to define the components of the wordpress stack.  The app metadata uses the same format as for the ec2-app, and is designed to use the ec2-app role with separate metadata to the application stacks.

Security
--------
The app is secured through the use of IAM profiles and security groups.  Load balancers, when required, are secured through the use of AWS security groups.

Variables
---------
- **wordpress_appdata**  A list of application components for wordpress stack. Default value **[]**



[Metadata details](../ec2-app/Readme.md)
