## F.3. auto_explain — 記錄慢速查詢的執行計畫 [#](#AUTO-EXPLAIN)

[F.3.1. 設定參數](auto-explain.md#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS)

[F.3.2. 範例](auto-explain.md#AUTO-EXPLAIN-EXAMPLE)

[F.3.3. 作者](auto-explain.md#AUTO-EXPLAIN-AUTHOR)

<a id="id-1.11.7.13.2"></a>

`auto_explain` 模組可自動記錄慢速陳述式的執行計畫，無須手動執行 [EXPLAIN](../../reference/sql-commands/sql-explain.md)。這對於找出大型應用程式中未最佳化的查詢特別有幫助。

此模組不提供可透過 SQL 存取的函式。若要使用它，只要將其載入伺服器。你可以將它載入個別工作階段：

```

LOAD 'auto_explain';
```

（這需要超級使用者權限。）更典型的用法是，在 `postgresql.conf` 的 [session_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES) 或 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) 中加入 `auto_explain`，以便將其預先載入部分或所有工作階段。如此即可追蹤隨時發生的非預期慢速查詢；當然，這會帶來額外負擔。

<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS"></a>

### F.3.1. 設定參數 [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS)

有數個設定參數可控制 `auto_explain` 的行為。請注意，預設行為是不執行任何動作；若要取得任何結果，至少必須設定 `auto_explain.log_min_duration`。

<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-MIN-DURATION"></a>

`auto_explain.log_min_duration` (`integer`) <a id="id-1.11.7.13.5.3.1.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-MIN-DURATION)
:   `auto_explain.log_min_duration` 是觸發記錄陳述式計畫所需的最短陳述式執行時間（以毫秒為單位）。設為 `0` 會記錄所有計畫。`-1`（預設）會停用計畫記錄。例如，設為 `250ms` 時，執行 250 毫秒以上的所有陳述式都會被記錄。只有超級使用者能變更此設定。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-PARAMETER-MAX-LENGTH"></a>

`auto_explain.log_parameter_max_length` (`integer`) <a id="id-1.11.7.13.5.3.2.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-PARAMETER-MAX-LENGTH)
:   `auto_explain.log_parameter_max_length` 控制查詢參數值的記錄。`-1`（預設）會完整記錄參數值；`0` 停用參數值記錄；大於零的值會將每個參數值截斷至該位元組數。只有超級使用者能變更此設定。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-ANALYZE"></a>

`auto_explain.log_analyze` (`boolean`) <a id="id-1.11.7.13.5.3.3.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-ANALYZE)
:   `auto_explain.log_analyze` 使記錄執行計畫時輸出 `EXPLAIN ANALYZE`，而非僅輸出 `EXPLAIN`。此參數預設為關閉，且只有超級使用者能變更。

    ### 注意

    啟用此參數時，所有已執行陳述式都會執行每個計畫節點的計時，不論是否長到實際被記錄。這可能對效能造成極大負面影響。關閉 `auto_explain.log_timing` 可減輕效能成本，但會取得較少資訊。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-BUFFERS"></a>

`auto_explain.log_buffers` (`boolean`) <a id="id-1.11.7.13.5.3.4.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-BUFFERS)
:   `auto_explain.log_buffers` 控制記錄執行計畫時是否輸出緩衝區使用統計資訊；它等同於 `EXPLAIN` 的 `BUFFERS` 選項。除非啟用 `auto_explain.log_analyze`，此參數不會生效。預設為關閉，且只有超級使用者能變更。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-WAL"></a>

`auto_explain.log_wal` (`boolean`) <a id="id-1.11.7.13.5.3.5.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-WAL)
:   `auto_explain.log_wal` 控制記錄執行計畫時是否輸出 WAL 使用統計資訊；它等同於 `EXPLAIN` 的 `WAL` 選項。除非啟用 `auto_explain.log_analyze`，此參數不會生效。預設為關閉，且只有超級使用者能變更。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-TIMING"></a>

`auto_explain.log_timing` (`boolean`) <a id="id-1.11.7.13.5.3.6.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-TIMING)
:   `auto_explain.log_timing` 控制記錄執行計畫時是否輸出每個節點的計時資訊；它等同於 `EXPLAIN` 的 `TIMING` 選項。在某些系統上，重複讀取系統時鐘的額外負擔可能顯著降低查詢速度，因此若只需要實際資料列計數而不需要精確時間，關閉此參數可能有用。除非啟用 `auto_explain.log_analyze`，此參數不會生效。預設為開啟，且只有超級使用者能變更。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-TRIGGERS"></a>

`auto_explain.log_triggers` (`boolean`) <a id="id-1.11.7.13.5.3.7.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-TRIGGERS)
:   `auto_explain.log_triggers` 使記錄執行計畫時包含觸發程序執行統計資訊。除非啟用 `auto_explain.log_analyze`，此參數不會生效。預設為關閉，且只有超級使用者能變更。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-VERBOSE"></a>

`auto_explain.log_verbose` (`boolean`) <a id="id-1.11.7.13.5.3.8.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-VERBOSE)
:   `auto_explain.log_verbose` 控制記錄執行計畫時是否輸出詳細資訊；它等同於 `EXPLAIN` 的 `VERBOSE` 選項。預設為關閉，且只有超級使用者能變更。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-SETTINGS"></a>

`auto_explain.log_settings` (`boolean`) <a id="id-1.11.7.13.5.3.9.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-SETTINGS)
:   `auto_explain.log_settings` 控制記錄執行計畫時是否輸出已修改設定選項的資訊。輸出只包括影響查詢規劃且值不同於內建預設值的選項。此參數預設為關閉，且只有超級使用者能變更。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-FORMAT"></a>

`auto_explain.log_format` (`enum`) <a id="id-1.11.7.13.5.3.10.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-FORMAT)
:   `auto_explain.log_format` 選取要使用的 `EXPLAIN` 輸出格式。允許的值為 `text`、`xml`、`json` 與 `yaml`，預設為 text。只有超級使用者能變更此設定。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-LEVEL"></a>

`auto_explain.log_level` (`enum`) <a id="id-1.11.7.13.5.3.11.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-LEVEL)
:   `auto_explain.log_level` 選取 auto_explain 記錄查詢計畫時使用的日誌層級。有效值為 `DEBUG5`、`DEBUG4`、`DEBUG3`、`DEBUG2`、`DEBUG1`、`INFO`、`NOTICE`、`WARNING` 及 `LOG`，預設為 `LOG`。只有超級使用者能變更此設定。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-NESTED-STATEMENTS"></a>

`auto_explain.log_nested_statements` (`boolean`) <a id="id-1.11.7.13.5.3.12.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-NESTED-STATEMENTS)
:   `auto_explain.log_nested_statements` 使巢狀陳述式（在函式內執行的陳述式）也納入記錄考量。關閉時只記錄最上層查詢計畫。此參數預設為關閉，且只有超級使用者能變更。
<a id="AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-SAMPLE-RATE"></a>

`auto_explain.sample_rate` (`real`) <a id="id-1.11.7.13.5.3.13.1.3"></a> [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-SAMPLE-RATE)
:   `auto_explain.sample_rate` 使 auto_explain 只對每個工作階段中的部分陳述式執行 explain。預設為 1，表示 explain 所有查詢。對巢狀陳述式而言，要麼全部 explain，要麼完全不執行。只有超級使用者能變更此設定。

一般使用時，這些參數會設定在 `postgresql.conf` 中，但超級使用者可在自己的工作階段中即時變更。典型用法如下：

```

# postgresql.conf
session_preload_libraries = 'auto_explain'

auto_explain.log_min_duration = '3s'
```

<a id="AUTO-EXPLAIN-EXAMPLE"></a>

### F.3.2. 範例 [#](#AUTO-EXPLAIN-EXAMPLE)

```

postgres=# LOAD 'auto_explain';
postgres=# SET auto_explain.log_min_duration = 0;
postgres=# SET auto_explain.log_analyze = true;
postgres=# SELECT count(*)
           FROM pg_class, pg_index
           WHERE oid = indrelid AND indisunique;
```

這可能產生如下的日誌輸出：

```

LOG:  duration: 3.651 ms  plan:
  Query Text: SELECT count(*)
              FROM pg_class, pg_index
              WHERE oid = indrelid AND indisunique;
  Aggregate  (cost=16.79..16.80 rows=1 width=0) (actual time=3.626..3.627 rows=1.00 loops=1)
    ->  Hash Join  (cost=4.17..16.55 rows=92 width=0) (actual time=3.349..3.594 rows=92.00 loops=1)
          Hash Cond: (pg_class.oid = pg_index.indrelid)
          ->  Seq Scan on pg_class  (cost=0.00..9.55 rows=255 width=4) (actual time=0.016..0.140 rows=255.00 loops=1)
          ->  Hash  (cost=3.02..3.02 rows=92 width=4) (actual time=3.238..3.238 rows=92.00 loops=1)
                Buckets: 1024  Batches: 1  Memory Usage: 4kB
                ->  Seq Scan on pg_index  (cost=0.00..3.02 rows=92 width=4) (actual time=0.008..3.187 rows=92.00 loops=1)
                      Filter: indisunique
```

<a id="AUTO-EXPLAIN-AUTHOR"></a>

### F.3.3. 作者 [#](#AUTO-EXPLAIN-AUTHOR)

Takahiro Itagaki `<itagaki.takahiro@oss.ntt.co.jp>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auto-explain.html)
