<a id="PGSTATSTATEMENTS"></a>

## F.32. pg_stat_statements — 追蹤 SQL 規劃與執行的統計資訊 [#](#pgstatstatements) <a href="#pgstatstatements" id="pgstatstatements"></a>

[F.32.1. `pg_stat_statements` 檢視表](pgstatstatements/pgstatstatements-pg-stat-statements.md#pgstatstatements-pg-stat-statements)

[F.32.2. `pg_stat_statements_info` 檢視表](pgstatstatements/pgstatstatements-pg-stat-statements-info.md#pgstatstatements-pg-stat-statements-info)

[F.32.3. 函式](pgstatstatements.md#pgstatstatements-funcs)

[F.32.4. 設定參數](pgstatstatements.md#pgstatstatements-config-params)

[F.32.5. 輸出範例](pgstatstatements.md#pgstatstatements-sample-output)

[F.32.6. 作者](pgstatstatements.md#pgstatstatements-authors)

<a id="id-1.11.7.42.2"></a>

`pg_stat_statements` 模組提供一種方式，用來追蹤伺服器所執行之所有 SQL 陳述式的規劃與執行統計資訊。

此模組必須透過在 `postgresql.conf` 的 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) 中加入 `pg_stat_statements` 來載入，因為它需要額外的共享記憶體。這表示新增或移除此模組都需要重新啟動伺服器。此外，必須啟用查詢識別碼計算，此模組才會運作；若 [compute_query_id](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID) 設為 `auto` 或 `on`，或已載入任何會計算查詢識別碼的第三方模組，就會自動啟用此計算。

`pg_stat_statements` 啟用時，會追蹤伺服器上所有資料庫的統計資訊。為了存取與操作這些統計資訊，此模組提供檢視表 `pg_stat_statements` 與 `pg_stat_statements_info`，以及公用函式 `pg_stat_statements_reset` 與 `pg_stat_statements`。這些並非全域可用，但可以用 `CREATE EXTENSION pg_stat_statements` 為特定資料庫啟用。

### F.32.1. `pg_stat_statements` 檢視表 [#](#pgstatstatements-pg-stat-statements) <a href="#pgstatstatements-pg-stat-statements" id="pgstatstatements-pg-stat-statements"></a>

完整內容請見 [F.32.1. pg_stat_statements 檢視表](pgstatstatements/pgstatstatements-pg-stat-statements.md#pgstatstatements-pg-stat-statements)。

### F.32.2. `pg_stat_statements_info` 檢視表 [#](#pgstatstatements-pg-stat-statements-info) <a href="#pgstatstatements-pg-stat-statements-info" id="pgstatstatements-pg-stat-statements-info"></a>

完整內容請見 [F.32.2. pg_stat_statements_info 檢視表](pgstatstatements/pgstatstatements-pg-stat-statements-info.md#pgstatstatements-pg-stat-statements-info)。

<a id="PGSTATSTATEMENTS-FUNCS"></a>

### F.32.3. 函式 [#](#pgstatstatements-funcs) <a href="#pgstatstatements-funcs" id="pgstatstatements-funcs"></a>

`pg_stat_statements_reset(userid Oid, dbid Oid, queryid bigint, minmax_only boolean) returns timestamp with time zone` <a id="id-1.11.7.42.8.2.1.1.2"></a>
:   `pg_stat_statements_reset` 會捨棄 `pg_stat_statements` 至今所收集、與指定之 `userid`、`dbid` 及 `queryid` 相對應的統計資訊。若有任何參數未指定，這些參數都會使用預設值 `0`（無效），並重設符合其他參數的統計資訊。若未指定任何參數，或所有指定的參數皆為 `0`（無效），則會捨棄所有統計資訊。若 `pg_stat_statements` 檢視表中的所有統計資訊都被捨棄，也會一併重設 `pg_stat_statements_info` 檢視表中的統計資訊。當 `minmax_only` 為 `true` 時，只會重設規劃與執行時間的最小值與最大值（亦即 `min_plan_time`、`max_plan_time`、`min_exec_time` 與 `max_exec_time` 欄位）。`minmax_only` 參數的預設值為 `false`。最後一次執行最小／最大值重設的時間，顯示在 `pg_stat_statements` 檢視表的 `minmax_stats_since` 欄位中。此函式會傳回重設的時間。若確實執行了相對應的重設，此時間會儲存到 `pg_stat_statements_info` 檢視表的 `stats_reset` 欄位，或 `pg_stat_statements` 檢視表的 `minmax_stats_since` 欄位。預設情況下，只有超級使用者可以執行此函式。可以使用 `GRANT` 將存取權授與其他人。

`pg_stat_statements(showtext boolean) returns setof record` <a id="id-1.11.7.42.8.2.2.1.2"></a>
:   `pg_stat_statements` 檢視表是以一個同樣名為 `pg_stat_statements` 的函式來定義的。用戶端可以直接呼叫 `pg_stat_statements` 函式，並藉由指定 `showtext := false` 來省略查詢文字（也就是說，對應於檢視表 `query` 欄位的 `OUT` 參數會傳回 null）。此功能旨在支援可能希望避免反覆擷取長度不定之查詢文字所造成負擔的外部工具。這類工具可以改為自行快取每個項目所觀察到的第一個查詢文字，因為 `pg_stat_statements` 本身也只是這麼做，之後只在需要時才擷取查詢文字。由於伺服器將查詢文字儲存在檔案中，這種做法可能減少反覆檢視 `pg_stat_statements` 資料時的實體 I/O。

<a id="PGSTATSTATEMENTS-CONFIG-PARAMS"></a>

### F.32.4. 設定參數 [#](#pgstatstatements-config-params) <a href="#pgstatstatements-config-params" id="pgstatstatements-config-params"></a>

`pg_stat_statements.max` (`integer`) <a id="id-1.11.7.42.9.2.1.1.3"></a>
:   `pg_stat_statements.max` 是此模組所追蹤之陳述式的最大數量（亦即 `pg_stat_statements` 檢視表中資料列的最大數量）。若觀察到的不同陳述式超過此數量，有關執行次數最少之陳述式的資訊就會被捨棄。此類資訊被捨棄的次數，可以在 `pg_stat_statements_info` 檢視表中查看。預設值為 5000。此參數只能在伺服器啟動時設定。

`pg_stat_statements.track` (`enum`) <a id="id-1.11.7.42.9.2.2.1.3"></a>
:   `pg_stat_statements.track` 控制此模組要計入哪些陳述式。指定 `top` 會追蹤頂層陳述式（由用戶端直接發出的陳述式），指定 `all` 會連巢狀陳述式（例如在函式中呼叫的陳述式）也一併追蹤，指定 `none` 則會停用陳述式統計資訊的收集。預設值為 `top`。只有超級使用者可以變更此設定。

`pg_stat_statements.track_utility` (`boolean`) <a id="id-1.11.7.42.9.2.3.1.3"></a>
:   `pg_stat_statements.track_utility` 控制此模組是否追蹤公用程式命令。公用程式命令是指 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 與 `MERGE` 以外的所有命令。預設值為 `on`。只有超級使用者可以變更此設定。

`pg_stat_statements.track_planning` (`boolean`) <a id="id-1.11.7.42.9.2.4.1.3"></a>
:   `pg_stat_statements.track_planning` 控制此模組是否追蹤規劃操作及其持續時間。啟用此參數可能造成明顯的效能損失，尤其是當具有相同查詢結構的陳述式由許多並行連線執行、而這些連線競相更新少數幾個 `pg_stat_statements` 項目時。預設值為 `off`。只有超級使用者可以變更此設定。

`pg_stat_statements.save` (`boolean`) <a id="id-1.11.7.42.9.2.5.1.3"></a>
:   `pg_stat_statements.save` 指定是否要在伺服器關閉後保留陳述式統計資訊。若設為 `off`，則統計資訊既不會在關閉時保存，也不會在伺服器啟動時重新載入。預設值為 `on`。此參數只能在 `postgresql.conf` 檔案中或伺服器命令列上設定。

此模組需要與 `pg_stat_statements.max` 成正比的額外共享記憶體。請注意，只要載入此模組就會占用這些記憶體，即使 `pg_stat_statements.track` 設為 `none` 也一樣。

這些參數必須在 `postgresql.conf` 中設定。典型的用法可能如下：

```

# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'

compute_query_id = on
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

<a id="PGSTATSTATEMENTS-SAMPLE-OUTPUT"></a>

### F.32.5. 輸出範例 [#](#pgstatstatements-sample-output) <a href="#pgstatstatements-sample-output" id="pgstatstatements-sample-output"></a>

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

### F.32.6. 作者 [#](#pgstatstatements-authors) <a href="#pgstatstatements-authors" id="pgstatstatements-authors"></a>

Takahiro Itagaki `<itagaki.takahiro@oss.ntt.co.jp>`。查詢正規化由 Peter Geoghegan `<peter@2ndquadrant.com>` 加入。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgstatstatements.html)（原文版本：18.6；核對日期：2026-10-23）
