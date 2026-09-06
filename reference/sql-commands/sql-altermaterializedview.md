<a id="id-1.9.3.19.1"></a>

## ALTER MATERIALIZED VIEW

ALTER MATERIALIZED VIEW — change the definition of a materialized view

## Synopsis

```

ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    action [, ... ]
ALTER MATERIALIZED VIEW name
    [ NO ] DEPENDS ON EXTENSION extension_name
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    RENAME [ COLUMN ] column_name TO new_column_name
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    RENAME TO new_name
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    SET SCHEMA new_schema
ALTER MATERIALIZED VIEW ALL IN TABLESPACE name [ OWNED BY role_name [, ... ] ]
    SET TABLESPACE new_tablespace [ NOWAIT ]

where action is one of:

    ALTER [ COLUMN ] column_name SET STATISTICS integer
    ALTER [ COLUMN ] column_name SET ( attribute_option = value [, ... ] )
    ALTER [ COLUMN ] column_name RESET ( attribute_option [, ... ] )
    ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }
    ALTER [ COLUMN ] column_name SET COMPRESSION compression_method
    CLUSTER ON index_name
    SET WITHOUT CLUSTER
    SET ACCESS METHOD new_access_method
    SET TABLESPACE new_tablespace
    SET ( storage_parameter [= value] [, ... ] )
    RESET ( storage_parameter [, ... ] )
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

<a id="id-1.9.3.19.5"></a>

## Description

`ALTER MATERIALIZED VIEW` changes various auxiliary
properties of an existing materialized view.

You must own the materialized view to use `ALTER MATERIALIZED
VIEW`. To change a materialized view's schema, you must also have
`CREATE` privilege on the new schema.
To alter the owner, you must be able to `SET ROLE` to the
new owning role, and that role must have `CREATE`
privilege on the materialized view's schema.
(These restrictions enforce that altering
the owner doesn't do anything you couldn't do by dropping and recreating the
materialized view. However, a superuser can alter ownership of any view
anyway.)

The statement subforms and actions available for
`ALTER MATERIALIZED VIEW` are a subset of those available
for `ALTER TABLE`, and have the same meaning when used for
materialized views. See the descriptions for
[`ALTER TABLE`](sql-altertable.md)
for details.

<a id="id-1.9.3.19.6"></a>

## Parameters

*`name`*
:   The name (optionally schema-qualified) of an existing materialized view.

*`column_name`*
:   Name of an existing column.

*`extension_name`*
:   The name of the extension that the materialized view is to depend on (or no longer
    dependent on, if `NO` is specified). A materialized view
    that's marked as dependent on an extension is automatically dropped when
    the extension is dropped.

*`new_column_name`*
:   New name for an existing column.

*`new_owner`*
:   The user name of the new owner of the materialized view.

*`new_name`*
:   The new name for the materialized view.

*`new_schema`*
:   The new schema for the materialized view.

<a id="id-1.9.3.19.7"></a>

## Examples

To rename the materialized view `foo` to
`bar`:

```

ALTER MATERIALIZED VIEW foo RENAME TO bar;
```

<a id="id-1.9.3.19.8"></a>

## Compatibility

`ALTER MATERIALIZED VIEW` is a
PostgreSQL extension.

<a id="id-1.9.3.19.9"></a>

## See Also

[CREATE MATERIALIZED VIEW](sql-creatematerializedview.md), [DROP MATERIALIZED VIEW](sql-dropmaterializedview.md), [REFRESH MATERIALIZED VIEW](sql-refreshmaterializedview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altermaterializedview.html)（英文原文，待翻譯）
