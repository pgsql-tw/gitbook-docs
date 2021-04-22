# 9.25. 系統資訊函數

[Table 9.63](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-INFO-SESSION-TABLE) shows several functions that extract session and system information.

In addition to the functions listed in this section, there are a number of functions related to the statistics system that also provide system information. See [Section 27.2.2](https://www.postgresql.org/docs/12/monitoring-stats.html#MONITORING-STATS-VIEWS) for more information.

## **Table 9.63. Session Information Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `current_catalog` | `name` | name of current database \(called “catalog” in the SQL standard\) |
| `current_database()` | `name` | name of current database |
| `current_query()` | `text` | text of the currently executing query, as submitted by the client \(might contain more than one statement\) |
| `current_role` | `name` | equivalent to `current_user` |
| `current_schema`\[\(\)\] | `name` | name of current schema |
| `current_schemas(boolean`\) | `name[]` | names of schemas in search path, optionally including implicit schemas |
| `current_user` | `name` | user name of current execution context |
| `inet_client_addr()` | `inet` | address of the remote connection |
| `inet_client_port()` | `int` | port of the remote connection |
| `inet_server_addr()` | `inet` | address of the local connection |
| `inet_server_port()` | `int` | port of the local connection |
| `pg_backend_pid()` | `int` | Process ID of the server process attached to the current session |
| `pg_blocking_pids(int`\) | `int[]` | Process ID\(s\) that are blocking specified server process ID from acquiring a lock |
| `pg_conf_load_time()` | `timestamp with time zone` | configuration load time |
| `pg_current_logfile([text`\]\) | `text` | Primary log file name, or log in the requested format, currently in use by the logging collector |
| `pg_my_temp_schema()` | `oid` | OID of session's temporary schema, or 0 if none |
| `pg_is_other_temp_schema(oid`\) | `boolean` | is schema another session's temporary schema? |
| `pg_jit_available()` | `boolean` | is a JIT compiler extension available \(see [Chapter 31](https://www.postgresql.org/docs/12/jit.html)\) and the [jit](https://www.postgresql.org/docs/12/runtime-config-query.html#GUC-JIT) configuration parameter set to `on`. |
| `pg_listening_channels()` | `setof text` | channel names that the session is currently listening on |
| `pg_notification_queue_usage()` | `double` | fraction of the asynchronous notification queue currently occupied \(0-1\) |
| `pg_postmaster_start_time()` | `timestamp with time zone` | server start time |
| `pg_safe_snapshot_blocking_pids(int`\) | `int[]` | Process ID\(s\) that are blocking specified server process ID from acquiring a safe snapshot |
| `pg_trigger_depth()` | `int` | current nesting level of PostgreSQL triggers \(0 if not called, directly or indirectly, from inside a trigger\) |
| `session_user` | `name` | session user name |
| `user` | `name` | equivalent to `current_user` |
| `version()` | `text` | PostgreSQL version information. See also [server\_version\_num](https://www.postgresql.org/docs/12/runtime-config-preset.html#GUC-SERVER-VERSION-NUM) for a machine-readable version. |

## Note

`current_catalog`, `current_role`, `current_schema`, `current_user`, `session_user`, and `user` have special syntactic status in SQL: they must be called without trailing parentheses. \(In PostgreSQL, parentheses can optionally be used with `current_schema`, but not with the others.\)

The `session_user` is normally the user who initiated the current database connection; but superusers can change this setting with [SET SESSION AUTHORIZATION](https://www.postgresql.org/docs/12/sql-set-session-authorization.html). The `current_user` is the user identifier that is applicable for permission checking. Normally it is equal to the session user, but it can be changed with [SET ROLE](https://www.postgresql.org/docs/12/sql-set-role.html). It also changes during the execution of functions with the attribute `SECURITY DEFINER`. In Unix parlance, the session user is the “real user” and the current user is the “effective user”. `current_role` and `user` are synonyms for `current_user`. \(The SQL standard draws a distinction between `current_role` and `current_user`, but PostgreSQL does not, since it unifies users and roles into a single kind of entity.\)

`current_schema` returns the name of the schema that is first in the search path \(or a null value if the search path is empty\). This is the schema that will be used for any tables or other named objects that are created without specifying a target schema. `current_schemas(boolean)` returns an array of the names of all schemas presently in the search path. The Boolean option determines whether or not implicitly included system schemas such as `pg_catalog` are included in the returned search path.

## Note

The search path can be altered at run time. The command is:

```text
SET search_path TO schema [, schema, ...]
```

`inet_client_addr` returns the IP address of the current client, and `inet_client_port` returns the port number. `inet_server_addr` returns the IP address on which the server accepted the current connection, and `inet_server_port` returns the port number. All these functions return NULL if the current connection is via a Unix-domain socket.

`pg_blocking_pids` returns an array of the process IDs of the sessions that are blocking the server process with the specified process ID, or an empty array if there is no such server process or it is not blocked. One server process blocks another if it either holds a lock that conflicts with the blocked process's lock request \(hard block\), or is waiting for a lock that would conflict with the blocked process's lock request and is ahead of it in the wait queue \(soft block\). When using parallel queries the result always lists client-visible process IDs \(that is, `pg_backend_pid` results\) even if the actual lock is held or awaited by a child worker process. As a result of that, there may be duplicated PIDs in the result. Also note that when a prepared transaction holds a conflicting lock, it will be represented by a zero process ID in the result of this function. Frequent calls to this function could have some impact on database performance, because it needs exclusive access to the lock manager's shared state for a short time.

`pg_conf_load_time` returns the `timestamp with time zone` when the server configuration files were last loaded. \(If the current session was alive at the time, this will be the time when the session itself re-read the configuration files, so the reading will vary a little in different sessions. Otherwise it is the time when the postmaster process re-read the configuration files.\)

`pg_current_logfile` returns, as `text`, the path of the log file\(s\) currently in use by the logging collector. The path includes the [log\_directory](https://www.postgresql.org/docs/12/runtime-config-logging.html#GUC-LOG-DIRECTORY) directory and the log file name. Log collection must be enabled or the return value is `NULL`. When multiple log files exist, each in a different format, `pg_current_logfile` called without arguments returns the path of the file having the first format found in the ordered list: stderr, csvlog. `NULL` is returned when no log file has any of these formats. To request a specific file format supply, as `text`, either csvlog or stderr as the value of the optional parameter. The return value is `NULL` when the log format requested is not a configured [log\_destination](https://www.postgresql.org/docs/12/runtime-config-logging.html#GUC-LOG-DESTINATION). The `pg_current_logfile` reflects the contents of the `current_logfiles` file.

`pg_my_temp_schema` returns the OID of the current session's temporary schema, or zero if it has none \(because it has not created any temporary tables\). `pg_is_other_temp_schema` returns true if the given OID is the OID of another session's temporary schema. \(This can be useful, for example, to exclude other sessions' temporary tables from a catalog display.\)

`pg_listening_channels` returns a set of names of asynchronous notification channels that the current session is listening to. `pg_notification_queue_usage` returns the fraction of the total available space for notifications currently occupied by notifications that are waiting to be processed, as a `double` in the range 0-1. See [LISTEN](https://www.postgresql.org/docs/12/sql-listen.html) and [NOTIFY](https://www.postgresql.org/docs/12/sql-notify.html) for more information.

`pg_postmaster_start_time` returns the `timestamp with time zone` when the server started.

`pg_safe_snapshot_blocking_pids` returns an array of the process IDs of the sessions that are blocking the server process with the specified process ID from acquiring a safe snapshot, or an empty array if there is no such server process or it is not blocked. A session running a `SERIALIZABLE` transaction blocks a `SERIALIZABLE READ ONLY DEFERRABLE` transaction from acquiring a snapshot until the latter determines that it is safe to avoid taking any predicate locks. See [Section 13.2.3](https://www.postgresql.org/docs/12/transaction-iso.html#XACT-SERIALIZABLE) for more information about serializable and deferrable transactions. Frequent calls to this function could have some impact on database performance, because it needs access to the predicate lock manager's shared state for a short time.

`version` returns a string describing the PostgreSQL server's version. You can also get this information from [server\_version](https://www.postgresql.org/docs/12/runtime-config-preset.html#GUC-SERVER-VERSION) or for a machine-readable version, [server\_version\_num](https://www.postgresql.org/docs/12/runtime-config-preset.html#GUC-SERVER-VERSION-NUM). Software developers should use `server_version_num` \(available since 8.2\) or [`PQserverVersion`](https://www.postgresql.org/docs/12/libpq-status.html#LIBPQ-PQSERVERVERSION) instead of parsing the text version.

[Table 9.64](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-INFO-ACCESS-TABLE) lists functions that allow the user to query object access privileges programmatically. See [Section 5.7](https://www.postgresql.org/docs/12/ddl-priv.html) for more information about privileges.

## **Table 9.64. Access Privilege Inquiry Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `has_any_column_privilege`\(_`user`_, _`table`_, _`privilege`_\) | `boolean` | does user have privilege for any column of table |
| `has_any_column_privilege`\(_`table`_, _`privilege`_\) | `boolean` | does current user have privilege for any column of table |
| `has_column_privilege`\(_`user`_, _`table`_, _`column`_, _`privilege`_\) | `boolean` | does user have privilege for column |
| `has_column_privilege`\(_`table`_, _`column`_, _`privilege`_\) | `boolean` | does current user have privilege for column |
| `has_database_privilege`\(_`user`_, _`database`_, _`privilege`_\) | `boolean` | does user have privilege for database |
| `has_database_privilege`\(_`database`_, _`privilege`_\) | `boolean` | does current user have privilege for database |
| `has_foreign_data_wrapper_privilege`\(_`user`_, _`fdw`_, _`privilege`_\) | `boolean` | does user have privilege for foreign-data wrapper |
| `has_foreign_data_wrapper_privilege`\(_`fdw`_, _`privilege`_\) | `boolean` | does current user have privilege for foreign-data wrapper |
| `has_function_privilege`\(_`user`_, _`function`_, _`privilege`_\) | `boolean` | does user have privilege for function |
| `has_function_privilege`\(_`function`_, _`privilege`_\) | `boolean` | does current user have privilege for function |
| `has_language_privilege`\(_`user`_, _`language`_, _`privilege`_\) | `boolean` | does user have privilege for language |
| `has_language_privilege`\(_`language`_, _`privilege`_\) | `boolean` | does current user have privilege for language |
| `has_schema_privilege`\(_`user`_, _`schema`_, _`privilege`_\) | `boolean` | does user have privilege for schema |
| `has_schema_privilege`\(_`schema`_, _`privilege`_\) | `boolean` | does current user have privilege for schema |
| `has_sequence_privilege`\(_`user`_, _`sequence`_, _`privilege`_\) | `boolean` | does user have privilege for sequence |
| `has_sequence_privilege`\(_`sequence`_, _`privilege`_\) | `boolean` | does current user have privilege for sequence |
| `has_server_privilege`\(_`user`_, _`server`_, _`privilege`_\) | `boolean` | does user have privilege for foreign server |
| `has_server_privilege`\(_`server`_, _`privilege`_\) | `boolean` | does current user have privilege for foreign server |
| `has_table_privilege`\(_`user`_, _`table`_, _`privilege`_\) | `boolean` | does user have privilege for table |
| `has_table_privilege`\(_`table`_, _`privilege`_\) | `boolean` | does current user have privilege for table |
| `has_tablespace_privilege`\(_`user`_, _`tablespace`_, _`privilege`_\) | `boolean` | does user have privilege for tablespace |
| `has_tablespace_privilege`\(_`tablespace`_, _`privilege`_\) | `boolean` | does current user have privilege for tablespace |
| `has_type_privilege`\(_`user`_, _`type`_, _`privilege`_\) | `boolean` | does user have privilege for type |
| `has_type_privilege`\(_`type`_, _`privilege`_\) | `boolean` | does current user have privilege for type |
| `pg_has_role`\(_`user`_, _`role`_, _`privilege`_\) | `boolean` | does user have privilege for role |
| `pg_has_role`\(_`role`_, _`privilege`_\) | `boolean` | does current user have privilege for role |
| `row_security_active`\(_`table`_\) | `boolean` | does current user have row level security active for table |

`has_table_privilege` checks whether a user can access a table in a particular way. The user can be specified by name, by OID \(`pg_authid.oid`\), `public` to indicate the PUBLIC pseudo-role, or if the argument is omitted `current_user` is assumed. The table can be specified by name or by OID. \(Thus, there are actually six variants of `has_table_privilege`, which can be distinguished by the number and types of their arguments.\) When specifying by name, the name can be schema-qualified if necessary. The desired access privilege type is specified by a text string, which must evaluate to one of the values `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, `REFERENCES`, or `TRIGGER`. Optionally, `WITH GRANT OPTION` can be added to a privilege type to test whether the privilege is held with grant option. Also, multiple privilege types can be listed separated by commas, in which case the result will be `true` if any of the listed privileges is held. \(Case of the privilege string is not significant, and extra whitespace is allowed between but not within privilege names.\) Some examples:

```text
SELECT has_table_privilege('myschema.mytable', 'select');
SELECT has_table_privilege('joe', 'mytable', 'INSERT, SELECT WITH GRANT OPTION');
```

`has_sequence_privilege` checks whether a user can access a sequence in a particular way. The possibilities for its arguments are analogous to `has_table_privilege`. The desired access privilege type must evaluate to one of `USAGE`, `SELECT`, or `UPDATE`.

`has_any_column_privilege` checks whether a user can access any column of a table in a particular way. Its argument possibilities are analogous to `has_table_privilege`, except that the desired access privilege type must evaluate to some combination of `SELECT`, `INSERT`, `UPDATE`, or `REFERENCES`. Note that having any of these privileges at the table level implicitly grants it for each column of the table, so `has_any_column_privilege` will always return `true` if `has_table_privilege` does for the same arguments. But `has_any_column_privilege` also succeeds if there is a column-level grant of the privilege for at least one column.

`has_column_privilege` checks whether a user can access a column in a particular way. Its argument possibilities are analogous to `has_table_privilege`, with the addition that the column can be specified either by name or attribute number. The desired access privilege type must evaluate to some combination of `SELECT`, `INSERT`, `UPDATE`, or `REFERENCES`. Note that having any of these privileges at the table level implicitly grants it for each column of the table.

`has_database_privilege` checks whether a user can access a database in a particular way. Its argument possibilities are analogous to `has_table_privilege`. The desired access privilege type must evaluate to some combination of `CREATE`, `CONNECT`, `TEMPORARY`, or `TEMP` \(which is equivalent to `TEMPORARY`\).

`has_function_privilege` checks whether a user can access a function in a particular way. Its argument possibilities are analogous to `has_table_privilege`. When specifying a function by a text string rather than by OID, the allowed input is the same as for the `regprocedure` data type \(see [Section 8.19](https://www.postgresql.org/docs/12/datatype-oid.html)\). The desired access privilege type must evaluate to `EXECUTE`. An example is:

```text
SELECT has_function_privilege('joeuser', 'myfunc(int, text)', 'execute');
```

`has_foreign_data_wrapper_privilege` checks whether a user can access a foreign-data wrapper in a particular way. Its argument possibilities are analogous to `has_table_privilege`. The desired access privilege type must evaluate to `USAGE`.

`has_language_privilege` checks whether a user can access a procedural language in a particular way. Its argument possibilities are analogous to `has_table_privilege`. The desired access privilege type must evaluate to `USAGE`.

`has_schema_privilege` checks whether a user can access a schema in a particular way. Its argument possibilities are analogous to `has_table_privilege`. The desired access privilege type must evaluate to some combination of `CREATE` or `USAGE`.

`has_server_privilege` checks whether a user can access a foreign server in a particular way. Its argument possibilities are analogous to `has_table_privilege`. The desired access privilege type must evaluate to `USAGE`.

`has_tablespace_privilege` checks whether a user can access a tablespace in a particular way. Its argument possibilities are analogous to `has_table_privilege`. The desired access privilege type must evaluate to `CREATE`.

`has_type_privilege` checks whether a user can access a type in a particular way. Its argument possibilities are analogous to `has_table_privilege`. When specifying a type by a text string rather than by OID, the allowed input is the same as for the `regtype` data type \(see [Section 8.19](https://www.postgresql.org/docs/12/datatype-oid.html)\). The desired access privilege type must evaluate to `USAGE`.

`pg_has_role` checks whether a user can access a role in a particular way. Its argument possibilities are analogous to `has_table_privilege`, except that `public` is not allowed as a user name. The desired access privilege type must evaluate to some combination of `MEMBER` or `USAGE`. `MEMBER` denotes direct or indirect membership in the role \(that is, the right to do `SET ROLE`\), while `USAGE` denotes whether the privileges of the role are immediately available without doing `SET ROLE`.

`row_security_active` checks whether row level security is active for the specified table in the context of the `current_user` and environment. The table can be specified by name or by OID.

[Table 9.65](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-ACLITEM-OP-TABLE) shows the operators available for the `aclitem` type, which is the catalog representation of access privileges. See [Section 5.7](https://www.postgresql.org/docs/12/ddl-priv.html) for information about how to read access privilege values.

## **Table 9.65. `aclitem` Operators**

| Operator | Description | Example | Result |
| :--- | :--- | :--- | :--- |
| `=` | equal | `'calvin=r*w/hobbes'::aclitem = 'calvin=r*w*/hobbes'::aclitem` | `f` |
| `@>` | contains element | `'{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] @> 'calvin=r*w/hobbes'::aclitem` | `t` |
| `~` | contains element | `'{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] ~ 'calvin=r*w/hobbes'::aclitem` | `t` |

[Table 9.66](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-ACLITEM-FN-TABLE) shows some additional functions to manage the `aclitem` type.

## **Table 9.66. `aclitem` Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `acldefault`\(_`type`_, _`ownerId`_\) | `aclitem[]` | get the default access privileges for an object belonging to _`ownerId`_ |
| `aclexplode`\(_`aclitem[]`_\) | `setof record` | get `aclitem` array as tuples |
| `makeaclitem`\(_`grantee`_, _`grantor`_, _`privilege`_, _`grantable`_\) | `aclitem` | build an `aclitem` from input |

`acldefault` returns the built-in default access privileges for an object of type _`type`_ belonging to role _`ownerId`_. These represent the access privileges that will be assumed when an object's ACL entry is null. \(The default access privileges are described in [Section 5.7](https://www.postgresql.org/docs/12/ddl-priv.html).\) The _`type`_ parameter is a `CHAR`: write 'c' for `COLUMN`, 'r' for `TABLE` and table-like objects, 's' for `SEQUENCE`, 'd' for `DATABASE`, 'f' for `FUNCTION` or `PROCEDURE`, 'l' for `LANGUAGE`, 'L' for `LARGE OBJECT`, 'n' for `SCHEMA`, 't' for `TABLESPACE`, 'F' for `FOREIGN DATA WRAPPER`, 'S' for `FOREIGN SERVER`, or 'T' for `TYPE` or `DOMAIN`.

`aclexplode` returns an `aclitem` array as a set of rows. Output columns are grantor `oid`, grantee `oid` \(`0` for `PUBLIC`\), granted privilege as `text` \(`SELECT`, ...\) and whether the privilege is grantable as `boolean`. `makeaclitem` performs the inverse operation.

[Table 9.67](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-INFO-SCHEMA-TABLE) shows functions that determine whether a certain object is _visible_ in the current schema search path. For example, a table is said to be visible if its containing schema is in the search path and no table of the same name appears earlier in the search path. This is equivalent to the statement that the table can be referenced by name without explicit schema qualification. To list the names of all visible tables:

```text
SELECT relname FROM pg_class WHERE pg_table_is_visible(oid);
```

## **Table 9.67. Schema Visibility Inquiry Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_collation_is_visible(`_`collation_oid`_\) | `boolean` | is collation visible in search path |
| `pg_conversion_is_visible(`_`conversion_oid`_\) | `boolean` | is conversion visible in search path |
| `pg_function_is_visible(`_`function_oid`_\) | `boolean` | is function visible in search path |
| `pg_opclass_is_visible(`_`opclass_oid`_\) | `boolean` | is operator class visible in search path |
| `pg_operator_is_visible(`_`operator_oid`_\) | `boolean` | is operator visible in search path |
| `pg_opfamily_is_visible(`_`opclass_oid`_\) | `boolean` | is operator family visible in search path |
| `pg_statistics_obj_is_visible(`_`stat_oid`_\) | `boolean` | is statistics object visible in search path |
| `pg_table_is_visible(`_`table_oid`_\) | `boolean` | is table visible in search path |
| `pg_ts_config_is_visible(`_`config_oid`_\) | `boolean` | is text search configuration visible in search path |
| `pg_ts_dict_is_visible(`_`dict_oid`_\) | `boolean` | is text search dictionary visible in search path |
| `pg_ts_parser_is_visible(`_`parser_oid`_\) | `boolean` | is text search parser visible in search path |
| `pg_ts_template_is_visible(`_`template_oid`_\) | `boolean` | is text search template visible in search path |
| `pg_type_is_visible(`_`type_oid`_\) | `boolean` | is type \(or domain\) visible in search path |

