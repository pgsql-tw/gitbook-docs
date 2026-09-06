<a id="id-1.9.3.130.1"></a>

## DROP SEQUENCE

DROP SEQUENCE — remove a sequence

## Synopsis

```

DROP SEQUENCE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.130.5"></a>

## Description

`DROP SEQUENCE` removes sequence number
generators. A sequence can only be dropped by its owner or a superuser.

<a id="id-1.9.3.130.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the sequence does not exist. A notice is issued
    in this case.

*`name`*
:   The name (optionally schema-qualified) of a sequence.

`CASCADE`
:   Automatically drop objects that depend on the sequence,
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the sequence if any objects depend on it. This
    is the default.

<a id="id-1.9.3.130.7"></a>

## Examples

To remove the sequence `serial`:

```

DROP SEQUENCE serial;
```

<a id="id-1.9.3.130.8"></a>

## Compatibility

`DROP SEQUENCE` conforms to the SQL
standard, except that the standard only allows one
sequence to be dropped per command, and apart from the
`IF EXISTS` option, which is a PostgreSQL
extension.

<a id="id-1.9.3.130.9"></a>

## See Also

[CREATE SEQUENCE](sql-createsequence.md), [ALTER SEQUENCE](sql-altersequence.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropsequence.html)（英文原文，待翻譯）
