<a id="SQL-ANALYZE"></a><a id="id-1.9.3.46.1"></a>

## ANALYZE

ANALYZE — 收集資料庫的統計資訊

<a id="id-1.9.3.46.4"></a>

## 語法

```

ANALYZE [ ( option [, ...] ) ] [ table_and_columns [, ...] ]

where option can be one of:

    VERBOSE [ boolean ]
    SKIP_LOCKED [ boolean ]
    BUFFER_USAGE_LIMIT size

and table_and_columns is:

    [ ONLY ] table_name [ * ] [ ( column_name [, ...] ) ]
```

<a id="id-1.9.3.46.5"></a>

## 說明

`ANALYZE` 會收集資料庫中資料表內容的統計資訊，並將結果儲存在 [`pg_statistic`](../../internals/catalogs/catalog-pg-statistic.md) 系統目錄中。之後，查詢規劃器會使用這些統計資訊，協助判斷查詢最有效率的執行計畫。

若沒有 *`table_and_columns`* 清單，`ANALYZE` 會處理目前資料庫中，目前使用者有權限分析的每一個資料表與具體化檢視表。若有清單，`ANALYZE` 只會處理清單中的資料表。此外，也可以為資料表提供欄位名稱清單，此時只會收集那些欄位的統計資訊。

<a id="id-1.9.3.46.6"></a>

## 參數

`VERBOSE`
:   啟用以 `INFO` 層級顯示進度訊息。

`SKIP_LOCKED`
:   指定 `ANALYZE` 在開始處理某個關聯時，不應等待任何衝突的鎖定被釋放：若某個關聯無法在不等待的情況下立即鎖定，就會略過該關聯。請注意，即使使用此選項，`ANALYZE` 在開啟關聯的索引時，或從分割區、資料表繼承子系以及某些類型的外部資料表取得樣本資料列時，仍然可能被阻擋。此外，雖然 `ANALYZE` 通常會處理指定分割資料表的所有分割區，但若分割資料表上有衝突的鎖定，此選項會使 `ANALYZE` 略過所有分割區。