Each function performs the visibility check for one type of database object. Note that `pg_table_is_visible` can also be used with views, materialized views, indexes, sequences and foreign tables; `pg_function_is_visible` can also be used with procedures and aggregates; `pg_type_is_visible` can also be used with domains. For functions and operators, an object in the search path is visible if there is no object of the same name _and argument data type\(s\)_ earlier in the path. For operator classes, both name and associated index access method are considered.

All these functions require object OIDs to identify the object to be checked. If you want to test an object by name, it is convenient to use the OID alias types \(`regclass`, `regtype`, `regprocedure`, `regoperator`, `regconfig`, or `regdictionary`\), for example:

```text
SELECT pg_type_is_visible('myschema.widget'::regtype);
```

Note that it would not make much sense to test a non-schema-qualified type name in this way — if the name can be recognized at all, it must be visible.

[Table 9.68](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-INFO-CATALOG-TABLE) lists functions that extract information from the system catalogs.

## **Table 9.68. System Catalog Information Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `format_type(`_`type_oid`_, _`typemod`_\) | `text` | get SQL name of a data type |
| `pg_get_constraintdef(`_`constraint_oid`_\) | `text` | get definition of a constraint |
| `pg_get_constraintdef(`_`constraint_oid`_, _`pretty_bool`_\) | `text` | get definition of a constraint |
| `pg_get_expr(`_`pg_node_tree`_, _`relation_oid`_\) | `text` | decompile internal form of an expression, assuming that any Vars in it refer to the relation indicated by the second parameter |
| `pg_get_expr(`_`pg_node_tree`_, _`relation_oid`_, _`pretty_bool`_\) | `text` | decompile internal form of an expression, assuming that any Vars in it refer to the relation indicated by the second parameter |
| `pg_get_functiondef(`_`func_oid`_\) | `text` | get definition of a function or procedure |
| `pg_get_function_arguments(`_`func_oid`_\) | `text` | get argument list of function's or procedure's definition \(with default values\) |
| `pg_get_function_identity_arguments(`_`func_oid`_\) | `text` | get argument list to identify a function or procedure \(without default values\) |
| `pg_get_function_result(`_`func_oid`_\) | `text` | get `RETURNS` clause for function \(returns null for a procedure\) |
| `pg_get_indexdef(`_`index_oid`_\) | `text` | get `CREATE INDEX` command for index |
| `pg_get_indexdef(`_`index_oid`_, _`column_no`_, _`pretty_bool`_\) | `text` | get `CREATE INDEX` command for index, or definition of just one index column when _`column_no`_ is not zero |
| `pg_get_keywords()` | `setof record` | get list of SQL keywords and their categories |
| `pg_get_ruledef(`_`rule_oid`_\) | `text` | get `CREATE RULE` command for rule |
| `pg_get_ruledef(`_`rule_oid`_, _`pretty_bool`_\) | `text` | get `CREATE RULE` command for rule |
| `pg_get_serial_sequence(`_`table_name`_, _`column_name`_\) | `text` | get name of the sequence that a serial or identity column uses |
| `pg_get_statisticsobjdef(`_`statobj_oid`_\) | `text` | get `CREATE STATISTICS` command for extended statistics object |
| `pg_get_triggerdef`\(_`trigger_oid`_\) | `text` | get `CREATE [ CONSTRAINT ] TRIGGER` command for trigger |
| `pg_get_triggerdef`\(_`trigger_oid`_, _`pretty_bool`_\) | `text` | get `CREATE [ CONSTRAINT ] TRIGGER` command for trigger |
| `pg_get_userbyid(`_`role_oid`_\) | `name` | get role name with given OID |
| `pg_get_viewdef(`_`view_name`_\) | `text` | get underlying `SELECT` command for view or materialized view \(_deprecated_\) |
| `pg_get_viewdef(`_`view_name`_, _`pretty_bool`_\) | `text` | get underlying `SELECT` command for view or materialized view \(_deprecated_\) |
| `pg_get_viewdef(`_`view_oid`_\) | `text` | get underlying `SELECT` command for view or materialized view |
| `pg_get_viewdef(`_`view_oid`_, _`pretty_bool`_\) | `text` | get underlying `SELECT` command for view or materialized view |
| `pg_get_viewdef(`_`view_oid`_, _`wrap_column_int`_\) | `text` | get underlying `SELECT` command for view or materialized view; lines with fields are wrapped to specified number of columns, pretty-printing is implied |
| `pg_index_column_has_property(`_`index_oid`_, _`column_no`_, _`prop_name`_\) | `boolean` | test whether an index column has a specified property |
| `pg_index_has_property(`_`index_oid`_, _`prop_name`_\) | `boolean` | test whether an index has a specified property |
| `pg_indexam_has_property(`_`am_oid`_, _`prop_name`_\) | `boolean` | test whether an index access method has a specified property |
| `pg_options_to_table(`_`reloptions`_\) | `setof record` | get the set of storage option name/value pairs |
| `pg_tablespace_databases(`_`tablespace_oid`_\) | `setof oid` | get the set of database OIDs that have objects in the tablespace |
| `pg_tablespace_location(`_`tablespace_oid`_\) | `text` | get the path in the file system that this tablespace is located in |
| `pg_typeof(`_`any`_\) | `regtype` | get the data type of any value |
| `collation for (`_`any`_\) | `text` | get the collation of the argument |
| `to_regclass(`_`rel_name`_\) | `regclass` | get the OID of the named relation |
| `to_regproc(`_`func_name`_\) | `regproc` | get the OID of the named function |
| `to_regprocedure(`_`func_name`_\) | `regprocedure` | get the OID of the named function |
| `to_regoper(`_`operator_name`_\) | `regoper` | get the OID of the named operator |
| `to_regoperator(`_`operator_name`_\) | `regoperator` | get the OID of the named operator |
| `to_regtype(`_`type_name`_\) | `regtype` | get the OID of the named type |
| `to_regnamespace(`_`schema_name`_\) | `regnamespace` | get the OID of the named schema |
| `to_regrole(`_`role_name`_\) | `regrole` | get the OID of the named role |

