# Part VI. Reference

<a id="id-1.9.2"></a>

The entries in this Reference are meant to provide in reasonable
length an authoritative, complete, and formal summary about their
respective subjects. More information about the use of
PostgreSQL, in narrative, tutorial, or
example form, can be found in other parts of this book. See the
cross-references listed on each reference page.

The reference entries are also available as traditional
“man” pages.

**Table of Contents**

[I. SQL Commands](sql-commands/README.md)
:   [ABORT](sql-commands/sql-abort.md) — abort the current transaction

    [ALTER AGGREGATE](sql-commands/sql-alteraggregate.md) — change the definition of an aggregate function

    [ALTER COLLATION](sql-commands/sql-altercollation.md) — change the definition of a collation

    [ALTER CONVERSION](sql-commands/sql-alterconversion.md) — change the definition of a conversion

    [ALTER DATABASE](sql-commands/sql-alterdatabase.md) — change a database

    [ALTER DEFAULT PRIVILEGES](sql-commands/sql-alterdefaultprivileges.md) — define default access privileges

    [ALTER DOMAIN](sql-commands/sql-alterdomain.md) — change the definition of a domain

    [ALTER EVENT TRIGGER](sql-commands/sql-altereventtrigger.md) — change the definition of an event trigger

    [ALTER EXTENSION](sql-commands/sql-alterextension.md) — change the definition of an extension

    [ALTER FOREIGN DATA WRAPPER](sql-commands/sql-alterforeigndatawrapper.md) — change the definition of a foreign-data wrapper

    [ALTER FOREIGN TABLE](sql-commands/sql-alterforeigntable.md) — change the definition of a foreign table

    [ALTER FUNCTION](sql-commands/sql-alterfunction.md) — change the definition of a function

    [ALTER GROUP](sql-commands/sql-altergroup.md) — change role name or membership

    [ALTER INDEX](sql-commands/sql-alterindex.md) — change the definition of an index

    [ALTER LANGUAGE](sql-commands/sql-alterlanguage.md) — change the definition of a procedural language

    [ALTER LARGE OBJECT](sql-commands/sql-alterlargeobject.md) — change the definition of a large object

    [ALTER MATERIALIZED VIEW](sql-commands/sql-altermaterializedview.md) — change the definition of a materialized view

    [ALTER OPERATOR](sql-commands/sql-alteroperator.md) — change the definition of an operator

    [ALTER OPERATOR CLASS](sql-commands/sql-alteropclass.md) — change the definition of an operator class

    [ALTER OPERATOR FAMILY](sql-commands/sql-alteropfamily.md) — change the definition of an operator family

    [ALTER POLICY](sql-commands/sql-alterpolicy.md) — change the definition of a row-level security policy

    [ALTER PROCEDURE](sql-commands/sql-alterprocedure.md) — change the definition of a procedure

    [ALTER PUBLICATION](sql-commands/sql-alterpublication.md) — change the definition of a publication

    [ALTER ROLE](sql-commands/sql-alterrole.md) — change a database role

    [ALTER ROUTINE](sql-commands/sql-alterroutine.md) — change the definition of a routine

    [ALTER RULE](sql-commands/sql-alterrule.md) — change the definition of a rule

    [ALTER SCHEMA](sql-commands/sql-alterschema.md) — change the definition of a schema

    [ALTER SEQUENCE](sql-commands/sql-altersequence.md) — change the definition of a sequence generator

    [ALTER SERVER](sql-commands/sql-alterserver.md) — change the definition of a foreign server

    [ALTER STATISTICS](sql-commands/sql-alterstatistics.md) — change the definition of an extended statistics object

    [ALTER SUBSCRIPTION](sql-commands/sql-altersubscription.md) — change the definition of a subscription

    [ALTER SYSTEM](sql-commands/sql-altersystem.md) — change a server configuration parameter

    [ALTER TABLE](sql-commands/sql-altertable.md) — change the definition of a table

    [ALTER TABLESPACE](sql-commands/sql-altertablespace.md) — change the definition of a tablespace

    [ALTER TEXT SEARCH CONFIGURATION](sql-commands/sql-altertsconfig.md) — change the definition of a text search configuration

    [ALTER TEXT SEARCH DICTIONARY](sql-commands/sql-altertsdictionary.md) — change the definition of a text search dictionary

    [ALTER TEXT SEARCH PARSER](sql-commands/sql-altertsparser.md) — change the definition of a text search parser

    [ALTER TEXT SEARCH TEMPLATE](sql-commands/sql-altertstemplate.md) — change the definition of a text search template

    [ALTER TRIGGER](sql-commands/sql-altertrigger.md) — change the definition of a trigger

    [ALTER TYPE](sql-commands/sql-altertype.md) — change the definition of a type

    [ALTER USER](sql-commands/sql-alteruser.md) — change a database role

    [ALTER USER MAPPING](sql-commands/sql-alterusermapping.md) — change the definition of a user mapping

    [ALTER VIEW](sql-commands/sql-alterview.md) — change the definition of a view

    [ANALYZE](sql-commands/sql-analyze.md) — collect statistics about a database

    [BEGIN](sql-commands/sql-begin.md) — start a transaction block

    [CALL](sql-commands/sql-call.md) — invoke a procedure

    [CHECKPOINT](sql-commands/sql-checkpoint.md) — force a write-ahead log checkpoint

    [CLOSE](sql-commands/sql-close.md) — close a cursor

    [CLUSTER](sql-commands/sql-cluster.md) — cluster a table according to an index

    [COMMENT](sql-commands/sql-comment.md) — define or change the comment of an object

    [COMMIT](sql-commands/sql-commit.md) — commit the current transaction

    [COMMIT PREPARED](sql-commands/sql-commit-prepared.md) — commit a transaction that was earlier prepared for two-phase commit

    [COPY](sql-commands/sql-copy.md) — copy data between a file and a table

    [CREATE ACCESS METHOD](sql-commands/sql-create-access-method.md) — define a new access method

    [CREATE AGGREGATE](sql-commands/sql-createaggregate.md) — define a new aggregate function

    [CREATE CAST](sql-commands/sql-createcast.md) — define a new cast

    [CREATE COLLATION](sql-commands/sql-createcollation.md) — define a new collation

    [CREATE CONVERSION](sql-commands/sql-createconversion.md) — define a new encoding conversion

    [CREATE DATABASE](sql-commands/sql-createdatabase.md) — create a new database

    [CREATE DOMAIN](sql-commands/sql-createdomain.md) — define a new domain

    [CREATE EVENT TRIGGER](sql-commands/sql-createeventtrigger.md) — define a new event trigger

    [CREATE EXTENSION](sql-commands/sql-createextension.md) — install an extension

    [CREATE FOREIGN DATA WRAPPER](sql-commands/sql-createforeigndatawrapper.md) — define a new foreign-data wrapper

    [CREATE FOREIGN TABLE](sql-commands/sql-createforeigntable.md) — define a new foreign table

    [CREATE FUNCTION](sql-commands/sql-createfunction.md) — define a new function

    [CREATE GROUP](sql-commands/sql-creategroup.md) — define a new database role

    [CREATE INDEX](sql-commands/sql-createindex.md) — define a new index

    [CREATE LANGUAGE](sql-commands/sql-createlanguage.md) — define a new procedural language

    [CREATE MATERIALIZED VIEW](sql-commands/sql-creatematerializedview.md) — define a new materialized view

    [CREATE OPERATOR](sql-commands/sql-createoperator.md) — define a new operator

    [CREATE OPERATOR CLASS](sql-commands/sql-createopclass.md) — define a new operator class

    [CREATE OPERATOR FAMILY](sql-commands/sql-createopfamily.md) — define a new operator family

    [CREATE POLICY](sql-commands/sql-createpolicy.md) — define a new row-level security policy for a table

    [CREATE PROCEDURE](sql-commands/sql-createprocedure.md) — define a new procedure

    [CREATE PUBLICATION](sql-commands/sql-createpublication.md) — define a new publication

    [CREATE ROLE](sql-commands/sql-createrole.md) — define a new database role

    [CREATE RULE](sql-commands/sql-createrule.md) — define a new rewrite rule

    [CREATE SCHEMA](sql-commands/sql-createschema.md) — define a new schema

    [CREATE SEQUENCE](sql-commands/sql-createsequence.md) — define a new sequence generator

    [CREATE SERVER](sql-commands/sql-createserver.md) — define a new foreign server

    [CREATE STATISTICS](sql-commands/sql-createstatistics.md) — define extended statistics

    [CREATE SUBSCRIPTION](sql-commands/sql-createsubscription.md) — define a new subscription

    [CREATE TABLE](sql-commands/sql-createtable.md) — define a new table

    [CREATE TABLE AS](sql-commands/sql-createtableas.md) — define a new table from the results of a query

    [CREATE TABLESPACE](sql-commands/sql-createtablespace.md) — define a new tablespace

    [CREATE TEXT SEARCH CONFIGURATION](sql-commands/sql-createtsconfig.md) — define a new text search configuration

    [CREATE TEXT SEARCH DICTIONARY](sql-commands/sql-createtsdictionary.md) — define a new text search dictionary

    [CREATE TEXT SEARCH PARSER](sql-commands/sql-createtsparser.md) — define a new text search parser

    [CREATE TEXT SEARCH TEMPLATE](sql-commands/sql-createtstemplate.md) — define a new text search template

    [CREATE TRANSFORM](sql-commands/sql-createtransform.md) — define a new transform

    [CREATE TRIGGER](sql-commands/sql-createtrigger.md) — define a new trigger

    [CREATE TYPE](sql-commands/sql-createtype.md) — define a new data type

    [CREATE USER](sql-commands/sql-createuser.md) — define a new database role

    [CREATE USER MAPPING](sql-commands/sql-createusermapping.md) — define a new mapping of a user to a foreign server

    [CREATE VIEW](sql-commands/sql-createview.md) — define a new view

    [DEALLOCATE](sql-commands/sql-deallocate.md) — deallocate a prepared statement

    [DECLARE](sql-commands/sql-declare.md) — define a cursor

    [DELETE](sql-commands/sql-delete.md) — delete rows of a table

    [DISCARD](sql-commands/sql-discard.md) — discard session state

    [DO](sql-commands/sql-do.md) — execute an anonymous code block

    [DROP ACCESS METHOD](sql-commands/sql-drop-access-method.md) — remove an access method

    [DROP AGGREGATE](sql-commands/sql-dropaggregate.md) — remove an aggregate function

    [DROP CAST](sql-commands/sql-dropcast.md) — remove a cast

    [DROP COLLATION](sql-commands/sql-dropcollation.md) — remove a collation

    [DROP CONVERSION](sql-commands/sql-dropconversion.md) — remove a conversion

    [DROP DATABASE](sql-commands/sql-dropdatabase.md) — remove a database

    [DROP DOMAIN](sql-commands/sql-dropdomain.md) — remove a domain

    [DROP EVENT TRIGGER](sql-commands/sql-dropeventtrigger.md) — remove an event trigger

    [DROP EXTENSION](sql-commands/sql-dropextension.md) — remove an extension

    [DROP FOREIGN DATA WRAPPER](sql-commands/sql-dropforeigndatawrapper.md) — remove a foreign-data wrapper

    [DROP FOREIGN TABLE](sql-commands/sql-dropforeigntable.md) — remove a foreign table

    [DROP FUNCTION](sql-commands/sql-dropfunction.md) — remove a function

    [DROP GROUP](sql-commands/sql-dropgroup.md) — remove a database role

    [DROP INDEX](sql-commands/sql-dropindex.md) — remove an index

    [DROP LANGUAGE](sql-commands/sql-droplanguage.md) — remove a procedural language

    [DROP MATERIALIZED VIEW](sql-commands/sql-dropmaterializedview.md) — remove a materialized view

    [DROP OPERATOR](sql-commands/sql-dropoperator.md) — remove an operator

    [DROP OPERATOR CLASS](sql-commands/sql-dropopclass.md) — remove an operator class

    [DROP OPERATOR FAMILY](sql-commands/sql-dropopfamily.md) — remove an operator family

    [DROP OWNED](sql-commands/sql-drop-owned.md) — remove database objects owned by a database role

    [DROP POLICY](sql-commands/sql-droppolicy.md) — remove a row-level security policy from a table

    [DROP PROCEDURE](sql-commands/sql-dropprocedure.md) — remove a procedure

    [DROP PUBLICATION](sql-commands/sql-droppublication.md) — remove a publication

    [DROP ROLE](sql-commands/sql-droprole.md) — remove a database role

    [DROP ROUTINE](sql-commands/sql-droproutine.md) — remove a routine

    [DROP RULE](sql-commands/sql-droprule.md) — remove a rewrite rule

    [DROP SCHEMA](sql-commands/sql-dropschema.md) — remove a schema

    [DROP SEQUENCE](sql-commands/sql-dropsequence.md) — remove a sequence

    [DROP SERVER](sql-commands/sql-dropserver.md) — remove a foreign server descriptor

    [DROP STATISTICS](sql-commands/sql-dropstatistics.md) — remove extended statistics

    [DROP SUBSCRIPTION](sql-commands/sql-dropsubscription.md) — remove a subscription

    [DROP TABLE](sql-commands/sql-droptable.md) — remove a table

    [DROP TABLESPACE](sql-commands/sql-droptablespace.md) — remove a tablespace

    [DROP TEXT SEARCH CONFIGURATION](sql-commands/sql-droptsconfig.md) — remove a text search configuration

    [DROP TEXT SEARCH DICTIONARY](sql-commands/sql-droptsdictionary.md) — remove a text search dictionary

    [DROP TEXT SEARCH PARSER](sql-commands/sql-droptsparser.md) — remove a text search parser

    [DROP TEXT SEARCH TEMPLATE](sql-commands/sql-droptstemplate.md) — remove a text search template

    [DROP TRANSFORM](sql-commands/sql-droptransform.md) — remove a transform

    [DROP TRIGGER](sql-commands/sql-droptrigger.md) — remove a trigger

    [DROP TYPE](sql-commands/sql-droptype.md) — remove a data type

    [DROP USER](sql-commands/sql-dropuser.md) — remove a database role

    [DROP USER MAPPING](sql-commands/sql-dropusermapping.md) — remove a user mapping for a foreign server

    [DROP VIEW](sql-commands/sql-dropview.md) — remove a view

    [END](sql-commands/sql-end.md) — commit the current transaction

    [EXECUTE](sql-commands/sql-execute.md) — execute a prepared statement

    [EXPLAIN](sql-commands/sql-explain.md) — show the execution plan of a statement

    [FETCH](sql-commands/sql-fetch.md) — retrieve rows from a query using a cursor

    [GRANT](sql-commands/sql-grant.md) — define access privileges

    [IMPORT FOREIGN SCHEMA](sql-commands/sql-importforeignschema.md) — import table definitions from a foreign server

    [INSERT](sql-commands/sql-insert.md) — create new rows in a table

    [LISTEN](sql-commands/sql-listen.md) — listen for a notification

    [LOAD](sql-commands/sql-load.md) — load a shared library file

    [LOCK](sql-commands/sql-lock.md) — lock a table

    [MERGE](sql-commands/sql-merge.md) — conditionally insert, update, or delete rows of a table

    [MOVE](sql-commands/sql-move.md) — position a cursor

    [NOTIFY](sql-commands/sql-notify.md) — generate a notification

    [PREPARE](sql-commands/sql-prepare.md) — prepare a statement for execution

    [PREPARE TRANSACTION](sql-commands/sql-prepare-transaction.md) — prepare the current transaction for two-phase commit

    [REASSIGN OWNED](sql-commands/sql-reassign-owned.md) — change the ownership of database objects owned by a database role

    [REFRESH MATERIALIZED VIEW](sql-commands/sql-refreshmaterializedview.md) — replace the contents of a materialized view

    [REINDEX](sql-commands/sql-reindex.md) — rebuild indexes

    [RELEASE SAVEPOINT](sql-commands/sql-release-savepoint.md) — release a previously defined savepoint

    [RESET](sql-commands/sql-reset.md) — restore the value of a run-time parameter to the default value

    [REVOKE](sql-commands/sql-revoke.md) — remove access privileges

    [ROLLBACK](sql-commands/sql-rollback.md) — abort the current transaction

    [ROLLBACK PREPARED](sql-commands/sql-rollback-prepared.md) — cancel a transaction that was earlier prepared for two-phase commit

    [ROLLBACK TO SAVEPOINT](sql-commands/sql-rollback-to.md) — roll back to a savepoint

    [SAVEPOINT](sql-commands/sql-savepoint.md) — define a new savepoint within the current transaction

    [SECURITY LABEL](sql-commands/sql-security-label.md) — define or change a security label applied to an object

    [SELECT](sql-commands/sql-select.md) — retrieve rows from a table or view

    [SELECT INTO](sql-commands/sql-selectinto.md) — define a new table from the results of a query

    [SET](sql-commands/sql-set.md) — change a run-time parameter

    [SET CONSTRAINTS](sql-commands/sql-set-constraints.md) — set constraint check timing for the current transaction

    [SET ROLE](sql-commands/sql-set-role.md) — set the current user identifier of the current session

    [SET SESSION AUTHORIZATION](sql-commands/sql-set-session-authorization.md) — set the session user identifier and the current user identifier of the current session

    [SET TRANSACTION](sql-commands/sql-set-transaction.md) — set the characteristics of the current transaction

    [SHOW](sql-commands/sql-show.md) — show the value of a run-time parameter

    [START TRANSACTION](sql-commands/sql-start-transaction.md) — start a transaction block

    [TRUNCATE](sql-commands/sql-truncate.md) — empty a table or set of tables

    [UNLISTEN](sql-commands/sql-unlisten.md) — stop listening for a notification

    [UPDATE](sql-commands/sql-update.md) — update rows of a table

    [VACUUM](sql-commands/sql-vacuum.md) — garbage-collect and optionally analyze a database

    [VALUES](sql-commands/sql-values.md) — compute a set of rows