`BUFFER_USAGE_LIMIT`
:   指定 `ANALYZE` 所使用的
    [*[緩衝區存取策略](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)*](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)
    環狀緩衝區大小。這個大小用來計算此策略中將重複使用的共享緩衝區數量。`0` 會停用 `Buffer Access Strategy` 的使用。若未指定這個選項，`ANALYZE` 會使用 [vacuum_buffer_usage_limit](../../server-administration/runtime-config/runtime-config-resource.md#GUC-VACUUM-BUFFER-USAGE-LIMIT) 的值。設定較高的值可以讓 `ANALYZE` 執行得更快，但設定過大的值，可能會導致其他太多有用的頁面被逐出共享緩衝區。最小值為 `128 kB`，最大值為 `16 GB`。

*`boolean`*
:   指定所選選項應開啟或關閉。你可以寫 `TRUE`、`ON` 或 `1` 來啟用該選項，寫 `FALSE`、`OFF` 或 `0` 來停用它。也可以省略 *`boolean`* 值，此時會假定為 `TRUE`。

*`size`*
:   以千位元組指定記憶體大小。大小也可以指定為一個字串，內容為數值大小後接以下任一記憶體單位：`B`（位元組）、`kB`（千位元組）、`MB`（百萬位元組）、`GB`（十億位元組）或 `TB`（兆位元組）。

*`table_name`*
:   要分析的特定資料表名稱（可能以綱要限定）。若省略，則會分析目前資料庫中所有一般資料表、分割資料表與具體化檢視表（但不包括外部資料表）。若在資料表名稱前指定了 `ONLY`，則只會分析該資料表。若未指定 `ONLY`，則會分析該資料表及其所有繼承子系資料表或分割區（若有）。也可以選擇在資料表名稱後指定 `*`，以明確表示要分析繼承子系資料表（或分割區）。

*`column_name`*
:   要分析的特定欄位名稱。預設為所有欄位。

<a id="id-1.9.3.46.7"></a>

## 輸出

指定 `VERBOSE` 時，`ANALYZE` 會發出進度訊息，指出目前正在處理哪個資料表。同時也會列印關於這些資料表的各項統計資訊。

<a id="id-1.9.3.46.8"></a>

## 注意事項

要分析資料表，通常必須擁有該資料表的 `MAINTAIN` 權限。不過，資料庫擁有者可以分析其資料庫中的所有資料表，共享系統目錄除外。`ANALYZE` 會略過呼叫的使用者沒有權限分析的任何資料表。

外部資料表只有在被明確選取時才會被分析。並非所有外部資料包裝器都支援 `ANALYZE`。若資料表的包裝器不支援 `ANALYZE`，此命令會印出警告且不做任何事。

在 PostgreSQL 的預設設定中，autovacuum 常駐程式（請參閱[第 24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)）會在資料表首次載入資料時，以及在一般運作過程中資料表內容變動時，負責自動分析資料表。停用 autovacuum 時，定期執行 `ANALYZE`，或在大幅變更資料表內容之後立即執行，是個好主意。準確的統計資訊有助於規劃器選擇最合適的查詢計畫，從而提升查詢處理的速度。對於以讀取為主的資料庫，常見的策略是每天在使用量低的時段執行一次 [`VACUUM`](sql-vacuum.md) 與 `ANALYZE`。（若更新活動頻繁，這樣做並不足夠。）

`ANALYZE` 執行期間，[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 會暫時變更為 `pg_catalog,
pg_temp`。

`ANALYZE` 只需要目標資料表上的讀取鎖定，因此可以與該資料表上其他非 DDL 的活動並行執行。

`ANALYZE` 收集的統計資訊通常包括每個欄位中一些最常見值的清單，以及顯示每個欄位近似資料分布的直方圖。若 `ANALYZE` 認為它們沒有意義（例如，唯一鍵欄位中沒有常見值），或欄位資料型別不支援適當的運算子，則可能省略其中一項或兩項。關於統計資訊的更多資訊，請參閱[第 24 章](../../server-administration/maintenance/README.md)。

對於大型資料表，`ANALYZE` 會隨機抽樣資料表內容，而不是檢查每一筆資料列。這使得即使是非常大的資料表，也能在短時間內完成分析。但請注意，統計資訊只是近似值，而且即使實際的資料表內容沒有變更，每次執行 `ANALYZE` 時也會略有不同。這可能導致 [`EXPLAIN`](sql-explain.md) 所顯示之規劃器估計成本出現小幅變化。在少數情況下，這種不確定性會導致規劃器在執行 `ANALYZE` 之後改變所選擇的查詢計畫。為避免這種情況，請依下文所述，提高 `ANALYZE` 所收集的統計資訊量。

分析的範圍可以透過調整 [default_statistics_target](../../server-administration/runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET) 設定變數來控制，或以 [`ALTER TABLE ... ALTER COLUMN ... SET
STATISTICS`](sql-altertable.md) 設定每個欄位的統計目標，逐欄控制。目標值會設定最常見值清單中的最大項目數，以及直方圖中的最大區間數。預設目標值為 100，但可以向上或向下調整，在規劃器估計的準確度，與 `ANALYZE` 所花費的時間及在 `pg_statistic` 中所佔用的空間之間取捨。特別是，將統計目標設為零，會停用該欄位的統計資訊收集。對於從未用於查詢之 `WHERE`、`GROUP BY` 或 `ORDER BY` 子句中的欄位，這樣做可能會很有用，因為規劃器不會用到這類欄位的統計資訊。

在被分析的欄位中，最大的統計目標決定了為準備統計資訊而抽樣的資料表資料列數。提高目標值會使執行 `ANALYZE` 所需的時間與空間成比例增加。

`ANALYZE` 所估計的值之一，是每個欄位中出現的相異值數量。由於只檢查了部分資料列，即使使用最大的統計目標，這個估計值有時仍可能相當不準確。若這種不準確導致不佳的查詢計畫，可以手動求得較準確的值，再以 [`ALTER TABLE ... ALTER COLUMN ... SET (n_distinct = ...)`](sql-altertable.md) 設定。

若被分析的資料表有繼承子系，`ANALYZE` 會收集兩組統計資訊：一組只針對父資料表的資料列，另一組則同時包含父資料表及其所有子系的資料列。規劃將繼承樹作為整體處理的查詢時，需要第二組統計資訊。然而，autovacuum 常駐程式在決定是否要對某個資料表觸發自動分析時，只會考慮該父資料表本身的插入或更新。若該資料表很少被插入或更新，除非你手動執行 `ANALYZE`，否則繼承統計資訊將不會是最新的。預設情況下，`ANALYZE` 也會遞迴收集並更新每個繼承子系資料表的統計資訊。可以使用 `ONLY` 關鍵字停用此行為。

對於分割資料表，`ANALYZE` 會從所有分割區抽樣資料列來收集統計資訊。預設情況下，`ANALYZE` 也會遞迴收集並更新每個分割區的統計資訊。可以使用 `ONLY` 關鍵字停用此行為。

autovacuum 常駐程式不會處理分割資料表；若始終只修改子系，它也不會處理繼承父資料表。通常需要定期手動執行 `ANALYZE`，以使資料表階層的統計資訊保持最新。

若有任何子系資料表或分割區是外部資料表，而其外部資料包裝器不支援 `ANALYZE`，則在收集繼承統計資訊時會忽略這些資料表。

若被分析的資料表完全為空，`ANALYZE` 不會為該資料表記錄新的統計資訊。任何既有的統計資訊都會保留。

每個執行 `ANALYZE` 的後端都會在 `pg_stat_progress_analyze` 檢視表中回報其進度。詳情請參閱[第 27.4.1 節](../../server-administration/monitoring/progress-reporting.md#ANALYZE-PROGRESS-REPORTING)。

<a id="id-1.9.3.46.9"></a>

## 相容性

SQL 標準中沒有 `ANALYZE` 陳述式。

下列語法在 PostgreSQL 第 11 版之前使用，目前仍受支援：

```

ANALYZE [ VERBOSE ] [ table_and_columns [, ...] ]
```

<a id="id-1.9.3.46.10"></a>

## 另請參閱

[VACUUM](sql-vacuum.md), [vacuumdb](../reference-client/app-vacuumdb.md), [第 19.10.2 節](../../server-administration/runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST), [第 24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM), [第 27.4.1 節](../../server-administration/monitoring/progress-reporting.md#ANALYZE-PROGRESS-REPORTING)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-analyze.html)（原文版本：18.6；核對日期：2026-10-04）