`format_type` returns the SQL name of a data type that is identified by its type OID and possibly a type modifier. Pass NULL for the type modifier if no specific modifier is known.

`pg_get_keywords` returns a set of records describing the SQL keywords recognized by the server. The `word` column contains the keyword. The `catcode` column contains a category code: `U` for unreserved, `C` for column name, `T` for type or function name, or `R` for reserved. The `catdesc` column contains a possibly-localized string describing the category.

`pg_get_constraintdef`, `pg_get_indexdef`, `pg_get_ruledef`, `pg_get_statisticsobjdef`, and `pg_get_triggerdef`, respectively reconstruct the creating command for a constraint, index, rule, extended statistics object, or trigger. \(Note that this is a decompiled reconstruction, not the original text of the command.\) `pg_get_expr` decompiles the internal form of an individual expression, such as the default value for a column. It can be useful when examining the contents of system catalogs. If the expression might contain Vars, specify the OID of the relation they refer to as the second parameter; if no Vars are expected, zero is sufficient. `pg_get_viewdef` reconstructs the `SELECT` query that defines a view. Most of these functions come in two variants, one of which can optionally “pretty-print” the result. The pretty-printed format is more readable, but the default format is more likely to be interpreted the same way by future versions of PostgreSQL; avoid using pretty-printed output for dump purposes. Passing `false` for the pretty-print parameter yields the same result as the variant that does not have the parameter at all.

