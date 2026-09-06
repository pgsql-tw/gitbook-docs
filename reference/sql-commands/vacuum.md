# VACUUM

VACUUM — 資源回收並且選擇性地重整資料庫

## 語法

```
VACUUM [ ( option [, ...] ) ] [ table_and_columns [, ...] ]
VACUUM [ FULL ] [ FREEZE ] [ VERBOSE ] [ ANALYZE ] [ table_and_columns [, ...] ]

where option can be one of:

    FULL [ boolean ]
    FREEZE [ boolean ]
    VERBOSE [ boolean ]
    ANALYZE [ boolean ]
    DISABLE_PAGE_SKIPPING [ boolean ]
    SKIP_LOCKED [ boolean ]
    INDEX_CLEANUP [ boolean ]
    TRUNCATE [ boolean ]
    PARALLEL integer

and table_and_columns is:

    table_name [ ( column_name [, ...] ) ]
```

## 說明

VACUUM 回收不再使用的儲存空間。在普通的 PostgreSQL 操作中，被刪除或被更新的儲存空間實際上並不會真實在磁碟上刪除；它們會一直存在，直到 VACUUM 完成。因此，必須定期執行 VACUUM，尤其是在經常更新的資料表上。

在沒有指定 TABLE 及欄位的情況下，VACUUM 處理目前資料庫中目前使用者有權清理的每個資料表。使用參數的話，VACUUM 就能只處理某個資料表。

VACUUM ANALYZE 為每個選定的資料表執行 VACUUM 然後進行 ANALYZE 分析。 這是日常維護腳本的便捷組合形式。有關其處理的更多詳細訊息，請參閱 [ANALYZE](analyze.md)。

普通的 VACUUM（不帶FULL）只是回收空間並使其可供重複使用。由於沒有獲得排他鎖定，此指令的這種形式可以與正常讀取和寫入資料表平行操作。但是，額外的空間不會還回到作業系統（大多數情況下）。它只是保持在同一張資料表內重新使用。我們可以利用多個 CPU 來處理索引。此功能稱為平行清理 (parallel vacuum)。要停用此功能，可以使用 PARALLEL 選項並將平行工作程序數量指定為零。 VACUUM FULL 會將資料表中的全部內容重寫為新的磁碟檔案，不會遺留額外的空間佔用，可將未使用的空間還回作業系統。這種形式顯然要慢得多，並且在處理每個資料表時需要排它鎖定 (exclusive lock)。

當選項列表被括號包圍時，選項可以按任意順序書寫。如果沒有括號，必須按照上面所示的順序指定選項。PostgreSQL 9.0 中加入了括號語法；未使用括號的語法已被棄用。

## 參數

`FULL`

選擇「FULL」清理，可以回收更多的空間，但需要更長的時間並且會完全鎖定資料表。此方法還需要額外的磁碟空間，因為它會寫入資料表的新的副本，並且在操作完成之前不會釋放舊副本。通常這只能在需要從資料表內回收大量空間時才會使用。

`FREEZE`

