SQL-Command Role 
===============

This role is used to execute an ad-hoc query against the database

Variables
---------
- **query_string** Required by the playbook, must be fully escaped `"'insert into foo (bar) values (\'baz\');'"`
- **output_directory** Not required, path to write our output to, defaults to project base dir
- **target_db_name** Not required, used to select the db we are going to work on as named in the rds metadata
- **use_su** Not required, allows us to override and use SU privileges
- **remote_file** not required, if set and True will assume there is already a template on the remote to execute
