# F.29. pg\_stat\_statements

The `pg_stat_statements` module provides a means for tracking execution statistics of all SQL statements executed by a server.

The module must be loaded by adding `pg_stat_statements` to [shared\_preload\_libraries](https://www.postgresql.org/docs/12/runtime-config-client.html#GUC-SHARED-PRELOAD-LIBRARIES) in `postgresql.conf`, because it requires additional shared memory. This means that a server restart is needed to add or remove the module.

When `pg_stat_statements` is loaded, it tracks statistics across all databases of the server. To access and manipulate these statistics, the module provides a view, `pg_stat_statements`, and the utility functions `pg_stat_statements_reset` and `pg_stat_statements`. These are not available globally but can be enabled for a specific database with `CREATE EXTENSION pg_stat_statements`.

## F.29.1. The `pg_stat_statements` View

The statistics gathered by the module are made available via a view named `pg_stat_statements`. This view contains one row for each distinct database ID, user ID and query ID \(up to the maximum number of distinct statements that the module can track\). The columns of the view are shown in [Table F.21](https://www.postgresql.org/docs/12/pgstatstatements.html#PGSTATSTATEMENTS-COLUMNS).

#### **Table F.21. `pg_stat_statements` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `userid` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/12/catalog-pg-authid.html).oid | OID of user who executed the statement |
| `dbid` | `oid` | [`pg_database`](https://www.postgresql.org/docs/12/catalog-pg-database.html).oid | OID of database in which the statement was executed |
| `queryid` | `bigint` |  | Internal hash code, computed from the statement's parse tree |
| `query` | `text` |  | Text of a representative statement |
| `calls` | `bigint` |  | Number of times executed |
| `total_time` | `double precision` |  | Total time spent in the statement, in milliseconds |
| `min_time` | `double precision` |  | Minimum time spent in the statement, in milliseconds |
| `max_time` | `double precision` |  | Maximum time spent in the statement, in milliseconds |
| `mean_time` | `double precision` |  | Mean time spent in the statement, in milliseconds |
| `stddev_time` | `double precision` |  | Population standard deviation of time spent in the statement, in milliseconds |
| `rows` | `bigint` |  | Total number of rows retrieved or affected by the statement |
| `shared_blks_hit` | `bigint` |  | Total number of shared block cache hits by the statement |
| `shared_blks_read` | `bigint` |  | Total number of shared blocks read by the statement |
| `shared_blks_dirtied` | `bigint` |  | Total number of shared blocks dirtied by the statement |
| `shared_blks_written` | `bigint` |  | Total number of shared blocks written by the statement |
| `local_blks_hit` | `bigint` |  | Total number of local block cache hits by the statement |
| `local_blks_read` | `bigint` |  | Total number of local blocks read by the statement |
| `local_blks_dirtied` | `bigint` |  | Total number of local blocks dirtied by the statement |
| `local_blks_written` | `bigint` |  | Total number of local blocks written by the statement |
| `temp_blks_read` | `bigint` |  | Total number of temp blocks read by the statement |
| `temp_blks_written` | `bigint` |  | Total number of temp blocks written by the statement |
| `blk_read_time` | `double precision` |  | Total time the statement spent reading blocks, in milliseconds \(if [track\_io\_timing](https://www.postgresql.org/docs/12/runtime-config-statistics.html#GUC-TRACK-IO-TIMING) is enabled, otherwise zero\) |
| `blk_write_time` | `double precision` |  | Total time the statement spent writing blocks, in milliseconds \(if [track\_io\_timing](https://www.postgresql.org/docs/12/runtime-config-statistics.html#GUC-TRACK-IO-TIMING) is enabled, otherwise zero\) |

For security reasons, only superusers and members of the `pg_read_all_stats` role are allowed to see the SQL text and `queryid` of queries executed by other users. Other users can see the statistics, however, if the view has been installed in their database.

Plannable queries \(that is, `SELECT`, `INSERT`, `UPDATE`, and `DELETE`\) are combined into a single `pg_stat_statements` entry whenever they have identical query structures according to an internal hash calculation. Typically, two queries will be considered the same for this purpose if they are semantically equivalent except for the values of literal constants appearing in the query. Utility commands \(that is, all other commands\) are compared strictly on the basis of their textual query strings, however.

When a constant's value has been ignored for purposes of matching the query to other queries, the constant is replaced by a parameter symbol, such as `$1`, in the `pg_stat_statements` display. The rest of the query text is that of the first query that had the particular `queryid` hash value associated with the `pg_stat_statements` entry.

In some cases, queries with visibly different texts might get merged into a single `pg_stat_statements` entry. Normally this will happen only for semantically equivalent queries, but there is a small chance of hash collisions causing unrelated queries to be merged into one entry. \(This cannot happen for queries belonging to different users or databases, however.\)

Since the `queryid` hash value is computed on the post-parse-analysis representation of the queries, the opposite is also possible: queries with identical texts might appear as separate entries, if they have different meanings as a result of factors such as different `search_path` settings.

Consumers of `pg_stat_statements` may wish to use `queryid` \(perhaps in combination with `dbid` and `userid`\) as a more stable and reliable identifier for each entry than its query text. However, it is important to understand that there are only limited guarantees around the stability of the `queryid` hash value. Since the identifier is derived from the post-parse-analysis tree, its value is a function of, among other things, the internal object identifiers appearing in this representation. This has some counterintuitive implications. For example, `pg_stat_statements` will consider two apparently-identical queries to be distinct, if they reference a table that was dropped and recreated between the executions of the two queries. The hashing process is also sensitive to differences in machine architecture and other facets of the platform. Furthermore, it is not safe to assume that `queryid` will be stable across major versions of PostgreSQL.

As a rule of thumb, `queryid` values can be assumed to be stable and comparable only so long as the underlying server version and catalog metadata details stay exactly the same. Two servers participating in replication based on physical WAL replay can be expected to have identical `queryid` values for the same query. However, logical replication schemes do not promise to keep replicas identical in all relevant details, so `queryid` will not be a useful identifier for accumulating costs across a set of logical replicas. If in doubt, direct testing is recommended.

The parameter symbols used to replace constants in representative query texts start from the next number after the highest `$`_`n`_ parameter in the original query text, or `$1` if there was none. It's worth noting that in some cases there may be hidden parameter symbols that affect this numbering. For example, PL/pgSQL uses hidden parameter symbols to insert values of function local variables into queries, so that a PL/pgSQL statement like `SELECT i + 1 INTO j` would have representative text like `SELECT i + $2`.

The representative query texts are kept in an external disk file, and do not consume shared memory. Therefore, even very lengthy query texts can be stored successfully. However, if many long query texts are accumulated, the external file might grow unmanageably large. As a recovery method if that happens, `pg_stat_statements` may choose to discard the query texts, whereupon all existing entries in the `pg_stat_statements` view will show null `query` fields, though the statistics associated with each `queryid` are preserved. If this happens, consider reducing `pg_stat_statements.max` to prevent recurrences.

## F.29.2. Functions

`pg_stat_statements_reset(userid Oid, dbid Oid, queryid bigint) returns void`

`pg_stat_statements_reset` discards statistics gathered so far by `pg_stat_statements` corresponding to the specified `userid`, `dbid` and `queryid`. If any of the parameters are not specified, the default value `0`\(invalid\) is used for each of them and the statistics that match with other parameters will be reset. If no parameter is specified or all the specified parameters are `0`\(invalid\), it will discard all statistics. By default, this function can only be executed by superusers. Access may be granted to others using `GRANT`.`pg_stat_statements(showtext boolean) returns setof record`

The `pg_stat_statements` view is defined in terms of a function also named `pg_stat_statements`. It is possible for clients to call the `pg_stat_statements` function directly, and by specifying `showtext := false` have query text be omitted \(that is, the `OUT` argument that corresponds to the view's `query` column will return nulls\). This feature is intended to support external tools that might wish to avoid the overhead of repeatedly retrieving query texts of indeterminate length. Such tools can instead cache the first query text observed for each entry themselves, since that is all `pg_stat_statements` itself does, and then retrieve query texts only as needed. Since the server stores query texts in a file, this approach may reduce physical I/O for repeated examination of the `pg_stat_statements` data.

## F.29.3. Configuration Parameters

`pg_stat_statements.max` \(`integer`\)

`pg_stat_statements.max` is the maximum number of statements tracked by the module \(i.e., the maximum number of rows in the `pg_stat_statements` view\). If more distinct statements than that are observed, information about the least-executed statements is discarded. The default value is 5000. This parameter can only be set at server start.

`pg_stat_statements.track` \(`enum`\)

`pg_stat_statements.track` controls which statements are counted by the module. Specify `top` to track top-level statements \(those issued directly by clients\), `all` to also track nested statements \(such as statements invoked within functions\), or `none` to disable statement statistics collection. The default value is `top`. Only superusers can change this setting.

`pg_stat_statements.track_utility` \(`boolean`\)

`pg_stat_statements.track_utility` controls whether utility commands are tracked by the module. Utility commands are all those other than `SELECT`, `INSERT`, `UPDATE` and `DELETE`. The default value is `on`. Only superusers can change this setting.

`pg_stat_statements.save` \(`boolean`\)

`pg_stat_statements.save` specifies whether to save statement statistics across server shutdowns. If it is `off` then statistics are not saved at shutdown nor reloaded at server start. The default value is `on`. This parameter can only be set in the `postgresql.conf` file or on the server command line.

The module requires additional shared memory proportional to `pg_stat_statements.max`. Note that this memory is consumed whenever the module is loaded, even if `pg_stat_statements.track` is set to `none`.

These parameters must be set in `postgresql.conf`. Typical usage might be:

```text
# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'

pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

## F.29.4. Sample Output

```text
bench=# SELECT pg_stat_statements_reset();

$ pgbench -i bench
$ pgbench -c10 -t300 bench

bench=# \x
bench=# SELECT query, calls, total_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_time DESC LIMIT 5;
-[ RECORD 1 ]--------------------------------------------------------------------
query       | UPDATE pgbench_branches SET bbalance = bbalance + $1 WHERE bid = $2
calls       | 3000
total_time  | 25565.855387
rows        | 3000
hit_percent | 100.0000000000000000
-[ RECORD 2 ]--------------------------------------------------------------------
query       | UPDATE pgbench_tellers SET tbalance = tbalance + $1 WHERE tid = $2
calls       | 3000
total_time  | 20756.669379
rows        | 3000
hit_percent | 100.0000000000000000
-[ RECORD 3 ]--------------------------------------------------------------------
query       | copy pgbench_accounts from stdin
calls       | 1
total_time  | 291.865911
rows        | 100000
hit_percent | 100.0000000000000000
-[ RECORD 4 ]--------------------------------------------------------------------
query       | UPDATE pgbench_accounts SET abalance = abalance + $1 WHERE aid = $2
calls       | 3000
total_time  | 271.232977
rows        | 3000
hit_percent | 98.5723926698852723
-[ RECORD 5 ]--------------------------------------------------------------------
query       | alter table pgbench_accounts add primary key (aid)
calls       | 1
total_time  | 160.588563
rows        | 0
hit_percent | 100.0000000000000000


bench=# SELECT pg_stat_statements_reset(0,0,s.queryid) FROM pg_stat_statements AS s
            WHERE s.query = 'UPDATE pgbench_branches SET bbalance = bbalance + $1 WHERE bid = $2';

bench=# SELECT query, calls, total_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_time DESC LIMIT 5;
-[ RECORD 1 ]--------------------------------------------------------------------
query       | UPDATE pgbench_tellers SET tbalance = tbalance + $1 WHERE tid = $2
calls       | 3000
total_time  | 20756.669379
rows        | 3000
hit_percent | 100.0000000000000000
-[ RECORD 2 ]--------------------------------------------------------------------
query       | copy pgbench_accounts from stdin
calls       | 1
total_time  | 291.865911
rows        | 100000
hit_percent | 100.0000000000000000
-[ RECORD 3 ]--------------------------------------------------------------------
query       | UPDATE pgbench_accounts SET abalance = abalance + $1 WHERE aid = $2
calls       | 3000
total_time  | 271.232977
rows        | 3000
hit_percent | 98.5723926698852723
-[ RECORD 4 ]--------------------------------------------------------------------
query       | alter table pgbench_accounts add primary key (aid)
calls       | 1
total_time  | 160.588563
rows        | 0
hit_percent | 100.0000000000000000
-[ RECORD 5 ]--------------------------------------------------------------------
query       | vacuum analyze pgbench_accounts
calls       | 1
total_time  | 136.448116
rows        | 0
hit_percent | 99.9201915403032721

bench=# SELECT pg_stat_statements_reset(0,0,0);

bench=# SELECT query, calls, total_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_time DESC LIMIT 5;
-[ RECORD 1 ]---------------------------------------
query       | SELECT pg_stat_statements_reset(0,0,0)
calls       | 1
total_time  | 0.189497
rows        | 1
hit_percent | 

```

## F.29.5. Authors

Takahiro Itagaki `<`[`itagaki.takahiro@oss.ntt.co.jp`](mailto:itagaki.takahiro@oss.ntt.co.jp)`>`. Query normalization added by Peter Geoghegan `<`[`peter@2ndquadrant.com`](mailto:peter@2ndquadrant.com)`>`.  


