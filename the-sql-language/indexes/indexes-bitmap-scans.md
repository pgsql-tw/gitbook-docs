## 11.5. Combining Multiple Indexes [#](#INDEXES-BITMAP-SCANS)

<a id="id-1.5.10.8.2"></a><a id="id-1.5.10.8.3"></a>

A single index scan can only use query clauses that use the index's
columns with operators of its operator class and are joined with
`AND`. For example, given an index on `(a, b)`
a query condition like `WHERE a = 5 AND b = 6` could
use the index, but a query like `WHERE a = 5 OR b = 6` could not
directly use the index.

Fortunately,
PostgreSQL has the ability to combine multiple indexes
(including multiple uses of the same index) to handle cases that cannot
be implemented by single index scans. The system can form `AND`
and `OR` conditions across several index scans. For example,
a query like `WHERE x = 42 OR x = 47 OR x = 53 OR x = 99`
could be broken down into four separate scans of an index on `x`,
each scan using one of the query clauses. The results of these scans are
then ORed together to produce the result. Another example is that if we
have separate indexes on `x` and `y`, one possible
implementation of a query like `WHERE x = 5 AND y = 6` is to
use each index with the appropriate query clause and then AND together
the index results to identify the result rows.

To combine multiple indexes, the system scans each needed index and
prepares a *bitmap* in memory giving the locations of
table rows that are reported as matching that index's conditions.
The bitmaps are then ANDed and ORed together as needed by the query.
Finally, the actual table rows are visited and returned. The table rows
are visited in physical order, because that is how the bitmap is laid
out; this means that any ordering of the original indexes is lost, and
so a separate sort step will be needed if the query has an `ORDER
BY` clause. For this reason, and because each additional index scan
adds extra time, the planner will sometimes choose to use a simple index
scan even though additional indexes are available that could have been
used as well.

In all but the simplest applications, there are various combinations of
indexes that might be useful, and the database developer must make
trade-offs to decide which indexes to provide. Sometimes multicolumn
indexes are best, but sometimes it's better to create separate indexes
and rely on the index-combination feature. For example, if your
workload includes a mix of queries that sometimes involve only column
`x`, sometimes only column `y`, and sometimes both
columns, you might choose to create two separate indexes on
`x` and `y`, relying on index combination to
process the queries that use both columns. You could also create a
multicolumn index on `(x, y)`. This index would typically be
more efficient than index combination for queries involving both
columns, but as discussed in [Section 11.3](indexes-multicolumn.md), it
would be less useful for queries involving only `y`. Just
how useful will depend on how effective the B-tree index skip scan
optimization is; if `x` has no more than several hundred
distinct values, skip scan will make searches for specific
`y` values execute reasonably efficiently. A combination
of a multicolumn index on `(x, y)` and a separate index on
`y` might also serve reasonably well. For
queries involving only `x`, the multicolumn index could be
used, though it would be larger and hence slower than an index on
`x` alone. The last alternative is to create all three
indexes, but this is probably only reasonable if the table is searched
much more often than it is updated and all three types of query are
common. If one of the types of query is much less common than the
others, you'd probably settle for creating just the two indexes that
best match the common types.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-bitmap-scans.html)（英文原文，待翻譯）
