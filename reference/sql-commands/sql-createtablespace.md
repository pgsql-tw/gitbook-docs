<a id="id-1.9.3.87.1"></a>

## CREATE TABLESPACE

CREATE TABLESPACE — define a new tablespace

## Synopsis

```

CREATE TABLESPACE tablespace_name
    [ OWNER { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER } ]
    LOCATION 'directory'
    [ WITH ( tablespace_option = value [, ... ] ) ]
```

<a id="id-1.9.3.87.5"></a>

## Description

`CREATE TABLESPACE` registers a new cluster-wide
tablespace. The tablespace name must be distinct from the name of any
existing tablespace in the database cluster.

A tablespace allows superusers to define an alternative location on
the file system where the data files containing database objects
(such as tables and indexes) can reside.

A user with appropriate privileges can pass
*`tablespace_name`* to
`CREATE DATABASE`, `CREATE TABLE`,
`CREATE INDEX` or `ADD CONSTRAINT` to have the data
files for these objects stored within the specified tablespace.

### Warning

A tablespace cannot be used independently of the cluster in which it
is defined; see [Section 22.6](../../server-administration/managing-databases/manage-ag-tablespaces.md).

<a id="id-1.9.3.87.6"></a>

## Parameters

*`tablespace_name`*
:   The name of a tablespace to be created. The name cannot
    begin with `pg_`, as such names
    are reserved for system tablespaces.

*`user_name`*
:   The name of the user who will own the tablespace. If omitted,
    defaults to the user executing the command. Only superusers
    can create tablespaces, but they can assign ownership of tablespaces
    to non-superusers.

*`directory`*
:   The directory that will be used for the tablespace. The directory
    must exist (`CREATE TABLESPACE` will not create it),
    should be empty, and must be owned by the
    PostgreSQL system user. The directory must be
    specified by an absolute path name.

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

<a id="id-1.9.3.87.7"></a>

## Notes

`CREATE TABLESPACE` cannot be executed inside a transaction
block.

<a id="id-1.9.3.87.8"></a>

## Examples

To create a tablespace `dbspace` at file system location
`/data/dbs`, first create the directory using operating
system facilities and set the correct ownership:

```

mkdir /data/dbs
chown postgres:postgres /data/dbs
```

Then issue the tablespace creation command inside
PostgreSQL:

```

CREATE TABLESPACE dbspace LOCATION '/data/dbs';
```

To create a tablespace owned by a different database user, use a command
like this:

```

CREATE TABLESPACE indexspace OWNER genevieve LOCATION '/data/indexes';
```

<a id="id-1.9.3.87.9"></a>

## Compatibility

`CREATE TABLESPACE` is a PostgreSQL
extension.

<a id="id-1.9.3.87.10"></a>

## See Also

[CREATE DATABASE](sql-createdatabase.md), [CREATE TABLE](sql-createtable.md), [CREATE INDEX](sql-createindex.md), [DROP TABLESPACE](sql-droptablespace.md), [ALTER TABLESPACE](sql-altertablespace.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtablespace.html)（英文原文，待翻譯）
