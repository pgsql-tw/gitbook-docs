# 11.6. 唯一值索引

Indexes can also be used to enforce uniqueness of a column's value, or the uniqueness of the combined values of more than one column.

```text
CREATE UNIQUE INDEX 
name
 ON 
table
 (
column
 [
, ...
]);
```

Currently, only B-tree indexes can be declared unique.

When an index is declared unique, multiple table rows with equal indexed values are not allowed. Null values are not considered equal. A multicolumn unique index will only reject cases where all indexed columns are equal in multiple rows.

PostgreSQLautomatically creates a unique index when a unique constraint or primary key is defined for a table. The index covers the columns that make up the primary key or unique constraint \(a multicolumn index, if appropriate\), and is the mechanism that enforces the constraint.

## Note

There's no need to manually create indexes on unique columns; doing so would just duplicate the automatically-created index.

