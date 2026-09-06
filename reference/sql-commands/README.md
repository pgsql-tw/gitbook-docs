# I. SQL 指令

本部分包含 PostgreSQL 支援的 SQL 指令的參考訊息。一般而言，「SQL」是指語言；內容包含了有關各標準的一致性和相容性。

連結將會連結至 PostgreSQL 官方使用手冊，本手冊連結請使用左側目錄。

**Table of Contents**

[ABORT](abort.md) — abort the current transaction

[ALTER AGGREGATE](alter-aggregate.md) — change the definition of an aggregate function

[ALTER COLLATION](alter-collation.md) — change the definition of a collation

[ALTER CONVERSION](alter-conversion.md) — change the definition of a conversion

[ALTER DATABASE](alter-database.md) — change a database

[ALTER DEFAULT PRIVILEGES](alter-default-privileges.md) — define default access privileges

[ALTER DOMAIN](alter-domain.md) — change the definition of a domain

[ALTER EVENT TRIGGER](alter-event-trigger.md) — change the definition of an event trigger

[ALTER EXTENSION](alter-extension.md) — change the definition of an extension

[ALTER FOREIGN DATA WRAPPER](alter-foreign-data-wrapper.md) — change the definition of a foreign-data wrapper

[ALTER FOREIGN TABLE](alter-foreign-table.md) — change the definition of a foreign table

[ALTER FUNCTION](alter-function.md) — change the definition of a function

[ALTER GROUP](alter-group.md) — change role name or membership

[ALTER INDEX](alter-index.md) — change the definition of an index

[ALTER LANGUAGE](alter-language.md) — change the definition of a procedural language

[ALTER LARGE OBJECT](alter-large-object.md) — change the definition of a large object

[ALTER MATERIALIZED VIEW](alter-materialized-view.md) — change the definition of a materialized view

[ALTER OPERATOR](alter-operator.md) — change the definition of an operator

[ALTER OPERATOR CLASS](alter-operator-class.md) — change the definition of an operator class

[ALTER OPERATOR FAMILY](alter-operator-family.md) — change the definition of an operator family

[ALTER POLICY](alter-policy.md) — change the definition of a row-level security policy

[ALTER PROCEDURE](alter-procedure.md) — change the definition of a procedure

[ALTER PUBLICATION](alter-publication.md) — change the definition of a publication

[ALTER ROLE](alter-role.md) — change a database role

[ALTER ROUTINE](alter-routine.md) — change the definition of a routine

[ALTER RULE](alter-rule.md) — change the definition of a rule

[ALTER SCHEMA](alter-schema.md) — change the definition of a schema

[ALTER SEQUENCE](alter-sequence.md) — change the definition of a sequence generator

[ALTER SERVER](alter-server.md) — change the definition of a foreign server

[ALTER STATISTICS](alter-statistics.md) — change the definition of an extended statistics object

[ALTER SUBSCRIPTION](alter-subscription.md) — change the definition of a subscription

[ALTER SYSTEM](alter-system.md) — change a server configuration parameter

[ALTER TABLE](alter-table.md) — change the definition of a table

[ALTER TABLESPACE](alter-tablespace.md) — change the definition of a tablespace

[ALTER TEXT SEARCH CONFIGURATION](alter-text-search-configuration.md) — change the definition of a text search configuration

[ALTER TEXT SEARCH DICTIONARY](alter-text-search-dictionary.md) — change the definition of a text search dictionary

[ALTER TEXT SEARCH PARSER](alter-text-search-parser.md) — change the definition of a text search parser

[ALTER TEXT SEARCH TEMPLATE](alter-text-search-template.md) — change the definition of a text search template

[ALTER TRIGGER](alter-trigger.md) — change the definition of a trigger

[ALTER TYPE](alter-type.md) — change the definition of a type

[ALTER USER](alter-user.md) — change a database role

[ALTER USER MAPPING](alter-user-mapping.md) — change the definition of a user mapping

[ALTER VIEW](alter-view.md) — change the definition of a view

[ANALYZE](analyze.md) — collect statistics about a database

[BEGIN](begin.md) — start a transaction block

[CALL](call.md) — invoke a procedure

[CHECKPOINT](checkpoint.md) — force a write-ahead log checkpoint

[CLOSE](close.md) — close a cursor

[CLUSTER](cluster.md) — cluster a table according to an index

[COMMENT](comment.md) — define or change the comment of an object

[COMMIT](commit.md) — commit the current transaction

[COMMIT PREPARED](commit-prepared.md) — commit a transaction that was earlier prepared for two-phase commit

[COPY](copy.md) — copy data between a file and a table

[CREATE ACCESS METHOD](create-access-method.md) — define a new access method

