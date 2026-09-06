<a id="id-1.9.3.10.1"></a>

## ALTER EVENT TRIGGER

ALTER EVENT TRIGGER — change the definition of an event trigger

## Synopsis

```

ALTER EVENT TRIGGER name DISABLE
ALTER EVENT TRIGGER name ENABLE [ REPLICA | ALWAYS ]
ALTER EVENT TRIGGER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER EVENT TRIGGER name RENAME TO new_name
```

<a id="id-1.9.3.10.5"></a>

## Description

`ALTER EVENT TRIGGER` changes properties of an
existing event trigger.

You must be superuser to alter an event trigger.

<a id="id-1.9.3.10.6"></a>

## Parameters

*`name`*
:   The name of an existing trigger to alter.

*`new_owner`*
:   The user name of the new owner of the event trigger.

*`new_name`*
:   The new name of the event trigger.

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ]`
:   These forms configure the firing of event triggers. A disabled trigger
    is still known to the system, but is not executed when its triggering
    event occurs. See also [session_replication_role](../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE).

<a id="SQL-ALTERVENTTRIGGER-COMPATIBILITY"></a>

## Compatibility

There is no `ALTER EVENT TRIGGER` statement in the
SQL standard.

<a id="id-1.9.3.10.8"></a>

## See Also

[CREATE EVENT TRIGGER](sql-createeventtrigger.md), [DROP EVENT TRIGGER](sql-dropeventtrigger.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altereventtrigger.html)（英文原文，待翻譯）
