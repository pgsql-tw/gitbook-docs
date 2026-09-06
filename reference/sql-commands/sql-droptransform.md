<a id="id-1.9.3.140.1"></a>

## DROP TRANSFORM

DROP TRANSFORM — remove a transform

## Synopsis

```

DROP TRANSFORM [ IF EXISTS ] FOR type_name LANGUAGE lang_name [ CASCADE | RESTRICT ]
```

<a id="SQL-DROPTRANSFORM-DESCRIPTION"></a>

## Description

`DROP TRANSFORM` removes a previously defined transform.

To be able to drop a transform, you must own the type and the language.
These are the same privileges that are required to create a transform.

<a id="id-1.9.3.140.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the transform does not exist. A notice is issued
    in this case.

*`type_name`*
:   The name of the data type of the transform.

*`lang_name`*
:   The name of the language of the transform.

`CASCADE`
:   Automatically drop objects that depend on the transform,
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the transform if any objects depend on it. This is the
    default.

<a id="SQL-DROPTRANSFORM-EXAMPLES"></a>

## Examples

To drop the transform for type `hstore` and language
`plpython3u`:

```

DROP TRANSFORM FOR hstore LANGUAGE plpython3u;
```

<a id="SQL-DROPTRANSFORM-COMPAT"></a>

## Compatibility

This form of `DROP TRANSFORM` is a
PostgreSQL extension. See [CREATE TRANSFORM](sql-createtransform.md) for details.

<a id="id-1.9.3.140.9"></a>

## See Also

[CREATE TRANSFORM](sql-createtransform.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptransform.html)（英文原文，待翻譯）
