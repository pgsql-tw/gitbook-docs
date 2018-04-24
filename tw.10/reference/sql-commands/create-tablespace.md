---
description: CREATE TABLESPACE — define a new tablespace
---

# CREATE TABLESPACE

### Synopsis

```text
CREATE TABLESPACE tablespace_name
    [ OWNER { new_owner | CURRENT_USER | SESSION_USER } ]
    LOCATION 'directory'
    [ WITH ( tablespace_option = value [, ... ] ) ]
```

### Description

`CREATE TABLESPACE` registers a new cluster-wide tablespace. The tablespace name must be distinct from the name of any existing tablespace in the database cluster.

A tablespace allows superusers to define an alternative location on the file system where the data files containing database objects \(such as tables and indexes\) can reside.

A user with appropriate privileges can pass _`tablespace_name`_ to `CREATE DATABASE`, `CREATE TABLE`, `CREATE INDEX` or `ADD CONSTRAINT` to have the data files for these objects stored within the specified tablespace.

#### Warning

A tablespace cannot be used independently of the cluster in which it is defined; see [Section 22.6](https://www.postgresql.org/docs/10/static/manage-ag-tablespaces.html).

### Parameters

_`tablespace_name`_

The name of a tablespace to be created. The name cannot begin with `pg_`, as such names are reserved for system tablespaces._`user_name`_

The name of the user who will own the tablespace. If omitted, defaults to the user executing the command. Only superusers can create tablespaces, but they can assign ownership of tablespaces to non-superusers._`directory`_

The directory that will be used for the tablespace. The directory should be empty and must be owned by the PostgreSQL system user. The directory must be specified by an absolute path name._`tablespace_option`_

A tablespace parameter to be set or reset. Currently, the only available parameters are `seq_page_cost`, `random_page_cost` and `effective_io_concurrency`. Setting either value for a particular tablespace will override the planner's usual estimate of the cost of reading pages from tables in that tablespace, as established by the configuration parameters of the same name \(see [seq\_page\_cost](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-SEQ-PAGE-COST), [random\_page\_cost](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-RANDOM-PAGE-COST), [effective\_io\_concurrency](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-EFFECTIVE-IO-CONCURRENCY)\). This may be useful if one tablespace is located on a disk which is faster or slower than the remainder of the I/O subsystem.

### Notes

Tablespaces are only supported on systems that support symbolic links.

`CREATE TABLESPACE` cannot be executed inside a transaction block.

### Examples

Create a tablespace `dbspace` at `/data/dbs`:

```text
CREATE TABLESPACE dbspace LOCATION '/data/dbs';
```

Create a tablespace `indexspace` at `/data/indexes` owned by user `genevieve`:

```text
CREATE TABLESPACE indexspace OWNER genevieve LOCATION '/data/indexes';
```

### Compatibility

`CREATE TABLESPACE` is a PostgreSQL extension.

### See Also

[CREATE DATABASE](https://www.postgresql.org/docs/10/static/sql-createdatabase.html), [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html), [CREATE INDEX](https://www.postgresql.org/docs/10/static/sql-createindex.html), [DROP TABLESPACE](drop-tablespace.md), [ALTER TABLESPACE](alter-tablespace.md)

### 參考資料

1.  [PostgreSQL: Documentation: 10: CREATE TABLESPACE](https://www.postgresql.org/docs/10/static/sql-createtablespace.html)



