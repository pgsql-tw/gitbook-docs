## 14.1. Using `EXPLAIN` [#](#USING-EXPLAIN)

[14.1.1. `EXPLAIN` Basics](using-explain.md#USING-EXPLAIN-BASICS)

[14.1.2. `EXPLAIN ANALYZE`](using-explain.md#USING-EXPLAIN-ANALYZE)

[14.1.3. Caveats](using-explain.md#USING-EXPLAIN-CAVEATS)

<a id="id-1.5.13.4.2"></a><a id="id-1.5.13.4.3"></a>

PostgreSQL devises a *query
plan* for each query it receives. Choosing the right
plan to match the query structure and the properties of the data
is absolutely critical for good performance, so the system includes
a complex *planner* that tries to choose good plans.
You can use the [`EXPLAIN`](../../reference/sql-commands/sql-explain.md) command
to see what query plan the planner creates for any query.
Plan-reading is an art that requires some experience to master,
but this section attempts to cover the basics.

Examples in this section are drawn from the regression test database
after doing a `VACUUM ANALYZE`, using v18 development sources.
You should be able to get similar results if you try the examples
yourself, but your estimated costs and row counts might vary slightly
because `ANALYZE`'s statistics are random samples rather
than exact, and because costs are inherently somewhat platform-dependent.

The examples use `EXPLAIN`'s default “text” output
format, which is compact and convenient for humans to read.
If you want to feed `EXPLAIN`'s output to a program for further
analysis, you should use one of its machine-readable output formats
(XML, JSON, or YAML) instead.

<a id="USING-EXPLAIN-BASICS"></a>

### 14.1.1. `EXPLAIN` Basics [#](#USING-EXPLAIN-BASICS)

The structure of a query plan is a tree of *plan nodes*.
Nodes at the bottom level of the tree are scan nodes: they return raw rows
from a table. There are different types of scan nodes for different
table access methods: sequential scans, index scans, and bitmap index
scans. There are also non-table row sources, such as `VALUES`
clauses and set-returning functions in `FROM`, which have their
own scan node types.
If the query requires joining, aggregation, sorting, or other
operations on the raw rows, then there will be additional nodes
above the scan nodes to perform these operations. Again,
there is usually more than one possible way to do these operations,
so different node types can appear here too. The output
of `EXPLAIN` has one line for each node in the plan
tree, showing the basic node type plus the cost estimates that the planner
made for the execution of that plan node. Additional lines might appear,
indented from the node's summary line,
to show additional properties of the node.
The very first line (the summary line for the topmost
node) has the estimated total execution cost for the plan; it is this
number that the planner seeks to minimize.

Here is a trivial example, just to show what the output looks like:

```

EXPLAIN SELECT * FROM tenk1;

                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..445.00 rows=10000 width=244)
```

Since this query has no `WHERE` clause, it must scan all the
rows of the table, so the planner has chosen to use a simple sequential
scan plan. The numbers that are quoted in parentheses are (left
to right):

* Estimated start-up cost. This is the time expended before the output
  phase can begin, e.g., time to do the sorting in a sort node.
* Estimated total cost. This is stated on the assumption that the plan
  node is run to completion, i.e., all available rows are retrieved.
  In practice a node's parent node might stop short of reading all
  available rows (see the `LIMIT` example below).
* Estimated number of rows output by this plan node. Again, the node
  is assumed to be run to completion.
* Estimated average width of rows output by this plan node (in bytes).

The costs are measured in arbitrary units determined by the planner's
cost parameters (see [Section 19.7.2](../../server-administration/runtime-config/runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)).
Traditional practice is to measure the costs in units of disk page
fetches; that is, [seq_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-SEQ-PAGE-COST) is conventionally
set to `1.0` and the other cost parameters are set relative
to that. The examples in this section are run with the default cost
parameters.

It's important to understand that the cost of an upper-level node includes
the cost of all its child nodes. It's also important to realize that
the cost only reflects things that the planner cares about.
In particular, the cost does not consider the time spent to convert
output values to text form or to transmit them to the client, which
could be important factors in the real elapsed time; but the planner
ignores those costs because it cannot change them by altering the
plan. (Every correct plan will output the same row set, we trust.)

The `rows` value is a little tricky because it is
not the number of rows processed or scanned by the
plan node, but rather the number emitted by the node. This is often
less than the number scanned, as a result of filtering by any
`WHERE`-clause conditions that are being applied at the node.
Ideally the top-level rows estimate will approximate the number of rows
actually returned, updated, or deleted by the query.

Returning to our example:

```

EXPLAIN SELECT * FROM tenk1;

                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..445.00 rows=10000 width=244)
```

These numbers are derived very straightforwardly. If you do:

```

SELECT relpages, reltuples FROM pg_class WHERE relname = 'tenk1';
```

you will find that `tenk1` has 345 disk
pages and 10000 rows. The estimated cost is computed as (disk pages read \*
[seq_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-SEQ-PAGE-COST)) + (rows scanned \*
[cpu_tuple_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-CPU-TUPLE-COST)). By default,
`seq_page_cost` is 1.0 and `cpu_tuple_cost` is 0.01,
so the estimated cost is (345 \* 1.0) + (10000 \* 0.01) = 445.

Now let's modify the query to add a `WHERE` condition:

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 7000;

                         QUERY PLAN
------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..470.00 rows=7000 width=244)
   Filter: (unique1 < 7000)
```

Notice that the `EXPLAIN` output shows the `WHERE`
clause being applied as a “filter” condition attached to the Seq
Scan plan node. This means that
the plan node checks the condition for each row it scans, and outputs
only the ones that pass the condition.
The estimate of output rows has been reduced because of the
`WHERE` clause.
However, the scan will still have to visit all 10000 rows, so the cost
hasn't decreased; in fact it has gone up a bit (by 10000 \* [cpu_operator_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-CPU-OPERATOR-COST), to be exact) to reflect the extra CPU
time spent checking the `WHERE` condition.

The actual number of rows this query would select is 7000, but the `rows`
estimate is only approximate. If you try to duplicate this experiment,
you may well get a slightly different estimate; moreover, it can
change after each `ANALYZE` command, because the
statistics produced by `ANALYZE` are taken from a
randomized sample of the table.

Now, let's make the condition more restrictive:

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100;

                                  QUERY PLAN
-------------------------------------------------------------------​-----------
 Bitmap Heap Scan on tenk1  (cost=5.06..224.98 rows=100 width=244)
   Recheck Cond: (unique1 < 100)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
         Index Cond: (unique1 < 100)
```

Here the planner has decided to use a two-step plan: the child plan
node visits an index to find the locations of rows matching the index
condition, and then the upper plan node actually fetches those rows
from the table itself. Fetching rows separately is much more
expensive than reading them sequentially, but because not all the pages
of the table have to be visited, this is still cheaper than a sequential
scan. (The reason for using two plan levels is that the upper plan
node sorts the row locations identified by the index into physical order
before reading them, to minimize the cost of separate fetches.
The “bitmap” mentioned in the node names is the mechanism that
does the sorting.)

Now let's add another condition to the `WHERE` clause:

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND stringu1 = 'xxx';

                                  QUERY PLAN
-------------------------------------------------------------------​-----------
 Bitmap Heap Scan on tenk1  (cost=5.04..225.20 rows=1 width=244)
   Recheck Cond: (unique1 < 100)
   Filter: (stringu1 = 'xxx'::name)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
         Index Cond: (unique1 < 100)
```

The added condition `stringu1 = 'xxx'` reduces the
output row count estimate, but not the cost because we still have to visit
the same set of rows. That's because the `stringu1` clause
cannot be applied as an index condition, since this index is only on
the `unique1` column. Instead it is applied as a filter on
the rows retrieved using the index. Thus the cost has actually gone up
slightly to reflect this extra checking.

In some cases the planner will prefer a “simple” index scan plan:

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 = 42;

                                 QUERY PLAN
-------------------------------------------------------------------​----------
 Index Scan using tenk1_unique1 on tenk1  (cost=0.29..8.30 rows=1 width=244)
   Index Cond: (unique1 = 42)
```

In this type of plan the table rows are fetched in index order, which
makes them even more expensive to read, but there are so few that the
extra cost of sorting the row locations is not worth it. You'll most
often see this plan type for queries that fetch just a single row. It's
also often used for queries that have an `ORDER BY` condition
that matches the index order, because then no extra sorting step is needed
to satisfy the `ORDER BY`. In this example, adding
`ORDER BY unique1` would use the same plan because the
index already implicitly provides the requested ordering.

The planner may implement an `ORDER BY` clause in several
ways. The above example shows that such an ordering clause may be
implemented implicitly. The planner may also add an explicit
`Sort` step:

```

EXPLAIN SELECT * FROM tenk1 ORDER BY unique1;

                            QUERY PLAN
-------------------------------------------------------------------
 Sort  (cost=1109.39..1134.39 rows=10000 width=244)
   Sort Key: unique1
   ->  Seq Scan on tenk1  (cost=0.00..445.00 rows=10000 width=244)
```

If a part of the plan guarantees an ordering on a prefix of the
required sort keys, then the planner may instead decide to use an
`Incremental Sort` step:

```

EXPLAIN SELECT * FROM tenk1 ORDER BY hundred, ten LIMIT 100;

                                              QUERY PLAN
-------------------------------------------------------------------​-----------------------------
 Limit  (cost=19.35..39.49 rows=100 width=244)
   ->  Incremental Sort  (cost=19.35..2033.39 rows=10000 width=244)
         Sort Key: hundred, ten
         Presorted Key: hundred
         ->  Index Scan using tenk1_hundred on tenk1  (cost=0.29..1574.20 rows=10000 width=244)
```

Compared to regular sorts, sorting incrementally allows returning tuples
before the entire result set has been sorted, which particularly enables
optimizations with `LIMIT` queries. It may also reduce
memory usage and the likelihood of spilling sorts to disk, but it comes at
the cost of the increased overhead of splitting the result set into multiple
sorting batches.

If there are separate indexes on several of the columns referenced
in `WHERE`, the planner might choose to use an AND or OR
combination of the indexes:

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000;

                                     QUERY PLAN
-------------------------------------------------------------------​------------------
 Bitmap Heap Scan on tenk1  (cost=25.07..60.11 rows=10 width=244)
   Recheck Cond: ((unique1 < 100) AND (unique2 > 9000))
   ->  BitmapAnd  (cost=25.07..25.07 rows=10 width=0)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
               Index Cond: (unique1 < 100)
         ->  Bitmap Index Scan on tenk1_unique2  (cost=0.00..19.78 rows=999 width=0)
               Index Cond: (unique2 > 9000)
```

But this requires visiting both indexes, so it's not necessarily a win
compared to using just one index and treating the other condition as
a filter. If you vary the ranges involved you'll see the plan change
accordingly.

Here is an example showing the effects of `LIMIT`:

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000 LIMIT 2;

                                     QUERY PLAN
-------------------------------------------------------------------​------------------
 Limit  (cost=0.29..14.28 rows=2 width=244)
   ->  Index Scan using tenk1_unique2 on tenk1  (cost=0.29..70.27 rows=10 width=244)
         Index Cond: (unique2 > 9000)
         Filter: (unique1 < 100)
```

This is the same query as above, but we added a `LIMIT` so that
not all the rows need be retrieved, and the planner changed its mind about
what to do. Notice that the total cost and row count of the Index Scan
node are shown as if it were run to completion. However, the Limit node
is expected to stop after retrieving only a fifth of those rows, so its
total cost is only a fifth as much, and that's the actual estimated cost
of the query. This plan is preferred over adding a Limit node to the
previous plan because the Limit could not avoid paying the startup cost
of the bitmap scan, so the total cost would be something over 25 units
with that approach.

Let's try joining two tables, using the columns we have been discussing:

```

EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t1.unique2 = t2.unique2;

                                      QUERY PLAN
-------------------------------------------------------------------​-------------------
 Nested Loop  (cost=4.65..118.50 rows=10 width=488)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.38 rows=10 width=244)
         Recheck Cond: (unique1 < 10)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0)
               Index Cond: (unique1 < 10)
   ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..7.90 rows=1 width=244)
         Index Cond: (unique2 = t1.unique2)
```

In this plan, we have a nested-loop join node with two table scans as
inputs, or children. The indentation of the node summary lines reflects
the plan tree structure. The join's first, or “outer”, child
is a bitmap scan similar to those we saw before. Its cost and row count
are the same as we'd get from `SELECT ... WHERE unique1 < 10`
because we are
applying the `WHERE` clause `unique1 < 10`
at that node.
The `t1.unique2 = t2.unique2` clause is not relevant yet,
so it doesn't affect the row count of the outer scan. The nested-loop
join node will run its second,
or “inner” child once for each row obtained from the outer child.
Column values from the current outer row can be plugged into the inner
scan; here, the `t1.unique2` value from the outer row is available,
so we get a plan and costs similar to what we saw above for a simple
`SELECT ... WHERE t2.unique2 = constant` case.
(The estimated cost is actually a bit lower than what was seen above,
as a result of caching that's expected to occur during the repeated
index scans on `t2`.) The
costs of the loop node are then set on the basis of the cost of the outer
scan, plus one repetition of the inner scan for each outer row (10 \* 7.90,
here), plus a little CPU time for join processing.

In this example the join's output row count is the same as the product
of the two scans' row counts, but that's not true in all cases because
there can be additional `WHERE` clauses that mention both tables
and so can only be applied at the join point, not to either input scan.
Here's an example:

```

EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t2.unique2 < 10 AND t1.hundred < t2.hundred;

                                         QUERY PLAN
-------------------------------------------------------------------​--------------------------
 Nested Loop  (cost=4.65..49.36 rows=33 width=488)
   Join Filter: (t1.hundred < t2.hundred)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.38 rows=10 width=244)
         Recheck Cond: (unique1 < 10)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0)
               Index Cond: (unique1 < 10)
   ->  Materialize  (cost=0.29..8.51 rows=10 width=244)
         ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..8.46 rows=10 width=244)
               Index Cond: (unique2 < 10)
```

The condition `t1.hundred < t2.hundred` can't be
tested in the `tenk2_unique2` index, so it's applied at the
join node. This reduces the estimated output row count of the join node,
but does not change either input scan.

Notice that here the planner has chosen to “materialize” the inner
relation of the join, by putting a Materialize plan node atop it. This
means that the `t2` index scan will be done just once, even
though the nested-loop join node needs to read that data ten times, once
for each row from the outer relation. The Materialize node saves the data
in memory as it's read, and then returns the data from memory on each
subsequent pass.

When dealing with outer joins, you might see join plan nodes with both
“Join Filter” and plain “Filter” conditions attached.
Join Filter conditions come from the outer join's `ON` clause,
so a row that fails the Join Filter condition could still get emitted as
a null-extended row. But a plain Filter condition is applied after the
outer-join rules and so acts to remove rows unconditionally. In an inner
join there is no semantic difference between these types of filters.

If we change the query's selectivity a bit, we might get a very different
join plan:

```

EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Hash Join  (cost=226.23..709.73 rows=100 width=488)
   Hash Cond: (t2.unique2 = t1.unique2)
   ->  Seq Scan on tenk2 t2  (cost=0.00..445.00 rows=10000 width=244)
   ->  Hash  (cost=224.98..224.98 rows=100 width=244)
         ->  Bitmap Heap Scan on tenk1 t1  (cost=5.06..224.98 rows=100 width=244)
               Recheck Cond: (unique1 < 100)
               ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
                     Index Cond: (unique1 < 100)
```

Here, the planner has chosen to use a hash join, in which rows of one
table are entered into an in-memory hash table, after which the other
table is scanned and the hash table is probed for matches to each row.
Again note how the indentation reflects the plan structure: the bitmap
scan on `tenk1` is the input to the Hash node, which constructs
the hash table. That's then returned to the Hash Join node, which reads
rows from its outer child plan and searches the hash table for each one.

Another possible type of join is a merge join, illustrated here:

```

EXPLAIN SELECT *
FROM tenk1 t1, onek t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Merge Join  (cost=0.56..233.49 rows=10 width=488)
   Merge Cond: (t1.unique2 = t2.unique2)
   ->  Index Scan using tenk1_unique2 on tenk1 t1  (cost=0.29..643.28 rows=100 width=244)
         Filter: (unique1 < 100)
   ->  Index Scan using onek_unique2 on onek t2  (cost=0.28..166.28 rows=1000 width=244)
```

Merge join requires its input data to be sorted on the join keys. In this
example each input is sorted by using an index scan to visit the rows
in the correct order; but a sequential scan and sort could also be used.
(Sequential-scan-and-sort frequently beats an index scan for sorting many rows,
because of the nonsequential disk access required by the index scan.)

One way to look at variant plans is to force the planner to disregard
whatever strategy it thought was the cheapest, using the enable/disable
flags described in [Section 19.7.1](../../server-administration/runtime-config/runtime-config-query.md#RUNTIME-CONFIG-QUERY-ENABLE).
(This is a crude tool, but useful. See
also [Section 14.3](explicit-joins.md).)
For example, if we're unconvinced that merge join is the best join
type for the previous example, we could try

```

SET enable_mergejoin = off;

EXPLAIN SELECT *
FROM tenk1 t1, onek t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Hash Join  (cost=226.23..344.08 rows=10 width=488)
   Hash Cond: (t2.unique2 = t1.unique2)
   ->  Seq Scan on onek t2  (cost=0.00..114.00 rows=1000 width=244)
   ->  Hash  (cost=224.98..224.98 rows=100 width=244)
         ->  Bitmap Heap Scan on tenk1 t1  (cost=5.06..224.98 rows=100 width=244)
               Recheck Cond: (unique1 < 100)
               ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
                     Index Cond: (unique1 < 100)
```

which shows that the planner thinks that hash join would be nearly 50%
more expensive than merge join for this case.
Of course, the next question is whether it's right about that.
We can investigate that using `EXPLAIN ANALYZE`, as
discussed [below](using-explain.md#USING-EXPLAIN-ANALYZE).

When using the enable/disable flags to disable plan node types, many of
the flags only discourage the use of the corresponding plan node and don't
outright disallow the planner's ability to use the plan node type. This
is by design so that the planner still maintains the ability to form a
plan for a given query. When the resulting plan contains a disabled node,
the `EXPLAIN` output will indicate this fact.

```

SET enable_seqscan = off;
EXPLAIN SELECT * FROM unit;

                       QUERY PLAN
---------------------------------------------------------
 Seq Scan on unit  (cost=0.00..21.30 rows=1130 width=44)
   Disabled: true
```

Because the `unit` table has no indexes, there is no
other means to read the table data, so the sequential scan is the only
option available to the query planner.

<a id="id-1.5.13.4.7.31.1"></a>
Some query plans involve *subplans*, which arise
from sub-`SELECT`s in the original query. Such
queries can sometimes be transformed into ordinary join plans, but
when they cannot be, we get plans like:

```

EXPLAIN VERBOSE SELECT unique1
FROM tenk1 t
WHERE t.ten < ALL (SELECT o.ten FROM onek o WHERE o.four = t.four);

                               QUERY PLAN
-------------------------------------------------------------------​------
 Seq Scan on public.tenk1 t  (cost=0.00..586095.00 rows=5000 width=4)
   Output: t.unique1
   Filter: (ALL (t.ten < (SubPlan 1).col1))
   SubPlan 1
     ->  Seq Scan on public.onek o  (cost=0.00..116.50 rows=250 width=4)
           Output: o.ten
           Filter: (o.four = t.four)
```

This rather artificial example serves to illustrate a couple of
points: values from the outer plan level can be passed down into a
subplan (here, `t.four` is passed down) and the
results of the sub-select are available to the outer plan. Those
result values are shown by `EXPLAIN` with notations
like
`(subplan_name).colN`,
which refers to the *`N`*'th output column of
the sub-`SELECT`.

<a id="id-1.5.13.4.7.32.1"></a>
In the example above, the `ALL` operator runs the
subplan again for each row of the outer query (which accounts for the
high estimated cost). Some queries can use a *hashed
subplan* to avoid that:

```

EXPLAIN SELECT *
FROM tenk1 t
WHERE t.unique1 NOT IN (SELECT o.unique1 FROM onek o);

                                         QUERY PLAN
-------------------------------------------------------------------​-------------------------
 Seq Scan on tenk1 t  (cost=61.77..531.77 rows=5000 width=244)
   Filter: (NOT (ANY (unique1 = (hashed SubPlan 1).col1)))
   SubPlan 1
     ->  Index Only Scan using onek_unique1 on onek o  (cost=0.28..59.27 rows=1000 width=4)
(4 rows)
```

Here, the subplan is run a single time and its output is loaded into
an in-memory hash table, which is then probed by the
outer `ANY` operator. This requires that the
sub-`SELECT` not reference any variables of the outer
query, and that the `ANY`'s comparison operator be
amenable to hashing.

<a id="id-1.5.13.4.7.33.1"></a>
If, in addition to not referencing any variables of the outer query,
the sub-`SELECT` cannot return more than one row,
it may instead be implemented as an *initplan*:

```

EXPLAIN VERBOSE SELECT unique1
FROM tenk1 t1 WHERE t1.ten = (SELECT (random() * 10)::integer);

                             QUERY PLAN
------------------------------------------------------------​--------
 Seq Scan on public.tenk1 t1  (cost=0.02..470.02 rows=1000 width=4)
   Output: t1.unique1
   Filter: (t1.ten = (InitPlan 1).col1)
   InitPlan 1
     ->  Result  (cost=0.00..0.02 rows=1 width=4)
           Output: ((random() * '10'::double precision))::integer
```

An initplan is run only once per execution of the outer plan, and its
results are saved for re-use in later rows of the outer plan. So in
this example `random()` is evaluated only once and
all the values of `t1.ten` are compared to the same
randomly-chosen integer. That's quite different from what would
happen without the sub-`SELECT` construct.

<a id="USING-EXPLAIN-ANALYZE"></a>

### 14.1.2. `EXPLAIN ANALYZE` [#](#USING-EXPLAIN-ANALYZE)

It is possible to check the accuracy of the planner's estimates
by using `EXPLAIN`'s `ANALYZE` option. With this
option, `EXPLAIN` actually executes the query, and then displays
the true row counts and true run time accumulated within each plan node,
along with the same estimates that a plain `EXPLAIN`
shows. For example, we might get a result like this:

```

EXPLAIN ANALYZE SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t1.unique2 = t2.unique2;

                                                           QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------------------
 Nested Loop  (cost=4.65..118.50 rows=10 width=488) (actual time=0.017..0.051 rows=10.00 loops=1)
   Buffers: shared hit=36 read=6
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.38 rows=10 width=244) (actual time=0.009..0.017 rows=10.00 loops=1)
         Recheck Cond: (unique1 < 10)
         Heap Blocks: exact=10
         Buffers: shared hit=3 read=5 written=4
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0) (actual time=0.004..0.004 rows=10.00 loops=1)
               Index Cond: (unique1 < 10)
               Index Searches: 1
               Buffers: shared hit=2
   ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..7.90 rows=1 width=244) (actual time=0.003..0.003 rows=1.00 loops=10)
         Index Cond: (unique2 = t1.unique2)
         Index Searches: 10
         Buffers: shared hit=24 read=6
 Planning:
   Buffers: shared hit=15 dirtied=9
 Planning Time: 0.485 ms
 Execution Time: 0.073 ms
```

Note that the “actual time” values are in milliseconds of
real time, whereas the `cost` estimates are expressed in
arbitrary units; so they are unlikely to match up.
The thing that's usually most important to look for is whether the
estimated row counts are reasonably close to reality. In this example
the estimates were all dead-on, but that's quite unusual in practice.

In some query plans, it is possible for a subplan node to be executed more
than once. For example, the inner index scan will be executed once per
outer row in the above nested-loop plan. In such cases, the
`loops` value reports the
total number of executions of the node, and the actual time and rows
values shown are averages per-execution. This is done to make the numbers
comparable with the way that the cost estimates are shown. Multiply by
the `loops` value to get the total time actually spent in
the node. In the above example, we spent a total of 0.030 milliseconds
executing the index scans on `tenk2`.

In some cases `EXPLAIN ANALYZE` shows additional execution
statistics beyond the plan node execution times and row counts.
For example, Sort and Hash nodes provide extra information:

```

EXPLAIN ANALYZE SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2 ORDER BY t1.fivethous;

                                                                 QUERY PLAN
-------------------------------------------------------------------​-------------------------------------------------------------------​------
 Sort  (cost=713.05..713.30 rows=100 width=488) (actual time=2.995..3.002 rows=100.00 loops=1)
   Sort Key: t1.fivethous
   Sort Method: quicksort  Memory: 74kB
   Buffers: shared hit=440
   ->  Hash Join  (cost=226.23..709.73 rows=100 width=488) (actual time=0.515..2.920 rows=100.00 loops=1)
         Hash Cond: (t2.unique2 = t1.unique2)
         Buffers: shared hit=437
         ->  Seq Scan on tenk2 t2  (cost=0.00..445.00 rows=10000 width=244) (actual time=0.026..1.790 rows=10000.00 loops=1)
               Buffers: shared hit=345
         ->  Hash  (cost=224.98..224.98 rows=100 width=244) (actual time=0.476..0.477 rows=100.00 loops=1)
               Buckets: 1024  Batches: 1  Memory Usage: 35kB
               Buffers: shared hit=92
               ->  Bitmap Heap Scan on tenk1 t1  (cost=5.06..224.98 rows=100 width=244) (actual time=0.030..0.450 rows=100.00 loops=1)
                     Recheck Cond: (unique1 < 100)
                     Heap Blocks: exact=90
                     Buffers: shared hit=92
                     ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.013..0.013 rows=100.00 loops=1)
                           Index Cond: (unique1 < 100)
                           Index Searches: 1
                           Buffers: shared hit=2
 Planning:
   Buffers: shared hit=12
 Planning Time: 0.187 ms
 Execution Time: 3.036 ms
```

The Sort node shows the sort method used (in particular, whether the sort
was in-memory or on-disk) and the amount of memory or disk space needed.
The Hash node shows the number of hash buckets and batches as well as the
peak amount of memory used for the hash table. (If the number of batches
exceeds one, there will also be disk space usage involved, but that is not
shown.)

Index Scan nodes (as well as Bitmap Index Scan and Index-Only Scan nodes)
show an “Index Searches” line that reports the total number
of searches across *all* node
executions/`loops`:

```

EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE thousand IN (1, 500, 700, 999);
                                                            QUERY PLAN
-------------------------------------------------------------------​---------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=9.45..73.44 rows=40 width=244) (actual time=0.012..0.028 rows=40.00 loops=1)
   Recheck Cond: (thousand = ANY ('{1,500,700,999}'::integer[]))
   Heap Blocks: exact=39
   Buffers: shared hit=47
   ->  Bitmap Index Scan on tenk1_thous_tenthous  (cost=0.00..9.44 rows=40 width=0) (actual time=0.009..0.009 rows=40.00 loops=1)
         Index Cond: (thousand = ANY ('{1,500,700,999}'::integer[]))
         Index Searches: 4
         Buffers: shared hit=8
 Planning Time: 0.029 ms
 Execution Time: 0.034 ms
```

Here we see a Bitmap Index Scan node that needed 4 separate index
searches. The scan had to search the index from the
`tenk1_thous_tenthous` index root page once per
`integer` value from the predicate's `IN`
construct. However, the number of index searches often won't have such a
simple correspondence to the query predicate:

```

EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE thousand IN (1, 2, 3, 4);
                                                            QUERY PLAN
-------------------------------------------------------------------​---------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=9.45..73.44 rows=40 width=244) (actual time=0.009..0.019 rows=40.00 loops=1)
   Recheck Cond: (thousand = ANY ('{1,2,3,4}'::integer[]))
   Heap Blocks: exact=38
   Buffers: shared hit=40
   ->  Bitmap Index Scan on tenk1_thous_tenthous  (cost=0.00..9.44 rows=40 width=0) (actual time=0.005..0.005 rows=40.00 loops=1)
         Index Cond: (thousand = ANY ('{1,2,3,4}'::integer[]))
         Index Searches: 1
         Buffers: shared hit=2
 Planning Time: 0.029 ms
 Execution Time: 0.026 ms
```

This variant of our `IN` query performed only 1 index
search. It spent less time traversing the index (compared to the original
query) because its `IN` construct uses values matching
index tuples stored next to each other, on the same
`tenk1_thous_tenthous` index leaf page.

The “Index Searches” line is also useful with B-tree index
scans that apply the *skip scan* optimization to
more efficiently traverse through an index:

```

EXPLAIN ANALYZE SELECT four, unique1 FROM tenk1 WHERE four BETWEEN 1 AND 3 AND unique1 = 42;
                                                              QUERY PLAN
-------------------------------------------------------------------​---------------------------------------------------------------
 Index Only Scan using tenk1_four_unique1_idx on tenk1  (cost=0.29..6.90 rows=1 width=8) (actual time=0.006..0.007 rows=1.00 loops=1)
   Index Cond: ((four >= 1) AND (four <= 3) AND (unique1 = 42))
   Heap Fetches: 0
   Index Searches: 3
   Buffers: shared hit=7
 Planning Time: 0.029 ms
 Execution Time: 0.012 ms
```

Here we see an Index-Only Scan node using
`tenk1_four_unique1_idx`, a multi-column index on the
`tenk1` table's `four` and
`unique1` columns. The scan performs 3 searches
that each read a single index leaf page:
“`four = 1 AND unique1 = 42`”,
“`four = 2 AND unique1 = 42`”, and
“`four = 3 AND unique1 = 42`”. This index
is generally a good target for skip scan, since, as discussed in
[Section 11.3](../indexes/indexes-multicolumn.md), its leading column (the
`four` column) contains only 4 distinct values,
while its second/final column (the `unique1`
column) contains many distinct values.

Another type of extra information is the number of rows removed by a
filter condition:

```

EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE ten < 7;

                                               QUERY PLAN
-------------------------------------------------------------------​--------------------------------------
 Seq Scan on tenk1  (cost=0.00..470.00 rows=7000 width=244) (actual time=0.030..1.995 rows=7000.00 loops=1)
   Filter: (ten < 7)
   Rows Removed by Filter: 3000
   Buffers: shared hit=345
 Planning Time: 0.102 ms
 Execution Time: 2.145 ms
```

These counts can be particularly valuable for filter conditions applied at
join nodes. The “Rows Removed” line only appears when at least
one scanned row, or potential join pair in the case of a join node,
is rejected by the filter condition.

A case similar to filter conditions occurs with “lossy”
index scans. For example, consider this search for polygons containing a
specific point:

```

EXPLAIN ANALYZE SELECT * FROM polygon_tbl WHERE f1 @> polygon '(0.5,2.0)';

                                              QUERY PLAN
-------------------------------------------------------------------​-----------------------------------
 Seq Scan on polygon_tbl  (cost=0.00..1.09 rows=1 width=85) (actual time=0.023..0.023 rows=0.00 loops=1)
   Filter: (f1 @> '((0.5,2))'::polygon)
   Rows Removed by Filter: 7
   Buffers: shared hit=1
 Planning Time: 0.039 ms
 Execution Time: 0.033 ms
```

The planner thinks (quite correctly) that this sample table is too small
to bother with an index scan, so we have a plain sequential scan in which
all the rows got rejected by the filter condition. But if we force an
index scan to be used, we see:

```

SET enable_seqscan TO off;

EXPLAIN ANALYZE SELECT * FROM polygon_tbl WHERE f1 @> polygon '(0.5,2.0)';

                                                        QUERY PLAN
-------------------------------------------------------------------​-------------------------------------------------------
 Index Scan using gpolygonind on polygon_tbl  (cost=0.13..8.15 rows=1 width=85) (actual time=0.074..0.074 rows=0.00 loops=1)
   Index Cond: (f1 @> '((0.5,2))'::polygon)
   Rows Removed by Index Recheck: 1
   Index Searches: 1
   Buffers: shared hit=1
 Planning Time: 0.039 ms
 Execution Time: 0.098 ms
```

Here we can see that the index returned one candidate row, which was
then rejected by a recheck of the index condition. This happens because a
GiST index is “lossy” for polygon containment tests: it actually
returns the rows with polygons that overlap the target, and then we have
to do the exact containment test on those rows.

`EXPLAIN` has a `BUFFERS` option which
provides additional detail about I/O operations performed during the
planning and execution of the given query. The buffer numbers displayed
show the count of the non-distinct buffers hit, read, dirtied, and written
for the given node and all of its child nodes. The
`ANALYZE` option implicitly enables the
`BUFFERS` option. If this
is undesired, `BUFFERS` may be explicitly disabled:

```

EXPLAIN (ANALYZE, BUFFERS OFF) SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000;

                                                           QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=25.07..60.11 rows=10 width=244) (actual time=0.105..0.114 rows=10.00 loops=1)
   Recheck Cond: ((unique1 < 100) AND (unique2 > 9000))
   Heap Blocks: exact=10
   ->  BitmapAnd  (cost=25.07..25.07 rows=10 width=0) (actual time=0.100..0.101 rows=0.00 loops=1)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.027..0.027 rows=100.00 loops=1)
               Index Cond: (unique1 < 100)
               Index Searches: 1
         ->  Bitmap Index Scan on tenk1_unique2  (cost=0.00..19.78 rows=999 width=0) (actual time=0.070..0.070 rows=999.00 loops=1)
               Index Cond: (unique2 > 9000)
               Index Searches: 1
 Planning Time: 0.162 ms
 Execution Time: 0.143 ms
```

Keep in mind that because `EXPLAIN ANALYZE` actually
runs the query, any side-effects will happen as usual, even though
whatever results the query might output are discarded in favor of
printing the `EXPLAIN` data. If you want to analyze a
data-modifying query without changing your tables, you can
roll the command back afterwards, for example:

```

BEGIN;

EXPLAIN ANALYZE UPDATE tenk1 SET hundred = hundred + 1 WHERE unique1 < 100;

                                                           QUERY PLAN
-------------------------------------------------------------------​-------------------------------------------------------------
 Update on tenk1  (cost=5.06..225.23 rows=0 width=0) (actual time=1.634..1.635 rows=0.00 loops=1)
   ->  Bitmap Heap Scan on tenk1  (cost=5.06..225.23 rows=100 width=10) (actual time=0.065..0.141 rows=100.00 loops=1)
         Recheck Cond: (unique1 < 100)
         Heap Blocks: exact=90
         Buffers: shared hit=4 read=2
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.031..0.031 rows=100.00 loops=1)
               Index Cond: (unique1 < 100)
               Index Searches: 1
               Buffers: shared read=2
 Planning Time: 0.151 ms
 Execution Time: 1.856 ms

ROLLBACK;
```

As seen in this example, when the query is an `INSERT`,
`UPDATE`, `DELETE`, or
`MERGE` command, the actual work of
applying the table changes is done by a top-level Insert, Update,
Delete, or Merge plan node. The plan nodes underneath this node perform
the work of locating the old rows and/or computing the new data.
So above, we see the same sort of bitmap table scan we've seen already,
and its output is fed to an Update node that stores the updated rows.
It's worth noting that although the data-modifying node can take a
considerable amount of run time (here, it's consuming the lion's share
of the time), the planner does not currently add anything to the cost
estimates to account for that work. That's because the work to be done is
the same for every correct query plan, so it doesn't affect planning
decisions.

When an `UPDATE`, `DELETE`, or
`MERGE` command affects a partitioned table or
inheritance hierarchy, the output might look like this:

```

EXPLAIN UPDATE gtest_parent SET f1 = CURRENT_DATE WHERE f2 = 101;

                                       QUERY PLAN
-------------------------------------------------------------------​---------------------
 Update on gtest_parent  (cost=0.00..3.06 rows=0 width=0)
   Update on gtest_child gtest_parent_1
   Update on gtest_child2 gtest_parent_2
   Update on gtest_child3 gtest_parent_3
   ->  Append  (cost=0.00..3.06 rows=3 width=14)
         ->  Seq Scan on gtest_child gtest_parent_1  (cost=0.00..1.01 rows=1 width=14)
               Filter: (f2 = 101)
         ->  Seq Scan on gtest_child2 gtest_parent_2  (cost=0.00..1.01 rows=1 width=14)
               Filter: (f2 = 101)
         ->  Seq Scan on gtest_child3 gtest_parent_3  (cost=0.00..1.01 rows=1 width=14)
               Filter: (f2 = 101)
```

In this example the Update node needs to consider three child tables,
but not the originally-mentioned partitioned table (since that never
stores any data). So there are three input
scanning subplans, one per table. For clarity, the Update node is
annotated to show the specific target tables that will be updated, in the
same order as the corresponding subplans.

The `Planning time` shown by `EXPLAIN
ANALYZE` is the time it took to generate the query plan from the
parsed query and optimize it. It does not include parsing or rewriting.

The `Execution time` shown by `EXPLAIN
ANALYZE` includes executor start-up and shut-down time, as well
as the time to run any triggers that are fired, but it does not include
parsing, rewriting, or planning time.
Time spent executing `BEFORE` triggers, if any, is included in
the time for the related Insert, Update, or Delete node; but time
spent executing `AFTER` triggers is not counted there because
`AFTER` triggers are fired after completion of the whole plan.
The total time spent in each trigger
(either `BEFORE` or `AFTER`) is also shown separately.
Note that deferred constraint triggers will not be executed
until end of transaction and are thus not considered at all by
`EXPLAIN ANALYZE`.

The time shown for the top-level node does not include any time needed
to convert the query's output data into displayable form or to send it
to the client. While `EXPLAIN ANALYZE` will never
send the data to the client, it can be told to convert the query's
output data to displayable form and measure the time needed for that,
by specifying the `SERIALIZE` option. That time will
be shown separately, and it's also included in the
total `Execution time`.

<a id="USING-EXPLAIN-CAVEATS"></a>

### 14.1.3. Caveats [#](#USING-EXPLAIN-CAVEATS)

There are two significant ways in which run times measured by
`EXPLAIN ANALYZE` can deviate from normal execution of
the same query. First, since no output rows are delivered to the client,
network transmission costs are not included. I/O conversion costs are
not included either unless `SERIALIZE` is specified.
Second, the measurement overhead added by `EXPLAIN
ANALYZE` can be significant, especially on machines with slow
`gettimeofday()` operating-system calls. You can use the
[pg_test_timing](../../reference/reference-server/pgtesttiming.md) tool to measure the overhead of timing
on your system.

`EXPLAIN` results should not be extrapolated to situations
much different from the one you are actually testing; for example,
results on a toy-sized table cannot be assumed to apply to large tables.
The planner's cost estimates are not linear and so it might choose
a different plan for a larger or smaller table. An extreme example
is that on a table that only occupies one disk page, you'll nearly
always get a sequential scan plan whether indexes are available or not.
The planner realizes that it's going to take one disk page read to
process the table in any case, so there's no value in expending additional
page reads to look at an index. (We saw this happening in the
`polygon_tbl` example above.)

There are cases in which the actual and estimated values won't match up
well, but nothing is really wrong. One such case occurs when
plan node execution is stopped short by a `LIMIT` or similar
effect. For example, in the `LIMIT` query we used before,

```

EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000 LIMIT 2;

                                                          QUERY PLAN
-------------------------------------------------------------------​------------------------------------------------------------
 Limit  (cost=0.29..14.33 rows=2 width=244) (actual time=0.051..0.071 rows=2.00 loops=1)
   Buffers: shared hit=16
   ->  Index Scan using tenk1_unique2 on tenk1  (cost=0.29..70.50 rows=10 width=244) (actual time=0.051..0.070 rows=2.00 loops=1)
         Index Cond: (unique2 > 9000)
         Filter: (unique1 < 100)
         Rows Removed by Filter: 287
         Index Searches: 1
         Buffers: shared hit=16
 Planning Time: 0.077 ms
 Execution Time: 0.086 ms
```

the estimated cost and row count for the Index Scan node are shown as
though it were run to completion. But in reality the Limit node stopped
requesting rows after it got two, so the actual row count is only 2 and
the run time is less than the cost estimate would suggest. This is not
an estimation error, only a discrepancy in the way the estimates and true
values are displayed.

Merge joins also have measurement artifacts that can confuse the unwary.
A merge join will stop reading one input if it's exhausted the other input
and the next key value in the one input is greater than the last key value
of the other input; in such a case there can be no more matches and so no
need to scan the rest of the first input. This results in not reading all
of one child, with results like those mentioned for `LIMIT`.
Also, if the outer (first) child contains rows with duplicate key values,
the inner (second) child is backed up and rescanned for the portion of its
rows matching that key value. `EXPLAIN ANALYZE` counts these
repeated emissions of the same inner rows as if they were real additional
rows. When there are many outer duplicates, the reported actual row count
for the inner child plan node can be significantly larger than the number
of rows that are actually in the inner relation.

BitmapAnd and BitmapOr nodes always report their actual row counts as zero,
due to implementation limitations.

Normally, `EXPLAIN` will display every plan node
created by the planner. However, there are cases where the executor
can determine that certain nodes need not be executed because they
cannot produce any rows, based on parameter values that were not
available at planning time. (Currently this can only happen for child
nodes of an Append or MergeAppend node that is scanning a partitioned
table.) When this happens, those plan nodes are omitted from
the `EXPLAIN` output and a `Subplans
Removed: N` annotation appears
instead.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/using-explain.html)（英文原文，待翻譯）
