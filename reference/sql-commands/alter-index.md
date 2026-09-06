# ALTER INDEX

ALTER INDEX — change the definition of an index

### Synopsis

```
ALTER INDEX [ IF EXISTS ] name RENAME TO new_name
ALTER INDEX [ IF EXISTS ] name SET TABLESPACE tablespace_name
ALTER INDEX name DEPENDS ON EXTENSION extension_name
ALTER INDEX [ IF EXISTS ] name SET ( storage_parameter = value [, ... ] )
ALTER INDEX [ IF EXISTS ] name RESET ( storage_parameter [, ... ] )
ALTER INDEX ALL IN TABLESPACE name [ OWNED BY role_name [, ... ] ]
    SET TABLESPACE new_tablespace [ NOWAIT ]
```

### Description

`ALTER INDEX` changes the definition of an existing index. There are several subforms:`RENAME`

The `RENAME` form changes the name of the index. There is no effect on the stored data.`SET TABLESPACE`

This form changes the index's tablespace to the specified tablespace and moves the data file(s) associated with the index to the new tablespace. To change the tablespace of an index, you must own the index and have `CREATE` privilege on the new tablespace. All indexes in the current database in a tablespace can be moved by using the `ALL IN TABLESPACE` form, which will lock all indexes to be moved and then move each one. This form also supports `OWNED BY`, which will only move indexes owned by the roles specified. If the `NOWAIT` option is specified then the command will fail if it is unable to acquire all of the locks required immediately. Note that system catalogs will not be moved by this command, use `ALTER DATABASE` or explicit `ALTER INDEX` invocations instead if desired. See also [CREATE TABLESPACE](https://www.postgresql.org/docs/current/static/sql-createtablespace.html).`DEPENDS ON EXTENSION`

This form marks the index as dependent on the extension, such that if the extension is dropped, the index will automatically be dropped as well.`SET (`` `_`storage_parameter`_ = _`value`_ \[, ... ] )

This form changes one or more index-method-specific storage parameters for the index. See [CREATE INDEX](https://www.postgresql.org/docs/current/static/sql-createindex.html) for details on the available parameters. Note that the index contents will not be modified immediately by this command; depending on the parameter you might need to rebuild the index with [REINDEX](https://www.postgresql.org/docs/current/static/sql-reindex.html) to get the desired effects.`RESET (`` `_`storage_parameter`_ \[, ... ] )

This form resets one or more index-method-specific storage parameters to their defaults. As with `SET`, a `REINDEX` might be needed to update the index entirely.

### Parameters

`IF EXISTS`

Do not throw an error if the index does not exist. A notice is issued in this case.

_`name`_

The name (possibly schema-qualified) of an existing index to alter.

_`new_name`_

The new name for the index.

_`tablespace_name`_

The tablespace to which the index will be moved.

_`extension_name`_

The name of the extension that the index is to depend on.

_`storage_parameter`_

The name of an index-method-specific storage parameter.

_`value`_

The new value for an index-method-specific storage parameter. This might be a number or a word depending on the parameter.

### Notes

These operations are also possible using [ALTER TABLE](https://www.postgresql.org/docs/current/static/sql-altertable.html). `ALTER INDEX` is in fact just an alias for the forms of `ALTER TABLE` that apply to indexes.

There was formerly an `ALTER INDEX OWNER` variant, but this is now ignored (with a warning). An index cannot have an owner different from its table's owner. Changing the table's owner automatically changes the index as well.

Changing any part of a system catalog index is not permitted.

### Examples

To rename an existing index:

```
ALTER INDEX distributors RENAME TO suppliers;
```

To move an index to a different tablespace:

```
ALTER INDEX distributors SET TABLESPACE fasttablespace;
```

To change an index's fill factor (assuming that the index method supports it):

```
ALTER INDEX distributors SET (fillfactor = 75);
REINDEX INDEX distributors;
```

### Compatibility

`ALTER INDEX` is a PostgreSQL extension.

### See Also

[CREATE INDEX](https://www.postgresql.org/docs/current/static/sql-createindex.html), [REINDEX](https://www.postgresql.org/docs/current/static/sql-reindex.html)
