<a id="id-1.9.3.36.1"></a>

## ALTER TABLESPACE

ALTER TABLESPACE — change the definition of a tablespace

## Synopsis

```

ALTER TABLESPACE name RENAME TO new_name
ALTER TABLESPACE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER TABLESPACE name SET ( tablespace_option = value [, ... ] )
ALTER TABLESPACE name RESET ( tablespace_option [, ... ] )
```

<a id="id-1.9.3.36.5"></a>

## Description

`ALTER TABLESPACE` can be used to change the definition of
a tablespace.

You must own the tablespace to change the definition of a tablespace.
To alter the owner, you must also be able to `SET ROLE`
to the new owning role.
(Note that superusers have these privileges automatically.)

<a id="id-1.9.3.36.6"></a>

## Parameters

*`name`*
:   The name of an existing tablespace.

*`new_name`*
:   The new name of the tablespace. The new name cannot
    begin with `pg_`, as such names
    are reserved for system tablespaces.

*`new_owner`*
:   The new owner of the tablespace.

*`tablespace_option`*
:   A tablespace parameter to be set or reset. Currently, the only
    available parameters are `seq_page_cost`,
    `random_page_cost`, `effective_io_concurrency`
    and `maintenance_io_concurrency`.
    Setting these values for a particular tablespace will override the
    planner's usual estimate of the cost of reading pages from tables in
    that tablespace, and how many concurrent I/Os are issued, as established
    by the configuration parameters of the
    same name (see [seq_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-SEQ-PAGE-COST),
    [random_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-RANDOM-PAGE-COST),
    [effective_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY),
    [maintenance_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY)). This may be useful if
    one tablespace is located on a disk which is faster or slower than the
    remainder of the I/O subsystem.

<a id="id-1.9.3.36.7"></a>

## Examples

Rename tablespace `index_space` to `fast_raid`:

```

ALTER TABLESPACE index_space RENAME TO fast_raid;
```

Change the owner of tablespace `index_space`:

```

ALTER TABLESPACE index_space OWNER TO mary;
```

<a id="id-1.9.3.36.8"></a>

## Compatibility

There is no `ALTER TABLESPACE` statement in
the SQL standard.

<a id="id-1.9.3.36.9"></a>

## See Also

[CREATE TABLESPACE](sql-createtablespace.md), [DROP TABLESPACE](sql-droptablespace.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertablespace.html)（英文原文，待翻譯）