[CREATE AGGREGATE](create-aggregate.md) — define a new aggregate function

[CREATE CAST](create-cast.md) — define a new cast

[CREATE COLLATION](create-collation.md) — define a new collation

[CREATE CONVERSION](create-conversion.md) — define a new encoding conversion

[CREATE DATABASE](create-database.md) — create a new database

[CREATE DOMAIN](create-domain.md) — define a new domain

[CREATE EVENT TRIGGER](create-event-trigger.md) — define a new event trigger

[CREATE EXTENSION](create-extension.md) — install an extension

[CREATE FOREIGN DATA WRAPPER](create-foreign-data-wrapper.md) — define a new foreign-data wrapper

[CREATE FOREIGN TABLE](create-foreign-table.md) — define a new foreign table

[CREATE FUNCTION](create-function.md) — define a new function

[CREATE GROUP](create-group.md) — define a new database role

[CREATE INDEX](create-index.md) — define a new index

[CREATE LANGUAGE](create-language.md) — define a new procedural language

[CREATE MATERIALIZED VIEW](create-materialized-view.md) — define a new materialized view

[CREATE OPERATOR](create-operator.md) — define a new operator

[CREATE OPERATOR CLASS](create-operator-class.md) — define a new operator class

[CREATE OPERATOR FAMILY](create-operator-family.md) — define a new operator family

[CREATE POLICY](create-policy.md) — define a new row-level security policy for a table

[CREATE PROCEDURE](create-procedure.md) — define a new procedure

[CREATE PUBLICATION](create-publication.md) — define a new publication

[CREATE ROLE](create-role.md) — define a new database role

[CREATE RULE](create-rule.md) — define a new rewrite rule

[CREATE SCHEMA](create-schema.md) — define a new schema

[CREATE SEQUENCE](create-sequence.md) — define a new sequence generator

[CREATE SERVER](create-server.md) — define a new foreign server

[CREATE STATISTICS](create-statistics.md) — define extended statistics

[CREATE SUBSCRIPTION](create-subscription.md) — define a new subscription

[CREATE TABLE](create-table.md) — define a new table

[CREATE TABLE AS](create-table-as.md) — define a new table from the results of a query

[CREATE TABLESPACE](create-tablespace.md) — define a new tablespace

[CREATE TEXT SEARCH CONFIGURATION](create-text-search-configuration.md) — define a new text search configuration

[CREATE TEXT SEARCH DICTIONARY](create-text-search-dictionary.md) — define a new text search dictionary

[CREATE TEXT SEARCH PARSER](create-text-search-parser.md) — define a new text search parser

[CREATE TEXT SEARCH TEMPLATE](create-text-search-template.md) — define a new text search template

[CREATE TRANSFORM](create-transform.md) — define a new transform

[CREATE TRIGGER](create-trigger.md) — define a new trigger

[CREATE TYPE](create-type.md) — define a new data type

[CREATE USER](create-user.md) — define a new database role

[CREATE USER MAPPING](create-user-mapping.md) — define a new mapping of a user to a foreign server

[CREATE VIEW](create-view.md) — define a new view

[DEALLOCATE](deallocate.md) — deallocate a prepared statement

[DECLARE](declare.md) — define a cursor

[DELETE](delete.md) — delete rows of a table

[DISCARD](discard.md) — discard session state

[DO](do.md) — execute an anonymous code block

[DROP ACCESS METHOD](drop-access-method.md) — remove an access method

[DROP AGGREGATE](drop-aggregate.md) — remove an aggregate function

[DROP CAST](drop-cast.md) — remove a cast

[DROP COLLATION](drop-collation.md) — remove a collation

[DROP CONVERSION](drop-conversion.md) — remove a conversion

[DROP DATABASE](drop-database.md) — remove a database

[DROP DOMAIN](drop-domain.md) — remove a domain

[DROP EVENT TRIGGER](drop-event-trigger.md) — remove an event trigger

[DROP EXTENSION](drop-extension.md) — remove an extension

[DROP FOREIGN DATA WRAPPER](drop-foreign-data-wrapper.md) — remove a foreign-data wrapper

[DROP FOREIGN TABLE](drop-foreign-table.md) — remove a foreign table

[DROP FUNCTION](drop-function.md) — remove a function

[DROP GROUP](drop-group.md) — remove a database role

[DROP INDEX](drop-index.md) — remove an index

[DROP LANGUAGE](drop-language.md) — remove a procedural language

[DROP MATERIALIZED VIEW](drop-materialized-view.md) — remove a materialized view

[DROP OPERATOR](drop-operator.md) — remove an operator

[DROP OPERATOR CLASS](drop-operator-class.md) — remove an operator class

