wordpress-sync
==============

Role to syncronise wordpress data from one instance to another

####Variables
 - sync_action - Required, either up or down to denote direction
   - up - pushes up `uploads`, `themes` and `plugins` to the hosts /data directory
   - down - pulls down the contents of `uploads` and a dump of the database from the remote host and commits them to the git repository
 - target - Required, which vpc are we targetting
 - restore_db - Optional, do we want to restore the db from a snapshot, only relevant for `sync_action=up`
 - restart_docker - Optional, do we want to restart the docker-compose service
 - domain_to_replace - Optional, what domain are we replacing when we do the SQL dump
 