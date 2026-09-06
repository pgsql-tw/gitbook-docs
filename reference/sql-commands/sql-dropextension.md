<a id="id-1.9.3.111.1"></a>

## DROP EXTENSION

DROP EXTENSION — remove an extension

## Synopsis

```

DROP EXTENSION [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.111.5"></a>

## Description

`DROP EXTENSION` removes extensions from the database.
Dropping an extension causes its member objects, and other explicitly
dependent routines (see [ALTER ROUTINE](sql-alterroutine.md),
the `DEPENDS ON EXTENSION extension_name` action), to be dropped as well.

You must own the extension to use `DROP EXTENSION`.

<a id="id-1.9.3.111.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the extension does not exist. A notice is issued
    in this case.

*`name`*
:   The name of an installed extension.

`CASCADE`
:   Automatically drop objects that depend on the extension,
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   This option prevents the specified extensions from being dropped if
    other objects, besides these extensions, their members, and their
    explicitly dependent routines, depend on them. This is the default.

<a id="id-1.9.3.111.7"></a>

## Examples

To remove the extension `hstore` from the current
database:

```

DROP EXTENSION hstore;
```

This command will fail if any of `hstore`'s objects
are in use in the database, for example if any tables have columns
of the `hstore` type. Add the `CASCADE` option to
forcibly remove those dependent objects as well.

<a id="id-1.9.3.111.8"></a>

## Compatibility

`DROP EXTENSION` is a PostgreSQL
extension.

<a id="id-1.9.3.111.9"></a>

## See Also

[CREATE EXTENSION](sql-createextension.md), [ALTER EXTENSION](sql-alterextension.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropextension.html)（英文原文，待翻譯）
