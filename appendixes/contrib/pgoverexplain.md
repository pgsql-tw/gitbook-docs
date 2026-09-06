## F.29. pg_overexplain — allow EXPLAIN to dump even more details [#](#PGOVEREXPLAIN)

[F.29.1. EXPLAIN (DEBUG)](pgoverexplain.md#PGOVEREXPLAIN-DEBUG)

[F.29.2. EXPLAIN (RANGE_TABLE)](pgoverexplain.md#PGOVEREXPLAIN-RANGE-TABLE)

[F.29.3. Author](pgoverexplain.md#PGOVEREXPLAIN-AUTHOR)

<a id="id-1.11.7.39.2"></a>

The `pg_overexplain` module extends `EXPLAIN`
with new options that provide additional output. It is mostly intended to
assist with debugging of and development of the planner, rather than for
general use. Since this module displays internal details of planner data
structures, it may be necessary to refer to the source code to make sense
of the output. Furthermore, the output is likely to change whenever (and as
often as) those data structures change.

To use it, simply load it into the server. You can load it into an
individual session:

```

LOAD 'pg_overexplain';
```

You can also preload it into some or all sessions by including
`pg_overexplain` in
[session_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES) or
[shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) in
`postgresql.conf`.

<a id="PGOVEREXPLAIN-DEBUG"></a>

### F.29.1. EXPLAIN (DEBUG) [#](#PGOVEREXPLAIN-DEBUG)

The `DEBUG` option displays miscellaneous information from
the plan tree that is not normally shown because it is not expected to be
of general interest. For each individual plan node, it will display the
following fields. See `Plan` in
`nodes/plannodes.h` for additional documentation of these
fields.

* `Disabled Nodes`. Normal `EXPLAIN`
  determines whether a node is disabled by checking whether the node's
  count of disabled nodes is larger than the sum of the counts for the
  underlying nodes. This option shows the raw counter value.
* `Parallel Safe`. Indicates whether it would be safe for
  a plan tree node to appear beneath a `Gather` or
  `Gather Merge` node, regardless of whether it is
  actually below such a node.
* `Plan Node ID`. An internal ID number that should be
  unique for every node in the plan tree. It is used to coordinate parallel
  query activity.
* `extParam` and `allParam`. Information
  about which numbered parameters affect this plan node or its children. In
  text mode, these fields are only displayed if they are non-empty sets.

Once per query, the `DEBUG` option will display the
following fields. See `PlannedStmt` in
`nodes/plannodes.h` for additional detail.

* `Command Type`. For example, `select`
  or `update`.
* `Flags`. A comma-separated list of Boolean structure
  member names from the `PlannedStmt` that are set to
  `true`. It covers the following structure members:
  `hasReturning`, `hasModifyingCTE`,
  `canSetTag`, `transientPlan`,
  `dependsOnRole`, `parallelModeNeeded`.
* `Subplans Needing Rewind`. Integer IDs of subplans that
  may need to be rewound by the executor.
* `Relation OIDs`. OIDs of relations upon which this plan
  depends.
* `Executor Parameter Types`. Type OID for each executor parameter
  (e.g. when a nested loop is chosen and a parameter is used to pass a value down
  to an inner index scan). Does not include parameters supplied to a prepared
  statement by the user.
* `Parse Location`. Location within the query string
  supplied to the planner where this query's text can be found. May be
  `Unknown` in some contexts. Otherwise, may be
  `NNN to end` for some integer `NNN` or
  `NNN for MMM bytes` for some integers
  `NNN` and `MMM`.

<a id="PGOVEREXPLAIN-RANGE-TABLE"></a>

### F.29.2. EXPLAIN (RANGE_TABLE) [#](#PGOVEREXPLAIN-RANGE-TABLE)

The `RANGE_TABLE` option displays information from the
plan tree specifically concerning the query's range table. Range table
entries correspond roughly to items appearing in the query's
`FROM` clause, but with numerous exceptions. For example,
subqueries that are proved unnecessary may be deleted from the range table
entirely, while inheritance expansion adds range table entries for child
tables that are not named directly in the query.

Range table entries are generally referenced within the query plan by a
range table index, or RTI. Plan nodes that reference one or more RTIs will
be labelled accordingly, using one of the following fields: `Scan
RTI`, `Nominal RTI`, `Exclude Relation
RTI`, `Append RTIs`.

In addition, the query as a whole may maintain lists of range table indexes
that are needed for various purposes. These lists will be displayed once
per query, labelled as appropriate as `Unprunable RTIs` or
`Result RTIs`. In text mode, these fields are only
displayed if they are non-empty sets.

Finally, but most importantly, the `RANGE_TABLE` option
will display a dump of the query's entire range table. Each range table
entry is labelled with the appropriate range table index, the kind of range
table entry (e.g. `relation`,
`subquery`, or `join`), followed by the
contents of various range table entry fields that are not normally part of
`EXPLAIN` output. Some of these fields are only displayed
for certain kinds of range table entries. For example,
`Eref` is displayed for all types of range table entries,
but `CTE Name` is displayed only for range table entries
of type `cte`.

For more information about range table entries, see the definition of
`RangeTblEntry` in `nodes/parsenodes.h`.

<a id="PGOVEREXPLAIN-AUTHOR"></a>

### F.29.3. Author [#](#PGOVEREXPLAIN-AUTHOR)

Robert Haas `<rhaas@postgresql.org>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgoverexplain.html)（英文原文，待翻譯）
