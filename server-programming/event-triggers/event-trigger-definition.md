## 38.1. Overview of Event Trigger Behavior [#](#EVENT-TRIGGER-DEFINITION)

[38.1.1. login](event-trigger-definition.md#EVENT-TRIGGER-LOGIN)

[38.1.2. ddl_command_start](event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_START)

[38.1.3. ddl_command_end](event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_END)

[38.1.4. sql_drop](event-trigger-definition.md#EVENT-TRIGGER-SQL_DROP)

[38.1.5. table_rewrite](event-trigger-definition.md#EVENT-TRIGGER-TABLE_REWRITE)

[38.1.6. Event Triggers in Aborted Transactions](event-trigger-definition.md#EVENT-TRIGGER-ABORTED-TRANSACTIONS)

[38.1.7. Creating Event Triggers](event-trigger-definition.md#EVENT-TRIGGER-CREATING)

An event trigger fires whenever the event with which it is associated
occurs in the database in which it is defined. Currently, the
supported events are
`login`,
`ddl_command_start`,
`ddl_command_end`,
`table_rewrite`
and `sql_drop`.
Support for additional events may be added in future releases.

<a id="EVENT-TRIGGER-LOGIN"></a>

### 38.1.1. login [#](#EVENT-TRIGGER-LOGIN)

The `login` event occurs when an authenticated user logs
into the system. Any bug in a trigger procedure for this event may
prevent successful login to the system. Such bugs may be worked around by
setting [event_triggers](../../server-administration/runtime-config/runtime-config-client.md#GUC-EVENT-TRIGGERS) to `false`
either in a connection string or configuration file. Alternatively, you can
restart the system in single-user mode (as event triggers are
disabled in this mode). See the [postgres](../../reference/reference-server/app-postgres.md) reference
page for details about using single-user mode.
The `login` event will also fire on standby servers.
To prevent servers from becoming inaccessible, such triggers must avoid
writing anything to the database when running on a standby.
Also, it's recommended to avoid long-running queries in
`login` event triggers. Note that, for instance,
canceling a connection in psql will not cancel
the in-progress `login` trigger.

For an example on how to use the `login` event trigger,
see [Section 38.5](event-trigger-database-login-example.md).

<a id="EVENT-TRIGGER-DDL_COMMAND_START"></a>

### 38.1.2. ddl_command_start [#](#EVENT-TRIGGER-DDL_COMMAND_START)

The `ddl_command_start` event occurs just before the
execution of a DDL command. DDL commands in this context are:

* `CREATE`
* `ALTER`
* `DROP`
* `COMMENT`
* `GRANT`
* `IMPORT FOREIGN SCHEMA`
* `REINDEX`
* `REFRESH MATERIALIZED VIEW`
* `REVOKE`
* `SECURITY LABEL`

`ddl_command_start` also occurs just before the
execution of a `SELECT INTO` command, since this is
equivalent to `CREATE TABLE AS`.

As an exception, this event does not occur for DDL commands targeting
shared objects:

* databases
* roles (role definitions and role memberships)
* tablespaces
* parameter privileges
* `ALTER SYSTEM`

This event also does not occur for commands targeting event triggers
themselves.

No check whether the affected object exists or doesn't exist is performed
before the event trigger fires.

<a id="EVENT-TRIGGER-DDL_COMMAND_END"></a>

### 38.1.3. ddl_command_end [#](#EVENT-TRIGGER-DDL_COMMAND_END)

The `ddl_command_end` event occurs just after the execution of
the same set of commands as `ddl_command_start`. To
obtain more details on the DDL
operations that took place, use the set-returning function
`pg_event_trigger_ddl_commands()` from the
`ddl_command_end` event trigger code (see
[Section 9.30](../../the-sql-language/functions/functions-event-triggers.md)). Note that the trigger fires
after the actions have taken place (but before the transaction commits),
and thus the system catalogs can be read as already changed.

<a id="EVENT-TRIGGER-SQL_DROP"></a>

### 38.1.4. sql_drop [#](#EVENT-TRIGGER-SQL_DROP)

The `sql_drop` event occurs just before the
`ddl_command_end` event trigger for any operation that drops
database objects. Note that besides the obvious `DROP`
commands, some `ALTER` commands can also trigger an
`sql_drop` event.

To list the objects that have been dropped, use the
set-returning function `pg_event_trigger_dropped_objects()` from the
`sql_drop` event trigger code (see
[Section 9.30](../../the-sql-language/functions/functions-event-triggers.md)). Note that
the trigger is executed after the objects have been deleted from the
system catalogs, so it's not possible to look them up anymore.

<a id="EVENT-TRIGGER-TABLE_REWRITE"></a>

### 38.1.5. table_rewrite [#](#EVENT-TRIGGER-TABLE_REWRITE)

The `table_rewrite` event occurs just before a table is
rewritten by some actions of the commands `ALTER TABLE` and
`ALTER TYPE`. While other
control statements are available to rewrite a table,
like `CLUSTER` and `VACUUM`,
the `table_rewrite` event is not triggered by them.
To find the OID of the table that was rewritten, use the function
`pg_event_trigger_table_rewrite_oid()`, to discover the
reason(s) for the rewrite, use the function
`pg_event_trigger_table_rewrite_reason()` (see [Section 9.30](../../the-sql-language/functions/functions-event-triggers.md)).

<a id="EVENT-TRIGGER-ABORTED-TRANSACTIONS"></a>

### 38.1.6. Event Triggers in Aborted Transactions [#](#EVENT-TRIGGER-ABORTED-TRANSACTIONS)

Event triggers (like other functions) cannot be executed in an aborted
transaction. Thus, if a DDL command fails with an error, any associated
`ddl_command_end` triggers will not be executed. Conversely,
if a `ddl_command_start` trigger fails with an error, no
further event triggers will fire, and no attempt will be made to execute
the command itself. Similarly, if a `ddl_command_end` trigger
fails with an error, the effects of the DDL statement will be rolled
back, just as they would be in any other case where the containing
transaction aborts.

<a id="EVENT-TRIGGER-CREATING"></a>

### 38.1.7. Creating Event Triggers [#](#EVENT-TRIGGER-CREATING)

Event triggers are created using the command [CREATE EVENT TRIGGER](../../reference/sql-commands/sql-createeventtrigger.md).
In order to create an event trigger, you must first create a function with
the special return type `event_trigger`. This function
need not (and may not) return a value; the return type serves merely as
a signal that the function is to be invoked as an event trigger.

If more than one event trigger is defined for a particular event, they will
fire in alphabetical order by trigger name.

A trigger definition can also specify a `WHEN`
condition so that, for example, a `ddl_command_start`
trigger can be fired only for particular commands which the user wishes
to intercept. A common use of such triggers is to restrict the range of
DDL operations which users may perform.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/event-trigger-definition.html)（英文原文，待翻譯）
