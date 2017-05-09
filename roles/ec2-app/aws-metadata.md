AWS Service Metadata Examples
=============================

Most options have sensible defaults.

1. DynamoDB

```
    dynamodbs:
      - name: app-locks
      - name: app-properties
        read_capacity: 4
        write_capacity: 4
      - name: app-queue
        indexes:
          - name: 'partition-order-index'
            type: 'global_include'
            hash_key_name: 'run_partition'
            hash_key_type: NUMBER
            range_key_name: 'run_after'
            range_key_type: NUMBER
            includes:
              - 'myfield'
            read_capacity: 12
            write_capacity: 8
```

2. S3 buckets

```
    s3_buckets:
      - mybucket
```

3. SNS Topics

```
    sns_topics:
      - my-topic
```

4. Elasticache

```
    elasticache_clusters:
       - ec_name: "cache"
         engine: "redis"
         node_type: "cache.m1.small"
         num_nodes: 1
         port: 6379
         cache_parameter_group: "{{ cache_parameter_group }}"
         private_dns: "cache-redis"
         ec_sg:
           name: 'cache' #Stackname appended at runtime
           desc: 'cache ec access'
           client_sg: "cache-client" #Stackname appended at runtime
           ruleset:
             - proto: 'tcp'
               ports: '6379'
```

5. RDS instances

See [RDS Metadata](../rds/rds-metadata.md)
    