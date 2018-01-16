AWS Service Metadata Examples
=============================

Most options have sensible defaults.

1. DynamoDB

```yaml
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
            
    # Support for dynamodb ttls
    dynamodbs_ttl:
      - state: enable
        name: "app-queue"
        attribute: "expires"
        
    #Support for dynamodb scaling policies
    dynamodb_scaling_policies:
      - name: "app-queue"
        write_min_units: 1
        write_max_units: 100
        read_min_units: 1
        read_max_units: 100
        scale_out_cooldown: 60
        scale_in_cooldown: 60
        target_value: 50
```

2. S3 buckets

```yaml
    s3_buckets:
      - mybucket
```

3. SNS Topics

```yaml
    sns_topics:
      - my-topic
        subscriptions:
          - endpoint: "my-topic@example.com"
            protocol: "email"
   
```

4. Elasticache

```yaml
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
    