`pg_get_functiondef` returns a complete `CREATE OR REPLACE FUNCTION` statement for a function. `pg_get_function_arguments` returns the argument list of a function, in the form it would need to appear in within `CREATE FUNCTION`. `pg_get_function_result` similarly returns the appropriate `RETURNS` clause for the function. `pg_get_function_identity_arguments` returns the argument list necessary to identify a function, in the form it would need to appear in within `ALTER FUNCTION`, for instance. This form omits default values.

`pg_get_serial_sequence` returns the name of the sequence associated with a column, or NULL if no sequence is associated with the column. If the column is an identity column, the associated sequence is the sequence internally created for the identity column. For columns created using one of the serial types \(`serial`, `smallserial`, `bigserial`\), it is the sequence created for that serial column definition. In the latter case, this association can be modified or removed with `ALTER SEQUENCE OWNED BY`. \(The function probably should have been called `pg_get_owned_sequence`; its current name reflects the fact that it has typically been used with `serial` or `bigserial` columns.\) The first input parameter is a table name with optional schema, and the second parameter is a column name. Because the first parameter is potentially a schema and table, it is not treated as a double-quoted identifier, meaning it is lower cased by default, while the second parameter, being just a column name, is treated as double-quoted and has its case preserved. The function returns a value suitably formatted for passing to sequence functions \(see [Section 9.16](https://www.postgresql.org/docs/12/functions-sequence.html)\). A typical use is in reading the current value of a sequence for an identity or serial column, for example:

```text
SELECT currval(pg_get_serial_sequence('sometable', 'id'));
```

`pg_get_userbyid` extracts a role's name given its OID.

`pg_index_column_has_property`, `pg_index_has_property`, and `pg_indexam_has_property` return whether the specified index column, index, or index access method possesses the named property. `NULL` is returned if the property name is not known or does not apply to the particular object, or if the OID or column number does not identify a valid object. Refer to [Table 9.69](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-INFO-INDEX-COLUMN-PROPS) for column properties, [Table 9.70](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-INFO-INDEX-PROPS) for index properties, and [Table 9.71](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-INFO-INDEXAM-PROPS) for access method properties. \(Note that extension access methods can define additional property names for their indexes.\)

## **Table 9.69. Index Column Properties**

| Name | Description |
| :--- | :--- |
| `asc` | Does the column sort in ascending order on a forward scan? |
| `desc` | Does the column sort in descending order on a forward scan? |
| `nulls_first` | Does the column sort with nulls first on a forward scan? |
| `nulls_last` | Does the column sort with nulls last on a forward scan? |
| `orderable` | Does the column possess any defined sort ordering? |
| `distance_orderable` | Can the column be scanned in order by a “distance” operator, for example `ORDER BY col <-> constant` ? |
| `returnable` | Can the column value be returned by an index-only scan? |
| `search_array` | Does the column natively support `col = ANY(array)` searches? |
| `search_nulls` | Does the column support `IS NULL` and `IS NOT NULL` searches? |

## **Table 9.70. Index Properties**

| Name | Description |
| :--- | :--- |
| `clusterable` | Can the index be used in a `CLUSTER` command? |
| `index_scan` | Does the index support plain \(non-bitmap\) scans? |
| `bitmap_scan` | Does the index support bitmap scans? |
| `backward_scan` | Can the scan direction be changed in mid-scan \(to support `FETCH BACKWARD` on a cursor without needing materialization\)? |

## **Table 9.71. Index Access Method Properties**

| Name | Description |
| :--- | :--- |
| `can_order` | Does the access method support `ASC`, `DESC` and related keywords in `CREATE INDEX`? |
| `can_unique` | Does the access method support unique indexes? |
| `can_multi_col` | Does the access method support indexes with multiple columns? |
| `can_exclude` | Does the access method support exclusion constraints? |
| `can_include` | Does the access method support the `INCLUDE` clause of `CREATE INDEX`? |

`pg_options_to_table` returns the set of storage option name/value pairs \(_`option_name`_/_`option_value`_\) when passed `pg_class`.`reloptions` or `pg_attribute`.`attoptions`.

`pg_tablespace_databases` allows a tablespace to be examined. It returns the set of OIDs of databases that have objects stored in the tablespace. If this function returns any rows, the tablespace is not empty and cannot be dropped. To display the specific objects populating the tablespace, you will need to connect to the databases identified by `pg_tablespace_databases` and query their `pg_class` catalogs.

`pg_typeof` returns the OID of the data type of the value that is passed to it. This can be helpful for troubleshooting or dynamically constructing SQL queries. The function is declared as returning `regtype`, which is an OID alias type \(see [Section 8.19](https://www.postgresql.org/docs/12/datatype-oid.html)\); this means that it is the same as an OID for comparison purposes but displays as a type name. For example:

```text
SELECT pg_typeof(33);

 pg_typeof 
-----------
 integer
(1 row)

SELECT typlen FROM pg_type WHERE oid = pg_typeof(33);
 typlen 
--------
      4
(1 row)
```

The expression `collation for` returns the collation of the value that is passed to it. Example:

```text
SELECT collation for (description) FROM pg_description LIMIT 1;
 pg_collation_for 
------------------
 "default"
(1 row)

SELECT collation for ('foo' COLLATE "de_DE");
 pg_collation_for 
------------------
 "de_DE"
(1 row)
```

The value might be quoted and schema-qualified. If no collation is derived for the argument expression, then a null value is returned. If the argument is not of a collatable data type, then an error is raised.

The `to_regclass`, `to_regproc`, `to_regprocedure`, `to_regoper`, `to_regoperator`, `to_regtype`, `to_regnamespace`, and `to_regrole` functions translate relation, function, operator, type, schema, and role names \(given as `text`\) to objects of type `regclass`, `regproc`, `regprocedure`, `regoper`, `regoperator`, `regtype`, `regnamespace`, and `regrole` respectively. These functions differ from a cast from text in that they don't accept a numeric OID, and that they return null rather than throwing an error if the name is not found \(or, for `to_regproc` and `to_regoper`, if the given name matches multiple objects\).

[Table 9.72](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-INFO-OBJECT-TABLE) lists functions related to database object identification and addressing.

## **Table 9.72. Object Information and Addressing Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_describe_object(`_`classid`_ `oid`, _`objid`_ `oid`, _`objsubid`_ `integer`\) | `text` | get description of a database object |
| `pg_identify_object(`_`classid`_ `oid`, _`objid`_ `oid`, _`objsubid`_ `integer`\) | _`type`_ `text`, _`schema`_ `text`, _`name`_ `text`, _`identity`_ `text` | get identity of a database object |
| `pg_identify_object_as_address(`_`classid`_ `oid`, _`objid`_ `oid`, _`objsubid`_ `integer`\) | _`type`_ `text`, _`object_names`_ `text[]`, _`object_args`_ `text[]` | get external representation of a database object's address |
| `pg_get_object_address(`_`type`_ `text`, _`object_names`_ `text[]`, _`object_args`_ `text[]`\) | _`classid`_ `oid`, _`objid`_ `oid`, _`objsubid`_ `integer` | get address of a database object from its external representation |

`pg_describe_object` returns a textual description of a database object specified by catalog OID, object OID, and sub-object ID \(such as a column number within a table; the sub-object ID is zero when referring to a whole object\). This description is intended to be human-readable, and might be translated, depending on server configuration. This is useful to determine the identity of an object as stored in the `pg_depend` catalog.

`pg_identify_object` returns a row containing enough information to uniquely identify the database object specified by catalog OID, object OID and sub-object ID. This information is intended to be machine-readable, and is never translated. _`type`_ identifies the type of database object; _`schema`_ is the schema name that the object belongs in, or `NULL` for object types that do not belong to schemas; _`name`_ is the name of the object, quoted if necessary, if the name \(along with schema name, if pertinent\) is sufficient to uniquely identify the object, otherwise `NULL`; _`identity`_ is the complete object identity, with the precise format depending on object type, and each name within the format being schema-qualified and quoted as necessary.

`pg_identify_object_as_address` returns a row containing enough information to uniquely identify the database object specified by catalog OID, object OID and sub-object ID. The returned information is independent of the current server, that is, it could be used to identify an identically named object in another server. _`type`_ identifies the type of database object; _`object_names`_ and _`object_args`_ are text arrays that together form a reference to the object. These three values can be passed to `pg_get_object_address` to obtain the internal address of the object. This function is the inverse of `pg_get_object_address`.

`pg_get_object_address` returns a row containing enough information to uniquely identify the database object specified by its type and object name and argument arrays. The returned values are the ones that would be used in system catalogs such as `pg_depend` and can be passed to other system functions such as `pg_identify_object` or `pg_describe_object`. _`classid`_ is the OID of the system catalog containing the object; _`objid`_ is the OID of the object itself, and _`objsubid`_ is the sub-object ID, or zero if none. This function is the inverse of `pg_identify_object_as_address`.

The functions shown in [Table 9.73](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-INFO-COMMENT-TABLE) extract comments previously stored with the [COMMENT](https://www.postgresql.org/docs/12/sql-comment.html) command. A null value is returned if no comment could be found for the specified parameters.

**Table 9.73. Comment Information Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `col_description(`_`table_oid`_, _`column_number`_\) | `text` | get comment for a table column |
| `obj_description(`_`object_oid`_, _`catalog_name`_\) | `text` | get comment for a database object |
| `obj_description(`_`object_oid`_\) | `text` | get comment for a database object \(_deprecated_\) |
| `shobj_description(`_`object_oid`_, _`catalog_name`_\) | `text` | get comment for a shared database object |

