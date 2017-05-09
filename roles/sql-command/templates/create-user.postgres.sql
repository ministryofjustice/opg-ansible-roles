DO
$body$
BEGIN
   IF NOT EXISTS (
      SELECT *
      FROM   pg_catalog.pg_user
      WHERE  usename = '{{ user_data.username }}') THEN

      CREATE USER {{ user_data.username }} WITH password '{{ user_data.password }}' {{ user_data.attributes }};
   END IF;
END
$body$;

GRANT CONNECT ON DATABASE {{ rds_instance_data.db_name }} TO {{ user_data.username }};
GRANT USAGE ON SCHEMA public TO {{ user_data.username }};
GRANT {{ user_data.permissions | default('SELECT') }} ON ALL TABLES IN SCHEMA public TO {{ user_data.username }};
GRANT SELECT, USAGE ON ALL SEQUENCES IN SCHEMA public TO {{ user_data.username }};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT {{ user_data.permissions | default('SELECT') }} ON TABLES TO {{ user_data.username }};