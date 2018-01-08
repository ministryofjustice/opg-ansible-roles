docker-compose-service
--------------

This role configures docker-compose based services on each node

The role is driven by a list of services defined in a list called `services` where each item is a dict which describes various service related configurations.


The service list can be defined in the `hostvars` or `group_vars` ansible directory structure

```yaml
#sample service metadata

docker_compose_services:
  - name: "api"
    docker_compose_template: "my-service.j2" #name of the compose service file template
    directories:  #optional list of directory paths for mount points
      - path: "/data/apidata"
        owner: 1000
        mode: 755
  - name: "sensuclient"
    docker_compose_template:
        ...

```
