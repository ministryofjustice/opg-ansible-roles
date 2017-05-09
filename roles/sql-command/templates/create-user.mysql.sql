GRANT SELECT ON `{{ rds_instance_data.db_name }}`.* TO '{{ user_data.username }}'@'*' IDENTIFIED BY '{{ user_data.password }}';
FLUSH PRIVILEGES;