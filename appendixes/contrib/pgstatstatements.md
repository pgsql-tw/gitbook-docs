## F.32. pg_stat_statements — track statistics of SQL planning and execution [#](#PGSTATSTATEMENTS)

[F.32.1. The `pg_stat_statements` View](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)

[F.32.2. The `pg_stat_statements_info` View](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO)

[F.32.3. Functions](pgstatstatements.md#PGSTATSTATEMENTS-FUNCS)

[F.32.4. Configuration Parameters](pgstatstatements.md#PGSTATSTATEMENTS-CONFIG-PARAMS)

[F.32.5. Sample Output](pgstatstatements.md#PGSTATSTATEMENTS-SAMPLE-OUTPUT)

[F.32.6. Authors](pgstatstatements.md#PGSTATSTATEMENTS-AUTHORS)

<a id="id-1.11.7.42.2"></a>

The `pg_stat_statements` module provides a means for
tracking planning and execution statistics of all SQL statements executed by
a server.

The module must be loaded by adding `pg_stat_statements` to
[shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) in
`postgresql.conf`, because it requires additional shared memory.
This means that a server restart is needed to add or remove the module.
In addition, query identifier calculation must be enabled in order for the
module to be active, which is done automatically if [compute_query_id](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID)
is set to `auto` or `on`, or any third-party
module that calculates query identifiers is loaded.

When `pg_stat_statements` is active, it tracks
statistics across all databases of the server. To access and manipulate
these statistics, the module provides views
`pg_stat_statements` and
`pg_stat_statements_info`,
and the utility functions `pg_stat_statements_reset` and
`pg_stat_statements`. These are not available globally but
can be enabled for a specific database with
`CREATE EXTENSION pg_stat_statements`.

<a id="PGSTATSTATEMENTS-PG-STAT-STATEMENTS"></a>

### F.32.1. The `pg_stat_statements` View [#](#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)

The statistics gathered by the module are made available via a
view named `pg_stat_statements`. This view
contains one row for each distinct combination of database ID, user
ID, query ID and whether it's a top-level statement or not (up to
the maximum number of distinct statements that the module can track).
The columns of the view are shown in
[Table F.22](pgstatstatements.md#PGSTATSTATEMENTS-COLUMNS).

<a id="PGSTATSTATEMENTS-COLUMNS"></a>

**Table F.22. `pg_stat_statements` Columns**

<table border="1" class="table" summary="pg_stat_statements Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">userid</code> <code class="type">oid</code>
       (references <a class="link" href="../../internals/catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of user who executed the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dbid</code> <code class="type">oid</code>
       (references <a class="link" href="../../internals/catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of database in which the statement was executed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">toplevel</code> <code class="type">bool</code>
</p>
<p>
       True if the query was executed as a top-level statement
       (always true if <code class="varname">pg_stat_statements.track</code> is set to
       <code class="literal">top</code>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">queryid</code> <code class="type">bigint</code>
</p>
<p>
       Hash code to identify identical normalized queries.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">query</code> <code class="type">text</code>
</p>
<p>
       Text of a representative statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">plans</code> <code class="type">bigint</code>
</p>
<p>
       Number of times the statement was planned
       (if <code class="varname">pg_stat_statements.track_planning</code> is enabled,
       otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_plan_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent planning the statement, in milliseconds
       (if <code class="varname">pg_stat_statements.track_planning</code> is enabled,
       otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">min_plan_time</code> <code class="type">double precision</code>
</p>
<p>
       Minimum time spent planning the statement, in milliseconds.
       This field will be zero if <code class="varname">pg_stat_statements.track_planning</code>
       is disabled, or if the counter has been reset using the
       <code class="function">pg_stat_statements_reset</code> function with the
       <code class="structfield">minmax_only</code> parameter set to <code class="literal">true</code>
       and never been planned since.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_plan_time</code> <code class="type">double precision</code>
</p>
<p>
       Maximum time spent planning the statement, in milliseconds.
       This field will be zero if <code class="varname">pg_stat_statements.track_planning</code>
       is disabled, or if the counter has been reset using the
       <code class="function">pg_stat_statements_reset</code> function with the
       <code class="structfield">minmax_only</code> parameter set to <code class="literal">true</code>
       and never been planned since.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">mean_plan_time</code> <code class="type">double precision</code>
</p>
<p>
       Mean time spent planning the statement, in milliseconds
       (if <code class="varname">pg_stat_statements.track_planning</code> is enabled,
       otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stddev_plan_time</code> <code class="type">double precision</code>
</p>
<p>
       Population standard deviation of time spent planning the statement,
       in milliseconds
       (if <code class="varname">pg_stat_statements.track_planning</code> is enabled,
       otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">calls</code> <code class="type">bigint</code>
</p>
<p>
       Number of times the statement was executed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_exec_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent executing the statement, in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">min_exec_time</code> <code class="type">double precision</code>
</p>
<p>
       Minimum time spent executing the statement, in milliseconds,
       this field will be zero until this statement
       is executed first time after reset performed by the
       <code class="function">pg_stat_statements_reset</code> function with the
       <code class="structfield">minmax_only</code> parameter set to <code class="literal">true</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_exec_time</code> <code class="type">double precision</code>
</p>
<p>
       Maximum time spent executing the statement, in milliseconds,
       this field will be zero until this statement
       is executed first time after reset performed by the
       <code class="function">pg_stat_statements_reset</code> function with the
       <code class="structfield">minmax_only</code> parameter set to <code class="literal">true</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">mean_exec_time</code> <code class="type">double precision</code>
</p>
<p>
       Mean time spent executing the statement, in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stddev_exec_time</code> <code class="type">double precision</code>
</p>
<p>
       Population standard deviation of time spent executing the statement, in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rows</code> <code class="type">bigint</code>
</p>
<p>
       Total number of rows retrieved or affected by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       Total number of shared block cache hits by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Total number of shared blocks read by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blks_dirtied</code> <code class="type">bigint</code>
</p>
<p>
       Total number of shared blocks dirtied by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blks_written</code> <code class="type">bigint</code>
</p>
<p>
       Total number of shared blocks written by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       Total number of local block cache hits by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Total number of local blocks read by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blks_dirtied</code> <code class="type">bigint</code>
</p>
<p>
       Total number of local blocks dirtied by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blks_written</code> <code class="type">bigint</code>
</p>
<p>
       Total number of local blocks written by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Total number of temp blocks read by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_blks_written</code> <code class="type">bigint</code>
</p>
<p>
       Total number of temp blocks written by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blk_read_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time the statement spent reading shared blocks, in milliseconds
       (if <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled, otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time the statement spent writing shared blocks, in milliseconds
       (if <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled, otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blk_read_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time the statement spent reading local blocks, in milliseconds
       (if <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled, otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time the statement spent writing local blocks, in milliseconds
       (if <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled, otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_blk_read_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time the statement spent reading temporary file blocks, in
       milliseconds (if <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled,
       otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time the statement spent writing temporary file blocks, in
       milliseconds (if <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled,
       otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_records</code> <code class="type">bigint</code>
</p>
<p>
       Total number of WAL records generated by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_fpi</code> <code class="type">bigint</code>
</p>
<p>
       Total number of WAL full page images generated by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_bytes</code> <code class="type">numeric</code>
</p>
<p>
       Total amount of WAL generated by the statement in bytes
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_buffers_full</code> <code class="type">bigint</code>
</p>
<p>
       Number of times the WAL buffers became full
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_functions</code> <code class="type">bigint</code>
</p>
<p>
       Total number of functions JIT-compiled by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_generation_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent by the statement on generating JIT code, in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_inlining_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of times functions have been inlined
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_inlining_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent by the statement on inlining functions, in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_optimization_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of times the statement has been optimized
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_optimization_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent by the statement on optimizing, in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_emission_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of times code has been emitted
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_emission_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent by the statement on emitting code, in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_deform_count</code> <code class="type">bigint</code>
</p>
<p>
       Total number of tuple deform functions JIT-compiled by the statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_deform_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent by the statement on JIT-compiling tuple deform
       functions, in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parallel_workers_to_launch</code> <code class="type">bigint</code>
</p>
<p>
       Number of parallel workers planned to be launched
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parallel_workers_launched</code> <code class="type">bigint</code>
</p>
<p>
       Number of parallel workers actually launched
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_since</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which statistics gathering started for this statement
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">minmax_stats_since</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which min/max statistics gathering started for this
       statement (fields <code class="structfield">min_plan_time</code>,
       <code class="structfield">max_plan_time</code>,
       <code class="structfield">min_exec_time</code> and
       <code class="structfield">max_exec_time</code>)
      </p></td></tr></tbody></table>

<br>

For security reasons, only superusers and roles with privileges of the
`pg_read_all_stats` role are allowed to see the SQL text and
`queryid` of queries executed by other users.
Other users can see the statistics, however, if the view has been installed
in their database.

Plannable queries (that is, `SELECT`, `INSERT`,
`UPDATE`, `DELETE`, and `MERGE`)
and utility commands are combined into a single
`pg_stat_statements` entry whenever they have identical query
structures according to an internal hash calculation. Typically, two
queries will be considered the same for this purpose if they are
semantically equivalent except for the values of literal constants
appearing in the query.

### Note

The following details about constant replacement and
`queryid` only apply when [compute_query_id](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID) is enabled. If you use an external
module instead to compute `queryid`, you
should refer to its documentation for details.

When a constant's value has been ignored for purposes of matching the query
to other queries, the constant is replaced by a parameter symbol, such
as `$1`, in the `pg_stat_statements`
display.
The rest of the query text is that of the first query that had the
particular `queryid` hash value associated with the
`pg_stat_statements` entry.

Queries on which normalization can be applied may be observed with constant
values in `pg_stat_statements`, especially when there
is a high rate of entry deallocations. To reduce the likelihood of this
happening, consider increasing `pg_stat_statements.max`.
The `pg_stat_statements_info` view, discussed below
in [Section F.32.2](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO),
provides statistics about entry deallocations.

In some cases, queries with visibly different texts might get merged into a
single `pg_stat_statements` entry; as explained above,
this is expected to happen for semantically equivalent queries.
In addition, if the only difference between queries is the number of elements
in a list of constants, the list will get squashed down to a single element but shown
with a commented-out list indicator:

```

=# SELECT pg_stat_statements_reset();
=# SELECT * FROM test WHERE a IN (1, 2, 3, 4, 5, 6, 7);
=# SELECT * FROM test WHERE a IN (1, 2, 3, 4, 5, 6, 7, 8);
=# SELECT query, calls FROM pg_stat_statements
   WHERE query LIKE 'SELECT%';
-[ RECORD 1 ]------------------------------
query | SELECT * FROM test WHERE a IN ($1 /*, ... */)
calls | 2
```

In addition to these cases, there is a small chance of hash collisions
causing unrelated queries to be merged into one entry.
(This cannot happen for queries belonging to different users or databases,
however.)

Since the `queryid` hash value is computed on the
post-parse-analysis representation of the queries, the opposite is
also possible: queries with identical texts might appear as
separate entries, if they have different meanings as a result of
factors such as different `search_path` settings.

Consumers of `pg_stat_statements` may wish to use
`queryid` (perhaps in combination with
`dbid` and `userid`) as a more stable
and reliable identifier for each entry than its query text.
However, it is important to understand that there are only limited
guarantees around the stability of the `queryid` hash
value. Since the identifier is derived from the
post-parse-analysis tree, its value is a function of, among other
things, the internal object identifiers appearing in this representation.
This has some counterintuitive implications. For example,
`pg_stat_statements` will consider two apparently-identical
queries to be distinct, if they reference for example a function that was
dropped and recreated between the executions of the two queries.
Conversely, if a table is dropped and recreated between the
executions of queries, two apparently-identical queries may be
considered the same. However, if the alias for a table is different
for otherwise-similar queries, these queries will be considered
distinct.
The hashing process is also sensitive to differences in
machine architecture and other facets of the platform.
Furthermore, it is not safe to assume that `queryid`
will be stable across major versions of PostgreSQL.

Two servers participating in replication based on physical WAL replay can
be expected to have identical `queryid` values for
the same query. However, logical replication schemes do not promise to
keep replicas identical in all relevant details, so
`queryid` will not be a useful identifier for
accumulating costs across a set of logical replicas.
If in doubt, direct testing is recommended.

Generally, it can be assumed that `queryid` values
are stable between minor version releases of PostgreSQL,
providing that instances are running on the same machine architecture and
the catalog metadata details match. Compatibility will only be broken
between minor versions as a last resort.

The parameter symbols used to replace constants in
representative query texts start from the next number after the
highest `$`*`n`* parameter in the original query
text, or `$1` if there was none. It's worth noting that in
some cases there may be hidden parameter symbols that affect this
numbering. For example, PL/pgSQL uses hidden parameter
symbols to insert values of function local variables into queries, so that
a PL/pgSQL statement like `SELECT i + 1 INTO j`
would have representative text like `SELECT i + $2`.

The representative query texts are kept in an external disk file, and do
not consume shared memory. Therefore, even very lengthy query texts can
be stored successfully. However, if many long query texts are
accumulated, the external file might grow unmanageably large. As a
recovery method if that happens, `pg_stat_statements` may
choose to discard the query texts, whereupon all existing entries in
the `pg_stat_statements` view will show
null `query` fields, though the statistics associated with
each `queryid` are preserved. If this happens, consider
reducing `pg_stat_statements.max` to prevent
recurrences.

`plans` and `calls` aren't
always expected to match because planning and execution statistics are
updated at their respective end phase, and only for successful operations.
For example, if a statement is successfully planned but fails during
the execution phase, only its planning statistics will be updated.
If planning is skipped because a cached plan is used, only its execution
statistics will be updated.

<a id="PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO"></a>

### F.32.2. The `pg_stat_statements_info` View [#](#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO)

<a id="id-1.11.7.42.7.2"></a>

The statistics of the `pg_stat_statements` module
itself are tracked and made available via a view named
`pg_stat_statements_info`. This view contains
only a single row. The columns of the view are shown in
[Table F.23](pgstatstatements.md#PGSTATSTATEMENTSINFO-COLUMNS).

<a id="PGSTATSTATEMENTSINFO-COLUMNS"></a>

**Table F.23. `pg_stat_statements_info` Columns**

<table border="1" class="table" summary="pg_stat_statements_info Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dealloc</code> <code class="type">bigint</code>
</p>
<p>
       Total number of times <code class="structname">pg_stat_statements</code>
       entries about the least-executed statements were deallocated
       because more distinct statements than
       <code class="varname">pg_stat_statements.max</code> were observed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which all statistics in the
       <code class="structname">pg_stat_statements</code> view were last reset.
      </p></td></tr></tbody></table>

<br>

<a id="PGSTATSTATEMENTS-FUNCS"></a>

### F.32.3. Functions [#](#PGSTATSTATEMENTS-FUNCS)

`pg_stat_statements_reset(userid Oid, dbid Oid, queryid bigint, minmax_only boolean) returns timestamp with time zone` <a id="id-1.11.7.42.8.2.1.1.2"></a>
:   `pg_stat_statements_reset` discards statistics
    gathered so far by `pg_stat_statements` corresponding
    to the specified `userid`, `dbid`
    and `queryid`. If any of the parameters are not
    specified, the default value `0`(invalid) is used for
    each of them and the statistics that match with other parameters will be
    reset. If no parameter is specified or all the specified parameters are
    `0`(invalid), it will discard all statistics.
    If all statistics in the `pg_stat_statements`
    view are discarded, it will also reset the statistics in the
    `pg_stat_statements_info` view.
    When `minmax_only` is `true` only the
    values of minimum and maximum planning and execution time will be reset (i.e.
    `min_plan_time`, `max_plan_time`,
    `min_exec_time` and `max_exec_time`
    fields). The default value for `minmax_only` parameter is
    `false`. Time of last min/max reset performed is shown in
    `minmax_stats_since` field of the
    `pg_stat_statements` view.
    This function returns the time of a reset. This time is saved to
    `stats_reset` field of
    `pg_stat_statements_info` view or to
    `minmax_stats_since` field of the
    `pg_stat_statements` view if the corresponding reset was
    actually performed.
    By default, this function can only be executed by superusers.
    Access may be granted to others using `GRANT`.

`pg_stat_statements(showtext boolean) returns setof record` <a id="id-1.11.7.42.8.2.2.1.2"></a>
:   The `pg_stat_statements` view is defined in
    terms of a function also named `pg_stat_statements`.
    It is possible for clients to call
    the `pg_stat_statements` function directly, and by
    specifying `showtext := false` have query text be
    omitted (that is, the `OUT` argument that corresponds
    to the view's `query` column will return nulls). This
    feature is intended to support external tools that might wish to avoid
    the overhead of repeatedly retrieving query texts of indeterminate
    length. Such tools can instead cache the first query text observed
    for each entry themselves, since that is
    all `pg_stat_statements` itself does, and then retrieve
    query texts only as needed. Since the server stores query texts in a
    file, this approach may reduce physical I/O for repeated examination
    of the `pg_stat_statements` data.

<a id="PGSTATSTATEMENTS-CONFIG-PARAMS"></a>

### F.32.4. Configuration Parameters [#](#PGSTATSTATEMENTS-CONFIG-PARAMS)

`pg_stat_statements.max` (`integer`) <a id="id-1.11.7.42.9.2.1.1.3"></a>
:   `pg_stat_statements.max` is the maximum number of
    statements tracked by the module (i.e., the maximum number of rows
    in the `pg_stat_statements` view). If more distinct
    statements than that are observed, information about the least-executed
    statements is discarded. The number of times such information was
    discarded can be seen in the
    `pg_stat_statements_info` view.
    The default value is 5000.
    This parameter can only be set at server start.

`pg_stat_statements.track` (`enum`) <a id="id-1.11.7.42.9.2.2.1.3"></a>
:   `pg_stat_statements.track` controls which statements
    are counted by the module.
    Specify `top` to track top-level statements (those issued
    directly by clients), `all` to also track nested statements
    (such as statements invoked within functions), or `none` to
    disable statement statistics collection.
    The default value is `top`.
    Only superusers can change this setting.

`pg_stat_statements.track_utility` (`boolean`) <a id="id-1.11.7.42.9.2.3.1.3"></a>
:   `pg_stat_statements.track_utility` controls whether
    utility commands are tracked by the module. Utility commands are
    all those other than `SELECT`, `INSERT`,
    `UPDATE`, `DELETE`, and `MERGE`.
    The default value is `on`.
    Only superusers can change this setting.

`pg_stat_statements.track_planning` (`boolean`) <a id="id-1.11.7.42.9.2.4.1.3"></a>
:   `pg_stat_statements.track_planning` controls whether
    planning operations and duration are tracked by the module.
    Enabling this parameter may incur a noticeable performance penalty,
    especially when statements with identical query structure are executed
    by many concurrent connections which compete to update a small number of
    `pg_stat_statements` entries.
    The default value is `off`.
    Only superusers can change this setting.

`pg_stat_statements.save` (`boolean`) <a id="id-1.11.7.42.9.2.5.1.3"></a>
:   `pg_stat_statements.save` specifies whether to
    save statement statistics across server shutdowns.
    If it is `off` then statistics are not saved at
    shutdown nor reloaded at server start.
    The default value is `on`.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.

The module requires additional shared memory proportional to
`pg_stat_statements.max`. Note that this
memory is consumed whenever the module is loaded, even if
`pg_stat_statements.track` is set to `none`.

These parameters must be set in `postgresql.conf`.
Typical usage might be:

```

# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'

compute_query_id = on
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

<a id="PGSTATSTATEMENTS-SAMPLE-OUTPUT"></a>

### F.32.5. Sample Output [#](#PGSTATSTATEMENTS-SAMPLE-OUTPUT)

```

bench=# SELECT pg_stat_statements_reset();

$ pgbench -i bench
$ pgbench -c10 -t300 bench

bench=# \x
bench=# SELECT query, calls, total_exec_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;
-[ RECORD 1 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_branches SET bbalance = bbalance + $1 WHERE bid = $2
calls           | 3000
total_exec_time | 25565.855387
rows            | 3000
hit_percent     | 100.0000000000000000
-[ RECORD 2 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_tellers SET tbalance = tbalance + $1 WHERE tid = $2
calls           | 3000
total_exec_time | 20756.669379
rows            | 3000
hit_percent     | 100.0000000000000000
-[ RECORD 3 ]---+--------------------------------------------------​------------------
query           | copy pgbench_accounts from stdin
calls           | 1
total_exec_time | 291.865911
rows            | 100000
hit_percent     | 100.0000000000000000
-[ RECORD 4 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_accounts SET abalance = abalance + $1 WHERE aid = $2
calls           | 3000
total_exec_time | 271.232977
rows            | 3000
hit_percent     | 98.8454011741682975
-[ RECORD 5 ]---+--------------------------------------------------​------------------
query           | alter table pgbench_accounts add primary key (aid)
calls           | 1
total_exec_time | 160.588563
rows            | 0
hit_percent     | 100.0000000000000000


bench=# SELECT pg_stat_statements_reset(0,0,s.queryid) FROM pg_stat_statements AS s
            WHERE s.query = 'UPDATE pgbench_branches SET bbalance = bbalance + $1 WHERE bid = $2';

bench=# SELECT query, calls, total_exec_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;
-[ RECORD 1 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_tellers SET tbalance = tbalance + $1 WHERE tid = $2
calls           | 3000
total_exec_time | 20756.669379
rows            | 3000
hit_percent     | 100.0000000000000000
-[ RECORD 2 ]---+--------------------------------------------------​------------------
query           | copy pgbench_accounts from stdin
calls           | 1
total_exec_time | 291.865911
rows            | 100000
hit_percent     | 100.0000000000000000
-[ RECORD 3 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_accounts SET abalance = abalance + $1 WHERE aid = $2
calls           | 3000
total_exec_time | 271.232977
rows            | 3000
hit_percent     | 98.8454011741682975
-[ RECORD 4 ]---+--------------------------------------------------​------------------
query           | alter table pgbench_accounts add primary key (aid)
calls           | 1
total_exec_time | 160.588563
rows            | 0
hit_percent     | 100.0000000000000000
-[ RECORD 5 ]---+--------------------------------------------------​------------------
query           | vacuum analyze pgbench_accounts
calls           | 1
total_exec_time | 136.448116
rows            | 0
hit_percent     | 99.9201915403032721

bench=# SELECT pg_stat_statements_reset(0,0,0);

bench=# SELECT query, calls, total_exec_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;
-[ RECORD 1 ]---+--------------------------------------------------​---------------------------
query           | SELECT pg_stat_statements_reset(0,0,0)
calls           | 1
total_exec_time | 0.189497
rows            | 1
hit_percent     |
-[ RECORD 2 ]---+--------------------------------------------------​---------------------------
query           | SELECT query, calls, total_exec_time, rows, $1 * shared_blks_hit /          +
                |                nullif(shared_blks_hit + shared_blks_read, $2) AS hit_percent+
                |           FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT $3
calls           | 0
total_exec_time | 0
rows            | 0
hit_percent     |
```

<a id="PGSTATSTATEMENTS-AUTHORS"></a>

### F.32.6. Authors [#](#PGSTATSTATEMENTS-AUTHORS)

Takahiro Itagaki `<itagaki.takahiro@oss.ntt.co.jp>`.
Query normalization added by Peter Geoghegan `<peter@2ndquadrant.com>`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgstatstatements.html)（英文原文，待翻譯）
