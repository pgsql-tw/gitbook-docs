# SQL Commands

---

<a id="id-1.9.3.2"></a>

This part contains reference information for the
SQL commands supported by
PostgreSQL. By “SQL” the
language in general is meant; information about the standards
conformance and compatibility of each command can be found on the
respective reference page.

**Table of Contents**

[ABORT](sql-abort.md) — abort the current transaction

[ALTER AGGREGATE](sql-alteraggregate.md) — change the definition of an aggregate function

[ALTER COLLATION](sql-altercollation.md) — change the definition of a collation

[ALTER CONVERSION](sql-alterconversion.md) — change the definition of a conversion

[ALTER DATABASE](sql-alterdatabase.md) — change a database

[ALTER DEFAULT PRIVILEGES](sql-alterdefaultprivileges.md) — define default access privileges

[ALTER DOMAIN](sql-alterdomain.md) — change the definition of a domain

[ALTER EVENT TRIGGER](sql-altereventtrigger.md) — change the definition of an event trigger

[ALTER EXTENSION](sql-alterextension.md) — change the definition of an extension

[ALTER FOREIGN DATA WRAPPER](sql-alterforeigndatawrapper.md) — change the definition of a foreign-data wrapper

[ALTER FOREIGN TABLE](sql-alterforeigntable.md) — change the definition of a foreign table

[ALTER FUNCTION](sql-alterfunction.md) — change the definition of a function

[ALTER GROUP](sql-altergroup.md) — change role name or membership

[ALTER INDEX](sql-alterindex.md) — change the definition of an index

[ALTER LANGUAGE](sql-alterlanguage.md) — change the definition of a procedural language

[ALTER LARGE OBJECT](sql-alterlargeobject.md) — change the definition of a large object

[ALTER MATERIALIZED VIEW](sql-altermaterializedview.md) — change the definition of a materialized view

[ALTER OPERATOR](sql-alteroperator.md) — change the definition of an operator

[ALTER OPERATOR CLASS](sql-alteropclass.md) — change the definition of an operator class

[ALTER OPERATOR FAMILY](sql-alteropfamily.md) — change the definition of an operator family

[ALTER POLICY](sql-alterpolicy.md) — change the definition of a row-level security policy

[ALTER PROCEDURE](sql-alterprocedure.md) — change the definition of a procedure

[ALTER PUBLICATION](sql-alterpublication.md) — change the definition of a publication

[ALTER ROLE](sql-alterrole.md) — change a database role

[ALTER ROUTINE](sql-alterroutine.md) — change the definition of a routine

[ALTER RULE](sql-alterrule.md) — change the definition of a rule

[ALTER SCHEMA](sql-alterschema.md) — change the definition of a schema

[ALTER SEQUENCE](sql-altersequence.md) — change the definition of a sequence generator

[ALTER SERVER](sql-alterserver.md) — change the definition of a foreign server

[ALTER STATISTICS](sql-alterstatistics.md) — change the definition of an extended statistics object

[ALTER SUBSCRIPTION](sql-altersubscription.md) — change the definition of a subscription

[ALTER SYSTEM](sql-altersystem.md) — change a server configuration parameter

[ALTER TABLE](sql-altertable.md) — change the definition of a table

[ALTER TABLESPACE](sql-altertablespace.md) — change the definition of a tablespace

[ALTER TEXT SEARCH CONFIGURATION](sql-altertsconfig.md) — change the definition of a text search configuration

[ALTER TEXT SEARCH DICTIONARY](sql-altertsdictionary.md) — change the definition of a text search dictionary

[ALTER TEXT SEARCH PARSER](sql-altertsparser.md) — change the definition of a text search parser

[ALTER TEXT SEARCH TEMPLATE](sql-altertstemplate.md) — change the definition of a text search template

[ALTER TRIGGER](sql-altertrigger.md) — change the definition of a trigger

[ALTER TYPE](sql-altertype.md) — change the definition of a type

[ALTER USER](sql-alteruser.md) — change a database role

[ALTER USER MAPPING](sql-alterusermapping.md) — change the definition of a user mapping

[ALTER VIEW](sql-alterview.md) — change the definition of a view

[ANALYZE](sql-analyze.md) — collect statistics about a database

[BEGIN](sql-begin.md) — start a transaction block

[CALL](sql-call.md) — invoke a procedure

[CHECKPOINT](sql-checkpoint.md) — force a write-ahead log checkpoint

[CLOSE](sql-close.md) — close a cursor

[CLUSTER](sql-cluster.md) — cluster a table according to an index

[COMMENT](sql-comment.md) — define or change the comment of an object

[COMMIT](sql-commit.md) — commit the current transaction

[COMMIT PREPARED](sql-commit-prepared.md) — commit a transaction that was earlier prepared for two-phase commit

[COPY](sql-copy.md) — copy data between a file and a table

[CREATE ACCESS METHOD](sql-create-access-method.md) — define a new access method

[CREATE AGGREGATE](sql-createaggregate.md) — define a new aggregate function

[CREATE CAST](sql-createcast.md) — define a new cast