`col_description` returns the comment for a table column, which is specified by the OID of its table and its column number. \(`obj_description` cannot be used for table columns since columns do not have OIDs of their own.\)

The two-parameter form of `obj_description` returns the comment for a database object specified by its OID and the name of the containing system catalog. For example, `obj_description(123456,'pg_class')` would retrieve the comment for the table with OID 123456. The one-parameter form of `obj_description` requires only the object OID. It is deprecated since there is no guarantee that OIDs are unique across different system catalogs; therefore, the wrong comment might be returned.

`shobj_description` is used just like `obj_description` except it is used for retrieving comments on shared objects. Some system catalogs are global to all databases within each cluster, and the descriptions for objects in them are stored globally as well.

The functions shown in [Table 9.74](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-TXID-SNAPSHOT) provide server transaction information in an exportable form. The main use of these functions is to determine which transactions were committed between two snapshots.

**Table 9.74. Transaction IDs and Snapshots**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `txid_current()` | `bigint` | get current transaction ID, assigning a new one if the current transaction does not have one |
| `txid_current_if_assigned()` | `bigint` | same as `txid_current()` but returns null instead of assigning a new transaction ID if none is already assigned |
| `txid_current_snapshot()` | `txid_snapshot` | get current snapshot |
| `txid_snapshot_xip(`_`txid_snapshot`_\) | `setof bigint` | get in-progress transaction IDs in snapshot |
| `txid_snapshot_xmax(`_`txid_snapshot`_\) | `bigint` | get `xmax` of snapshot |
| `txid_snapshot_xmin(`_`txid_snapshot`_\) | `bigint` | get `xmin` of snapshot |
| `txid_visible_in_snapshot(`_`bigint`_, _`txid_snapshot`_\) | `boolean` | is transaction ID visible in snapshot? \(do not use with subtransaction ids\) |
| `txid_status(`_`bigint`_\) | `text` | report the status of the given transaction: `committed`, `aborted`, `in progress`, or null if the transaction ID is too old |

