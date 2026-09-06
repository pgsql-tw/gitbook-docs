## 11.3. Multicolumn Indexes [#](#INDEXES-MULTICOLUMN)

<a id="id-1.5.10.6.2"></a>

An index can be defined on more than one column of a table. For example, if
you have a table of this form:

```

CREATE TABLE test2 (
  major int,
  minor int,
  name varchar
);
```

(say, you keep your `/dev`
directory in a database...) and you frequently issue queries like:

```

SELECT name FROM test2 WHERE major = constant AND minor = constant;
```

then it might be appropriate to define an index on the columns
`major` and
`minor` together, e.g.:

```

CREATE INDEX test2_mm_idx ON test2 (major, minor);
```

Currently, only the B-tree, GiST, GIN, and BRIN index types support
multiple-key-column indexes. Whether there can be multiple key
columns is independent of whether `INCLUDE` columns
can be added to the index. Indexes can have up to 32 columns,
including `INCLUDE` columns. (This limit can be
altered when building PostgreSQL; see the
file `pg_config_manual.h`.)

A multicolumn B-tree index can be used with query conditions that
involve any subset of the index's columns, but the index is most
efficient when there are constraints on the leading (leftmost) columns.
The exact rule is that equality constraints on leading columns, plus
any inequality constraints on the first column that does not have an
equality constraint, will always be used to limit the portion of the index
that is scanned. Constraints on columns to the right of these columns
are checked in the index, so they'll always save visits to the table
proper, but they do not necessarily reduce the portion of the index that
has to be scanned. If a B-tree index scan can apply the skip scan
optimization effectively, it will apply every column constraint when
navigating through the index via repeated index searches. This can reduce
the portion of the index that has to be read, even though one or more
columns (prior to the least significant index column from the query
predicate) lacks a conventional equality constraint. Skip scan works by
generating a dynamic equality constraint internally, that matches every
possible value in an index column (though only given a column that lacks
an equality constraint that comes from the query predicate, and only when
the generated constraint can be used in conjunction with a later column
constraint from the query predicate).

For example, given an index on `(x, y)`, and a query
condition `WHERE y = 7700`, a B-tree index scan might be
able to apply the skip scan optimization. This generally happens when the
query planner expects that repeated `WHERE x = N AND y = 7700`
searches for every possible value of `N` (or for every
`x` value that is actually stored in the index) is the
fastest possible approach, given the available indexes on the table. This
approach is generally only taken when there are so few distinct
`x` values that the planner expects the scan to skip over
most of the index (because most of its leaf pages cannot possibly contain
relevant tuples). If there are many distinct `x` values,
then the entire index will have to be scanned, so in most cases the planner
will prefer a sequential table scan over using the index.

The skip scan optimization can also be applied selectively, during B-tree
scans that have at least some useful constraints from the query predicate.
For example, given an index on `(a, b, c)` and a
query condition `WHERE a = 5 AND b >= 42 AND c < 77`,
the index might have to be scanned from the first entry with
`a` = 5 and `b` = 42 up through the last
entry with `a` = 5. Index entries with
`c` >= 77 will never need to be filtered at the table
level, but it may or may not be profitable to skip over them within the
index. When skipping takes place, the scan starts a new index search to
reposition itself from the end of the current `a` = 5 and
`b` = N grouping (i.e. from the position in the index
where the first tuple `a = 5 AND b = N AND c >= 77`
appears), to the start of the next such grouping (i.e. the position in the
index where the first tuple `a = 5 AND b = N + 1`
appears).

A multicolumn GiST index can be used with query conditions that
involve any subset of the index's columns. Conditions on additional
columns restrict the entries returned by the index, but the condition on
the first column is the most important one for determining how much of
the index needs to be scanned. A GiST index will be relatively
ineffective if its first column has only a few distinct values, even if
there are many distinct values in additional columns.

A multicolumn GIN index can be used with query conditions that
involve any subset of the index's columns. Unlike B-tree or GiST,
index search effectiveness is the same regardless of which index column(s)
the query conditions use.

A multicolumn BRIN index can be used with query conditions that
involve any subset of the index's columns. Like GIN and unlike B-tree or
GiST, index search effectiveness is the same regardless of which index
column(s) the query conditions use. The only reason to have multiple BRIN
indexes instead of one multicolumn BRIN index on a single table is to have
a different `pages_per_range` storage parameter.

Of course, each column must be used with operators appropriate to the index
type; clauses that involve other operators will not be considered.

Multicolumn indexes should be used sparingly. In most situations,
an index on a single column is sufficient and saves space and time.
Indexes with more than three columns are unlikely to be helpful
unless the usage of the table is extremely stylized. See also
[Section 11.5](indexes-bitmap-scans.md) and
[Section 11.9](indexes-index-only-scans.md) for some discussion of the
merits of different index configurations.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-multicolumn.html)（英文原文，待翻譯）
