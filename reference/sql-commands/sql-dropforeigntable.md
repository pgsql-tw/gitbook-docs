<a id="id-1.9.3.113.1"></a>

## DROP FOREIGN TABLE

DROP FOREIGN TABLE — remove a foreign table

## Synopsis

```

DROP FOREIGN TABLE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.113.5"></a>

## Description

`DROP FOREIGN TABLE` removes a foreign table.
Only the owner of a foreign table can remove it.

<a id="id-1.9.3.113.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the foreign table does not exist.
    A notice is issued in this case.

*`name`*
:   The name (optionally schema-qualified) of the foreign table to drop.

`CASCADE`
:   Automatically drop objects that depend on the foreign table (such as
    views), and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the foreign table if any objects depend on it. This is
    the default.

<a id="id-1.9.3.113.7"></a>

## Examples

To destroy two foreign tables, `films` and
`distributors`:

```

DROP FOREIGN TABLE films, distributors;
```

<a id="id-1.9.3.113.8"></a>

## Compatibility

This command conforms to ISO/IEC 9075-9 (SQL/MED), except that the
standard only allows one foreign table to be dropped per command, and apart
from the `IF EXISTS` option, which is a PostgreSQL
extension.

<a id="id-1.9.3.113.9"></a>

## See Also

[ALTER FOREIGN TABLE](sql-alterforeigntable.md), [CREATE FOREIGN TABLE](sql-createforeigntable.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropforeigntable.html)（英文原文，待翻譯）
