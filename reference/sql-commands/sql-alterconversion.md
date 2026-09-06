<a id="id-1.9.3.6.1"></a>

## ALTER CONVERSION

ALTER CONVERSION — change the definition of a conversion

## Synopsis

```

ALTER CONVERSION name RENAME TO new_name
ALTER CONVERSION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER CONVERSION name SET SCHEMA new_schema
```

<a id="id-1.9.3.6.5"></a>

## Description

`ALTER CONVERSION` changes the definition of a
conversion.

You must own the conversion to use `ALTER CONVERSION`.
To alter the owner, you must be able to `SET ROLE` to the
new owning role, and that role must have `CREATE`
privilege on the conversion's schema.
(These restrictions enforce that altering the
owner doesn't do anything you couldn't do by dropping and recreating the
conversion. However, a superuser can alter ownership of any conversion
anyway.)

<a id="id-1.9.3.6.6"></a>

## Parameters

*`name`*
:   The name (optionally schema-qualified) of an existing conversion.

*`new_name`*
:   The new name of the conversion.

*`new_owner`*
:   The new owner of the conversion.

*`new_schema`*
:   The new schema for the conversion.

<a id="id-1.9.3.6.7"></a>

## Examples

To rename the conversion `iso_8859_1_to_utf8` to
`latin1_to_unicode`:

```

ALTER CONVERSION iso_8859_1_to_utf8 RENAME TO latin1_to_unicode;
```

To change the owner of the conversion `iso_8859_1_to_utf8` to
`joe`:

```

ALTER CONVERSION iso_8859_1_to_utf8 OWNER TO joe;
```

<a id="id-1.9.3.6.8"></a>

## Compatibility

There is no `ALTER CONVERSION` statement in the SQL
standard.

<a id="id-1.9.3.6.9"></a>

## See Also

[CREATE CONVERSION](sql-createconversion.md), [DROP CONVERSION](sql-dropconversion.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterconversion.html)（英文原文，待翻譯）
