<a id="id-1.9.3.110.1"></a>

## DROP EVENT TRIGGER

DROP EVENT TRIGGER — remove an event trigger

## Synopsis

```

DROP EVENT TRIGGER [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.110.5"></a>

## Description

`DROP EVENT TRIGGER` removes an existing event trigger.
To execute this command, the current user must be the owner of the event
trigger.

<a id="id-1.9.3.110.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the event trigger does not exist. A notice
    is issued in this case.

*`name`*
:   The name of the event trigger to remove.

`CASCADE`
:   Automatically drop objects that depend on the trigger,
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the trigger if any objects depend on it. This is
    the default.

<a id="SQL-DROPEVENTTRIGGER-EXAMPLES"></a>

## Examples

Destroy the trigger `snitch`:

```

DROP EVENT TRIGGER snitch;
```

<a id="SQL-DROPEVENTTRIGGER-COMPATIBILITY"></a>

## Compatibility

There is no `DROP EVENT TRIGGER` statement in the
SQL standard.

<a id="id-1.9.3.110.9"></a>

## See Also

[CREATE EVENT TRIGGER](sql-createeventtrigger.md), [ALTER EVENT TRIGGER](sql-altereventtrigger.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropeventtrigger.html)（英文原文，待翻譯）
