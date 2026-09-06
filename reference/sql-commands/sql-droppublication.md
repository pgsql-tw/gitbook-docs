<a id="id-1.9.3.125.1"></a>

## DROP PUBLICATION

DROP PUBLICATION — remove a publication

## Synopsis

```

DROP PUBLICATION [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.125.5"></a>

## Description

`DROP PUBLICATION` removes an existing publication from
the database.

A publication can only be dropped by its owner or a superuser.

<a id="id-1.9.3.125.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the publication does not exist. A notice is
    issued in this case.

*`name`*
:   The name of an existing publication.

`CASCADE`<br>`RESTRICT`
:   These key words do not have any effect, since there are no dependencies
    on publications.

<a id="id-1.9.3.125.7"></a>

## Examples

Drop a publication:

```

DROP PUBLICATION mypublication;
```

<a id="id-1.9.3.125.8"></a>

## Compatibility

`DROP PUBLICATION` is a PostgreSQL
extension.

<a id="id-1.9.3.125.9"></a>

## See Also

[CREATE PUBLICATION](sql-createpublication.md), [ALTER PUBLICATION](sql-alterpublication.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droppublication.html)（英文原文，待翻譯）
