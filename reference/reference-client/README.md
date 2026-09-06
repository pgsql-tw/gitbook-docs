# PostgreSQL Client Applications

---

<a id="id-1.9.4.2"></a>

This part contains reference information for
PostgreSQL client applications and
utilities. Not all of these commands are of general utility; some
might require special privileges. The common feature of these
applications is that they can be run on any host, independent of
where the database server resides.

When specified on the command line, user and database names have
their case preserved — the presence of spaces or special
characters might require quoting. Table names and other identifiers
do not have their case preserved, except where documented, and
might require quoting.

**Table of Contents**

[clusterdb](app-clusterdb.md) — cluster a PostgreSQL database

[createdb](app-createdb.md) — create a new PostgreSQL database

[createuser](app-createuser.md) — define a new PostgreSQL user account

[dropdb](app-dropdb.md) — remove a PostgreSQL database

[dropuser](app-dropuser.md) — remove a PostgreSQL user account

[ecpg](app-ecpg.md) — embedded SQL C preprocessor

[pg_amcheck](app-pgamcheck.md) — checks for corruption in one or more PostgreSQL databases

[pg_basebackup](app-pgbasebackup.md) — take a base backup of a PostgreSQL cluster

[pgbench](pgbench.md) — run a benchmark test on PostgreSQL

[pg_combinebackup](app-pgcombinebackup.md) — reconstruct a full backup from an incremental backup and dependent backups

[pg_config](app-pgconfig.md) — retrieve information about the installed version of PostgreSQL

[pg_dump](app-pgdump.md) — export a PostgreSQL database as an SQL script or to other formats

[pg_dumpall](app-pg-dumpall.md) — extract a PostgreSQL database cluster into a script file

[pg_isready](app-pg-isready.md) — check the connection status of a PostgreSQL server

[pg_receivewal](app-pgreceivewal.md) — stream write-ahead logs from a PostgreSQL server

[pg_recvlogical](app-pgrecvlogical.md) — control PostgreSQL logical decoding streams

[pg_restore](app-pgrestore.md) — restore a PostgreSQL database from an archive file created by pg_dump

[pg_verifybackup](app-pgverifybackup.md) — verify the integrity of a base backup of a PostgreSQL cluster

[psql](app-psql.md) — PostgreSQL interactive terminal

[reindexdb](app-reindexdb.md) — reindex a PostgreSQL database

[vacuumdb](app-vacuumdb.md) — garbage-collect and analyze a PostgreSQL database

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/reference-client.html)（英文原文，待翻譯）
