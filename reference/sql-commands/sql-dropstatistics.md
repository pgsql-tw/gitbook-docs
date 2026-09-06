<a id="id-1.9.3.132.1"></a>

## DROP STATISTICS

DROP STATISTICS — remove extended statistics

## Synopsis

```

DROP STATISTICS [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.132.5"></a>

## Description

`DROP STATISTICS` removes statistics object(s) from the
database. Only the statistics object's owner, the schema owner, or a
superuser can drop a statistics object.

<a id="id-1.9.3.132.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the statistics object does not exist. A notice
    is issued in this case.

*`name`*
:   The name (optionally schema-qualified) of the statistics object to drop.

`CASCADE`<br>`RESTRICT`
:   These key words do not have any effect, since there are no dependencies
    on statistics.

<a id="id-1.9.3.132.7"></a>

## Examples

To destroy two statistics objects in different schemas, without failing
if they don't exist:

```

DROP STATISTICS IF EXISTS
    accounting.users_uid_creation,
    public.grants_user_role;
```

<a id="id-1.9.3.132.8"></a>

## Compatibility

There is no `DROP STATISTICS` command in the SQL standard.

<a id="id-1.9.3.132.9"></a>

## See Also

[ALTER STATISTICS](sql-alterstatistics.md), [CREATE STATISTICS](sql-createstatistics.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropstatistics.html)（英文原文，待翻譯）
