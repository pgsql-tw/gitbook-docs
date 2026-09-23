<a id="RUNTIME-CONFIG-STATISTICS"></a>

## 19.9. 執行時期統計資訊 [#](#RUNTIME-CONFIG-STATISTICS)

[19.9.1. 累計查詢與索引統計資訊](runtime-config-statistics.md#RUNTIME-CONFIG-CUMULATIVE-STATISTICS)

[19.9.2. 統計資訊監控](runtime-config-statistics.md#RUNTIME-CONFIG-STATISTICS-MONITOR)

<a id="RUNTIME-CONFIG-CUMULATIVE-STATISTICS"></a>

### 19.9.1. 累計查詢與索引統計資訊 [#](#RUNTIME-CONFIG-CUMULATIVE-STATISTICS)

這些參數控制伺服器層級的累計統計系統。
啟用後，收集到的資料可以透過
`pg_stat` 與 `pg_statio`
系列的系統檢視表存取。詳情請參閱[第 27 章](../monitoring/README.md)。

<a id="GUC-TRACK-ACTIVITIES"></a>

`track_activities` (`boolean`) <a id="id-1.6.6.12.2.3.1.1.3"></a> [#](#GUC-TRACK-ACTIVITIES)
:   啟用對每個工作階段目前執行中命令的資訊收集，
    包括其識別碼以及該命令開始執行的時間。此參數預設為
    開啟。請注意，即使啟用此參數，這項資訊也僅對超級使用者、
    具備 `pg_read_all_stats` 角色權限的角色，
    以及擁有被回報之工作階段的使用者（包括屬於該使用者所具權限之角色的工作階段）
    可見，因此不應構成安全性風險。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-TRACK-ACTIVITY-QUERY-SIZE"></a>

`track_activity_query_size` (`integer`) <a id="id-1.6.6.12.2.3.2.1.3"></a> [#](#GUC-TRACK-ACTIVITY-QUERY-SIZE)
:   指定為每個作用中工作階段保留、用於儲存目前執行中命令文字的
    記憶體量，供
    `pg_stat_activity`.`query` 欄位使用。
    若此值指定時未帶單位，則以位元組為單位。
    預設值為 1024 位元組。
    此參數只能在伺服器啟動時設定。
<a id="GUC-TRACK-COUNTS"></a>

`track_counts` (`boolean`) <a id="id-1.6.6.12.2.3.3.1.3"></a> [#](#GUC-TRACK-COUNTS)
:   啟用資料庫活動統計資訊的收集。
    此參數預設為開啟，因為 autovacuum
    守護程序需要用到收集到的資訊。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-TRACK-COST-DELAY-TIMING"></a>

`track_cost_delay_timing` (`boolean`) <a id="id-1.6.6.12.2.3.4.1.3"></a> [#](#GUC-TRACK-COST-DELAY-TIMING)
:   啟用以成本為基礎的 vacuum 延遲計時（參閱
    [19.10.2 節](runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)）。此參數
    預設為關閉，因為它會反覆向作業系統查詢
    目前時間，在某些平台上可能造成顯著額外負擔。
    你可以使用 [pg_test_timing](../../reference/reference-server/pgtesttiming.md) 工具
    來測量你的系統上計時功能的額外負擔。以成本為基礎的 vacuum 延遲
    計時資訊會顯示在
    [`pg_stat_progress_vacuum`](../monitoring/progress-reporting.md#VACUUM-PROGRESS-REPORTING)、
    [`pg_stat_progress_analyze`](../monitoring/progress-reporting.md#ANALYZE-PROGRESS-REPORTING)、
    在使用 `VERBOSE` 選項時 [VACUUM](../../reference/sql-commands/sql-vacuum.md) 與
    [ANALYZE](../../reference/sql-commands/sql-analyze.md) 的輸出中，
    以及在設定 [log_autovacuum_min_duration](runtime-config-logging.md#GUC-LOG-AUTOVACUUM-MIN-DURATION)
    時，由 autovacuum 針對自動 vacuum 與自動 analyze 輸出。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-TRACK-IO-TIMING"></a>

`track_io_timing` (`boolean`) <a id="id-1.6.6.12.2.3.5.1.3"></a> [#](#GUC-TRACK-IO-TIMING)
:   啟用資料庫 I/O 等待的計時。此參數預設為
    關閉，因為它會反覆向作業系統查詢
    目前時間，在某些平台上可能造成顯著額外負擔。
    你可以使用 [pg_test_timing](../../reference/reference-server/pgtesttiming.md) 工具
    來測量你的系統上計時功能的額外負擔。
    I/O 計時資訊會顯示在
    [`pg_stat_database`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW)、
    [`pg_stat_io`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW)（若 `object`
    不是 `wal`）、在使用
    [`pg_stat_get_backend_io()`](../monitoring/monitoring-stats.md#PG-STAT-GET-BACKEND-IO) 函式的輸出中（若
    `object` 不是 `wal`）、在使用 `BUFFERS`
    選項時 [EXPLAIN](../../reference/sql-commands/sql-explain.md) 的輸出中、在使用
    `VERBOSE` 選項時 [VACUUM](../../reference/sql-commands/sql-vacuum.md) 的輸出中、
    在設定 [log_autovacuum_min_duration](runtime-config-logging.md#GUC-LOG-AUTOVACUUM-MIN-DURATION)
    時由 autovacuum 針對自動 vacuum 與自動 analyze 輸出，
    以及在 [pg_stat_statements](../../appendixes/contrib/pgstatstatements.md) 中。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-TRACK-WAL-IO-TIMING"></a>

`track_wal_io_timing` (`boolean`) <a id="id-1.6.6.12.2.3.6.1.3"></a> [#](#GUC-TRACK-WAL-IO-TIMING)
:   啟用 WAL I/O 等待的計時。此參數預設為關閉，
    因為它會反覆向作業系統查詢目前時間，
    在某些平台上可能造成顯著額外負擔。
    你可以使用 pg_test_timing 工具
    來測量你的系統上計時功能的額外負擔。
    I/O 計時資訊會顯示在
    `object` 為 `wal` 的
    [`pg_stat_io`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW) 中，以及
    `object` 為 `wal` 時
    [`pg_stat_get_backend_io()`](../monitoring/monitoring-stats.md#PG-STAT-GET-BACKEND-IO) 函式的輸出中。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-TRACK-FUNCTIONS"></a>

`track_functions` (`enum`) <a id="id-1.6.6.12.2.3.7.1.3"></a> [#](#GUC-TRACK-FUNCTIONS)
:   啟用函式呼叫次數與使用時間的追蹤。指定
    `pl` 僅追蹤程序語言（procedural-language）函式，
    `all` 則同時追蹤 SQL 與 C 語言函式。
    預設值為 `none`，即停用函式
    統計追蹤。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。

    ### 注意

    簡單到可以被「內聯（inline）」進呼叫查詢的 SQL 語言函式，
    無論此設定為何，都不會被追蹤。
<a id="GUC-STATS-FETCH-CONSISTENCY"></a>

`stats_fetch_consistency` (`enum`) <a id="id-1.6.6.12.2.3.8.1.3"></a> [#](#GUC-STATS-FETCH-CONSISTENCY)
:   決定在同一交易中多次存取累計統計資訊時的行為。
    當設為 `none` 時，每次存取都會重新從
    共享記憶體擷取計數器。當設為 `cache` 時，
    首次存取某物件的統計資訊時，會快取該統計資訊直到交易結束，
    除非呼叫了 `pg_stat_clear_snapshot()`。
    當設為 `snapshot` 時，首次存取統計資訊時，
    會快取目前資料庫中可存取的所有統計資訊，直到
    交易結束，除非呼叫了
    `pg_stat_clear_snapshot()`。在交易中變更此
    參數會捨棄該統計資訊快照。
    預設值為 `cache`。

    ### 注意

    `none` 最適合用於監控系統。若
    數值僅會被存取一次，此選項是最有
    效率的。`cache` 可確保重複存取時取得
    相同的數值，這對於涉及例如自我聯結（self-join）的查詢很重要。
    `snapshot` 在互動式檢視統計資訊時很有用，
    但額外負擔較高，尤其是在存在許多資料庫物件時。

<a id="RUNTIME-CONFIG-STATISTICS-MONITOR"></a>

### 19.9.2. 統計資訊監控 [#](#RUNTIME-CONFIG-STATISTICS-MONITOR)

<a id="GUC-COMPUTE-QUERY-ID"></a>

`compute_query_id` (`enum`) <a id="id-1.6.6.12.3.2.1.1.3"></a> [#](#GUC-COMPUTE-QUERY-ID)
:   啟用核心內建的查詢識別碼計算功能。
    查詢識別碼可以顯示在 [`pg_stat_activity`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW)
    檢視表中、透過 `EXPLAIN` 顯示，或若透過
    [log_line_prefix](runtime-config-logging.md#GUC-LOG-LINE-PREFIX) 參數設定，也可以輸出到日誌中。
    [pg_stat_statements](../../appendixes/contrib/pgstatstatements.md) 延伸模組同樣需要
    計算查詢識別碼。請注意，如果核心內建的查詢識別碼
    計算方式不被接受，也可以改用外部模組。在這種情況下，
    必須永遠停用核心內建的計算功能。
    合法的值有 `off`（永遠停用）、
    `on`（永遠啟用）、`auto`
    （讓 [pg_stat_statements](../../appendixes/contrib/pgstatstatements.md) 等模組
    自動啟用此功能），以及 `regress`（效果
    與 `auto` 相同，只是為了方便自動化迴歸測試，
    查詢識別碼不會顯示在 `EXPLAIN` 輸出中）。
    預設值為 `auto`。

    ### 注意

    為確保只計算並顯示一個查詢識別碼，
    計算查詢識別碼的延伸模組在查詢識別碼已經
    被計算過的情況下應該要拋出錯誤。
<a id="GUC-LOG-STATEMENT-STATS"></a>

`log_statement_stats` (`boolean`) <a id="id-1.6.6.12.3.2.2.1.3"></a> <br>`log_parser_stats` (`boolean`) <a id="id-1.6.6.12.3.2.2.2.3"></a> <br>`log_planner_stats` (`boolean`) <a id="id-1.6.6.12.3.2.2.3.3"></a> <br>`log_executor_stats` (`boolean`) <a id="id-1.6.6.12.3.2.2.4.3"></a> [#](#GUC-LOG-STATEMENT-STATS)
:   針對每個查詢，將對應模組的效能統計資訊輸出到伺服器日誌。
    這是一種簡陋的效能剖析工具，類似 Unix 的
    `getrusage()` 作業系統機制。`log_statement_stats`
    回報整體陳述式統計資訊，而其他選項則回報各模組的統計資訊。
    `log_statement_stats` 無法與任何各模組選項
    同時啟用。這些選項預設皆為停用。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更這些設定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-statistics.html)（原文版本：18.6；核對日期：2026-09-22）