[CREATE COLLATION](sql-createcollation.md) — define a new collation

[CREATE CONVERSION](sql-createconversion.md) — define a new encoding conversion

[CREATE DATABASE](sql-createdatabase.md) — create a new database

[CREATE DOMAIN](sql-createdomain.md) — define a new domain

[CREATE EVENT TRIGGER](sql-createeventtrigger.md) — define a new event trigger

[CREATE EXTENSION](sql-createextension.md) — install an extension

[CREATE FOREIGN DATA WRAPPER](sql-createforeigndatawrapper.md) — define a new foreign-data wrapper

[CREATE FOREIGN TABLE](sql-createforeigntable.md) — define a new foreign table

[CREATE FUNCTION](sql-createfunction.md) — define a new function

[CREATE GROUP](sql-creategroup.md) — define a new database role

[CREATE INDEX](sql-createindex.md) — define a new index

[CREATE LANGUAGE](sql-createlanguage.md) — define a new procedural language

[CREATE MATERIALIZED VIEW](sql-creatematerializedview.md) — define a new materialized view

[CREATE OPERATOR](sql-createoperator.md) — define a new operator

[CREATE OPERATOR CLASS](sql-createopclass.md) — define a new operator class

[CREATE OPERATOR FAMILY](sql-createopfamily.md) — define a new operator family

[CREATE POLICY](sql-createpolicy.md) — define a new row-level security policy for a table

[CREATE PROCEDURE](sql-createprocedure.md) — define a new procedure

[CREATE PUBLICATION](sql-createpublication.md) — define a new publication

[CREATE ROLE](sql-createrole.md) — define a new database role

[CREATE RULE](sql-createrule.md) — define a new rewrite rule

[CREATE SCHEMA](sql-createschema.md) — define a new schema

[CREATE SEQUENCE](sql-createsequence.md) — define a new sequence generator

[CREATE SERVER](sql-createserver.md) — define a new foreign server

[CREATE STATISTICS](sql-createstatistics.md) — define extended statistics

[CREATE SUBSCRIPTION](sql-createsubscription.md) — define a new subscription

[CREATE TABLE](sql-createtable.md) — define a new table

[CREATE TABLE AS](sql-createtableas.md) — define a new table from the results of a query

[CREATE TABLESPACE](sql-createtablespace.md) — define a new tablespace

[CREATE TEXT SEARCH CONFIGURATION](sql-createtsconfig.md) — define a new text search configuration

[CREATE TEXT SEARCH DICTIONARY](sql-createtsdictionary.md) — define a new text search dictionary

[CREATE TEXT SEARCH PARSER](sql-createtsparser.md) — define a new text search parser

[CREATE TEXT SEARCH TEMPLATE](sql-createtstemplate.md) — define a new text search template

[CREATE TRANSFORM](sql-createtransform.md) — define a new transform

[CREATE TRIGGER](sql-createtrigger.md) — define a new trigger

[CREATE TYPE](sql-createtype.md) — define a new data type

[CREATE USER](sql-createuser.md) — define a new database role

[CREATE USER MAPPING](sql-createusermapping.md) — define a new mapping of a user to a foreign server

[CREATE VIEW](sql-createview.md) — define a new view

[DEALLOCATE](sql-deallocate.md) — deallocate a prepared statement

[DECLARE](sql-declare.md) — define a cursor

[DELETE](sql-delete.md) — delete rows of a table

[DISCARD](sql-discard.md) — discard session state

[DO](sql-do.md) — execute an anonymous code block

[DROP ACCESS METHOD](sql-drop-access-method.md) — remove an access method

[DROP AGGREGATE](sql-dropaggregate.md) — remove an aggregate function

[DROP CAST](sql-dropcast.md) — remove a cast

[DROP COLLATION](sql-dropcollation.md) — remove a collation

[DROP CONVERSION](sql-dropconversion.md) — remove a conversion

[DROP DATABASE](sql-dropdatabase.md) — remove a database

[DROP DOMAIN](sql-dropdomain.md) — remove a domain

[DROP EVENT TRIGGER](sql-dropeventtrigger.md) — remove an event trigger

[DROP EXTENSION](sql-dropextension.md) — remove an extension

[DROP FOREIGN DATA WRAPPER](sql-dropforeigndatawrapper.md) — remove a foreign-data wrapper

[DROP FOREIGN TABLE](sql-dropforeigntable.md) — remove a foreign table

[DROP FUNCTION](sql-dropfunction.md) — remove a function

[DROP GROUP](sql-dropgroup.md) — remove a database role

[DROP INDEX](sql-dropindex.md) — remove an index

[DROP LANGUAGE](sql-droplanguage.md) — remove a procedural language

[DROP MATERIALIZED VIEW](sql-dropmaterializedview.md) — remove a materialized view

[DROP OPERATOR](sql-dropoperator.md) — remove an operator

[DROP OPERATOR CLASS](sql-dropopclass.md) — remove an operator class

[DROP OPERATOR FAMILY](sql-dropopfamily.md) — remove an operator family

