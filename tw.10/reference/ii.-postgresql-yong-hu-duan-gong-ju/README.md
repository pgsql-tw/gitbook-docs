# II. PostgreSQL 用戶端工具

his part contains reference information forPostgreSQLclient applications and utilities. Not all of these commands are of general utility; some might require special privileges. The common feature of these applications is that they can be run on any host, independent of where the database server resides.

When specified on the command line, user and database names have their case preserved — the presence of spaces or special characters might require quoting. Table names and other identifiers do not have their case preserved, except where documented, and might require quoting.

**Table of Contents**

[clusterdb](https://www.postgresql.org/docs/10/static/app-clusterdb.html)

— cluster a

PostgreSQL

database

[createdb](https://www.postgresql.org/docs/10/static/app-createdb.html)

— create a new

PostgreSQL

database

[createuser](https://www.postgresql.org/docs/10/static/app-createuser.html)

— define a new

PostgreSQL

user account

[dropdb](https://www.postgresql.org/docs/10/static/app-dropdb.html)

— remove a

PostgreSQL

database

[dropuser](https://www.postgresql.org/docs/10/static/app-dropuser.html)

— remove a

PostgreSQL

user account

[ecpg](https://www.postgresql.org/docs/10/static/app-ecpg.html)

— embedded SQL C preprocessor

[pg\_basebackup](https://www.postgresql.org/docs/10/static/app-pgbasebackup.html)

— take a base backup of a

PostgreSQL

cluster

[pgbench](https://www.postgresql.org/docs/10/static/pgbench.html)

— run a benchmark test on

PostgreSQL

[pg\_config](https://www.postgresql.org/docs/10/static/app-pgconfig.html)

— retrieve information about the installed version of

PostgreSQL

[pg\_dump](https://www.postgresql.org/docs/10/static/app-pgdump.html)

— extract a

PostgreSQL

database into a script file or other archive file

[pg\_dumpall](https://www.postgresql.org/docs/10/static/app-pg-dumpall.html)

— extract a

PostgreSQL

database cluster into a script file

[pg\_isready](https://www.postgresql.org/docs/10/static/app-pg-isready.html)

— check the connection status of a

PostgreSQL

server

[pg\_receivewal](https://www.postgresql.org/docs/10/static/app-pgreceivewal.html)

— stream write-ahead logs from a

PostgreSQL

server

[pg\_recvlogical](https://www.postgresql.org/docs/10/static/app-pgrecvlogical.html)

— control

PostgreSQL

logical decoding streams

[pg\_restore](https://www.postgresql.org/docs/10/static/app-pgrestore.html)

— restore a

PostgreSQL

database from an archive file created by

pg\_dump

[psql](https://www.postgresql.org/docs/10/static/app-psql.html)

—

PostgreSQL

interactive terminal

[reindexdb](https://www.postgresql.org/docs/10/static/app-reindexdb.html)

— reindex a

PostgreSQL

database

[vacuumdb](https://www.postgresql.org/docs/10/static/app-vacuumdb.html)

— garbage-collect and analyze a

PostgreSQL

database

