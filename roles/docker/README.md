###Docker Role

Role that simply consumes metadata to create a .dockercfg file

Example Meta-Data

```yaml
docker-registries:
  https://index.docker.io/v1/:
    email: docker@example.com
    password: foo
    username: bar
    auth: myauthhash
  https://private.docker.registry:
    email: docker@example.com
    username: bar
    password: foo
    auth: myauthhash
```