選擇積極的「凍結」tuple。指定 FREEZE 等同於使用將 [vacuum\_freeze\_min\_age ](../../server-administration/server-configuration/client-connection-defaults.md#19-11-1-cha-ju-de-hang)和 [vacuum\_freeze\_table\_age](../../server-administration/server-configuration/client-connection-defaults.md#19-11-1-cha-ju-de-hang) 參數設定為零來執行 VACUUM。資料表在重寫時始終執行積極凍結，因此當指定 FULL 時這個選項是多餘的。

`VERBOSE`

為每個資料表輸出詳細的清理活動報告。

`ANALYZE`

更新查詢規劃單元需要使用的統計訊息，以決定最有效執行查詢的方式。

`DISABLE_PAGE_SKIPPING`

通常情況下，VACUUM 將根據可見性記錄跳過頁面。已知所有 tuple 都被凍結的頁面總是可以被跳過，並且所有 tuple 被知道對所有交易事務都可見的頁面也可能會被跳過，除非執行積極的清理。此外，除了執行積極的清理時，可能會跳過某些頁面以避免等待其他連線完成使用。此選項禁用所有頁面跳轉行為，並且僅用於可見性映射的內容被認為是可疑的，只有在存在導致資料庫損壞的硬體或軟體問題時才會發生。

`SKIP_LOCKED`

指定 VACUUM 在開始處理時不要等待任何關連鎖定被釋放：如果不等待就不能立即鎖定關連，則跳過該關連物件。 請注意，即使使用此選項，VACUUM 在處理關連的索引時仍可能會阻塞。 此外，VACUUM ANALYZE 在從分割區、資料表繼承的子項和某些型態的外部資料表中取得樣本行時仍可能會阻塞。 此外，雖然 VACUUM 通常處理指定分割區資料表的所有分割區，但如果分割區資料表上存在衝突鎖定，此選項將導致 VACUUM 跳過所有分割區。

`INDEX_CLEANUP`

Normally, `VACUUM` will skip index vacuuming when there are very few dead tuples in the table. The cost of processing all of the table's indexes is expected to greatly exceed the benefit of removing dead index tuples when this happens. This option can be used to force `VACUUM` to process indexes when there are more than zero dead tuples. The default is `AUTO`, which allows `VACUUM` to skip index vacuuming when appropriate. If `INDEX_CLEANUP` is set to `ON`, `VACUUM` will conservatively remove all dead tuples from indexes. This may be useful for backwards compatibility with earlier releases of PostgreSQL where this was the standard behavior.

`INDEX_CLEANUP` can also be set to `OFF` to force `VACUUM` to _always_ skip index vacuuming, even when there are many dead tuples in the table. This may be useful when it is necessary to make `VACUUM` run as quickly as possible to avoid imminent transaction ID wraparound (see [Section 25.1.5](https://www.postgresql.org/docs/current/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND)). However, the wraparound failsafe mechanism controlled by [vacuum\_failsafe\_age](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-VACUUM-FAILSAFE-AGE) will generally trigger automatically to avoid transaction ID wraparound failure, and should be preferred. If index cleanup is not performed regularly, performance may suffer, because as the table is modified indexes will accumulate dead tuples and the table itself will accumulate dead line pointers that cannot be removed until index cleanup is completed.

This option has no effect for tables that have no index and is ignored if the `FULL` option is used. It also has no effect on the transaction ID wraparound failsafe mechanism. When triggered it will skip index vacuuming, even when `INDEX_CLEANUP` is set to `ON`.

`PROCESS_TOAST`

Specifies that `VACUUM` should attempt to process the corresponding `TOAST` table for each relation, if one exists. This is usually the desired behavior and is the default. Setting this option to false may be useful when it is only necessary to vacuum the main relation. This option is required when the `FULL` option is used.

`TRUNCATE`

Specifies that `VACUUM` should attempt to truncate off any empty pages at the end of the table and allow the disk space for the truncated pages to be returned to the operating system. This is normally the desired behavior and is the default unless the `vacuum_truncate` option has been set to false for the table to be vacuumed. Setting this option to false may be useful to avoid `ACCESS EXCLUSIVE` lock on the table that the truncation requires. This option is ignored if the `FULL` option is used.

`PARALLEL`

Perform index vacuum and index cleanup phases of `VACUUM` in parallel using _`integer`_ background workers (for the details of each vacuum phase, please refer to [Table 28.41](https://www.postgresql.org/docs/current/progress-reporting.html#VACUUM-PHASES)). The number of workers used to perform the operation is equal to the number of indexes on the relation that support parallel vacuum which is limited by the number of workers specified with `PARALLEL` option if any which is further limited by [max\_parallel\_maintenance\_workers](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS). An index can participate in parallel vacuum if and only if the size of the index is more than [min\_parallel\_index\_scan\_size](https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-MIN-PARALLEL-INDEX-SCAN-SIZE). Please note that it is not guaranteed that the number of parallel workers specified in _`integer`_ will be used during execution. It is possible for a vacuum to run with fewer workers than specified, or even with no workers at all. Only one worker can be used per index. So parallel workers are launched only when there are at least `2` indexes in the table. Workers for vacuum are launched before the start of each phase and exit at the end of the phase. These behaviors might change in a future release. This option can't be used with the `FULL` option.

_`boolean`_

Specifies whether the selected option should be turned on or off. You can write `TRUE`, `ON`, or `1` to enable the option, and `FALSE`, `OFF`, or `0` to disable it. The _`boolean`_ value can also be omitted, in which case `TRUE` is assumed.

_`integer`_

Specifies a non-negative integer value passed to the selected option.

_`table_name`_

要清理的特定資料表名稱（可選擇性加上綱要）。如果省略，則目前資料庫中的所有常態的資料表和具體化檢視表都會被清理。如果指定的資料表是分割資料表，則其所有子分區都將被清理。

_`column_name`_

要分析的特定欄位的名稱。預設為所有欄位。 如果指定了列表，則隱含 ANALYZE。

## 輸出

當指定 VERBOSE 時，VACUUM 發出進度訊息以表示目前正在處理哪個資料表。有關資料表的各種統計訊息也會顯示出來。

## 注意

要清理資料表，通常必須是資料表的擁有者或超級使用者。但是，資料庫擁有者可以清理資料庫中的所有資料表，共享目錄除外。（對共享目錄的限制意味著真正的資料庫範圍內的 VACUUM 只能由超級使用者執行。）VACUUM 將跳過無權清理的所有資料表。

VACUUM 不能在交易事務區塊內執行。

對於具有 GIN 索引的資料表，透過將掛起的索引項目移動到主 GIN 索引結構中的適當位置，VACUUM（以任何形式）還是可以完成任何掛起的索引插入。詳情請參閱[第 70.4.1 節](../../internals/gin-indexes/implementation.md#64-4-1-gin-fast-update-technique)。

我們建議定期清理所有資料庫以淘汰 dead row。 PostgreSQL 有一個「autovacuum」的功能，可以自動執行日常清理維護。有關自動和手動清理的更多說明，請參閱[第 25.1 節](../../server-administration/routine-database-maintenance-tasks/routine-vacuuming.md)。

FULL 選項不推薦於日常使用，但在特殊情況下可能會有用。例如，您刪除或更新了資料表中的大部分資料列，並且希望資料表在物理上縮小以佔用較少的磁碟空間以允許更快的資料表掃描。VACUUM FULL 通常會縮小資料表，而不是簡單的 VACUUM。

PARALLEL 選項僅用於單純的清理目的。 如果此選項與 ANALYZE 選項一起使用話，則也不會影響 ANALYZE。

VACUUM 會導致 I/O 流量大幅增加，這可能會導致其他連線活動的效能下降。因此，有時建議使用基於成本的清理延遲功能。詳情請參閱[第 20.4.4 節](../../server-administration/server-configuration/resource-consumption.md#19-4-4-cost-based-vacuum-delay)。

每個執行沒有 FULL 選項的 VACUUM 的後端都可以在 pg\_stat\_progress\_vacuum 檢視表中回報它的進度。 執行 VACUUM FULL 的後端將改為在 pg\_stat\_progress\_cluster 檢視表中回報它們的進度。 有關詳細說明，請參閱[第 28.4.3 節](../../server-administration/monitoring-database-activity/progress-reporting.md#28.4.3.-vacuum-progress-reporting)和[第 28.4.4 節](../../server-administration/monitoring-database-activity/progress-reporting.md#28.4.4.-cluster-progress-reporting)。

## 範例

要清理單個資料表，請為其進行最佳化程序分析並輸出詳細的清理活動報告：

```
VACUUM (VERBOSE, ANALYZE) onek;
```

## 相容性

SQL 標準中並沒有 VACUUM 語句。

## 參閱

[vacuumdb](../client-applications/vacuumdb.md), [Section 20.4.4](../../server-administration/server-configuration/resource-consumption.md#19.4.4.-cheng-ben-kao-liang-de-vacuum-yan-chi), [Section 25.1.6](../../server-administration/routine-database-maintenance-tasks/routine-vacuuming.md#25.1.6.-autovacuum-bei-jing-cheng-xu), [Section 28.4.3](../../server-administration/monitoring-database-activity/progress-reporting.md#28.4.3.-vacuum-progress-reporting), [Section 28.4.4](../../server-administration/monitoring-database-activity/progress-reporting.md#28.4.4.-cluster-progress-reporting)
