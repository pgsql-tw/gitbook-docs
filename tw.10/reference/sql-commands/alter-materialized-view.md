# ALTER MATERIALIZED VIEW

ALTER MATERIALIZED VIEW — change the definition of a materialized view

### Synopsis

```text
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    action [, ... ]
ALTER MATERIALIZED VIEW name
    DEPENDS ON EXTENSION extension_name
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
    ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
    CLUSTER ON index_name
    SET WITHOUT CLUSTER
    SET ( storage_parameter = value [, ... ] )
    RESET ( storage_parameter [, ... ] )
    OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
```

### Description

`ALTER MATERIALIZED VIEW` changes various auxiliary properties of an existing materialized view.

You must own the materialized view to use `ALTER MATERIALIZED VIEW`. To change a materialized view's schema, you must also have `CREATE` privilege on the new schema. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the materialized view's schema. \(These restrictions enforce that altering the owner doesn't do anything you couldn't do by dropping and recreating the materialized view. However, a superuser can alter ownership of any view anyway.\)

The `DEPENDS ON EXTENSION` form marks the materialized view as dependent on an extension, such that the materialized view will automatically be dropped if the extension is dropped.

The statement subforms and actions available for `ALTER MATERIALIZED VIEW` are a subset of those available for `ALTER TABLE`, and have the same meaning when used for materialized views. See the descriptions for [ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html) for details.

### Parameters

_`name`_

The name \(optionally schema-qualified\) of an existing materialized view._`column_name`_

Name of a new or existing column._`extension_name`_

The name of the extension that the materialized view is to depend on._`new_column_name`_

New name for an existing column._`new_owner`_

The user name of the new owner of the materialized view._`new_name`_

The new name for the materialized view._`new_schema`_

The new schema for the materialized view.

### Examples

To rename the materialized view `foo` to `bar`:

```text
ALTER MATERIALIZED VIEW foo RENAME TO bar;
```

### Compatibility

`ALTER MATERIALIZED VIEW` is a PostgreSQL extension.

### See Also

[CREATE MATERIALIZED VIEW](create-materialized-view.md), [DROP MATERIALIZED VIEW](https://www.postgresql.org/docs/10/static/sql-dropmaterializedview.html), [REFRESH MATERIALIZED VIEW](https://www.postgresql.org/docs/10/static/sql-refreshmaterializedview.html)