[II. PostgreSQL Client Applications](reference-client/README.md)
:   [clusterdb](reference-client/app-clusterdb.md) — cluster a PostgreSQL database

    [createdb](reference-client/app-createdb.md) — create a new PostgreSQL database

    [createuser](reference-client/app-createuser.md) — define a new PostgreSQL user account

    [dropdb](reference-client/app-dropdb.md) — remove a PostgreSQL database

    [dropuser](reference-client/app-dropuser.md) — remove a PostgreSQL user account

    [ecpg](reference-client/app-ecpg.md) — embedded SQL C preprocessor

    [pg_amcheck](reference-client/app-pgamcheck.md) — checks for corruption in one or more PostgreSQL databases

    [pg_basebackup](reference-client/app-pgbasebackup.md) — take a base backup of a PostgreSQL cluster

    [pgbench](reference-client/pgbench.md) — run a benchmark test on PostgreSQL

    [pg_combinebackup](reference-client/app-pgcombinebackup.md) — reconstruct a full backup from an incremental backup and dependent backups

    [pg_config](reference-client/app-pgconfig.md) — retrieve information about the installed version of PostgreSQL

    [pg_dump](reference-client/app-pgdump.md) — export a PostgreSQL database as an SQL script or to other formats

    [pg_dumpall](reference-client/app-pg-dumpall.md) — extract a PostgreSQL database cluster into a script file

    [pg_isready](reference-client/app-pg-isready.md) — check the connection status of a PostgreSQL server

    [pg_receivewal](reference-client/app-pgreceivewal.md) — stream write-ahead logs from a PostgreSQL server

    [pg_recvlogical](reference-client/app-pgrecvlogical.md) — control PostgreSQL logical decoding streams

    [pg_restore](reference-client/app-pgrestore.md) — restore a PostgreSQL database from an archive file created by pg_dump

    [pg_verifybackup](reference-client/app-pgverifybackup.md) — verify the integrity of a base backup of a PostgreSQL cluster

    [psql](reference-client/app-psql.md) — PostgreSQL interactive terminal

    [reindexdb](reference-client/app-reindexdb.md) — reindex a PostgreSQL database

    [vacuumdb](reference-client/app-vacuumdb.md) — garbage-collect and analyze a PostgreSQL database

