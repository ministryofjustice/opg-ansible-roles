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

```
    rds_dbs:
      - db_name: "mydb"
        storage_type: 'gp2'
        intial_storage: 10
        instance_type: "{{ opg_data.database_instance_type }}"
        instance_name: "mydb-{{ target }}"
        db_engine: "postgres"
        engine_version: "9.3.10"
        username: "{{ opg_data.database_master_username }}"
        password: "{{ opg_data.database_master_password }}"
        rds_sg:
          name: 'rds' #Stack name is appended automatically at run time
          desc: 'rds access'
          client_sg: "rds-client" #Stack name is appended automatically at run time
          ruleset:
            - proto: 'tcp'
              ports: '5432'
        maint_window: "sun:01:00-sun:01:30"
        backup_retention: 14
        backup_window: "00:00-00:30"
        tags: '"Key"="Environment","Value"="{{ opg_data.environment }}","Key"="Application","Value"="{{ opg_data.project }}","Key"="Name","Value"="mydb.{{ target }}.{{ opg_data.domain }}","Key"="Stack","Value"="{{ target }}"'
        public_dns: "pgsql-{{ opg_data.database_name }}"
```
    