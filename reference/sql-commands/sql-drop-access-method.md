<a id="id-1.9.3.103.1"></a>

## DROP ACCESS METHOD

DROP ACCESS METHOD — remove an access method

## Synopsis

```

DROP ACCESS METHOD [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.103.5"></a>

## Description

`DROP ACCESS METHOD` removes an existing access method.
Only superusers can drop access methods.

<a id="id-1.9.3.103.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the access method does not exist.
    A notice is issued in this case.

*`name`*
:   The name of an existing access method.

`CASCADE`
:   Automatically drop objects that depend on the access method
    (such as operator classes, operator families, and indexes),
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the access method if any objects depend on it.
    This is the default.

<a id="id-1.9.3.103.7"></a>

## Examples

Drop the access method `heptree`:

```

DROP ACCESS METHOD heptree;
```

<a id="id-1.9.3.103.8"></a>

## Compatibility

`DROP ACCESS METHOD` is a
PostgreSQL extension.

<a id="id-1.9.3.103.9"></a>

## See Also

[CREATE ACCESS METHOD](sql-create-access-method.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-drop-access-method.html)（英文原文，待翻譯）
