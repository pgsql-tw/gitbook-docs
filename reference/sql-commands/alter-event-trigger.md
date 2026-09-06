<a id="SQL-ALTEREVENTTRIGGER"></a><a id="id-1.9.3.10.1"></a>

# ALTER EVENT TRIGGER

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

`ALTER EVENT TRIGGER` changes properties of an existing event trigger.

You must be superuser to alter an event trigger.

<a id="id-1.9.3.10.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name of an existing trigger to alter.

<em class="replaceable"><code>new&#95;owner</code></em>

The user name of the new owner of the event trigger.

<em class="replaceable"><code>new&#95;name</code></em>

The new name of the event trigger.

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ]`

These forms configure the firing of event triggers. A disabled trigger is still known to the system, but is not executed when its triggering event occurs. See also [session_replication_role](../../server-administration/server-configuration/client-connection-defaults.md#GUC-SESSION-REPLICATION-ROLE).

<a id="SQL-ALTERVENTTRIGGER-COMPATIBILITY"></a>

## Compatibility

There is no `ALTER EVENT TRIGGER` statement in the SQL standard.

<a id="id-1.9.3.10.8"></a>

## See Also

[CREATE EVENT TRIGGER](create-event-trigger.md), [DROP EVENT TRIGGER](drop-event-trigger.md)

---

原文：[PostgreSQL 15.19 Documentation](alter-event-trigger.md)（英文原文，待翻譯）