[DROP OWNED](sql-drop-owned.md) — remove database objects owned by a database role

[DROP POLICY](sql-droppolicy.md) — remove a row-level security policy from a table

[DROP PROCEDURE](sql-dropprocedure.md) — remove a procedure

[DROP PUBLICATION](sql-droppublication.md) — remove a publication

[DROP ROLE](sql-droprole.md) — remove a database role

[DROP ROUTINE](sql-droproutine.md) — remove a routine

[DROP RULE](sql-droprule.md) — remove a rewrite rule

[DROP SCHEMA](sql-dropschema.md) — remove a schema

[DROP SEQUENCE](sql-dropsequence.md) — remove a sequence

[DROP SERVER](sql-dropserver.md) — remove a foreign server descriptor

[DROP STATISTICS](sql-dropstatistics.md) — remove extended statistics

[DROP SUBSCRIPTION](sql-dropsubscription.md) — remove a subscription

[DROP TABLE](sql-droptable.md) — remove a table

[DROP TABLESPACE](sql-droptablespace.md) — remove a tablespace

[DROP TEXT SEARCH CONFIGURATION](sql-droptsconfig.md) — remove a text search configuration

[DROP TEXT SEARCH DICTIONARY](sql-droptsdictionary.md) — remove a text search dictionary

[DROP TEXT SEARCH PARSER](sql-droptsparser.md) — remove a text search parser

[DROP TEXT SEARCH TEMPLATE](sql-droptstemplate.md) — remove a text search template

[DROP TRANSFORM](sql-droptransform.md) — remove a transform

[DROP TRIGGER](sql-droptrigger.md) — remove a trigger

[DROP TYPE](sql-droptype.md) — remove a data type

[DROP USER](sql-dropuser.md) — remove a database role

[DROP USER MAPPING](sql-dropusermapping.md) — remove a user mapping for a foreign server

[DROP VIEW](sql-dropview.md) — remove a view

[END](sql-end.md) — commit the current transaction

[EXECUTE](sql-execute.md) — execute a prepared statement

[EXPLAIN](sql-explain.md) — show the execution plan of a statement

[FETCH](sql-fetch.md) — retrieve rows from a query using a cursor

[GRANT](sql-grant.md) — define access privileges

[IMPORT FOREIGN SCHEMA](sql-importforeignschema.md) — import table definitions from a foreign server

[INSERT](sql-insert.md) — create new rows in a table

[LISTEN](sql-listen.md) — listen for a notification

[LOAD](sql-load.md) — load a shared library file

[LOCK](sql-lock.md) — lock a table

[MERGE](sql-merge.md) — conditionally insert, update, or delete rows of a table

[MOVE](sql-move.md) — position a cursor

[NOTIFY](sql-notify.md) — generate a notification

[PREPARE](sql-prepare.md) — prepare a statement for execution

[PREPARE TRANSACTION](sql-prepare-transaction.md) — prepare the current transaction for two-phase commit

[REASSIGN OWNED](sql-reassign-owned.md) — change the ownership of database objects owned by a database role

[REFRESH MATERIALIZED VIEW](sql-refreshmaterializedview.md) — replace the contents of a materialized view

[REINDEX](sql-reindex.md) — rebuild indexes

[RELEASE SAVEPOINT](sql-release-savepoint.md) — release a previously defined savepoint

[RESET](sql-reset.md) — restore the value of a run-time parameter to the default value

[REVOKE](sql-revoke.md) — remove access privileges

[ROLLBACK](sql-rollback.md) — abort the current transaction

[ROLLBACK PREPARED](sql-rollback-prepared.md) — cancel a transaction that was earlier prepared for two-phase commit

[ROLLBACK TO SAVEPOINT](sql-rollback-to.md) — roll back to a savepoint

[SAVEPOINT](sql-savepoint.md) — define a new savepoint within the current transaction

[SECURITY LABEL](sql-security-label.md) — define or change a security label applied to an object

[SELECT](sql-select.md) — retrieve rows from a table or view

[SELECT INTO](sql-selectinto.md) — define a new table from the results of a query

[SET](sql-set.md) — change a run-time parameter

[SET CONSTRAINTS](sql-set-constraints.md) — set constraint check timing for the current transaction

[SET ROLE](sql-set-role.md) — set the current user identifier of the current session

[SET SESSION AUTHORIZATION](sql-set-session-authorization.md) — set the session user identifier and the current user identifier of the current session

[SET TRANSACTION](sql-set-transaction.md) — set the characteristics of the current transaction

[SHOW](sql-show.md) — show the value of a run-time parameter

[START TRANSACTION](sql-start-transaction.md) — start a transaction block

[TRUNCATE](sql-truncate.md) — empty a table or set of tables

[UNLISTEN](sql-unlisten.md) — stop listening for a notification

[UPDATE](sql-update.md) — update rows of a table

[VACUUM](sql-vacuum.md) — garbage-collect and optionally analyze a database

[VALUES](sql-values.md) — compute a set of rows

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-commands.html)（英文原文，待翻譯）