[DROP OPERATOR FAMILY](drop-operator-family.md) — remove an operator family

[DROP OWNED](drop-owned.md) — remove database objects owned by a database role

[DROP POLICY](drop-policy.md) — remove a row-level security policy from a table

[DROP PROCEDURE](drop-procedure.md) — remove a procedure

[DROP PUBLICATION](drop-publication.md) — remove a publication

[DROP ROLE](drop-role.md) — remove a database role

[DROP ROUTINE](drop-routine.md) — remove a routine

[DROP RULE](drop-rule.md) — remove a rewrite rule

[DROP SCHEMA](drop-schema.md) — remove a schema

[DROP SEQUENCE](drop-sequence.md) — remove a sequence

[DROP SERVER](drop-server.md) — remove a foreign server descriptor

[DROP STATISTICS](drop-statistics.md) — remove extended statistics

[DROP SUBSCRIPTION](drop-subscription.md) — remove a subscription

[DROP TABLE](drop-table.md) — remove a table

[DROP TABLESPACE](drop-tablespace.md) — remove a tablespace

[DROP TEXT SEARCH CONFIGURATION](drop-text-search-configuration.md) — remove a text search configuration

[DROP TEXT SEARCH DICTIONARY](drop-text-search-dictionary.md) — remove a text search dictionary

[DROP TEXT SEARCH PARSER](drop-text-search-parser.md) — remove a text search parser

[DROP TEXT SEARCH TEMPLATE](drop-text-search-template.md) — remove a text search template

[DROP TRANSFORM](drop-transform.md) — remove a transform

[DROP TRIGGER](drop-trigger.md) — remove a trigger

[DROP TYPE](drop-type.md) — remove a data type

[DROP USER](drop-user.md) — remove a database role

[DROP USER MAPPING](drop-user-mapping.md) — remove a user mapping for a foreign server

[DROP VIEW](drop-view.md) — remove a view

[END](end.md) — commit the current transaction

[EXECUTE](execute.md) — execute a prepared statement

[EXPLAIN](explain.md) — show the execution plan of a statement

[FETCH](fetch.md) — retrieve rows from a query using a cursor

[GRANT](grant.md) — define access privileges

[IMPORT FOREIGN SCHEMA](import-foreign-schema.md) — import table definitions from a foreign server

[INSERT](insert.md) — create new rows in a table

[LISTEN](listen.md) — listen for a notification

[LOAD](load.md) — load a shared library file

[LOCK](lock.md) — lock a table

[MERGE](merge.md) — conditionally insert, update, or delete rows of a table

[MOVE](move.md) — position a cursor

[NOTIFY](notify.md) — generate a notification

[PREPARE](prepare.md) — prepare a statement for execution

[PREPARE TRANSACTION](prepare-transaction.md) — prepare the current transaction for two-phase commit

[REASSIGN OWNED](reassign-owned.md) — change the ownership of database objects owned by a database role

[REFRESH MATERIALIZED VIEW](refresh-materialized-view.md) — replace the contents of a materialized view

[REINDEX](reindex.md) — rebuild indexes

[RELEASE SAVEPOINT](release-savepoint.md) — destroy a previously defined savepoint

[RESET](reset.md) — restore the value of a run-time parameter to the default value

[REVOKE](revoke.md) — remove access privileges

[ROLLBACK](rollback.md) — abort the current transaction

[ROLLBACK PREPARED](rollback-prepared.md) — cancel a transaction that was earlier prepared for two-phase commit

[ROLLBACK TO SAVEPOINT](rollback-to-savepoint.md) — roll back to a savepoint

[SAVEPOINT](savepoint.md) — define a new savepoint within the current transaction

[SECURITY LABEL](security-label.md) — define or change a security label applied to an object

[SELECT](select.md) — retrieve rows from a table or view

[SELECT INTO](select-into.md) — define a new table from the results of a query

[SET](set.md) — change a run-time parameter

[SET CONSTRAINTS](set-constraints.md) — set constraint check timing for the current transaction

[SET ROLE](set-role.md) — set the current user identifier of the current session

[SET SESSION AUTHORIZATION](set-session-authorization.md) — set the session user identifier and the current user identifier of the current session

[SET TRANSACTION](set-transaction.md) — set the characteristics of the current transaction

[SHOW](show.md) — show the value of a run-time parameter

[START TRANSACTION](start-transaction.md) — start a transaction block

[TRUNCATE](truncate.md) — empty a table or set of tables

[UNLISTEN](unlisten.md) — stop listening for a notification

[UPDATE](update.md) — update rows of a table

[VACUUM](vacuum.md) — garbage-collect and optionally analyze a database

[VALUES](values.md) — compute a set of rows