[III. PostgreSQL Server Applications](reference-server/README.md)
:   [initdb](reference-server/app-initdb.md) — create a new PostgreSQL database cluster

    [pg_archivecleanup](reference-server/pgarchivecleanup.md) — clean up PostgreSQL WAL archive files

    [pg_checksums](reference-server/app-pgchecksums.md) — enable, disable or check data checksums in a PostgreSQL database cluster

    [pg_controldata](reference-server/app-pgcontroldata.md) — display control information of a PostgreSQL database cluster

    [pg_createsubscriber](reference-server/app-pgcreatesubscriber.md) — convert a physical replica into a new logical replica

    [pg_ctl](reference-server/app-pg-ctl.md) — initialize, start, stop, or control a PostgreSQL server

    [pg_resetwal](reference-server/app-pgresetwal.md) — reset the write-ahead log and other control information of a PostgreSQL database cluster

    [pg_rewind](reference-server/app-pgrewind.md) — synchronize a PostgreSQL data directory with another data directory that was forked from it

    [pg_test_fsync](reference-server/pgtestfsync.md) — determine fastest `wal_sync_method` for PostgreSQL

    [pg_test_timing](reference-server/pgtesttiming.md) — measure timing overhead

    [pg_upgrade](reference-server/pgupgrade.md) — upgrade a PostgreSQL server instance

    [pg_waldump](reference-server/pgwaldump.md) — display a human-readable rendering of the write-ahead log of a PostgreSQL database cluster

    [pg_walsummary](reference-server/app-pgwalsummary.md) — print contents of WAL summary files

    [postgres](reference-server/app-postgres.md) — PostgreSQL database server

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/reference.html)（英文原文，待翻譯）