The internal transaction ID type \(`xid`\) is 32 bits wide and wraps around every 4 billion transactions. However, these functions export a 64-bit format that is extended with an “epoch” counter so it will not wrap around during the life of an installation. The data type used by these functions, `txid_snapshot`, stores information about transaction ID visibility at a particular moment in time. Its components are described in [Table 9.75](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-TXID-SNAPSHOT-PARTS).

**Table 9.75. Snapshot Components**

| Name | Description |
| :--- | :--- |
| `xmin` | Earliest transaction ID \(txid\) that is still active. All earlier transactions will either be committed and visible, or rolled back and dead. |
| `xmax` | First as-yet-unassigned txid. All txids greater than or equal to this are not yet started as of the time of the snapshot, and thus invisible. |
| `xip_list` | Active txids at the time of the snapshot. The list includes only those active txids between `xmin` and `xmax`; there might be active txids higher than `xmax`. A txid that is `xmin <= txid < xmax` and not in this list was already completed at the time of the snapshot, and thus either visible or dead according to its commit status. The list does not include txids of subtransactions. |

`txid_snapshot`'s textual representation is _`xmin`_:_`xmax`_:_`xip_list`_. For example `10:20:10,14,15` means `xmin=10, xmax=20, xip_list=10, 14, 15`.

