# F.29. pg\_stat\_statements

pg\_stat\_statements 模組提供了一個追踪在伺服器上執行的 SQL 語句統計資訊方法。

必須透過將 pg\_stat\_statements 加到 postgresql.conf 中的 [shared\_preload\_libraries](../../server-administration/server-configuration/client-connection-defaults.md#shared_preload_libraries-string) 中來載入模組，因為它需要額外的共享記憶體。這意味著需要重新啟動伺服器才能載加或刪除模組。

載入 pg\_stat\_statements 後，它將追踪伺服器所有資料庫的統計資訊。 為了存取和處理這些統計資訊，此模組提供了一個檢視表 pg\_stat\_statements 以及工具程序函數 pg\_stat\_statements\_reset 和 pg\_stat\_statements。這些不是全域可用的，但可以使用 `CREATE EXTENSION pg_stat_statements` 為特定資料庫啟用。

## F.29.1. The `pg_stat_statements` View

此延伸功能收集的統計數據可透過名為 pg\_stat\_statements 的檢視表查詢。對於每個不同的資料庫 ID、使用者 ID和查詢語句 ID（此延伸功能可以追踪的最大不同查詢語句數量），在此檢視表會在一筆資料中呈現。 檢視表的欄位在 Table F.21 中說明。

#### **Table F.21. `pg_stat_statements` Columns**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>userid</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-authid.html"><code>pg_authid</code></a>.<code>oid</code>)</p>
        <p>OID of user who executed the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>dbid</code>  <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-database.html"><code>pg_database</code></a>.<code>oid</code>)</p>
        <p>OID of database in which the statement was executed</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>queryid</code>  <code>bigint</code>
        </p>
        <p>Internal hash code, computed from the statement&apos;s parse tree</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>query</code>  <code>text</code>
        </p>
        <p>Text of a representative statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>plans</code>  <code>bigint</code>
        </p>
        <p>Number of times the statement was planned (if <code>pg_stat_statements.track_planning</code> is
          enabled, otherwise zero)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>total_plan_time</code>  <code>double precision</code>
        </p>
        <p>Total time spent planning the statement, in milliseconds (if <code>pg_stat_statements.track_planning</code> is
          enabled, otherwise zero)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>min_plan_time</code>  <code>double precision</code>
        </p>
        <p>Minimum time spent planning the statement, in milliseconds (if <code>pg_stat_statements.track_planning</code> is
          enabled, otherwise zero)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>max_plan_time</code>  <code>double precision</code>
        </p>
        <p>Maximum time spent planning the statement, in milliseconds (if <code>pg_stat_statements.track_planning</code> is
          enabled, otherwise zero)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>mean_plan_time</code>  <code>double precision</code>
        </p>
        <p>Mean time spent planning the statement, in milliseconds (if <code>pg_stat_statements.track_planning</code> is
          enabled, otherwise zero)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stddev_plan_time</code>  <code>double precision</code>
        </p>
        <p>Population standard deviation of time spent planning the statement, in
          milliseconds (if <code>pg_stat_statements.track_planning</code> is enabled,
          otherwise zero)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>calls</code>  <code>bigint</code>
        </p>
        <p>Number of times the statement was executed</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>total_exec_time</code>  <code>double precision</code>
        </p>
        <p>Total time spent executing the statement, in milliseconds</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>min_exec_time</code>  <code>double precision</code>
        </p>
        <p>Minimum time spent executing the statement, in milliseconds</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>max_exec_time</code>  <code>double precision</code>
        </p>
        <p>Maximum time spent executing the statement, in milliseconds</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>mean_exec_time</code>  <code>double precision</code>
        </p>
        <p>Mean time spent executing the statement, in milliseconds</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stddev_exec_time</code>  <code>double precision</code>
        </p>
        <p>Population standard deviation of time spent executing the statement, in
          milliseconds</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>rows</code>  <code>bigint</code>
        </p>
        <p>Total number of rows retrieved or affected by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>shared_blks_hit</code>  <code>bigint</code>
        </p>
        <p>Total number of shared block cache hits by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>shared_blks_read</code>  <code>bigint</code>
        </p>
        <p>Total number of shared blocks read by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>shared_blks_dirtied</code>  <code>bigint</code>
        </p>
        <p>Total number of shared blocks dirtied by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>shared_blks_written</code>  <code>bigint</code>
        </p>
        <p>Total number of shared blocks written by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>local_blks_hit</code>  <code>bigint</code>
        </p>
        <p>Total number of local block cache hits by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>local_blks_read</code>  <code>bigint</code>
        </p>
        <p>Total number of local blocks read by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>local_blks_dirtied</code>  <code>bigint</code>
        </p>
        <p>Total number of local blocks dirtied by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>local_blks_written</code>  <code>bigint</code>
        </p>
        <p>Total number of local blocks written by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>temp_blks_read</code>  <code>bigint</code>
        </p>
        <p>Total number of temp blocks read by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>temp_blks_written</code>  <code>bigint</code>
        </p>
        <p>Total number of temp blocks written by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blk_read_time</code>  <code>double precision</code>
        </p>
        <p>Total time the statement spent reading blocks, in milliseconds (if <a href="https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-IO-TIMING">track_io_timing</a> is
          enabled, otherwise zero)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blk_write_time</code>  <code>double precision</code>
        </p>
        <p>Total time the statement spent writing blocks, in milliseconds (if <a href="https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-IO-TIMING">track_io_timing</a> is
          enabled, otherwise zero)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>wal_records</code>  <code>bigint</code>
        </p>
        <p>Total number of WAL records generated by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>wal_fpi</code>  <code>bigint</code>
        </p>
        <p>Total number of WAL full page images generated by the statement</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>wal_bytes</code>  <code>numeric</code>
        </p>
        <p>Total amount of WAL bytes generated by the statement</p>
      </td>
    </tr>
  </tbody>
</table>

因為安全因素，僅超級使用者和 pg\_read\_all\_stats 角色成員被允許查看其他使用者所執行的 SQL 語句和 queryid。但是，如果檢視圖已安裝在他們的資料庫中，則其他使用者也可以查看統計內容。

只要是有**查詢**計劃查詢的查詢（即 SELECT、INSERT、UPDATE 和 DELETE）根據內部雜湊計算具有相同的查詢結構，它們就會組合到單筆 pg\_stat\_statements 資料中。通常，如果兩個查詢在語義上等效，即兩個查詢在此意義上是相同的，只是出現在查詢中的常數內容的值除外。 但是，會嚴格地根據資料庫結構維護指令（即所有其他指令）的查詢字串進行比較。

為了將查詢與其他查詢搭配而忽略了常數內容時，該常數內容會在 pg\_stat\_statements 顯示中替換為參數符號，例如 $1。查詢語句的其餘部分是第一個查詢的內容，該查詢具有與 pg\_stat\_statements 項目關聯的特定 queryid 雜湊值。

In some cases, queries with visibly different texts might get merged into a single `pg_stat_statements` entry. Normally this will happen only for semantically equivalent queries, but there is a small chance of hash collisions causing unrelated queries to be merged into one entry. \(This cannot happen for queries belonging to different users or databases, however.\)

Since the `queryid` hash value is computed on the post-parse-analysis representation of the queries, the opposite is also possible: queries with identical texts might appear as separate entries, if they have different meanings as a result of factors such as different `search_path` settings.

Consumers of `pg_stat_statements` may wish to use `queryid` \(perhaps in combination with `dbid` and `userid`\) as a more stable and reliable identifier for each entry than its query text. However, it is important to understand that there are only limited guarantees around the stability of the `queryid` hash value. Since the identifier is derived from the post-parse-analysis tree, its value is a function of, among other things, the internal object identifiers appearing in this representation. This has some counterintuitive implications. For example, `pg_stat_statements` will consider two apparently-identical queries to be distinct, if they reference a table that was dropped and recreated between the executions of the two queries. The hashing process is also sensitive to differences in machine architecture and other facets of the platform. Furthermore, it is not safe to assume that `queryid` will be stable across major versions of PostgreSQL.

As a rule of thumb, `queryid` values can be assumed to be stable and comparable only so long as the underlying server version and catalog metadata details stay exactly the same. Two servers participating in replication based on physical WAL replay can be expected to have identical `queryid` values for the same query. However, logical replication schemes do not promise to keep replicas identical in all relevant details, so `queryid` will not be a useful identifier for accumulating costs across a set of logical replicas. If in doubt, direct testing is recommended.

The parameter symbols used to replace constants in representative query texts start from the next number after the highest `$`_`n`_ parameter in the original query text, or `$1` if there was none. It's worth noting that in some cases there may be hidden parameter symbols that affect this numbering. For example, PL/pgSQL uses hidden parameter symbols to insert values of function local variables into queries, so that a PL/pgSQL statement like `SELECT i + 1 INTO j` would have representative text like `SELECT i + $2`.

The representative query texts are kept in an external disk file, and do not consume shared memory. Therefore, even very lengthy query texts can be stored successfully. However, if many long query texts are accumulated, the external file might grow unmanageably large. As a recovery method if that happens, `pg_stat_statements` may choose to discard the query texts, whereupon all existing entries in the `pg_stat_statements` view will show null `query` fields, though the statistics associated with each `queryid` are preserved. If this happens, consider reducing `pg_stat_statements.max` to prevent recurrences.

 plans 和 calls 不一定會完全相等，因為查詢計劃和執行統計資訊會在其各自的執行階段進行更新，並且僅針對成功的操作進行更新。例如，某一條語句已經進行了查詢計劃，但在執行階段卻失敗了，則僅更新其查詢計劃統計資訊。如果由於使用了快取的查詢計劃而跳過了計劃階段，也只會更新其執行階段的統計資訊。

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

