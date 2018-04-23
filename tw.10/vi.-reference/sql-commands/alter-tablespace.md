# ALTER TABLESPACE

ALTER TABLESPACE — change the definition of a tablespace

### Synopsis

```text
ALTER TABLESPACE name RENAME TO new_name
ALTER TABLESPACE name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER TABLESPACE name SET ( tablespace_option = value [, ... ] )
ALTER TABLESPACE name RESET ( tablespace_option [, ... ] )
```

### Description

`ALTER TABLESPACE` can be used to change the definition of a tablespace.

You must own the tablespace to change the definition of a tablespace. To alter the owner, you must also be a direct or indirect member of the new owning role. \(Note that superusers have these privileges automatically.\)

### Parameters

_`name`_

The name of an existing tablespace._`new_name`_

The new name of the tablespace. The new name cannot begin with `pg_`, as such names are reserved for system tablespaces._`new_owner`_

The new owner of the tablespace._`tablespace_option`_

A tablespace parameter to be set or reset. Currently, the only available parameters are `seq_page_cost`, `random_page_cost` and `effective_io_concurrency`. Setting either value for a particular tablespace will override the planner's usual estimate of the cost of reading pages from tables in that tablespace, as established by the configuration parameters of the same name \(see [seq\_page\_cost](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-SEQ-PAGE-COST), [random\_page\_cost](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-RANDOM-PAGE-COST), [effective\_io\_concurrency](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-EFFECTIVE-IO-CONCURRENCY)\). This may be useful if one tablespace is located on a disk which is faster or slower than the remainder of the I/O subsystem.

### Examples

Rename tablespace `index_space` to `fast_raid`:

```text
ALTER TABLESPACE index_space RENAME TO fast_raid;
```

Change the owner of tablespace `index_space`:

```text
ALTER TABLESPACE index_space OWNER TO mary;
```

### Compatibility

There is no `ALTER TABLESPACE` statement in the SQL standard.

### See Also

[CREATE TABLESPACE](create-tablespace.md), [DROP TABLESPACE](drop-tablespace.md)

