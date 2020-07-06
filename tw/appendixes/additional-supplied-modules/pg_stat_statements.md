# F.29. pg\_stat\_statements

pg\_stat\_statements 模組提供了一個追踪在伺服器上執行的 SQL 語句統計資訊方法。

必須透過將 pg\_stat\_statements 加到 postgresql.conf 中的 [shared\_preload\_libraries](../../server-administration/server-configuration/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#shared_preload_libraries-string) 中來載入模組，因為它需要額外的共享記憶體。這意味著需要重新啟動伺服器才能載加或刪除模組。

載入 pg\_stat\_statements 後，它將追踪伺服器所有資料庫的統計資訊。 為了存取和處理這些統計資訊，此模組提供了一個檢視表 pg\_stat\_statements 以及工具程序函數 pg\_stat\_statements\_reset 和 pg\_stat\_statements。這些不是全域可用的，但可以使用 `CREATE EXTENSION pg_stat_statements` 為特定資料庫啟用。

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

pg\_stat\_statements\_reset 會移除到目前為止由 pg\_stat\_statements 收集的與指定的 userid、dbid 和 queryid 相對應的統計資訊。如果未指定任何參數，則對每個參數使用預設值 0（無效），並且將重置與其他參數相對應的統計資訊。如果未指定任何參數，或者所有指定的參數均為0（無效），則將移除所有統計資訊。預設情況下，此功能只能由超級使用者執行。可以使用 GRANT 將存取權限授予其他人。

`pg_stat_statements(showtext boolean) returns setof record`

pg\_stat\_statements 檢視表是根據也稱為 pg\_stat\_statements 的函數定義的。用戶端可以直接呼叫 pg\_stat\_statements 函數，並透過指定showtext := false 可以省略查詢字串（即，對應於檢視圖查詢欄位的 OUT 參數將回傳 null）。此功能旨在支持可能希望避免重複獲取長度不確定的查詢字串成本的外部工具。這樣的工具可以代替暫存每個項目本身觀察到的第一個查詢字串，因為 pg\_stat\_statements 本身就是這樣做的，然後僅根據需要檢索查詢字串。由於伺服器將查詢字串儲存在檔案中，因此此方法可以減少用於重複檢查 pg\_stat\_statements 資料的實際 I/O 成本。

## F.29.3. Configuration Parameters

`pg_stat_statements.max` \(`integer`\)

pg\_stat\_statements.max 設定此模組所追踪的語句數量上限（即 pg\_stat\_statements 檢視表中的最大資料列數）。如果觀察到的語句不同，則將丟棄有關執行最少的語句的資訊。預設值為 5,000。只能在伺服器啟動時設定此參數。

`pg_stat_statements.track` \(`enum`\)

pg\_stat\_statements.track 控制此模組關注哪些語句。指定 top 表示追踪最上層語句（由用戶端直接發出的語句），也可以全部追踪巢狀語句（例如在函數內呼叫的語句），或者不指定以停用語句統計資訊收集。預設值為 top。只有超級使用者可以變更此設定。

`pg_stat_statements.track_utility` \(`boolean`\)

pg\_stat\_statements.track\_utility 控制模組是否追踪管理程序命令。管理程序命令是除 SELECT、INSERT、UPDATE 和 DELETE 之外的所有命令。預設值為 on。只有超級使用者可以變更改此設定。

`pg_stat_statements.save` \(`boolean`\)

pg\_stat\_statements.save 指定是否在伺服器關閉時保存語句統計資訊。 如果關閉，則統計資訊不會在關閉時保存，也不會在伺服器啟動時重新載入。預設值為開。只能在 postgresql.conf 檔案或伺服器命令列中設定此參數。

此模塊需要與 pg\_stat\_statements.max 成比例的額外共享記憶體。請注意，即使將 pg\_stat\_statements.track 設定為 none，只要載入模組，就會佔用記憶體空間。

這些參數必須在 postgresql.conf 中設定。典型的用法可能是：

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

