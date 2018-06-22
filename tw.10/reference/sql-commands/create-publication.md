---
description: 版本：10
---

# CREATE PUBLICATION

CREATE PUBLICATION — define a new publication

### Synopsis

```text
CREATE PUBLICATION name
    [ FOR TABLE [ ONLY ] table_name [ * ] [, ...]
      | FOR ALL TABLES ]
    [ WITH ( publication_parameter [= value] [, ... ] ) ]
```

### Description

`CREATE PUBLICATION` adds a new publication into the current database. The publication name must be distinct from the name of any existing publication in the current database.

A publication is essentially a group of tables whose data changes are intended to be replicated through logical replication. See [Section 31.1](https://www.postgresql.org/docs/10/static/logical-replication-publication.html) for details about how publications fit into the logical replication setup.

### Parameters

_`name`_

The name of the new publication.`FOR TABLE`

Specifies a list of tables to add to the publication. If `ONLY` is specified before the table name, only that table is added to the publication. If `ONLY` is not specified, the table and all its descendant tables \(if any\) are added. Optionally, `*` can be specified after the table name to explicitly indicate that descendant tables are included.

Only persistent base tables can be part of a publication. Temporary tables, unlogged tables, foreign tables, materialized views, regular views, and partitioned tables cannot be part of a publication. To replicate a partitioned table, add the individual partitions to the publication.`FOR ALL TABLES`

Marks the publication as one that replicates changes for all tables in the database, including tables created in the future.`WITH (` _`publication_parameter`_ \[= _`value`_\] \[, ... \] \)

This clause specifies optional parameters for a publication. The following parameters are supported:`publish` \(`string`\)

This parameter determines which DML operations will be published by the new publication to the subscribers. The value is comma-separated list of operations. The allowed operations are `insert`, `update`, and `delete`. The default is to publish all actions, and so the default value for this option is `'insert, update, delete'`.

### Notes

If neither `FOR TABLE` nor `FOR ALL TABLES` is specified, then the publication starts out with an empty set of tables. That is useful if tables are to be added later.

The creation of a publication does not start replication. It only defines a grouping and filtering logic for future subscribers.

To create a publication, the invoking user must have the `CREATE` privilege for the current database. \(Of course, superusers bypass this check.\)

To add a table to a publication, the invoking user must have ownership rights on the table. The `FOR ALL TABLES` clause requires the invoking user to be a superuser.

The tables added to a publication that publishes `UPDATE` and/or `DELETE` operations must have `REPLICA IDENTITY` defined. Otherwise those operations will be disallowed on those tables.

For an `INSERT ... ON CONFLICT` command, the publication will publish the operation that actually results from the command. So depending of the outcome, it may be published as either `INSERT` or `UPDATE`, or it may not be published at all.

`COPY ... FROM` commands are published as `INSERT` operations.

`TRUNCATE` and DDL operations are not published.

### Examples

Create a publication that publishes all changes in two tables:

```text
CREATE PUBLICATION mypublication FOR TABLE users, departments;
```

Create a publication that publishes all changes in all tables:

```text
CREATE PUBLICATION alltables FOR ALL TABLES;
```

Create a publication that only publishes `INSERT` operations in one table:

```text
CREATE PUBLICATION insert_only FOR TABLE mydata
    WITH (publish = 'insert');
```

### Compatibility

`CREATE PUBLICATION` is a PostgreSQL extension.

### See Also

[ALTER PUBLICATION](https://www.postgresql.org/docs/10/static/sql-alterpublication.html), [DROP PUBLICATION](https://www.postgresql.org/docs/10/static/sql-droppublication.html)

