# F.4. auto\_explain

auto\_explain 模組提供了一種自動記錄慢速語句執行計劃的方法，毌須手動執行 [EXPLAIN](../../reference/sql-commands/explain.md)。這對於在大型應用程序中追踪未最佳化的查詢特別有用。

該模組不提供 SQL 可存取的功能。要使用它，只需將其載入到伺服器中即可。您也可以將其載入到單個連線之中：

```text
LOAD 'auto_explain';
```

（您必須是超級使用者才能這樣做。）更典型的用法是透過在 postgresql.conf 中的 [session\_preload\_libraries](../../server-administration/server-configuration/client-connection-defaults.md#session_preload_libraries-string) 或 [shared\_preload\_libraries](../../server-administration/server-configuration/client-connection-defaults.md#shared_preload_libraries-string) 中包含 auto\_explain 將其預先載入到部分或全部連線中。然後，無論何時發生，您都可以追踪意外緩慢的查詢。當然，會有一些系統代價。

## F.4.1. 組態參數

有幾個組態參數可以控制 auto\_explain 的行為。請注意，預設行為是什麼都不做，因此如果需要任何結果，必須至少設定 auto\_explain.log\_min\_duration。

`auto_explain.log_min_duration` \(`integer`\)

auto\_explain.log\_min\_duration 是記錄語句計劃的最小語句執行時間（以毫秒為單位）。將此設定為零會記錄所有計劃。減號（預設值）停用計劃的記錄。例如，如果將其設定為 250ms，則將記錄執行 250ms 或更長時間的所有語句。只有超級使用者才能變更此設定。

`auto_explain.log_analyze` \(`boolean`\)

auto\_explain.log\_analyze 會在記錄執行計劃時列印 EXPLAIN ANALYZE 輸出，而不僅僅是 EXPLAIN 輸出。預設情況下，此參數處於停用狀態。只有超級使用者才能變更此設定。

{% hint style="info" %}
啟用此參數後，將對所有執行的語句執行每計劃節點計時，無論它們是否執行足夠長時間以實際記錄。這可能會對效能產生極為不利的影響。關閉 auto\_explain.log\_timing 可以獲得較少的訊息，從而改善效能成本。
{% endhint %}

`auto_explain.log_buffers` \(`boolean`\)

auto\_explain.log\_buffers 控制是否在記錄執行計劃時輸出緩衝區使用情況統計訊息；它相當於 EXPLAIN 的 BUFFERS 選項。除非啟用了 auto\_explain.log\_analyze，否則此參數無效。預鉆水情況下，此參數處於停用狀態。只有超級使用者才能變更改此設定。

`auto_explain.log_wal` \(`boolean`\)

auto\_explain.log\_wal 控制在記錄執行計劃時是否輸出 WAL 使用情況統計資訊。它等同於 EXPLAIN 的 WAL 選項。除非啟用了 auto\_explain.log\_analyze，否則此參數無效。預設情況下，此參數是停用的。只有超級使用者可以變更此設定。

`auto_explain.log_timing` \(`boolean`\)

auto\_explain.log\_timing 控制在記錄執行計劃時是否輸出每個節點的計時訊息；它相當於 EXPLAIN 的 TIMING 選項。重複讀取系統時鐘的成本會在某些系統上明顯減慢查詢速度，因此當只需要實際資料列計數而非精確時間計時，將此參數設定為關閉可能很有用。除非啟用了 auto\_explain.log\_analyze，否則此參數無效。預設情況下，此參數處於啟用狀態。只有超級使用者才能變更此設定。

`auto_explain.log_triggers` \(`boolean`\)

auto\_explain.log\_triggers 會在記錄執行計劃時包含觸發器執行統計訊息。除非啟用了 auto\_explain.log\_analyze，否則此參數無效。預設情況下，此參數處於停用狀態。只有超級使用者才能變更此設定。

`auto_explain.log_verbose` \(`boolean`\)

auto\_explain.log\_verbose 控制是否在記錄執行計劃時輸出詳細訊息；它相當於 EXPLAIN 的 VERBOSE 選項。預設情況下，此參數處於停用狀態。只有超級使用者才能變更此設定。

`auto_explain.log_settings` \(`boolean`\)

auto\_explain.log\_settings 控制記錄執行計劃時是否輸出有關被修改的組態選項資訊。輸出中僅包含影響其值與內建預設值不同的查詢計劃的選項。預設情況下，此參數是停用的。 只有超級使用者可以變更此設定。

`auto_explain.log_format` \(`enum`\)

auto\_explain.log\_format 選擇要使用的 EXPLAIN 輸出格式。允許的值為 text、xml、json 和 yaml。預設為 text。只有超級使用者才能變更此設定。

`auto_explain.log_level` \(`enum`\)

auto\_explain.log\_level 選擇 auto\_explain 將記錄查詢計劃的日誌等級。 有效值為 DEBUG5，DEBUG4，DEBUG3，DEBUG2，DEBUG1，INFO，NOTICE，WARNING 和 LOG。預設值為 LOG。只有超級使用者可以變更此設定。

`auto_explain.log_nested_statements` \(`boolean`\)

auto\_explain.log\_nested\_statements 會讓巢狀語句（在函數內執行的語句）記錄下來。關閉時，僅記錄最上層查詢計劃。預設情況下，此參數處於停用狀態。只有超級使用者才能變更此設定。

`auto_explain.sample_rate` \(`real`\)

auto\_explain.sample\_rate 使 auto\_explain 僅解釋每個連線中的一小部分語句。預設值為 1，表示 EXPLAIN 所有查詢。在巢狀語句的情況下，要就全部都要解釋，要就都不解釋。只有超級使用者才能變更此設定。

在一般的用法中，這些參數在 postgresql.conf 中設定，儘管超級使用者可以在他們自己的連線中即時更改它們。典型用法可能是：

```text
# postgresql.conf
session_preload_libraries = 'auto_explain'

auto_explain.log_min_duration = '3s'
```

## F.4.2. 範例

```text
postgres=# LOAD 'auto_explain';
postgres=# SET auto_explain.log_min_duration = 0;
postgres=# SET auto_explain.log_analyze = true;
postgres=# SELECT count(*)
           FROM pg_class, pg_index
           WHERE oid = indrelid AND indisunique;
```

這可能會產生如下的日誌輸出：

```text
LOG:  duration: 3.651 ms  plan:
  Query Text: SELECT count(*)
              FROM pg_class, pg_index
              WHERE oid = indrelid AND indisunique;
  Aggregate  (cost=16.79..16.80 rows=1 width=0) (actual time=3.626..3.627 rows=1 loops=1)
    ->  Hash Join  (cost=4.17..16.55 rows=92 width=0) (actual time=3.349..3.594 rows=92 loops=1)
          Hash Cond: (pg_class.oid = pg_index.indrelid)
          ->  Seq Scan on pg_class  (cost=0.00..9.55 rows=255 width=4) (actual time=0.016..0.140 rows=255 loops=1)
          ->  Hash  (cost=3.02..3.02 rows=92 width=4) (actual time=3.238..3.238 rows=92 loops=1)
                Buckets: 1024  Batches: 1  Memory Usage: 4kB
                ->  Seq Scan on pg_index  (cost=0.00..3.02 rows=92 width=4) (actual time=0.008..3.187 rows=92 loops=1)
                      Filter: indisunique
```

## F.4.3. 作者

Takahiro Itagaki `<`[`itagaki.takahiro@oss.ntt.co.jp`](mailto:itagaki.takahiro@oss.ntt.co.jp)`>`