`txid_status(bigint)` reports the commit status of a recent transaction. Applications may use it to determine whether a transaction committed or aborted when the application and database server become disconnected while a `COMMIT` is in progress. The status of a transaction will be reported as either `in progress`, `committed`, or `aborted`, provided that the transaction is recent enough that the system retains the commit status of that transaction. If is old enough that no references to that transaction survive in the system and the commit status information has been discarded, this function will return NULL. Note that prepared transactions are reported as `in progress`; applications must check [`pg_prepared_xacts`](https://www.postgresql.org/docs/12/view-pg-prepared-xacts.html) if they need to determine whether the txid is a prepared transaction.

The functions shown in [Table 9.76](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-COMMIT-TIMESTAMP) provide information about transactions that have been already committed. These functions mainly provide information about when the transactions were committed. They only provide useful data when [track\_commit\_timestamp](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-TRACK-COMMIT-TIMESTAMP) configuration option is enabled and only for transactions that were committed after it was enabled.

**Table 9.76. Committed Transaction Information**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_xact_commit_timestamp(`_`xid`_\) | `timestamp with time zone` | get commit timestamp of a transaction |
| `pg_last_committed_xact()` | _`xid`_ `xid`, _`timestamp`_ `timestamp with time zone` | get transaction ID and commit timestamp of latest committed transaction |

The functions shown in [Table 9.77](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-CONTROLDATA) print information initialized during `initdb`, such as the catalog version. They also show information about write-ahead logging and checkpoint processing. This information is cluster-wide, and not specific to any one database. They provide most of the same information, from the same source, as [pg\_controldata](https://www.postgresql.org/docs/12/app-pgcontroldata.html), although in a form better suited to SQL functions.

**Table 9.77. Control Data Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_control_checkpoint()` | `record` | Returns information about current checkpoint state. |
| `pg_control_system()` | `record` | Returns information about current control file state. |
| `pg_control_init()` | `record` | Returns information about cluster initialization state. |
| `pg_control_recovery()` | `record` | Returns information about recovery state. |

`pg_control_checkpoint` returns a record, shown in [Table 9.78](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-PG-CONTROL-CHECKPOINT)

**Table 9.78. `pg_control_checkpoint` Columns**

| Column Name | Data Type |
| :--- | :--- |
| `checkpoint_lsn` | `pg_lsn` |
| `redo_lsn` | `pg_lsn` |
| `redo_wal_file` | `text` |
| `timeline_id` | `integer` |
| `prev_timeline_id` | `integer` |
| `full_page_writes` | `boolean` |
| `next_xid` | `text` |
| `next_oid` | `oid` |
| `next_multixact_id` | `xid` |
| `next_multi_offset` | `xid` |
| `oldest_xid` | `xid` |
| `oldest_xid_dbid` | `oid` |
| `oldest_active_xid` | `xid` |
| `oldest_multi_xid` | `xid` |
| `oldest_multi_dbid` | `oid` |
| `oldest_commit_ts_xid` | `xid` |
| `newest_commit_ts_xid` | `xid` |
| `checkpoint_time` | `timestamp with time zone` |

`pg_control_system` returns a record, shown in [Table 9.79](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-PG-CONTROL-SYSTEM)

**Table 9.79. `pg_control_system` Columns**

| Column Name | Data Type |
| :--- | :--- |
| `pg_control_version` | `integer` |
| `catalog_version_no` | `integer` |
| `system_identifier` | `bigint` |
| `pg_control_last_modified` | `timestamp with time zone` |

`pg_control_init` returns a record, shown in [Table 9.80](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-PG-CONTROL-INIT)

**Table 9.80. `pg_control_init` Columns**

| Column Name | Data Type |
| :--- | :--- |
| `max_data_alignment` | `integer` |
| `database_block_size` | `integer` |
| `blocks_per_segment` | `integer` |
| `wal_block_size` | `integer` |
| `bytes_per_wal_segment` | `integer` |
| `max_identifier_length` | `integer` |
| `max_index_columns` | `integer` |
| `max_toast_chunk_size` | `integer` |
| `large_object_chunk_size` | `integer` |
| `float4_pass_by_value` | `boolean` |
| `float8_pass_by_value` | `boolean` |
| `data_page_checksum_version` | `integer` |

`pg_control_recovery` returns a record, shown in [Table 9.81](https://www.postgresql.org/docs/12/functions-info.html#FUNCTIONS-PG-CONTROL-RECOVERY)

**Table 9.81. `pg_control_recovery` Columns**

| Column Name | Data Type |
| :--- | :--- |
| `min_recovery_end_lsn` | `pg_lsn` |
| `min_recovery_end_timeline` | `integer` |
| `backup_start_lsn` | `pg_lsn` |
| `backup_end_lsn` | `pg_lsn` |
| `end_of_backup_record_required` | `boolean` |

