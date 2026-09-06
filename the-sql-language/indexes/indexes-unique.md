## 11.6. Unique Indexes [#](#INDEXES-UNIQUE)

<a id="id-1.5.10.9.2"></a>

Indexes can also be used to enforce uniqueness of a column's value,
or the uniqueness of the combined values of more than one column.

```

CREATE UNIQUE INDEX name ON table (column [, ...]) [ NULLS [ NOT ] DISTINCT ];
```

Currently, only B-tree indexes can be declared unique.

When an index is declared unique, multiple table rows with equal
indexed values are not allowed. By default, null values in a unique column
are not considered equal, allowing multiple nulls in the column. The
`NULLS NOT DISTINCT` option modifies this and causes the
index to treat nulls as equal. A multicolumn unique index will only reject
cases where all indexed columns are equal in multiple rows.

PostgreSQL automatically creates a unique
index when a unique constraint or primary key is defined for a table.
The index covers the columns that make up the primary key or unique
constraint (a multicolumn index, if appropriate), and is the mechanism
that enforces the constraint.

### Note

There's no need to manually
create indexes on unique columns; doing so would just duplicate
the automatically-created index.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-unique.html)（英文原文，待翻譯）
