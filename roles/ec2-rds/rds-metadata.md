RDS instances
=============

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
        db_users:
          - username: readonly
            password:  foobarbaz
            encrypted: no
            schema: public
            permissions: USAGE
            
```