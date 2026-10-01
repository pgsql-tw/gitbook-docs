<a id="id-1.9.3.184.1"></a>

## VACUUM

VACUUM — 資料庫的垃圾回收，並可選擇進行分析

<a id="id-1.9.3.184.2"></a>

## 語法

```

VACUUM [ ( option [, ...] ) ] [ table_and_columns [, ...] ]

where option can be one of:

    FULL [ boolean ]
    FREEZE [ boolean ]
    VERBOSE [ boolean ]
    ANALYZE [ boolean ]
    DISABLE_PAGE_SKIPPING [ boolean ]
    SKIP_LOCKED [ boolean ]
    INDEX_CLEANUP { AUTO | ON | OFF }
    PROCESS_MAIN [ boolean ]
    PROCESS_TOAST [ boolean ]
    TRUNCATE [ boolean ]
    PARALLEL integer
    SKIP_DATABASE_STATS [ boolean ]
    ONLY_DATABASE_STATS [ boolean ]
    BUFFER_USAGE_LIMIT size

and table_and_columns is:

    [ ONLY ] table_name [ * ] [ ( column_name [, ...] ) ]
```

<a id="id-1.9.3.184.5"></a>

## 說明

`VACUUM` 會回收被死亡資料列所佔用的儲存空間。
在 PostgreSQL 正常運作下，被刪除或因更新而過時的
資料列，並不會立即從資料表中實體移除；它們會一直存在，
直到執行了一次 `VACUUM` 為止。因此，定期執行
`VACUUM` 是必要的，特別是在頻繁更新的資料表上。

若沒有指定 *`table_and_columns`*
清單，`VACUUM` 會處理目前資料庫中，目前使用者
有權限清理的每一個資料表與具體化檢視表。若指定了清單，
`VACUUM` 就只會處理清單中的資料表。

`VACUUM ANALYZE` 會對每個選定的資料表執行一次
`VACUUM`，接著再執行一次 `ANALYZE`。
這是例行維護指令稿中很方便的組合形式。詳情請參閱
[ANALYZE](sql-analyze.md)。

單純的 `VACUUM`（不含 `FULL`）只會回收空間，
並讓該空間可供重複使用。這種形式的指令可以與資料表上
正常的讀寫操作並行運作，因為它不會取得獨佔鎖。不過，
額外釋出的空間（在大多數情況下）不會歸還給作業系統；
它只會在同一個資料表內保留下來，供之後重複使用。它也讓我們
得以運用多顆 CPU 來處理索引，這項功能稱為*平行清理（parallel
vacuum）*。若要停用這項功能，可以使用 `PARALLEL`
選項，並將平行工作程序數指定為零。`VACUUM FULL`
會將資料表的整個內容重寫到一個沒有多餘空間的新磁碟檔案中，
讓未使用的空間得以歸還給作業系統。這種形式的速度慢得多，
且在處理期間需要對每個資料表取得 `ACCESS EXCLUSIVE`
鎖。

<a id="id-1.9.3.184.6"></a>

## 參數

`FULL`
:   選擇「完整」清理，這可以回收更多空間，
    但耗時長得多，且會對資料表取得獨佔鎖。這個方式也需要
    額外的磁碟空間，因為它會寫入資料表的一份新副本，
    且在操作完成前不會釋放舊副本。通常只有在需要從資料表中
    回收大量空間時，才應該使用這個選項。

`FREEZE`
:   選擇對資料列進行積極的「凍結」。指定
    `FREEZE` 等同於在執行 `VACUUM` 時，
    將
    [vacuum_freeze_min_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-FREEZE-MIN-AGE)
    與
    [vacuum_freeze_table_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-FREEZE-TABLE-AGE)
    參數都設為零。當資料表被重寫時，一律會執行積極凍結，
    因此指定 `FULL` 時，這個選項就顯得多餘。

`VERBOSE`
:   以 `INFO` 層級，針對每個資料表輸出詳細的清理活動報告。

`ANALYZE`
:   更新規劃器用來判定執行查詢最有效率方式的統計資訊。

`DISABLE_PAGE_SKIPPING`
:   一般而言，`VACUUM` 會根據
    [能見度對照表](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-VISIBILITY-MAP)
    略過某些頁面。已知全部資料列都已凍結的頁面永遠可以略過，
    而已知全部資料列對所有交易皆可見的頁面，除了在執行
    積極清理時之外，也可以略過。此外，除了在執行積極清理時
    之外，有些頁面可能會為了避免等待其他工作階段使用完畢
    而被略過。這個選項會停用所有的頁面略過行為，
    只有在能見度對照表的內容可疑時才應該使用，
    而這種情況應該只會在硬體或軟體問題導致資料庫損毀時發生。

`SKIP_LOCKED`
:   指定 `VACUUM` 在開始處理某個關聯之前，
    不應等待任何衝突的鎖被釋放：若某個關聯無法立即取得鎖
    而不需等待，就會略過該關聯。請注意，即使指定了這個選項，
    `VACUUM` 在開啟關聯的索引時仍可能會阻塞。此外，
    `VACUUM ANALYZE` 在從分割區、資料表繼承子系，
    以及某些型別的外部資料表中取樣資料列時，仍可能會阻塞。
    另外，雖然 `VACUUM` 通常會處理指定分割表的
    所有分割區，但若該分割表上存在衝突的鎖，
    這個選項會使 `VACUUM` 略過所有分割區。

`INDEX_CLEANUP`
:   一般而言，當資料表中的死亡資料列非常少時，
    `VACUUM` 會略過索引清理。在這種情況下，
    處理資料表所有索引的成本，預期會遠遠超過移除死亡索引項目
    所帶來的效益。這個選項可用來強制 `VACUUM`
    在死亡資料列數超過零時處理索引。預設值為
    `AUTO`，會讓 `VACUUM` 在適當時
    略過索引清理。若 `INDEX_CLEANUP` 設為
    `ON`，`VACUUM` 就會保守地
    移除索引中所有的死亡資料列。這對於要與較早版本的
    PostgreSQL（其標準行為即是如此）維持向後相容性
    可能會很有用。

    `INDEX_CLEANUP` 也可以設為
    `OFF`，強制 `VACUUM`
    *一律*略過索引清理，即使資料表中有許多死亡資料列
    也一樣。當有必要讓 `VACUUM` 盡可能快速執行，
    以避免即將發生的交易 ID 回捲時，這可能會很有用
    （參閱[第 24.1.5 節](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)）。
    不過，由
    [vacuum_failsafe_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-FAILSAFE-AGE)
    所控制的回捲失效保護機制，一般會自動觸發，以避免交易 ID
    回捲失敗，因此通常應優先採用該機制。若未定期執行索引清理，
    效能可能會受影響，因為隨著資料表被修改，索引會累積
    死亡項目，而資料表本身也會累積死亡的行指標，這些行指標
    要等到索引清理完成才能被移除。

    這個選項對沒有索引的資料表沒有作用，且若使用了
    `FULL` 選項，這個選項就會被忽略。它對交易 ID
    回捲失效保護機制也沒有作用。當該機制被觸發時，
    即使 `INDEX_CLEANUP` 設為 `ON`，
    它仍會略過索引清理。

`PROCESS_MAIN`
:   指定 `VACUUM` 應嘗試處理主要關聯。
    這通常是所需的行為，也是預設值。若只需要清理某個關聯
    對應的 `TOAST` 資料表，將這個選項設為 false
    可能會很有用。

`PROCESS_TOAST`
:   指定 `VACUUM` 應嘗試處理每個關聯所對應的
    `TOAST` 資料表（若存在）。這通常是所需的行為，
    也是預設值。若只需要清理主要關聯，將這個選項設為 false
    可能會很有用。使用 `FULL` 選項時，
    此選項為必要項目，無法停用。

`TRUNCATE`
:   指定 `VACUUM` 應嘗試截斷資料表末端的任何空頁，
    並讓被截斷頁面所佔用的磁碟空間歸還給作業系統。
    除非
    [vacuum_truncate](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-TRUNCATE)
    被設為 false，或是要清理的資料表已將
    `vacuum_truncate` 選項設為 false，
    否則這通常是所需的行為，也是預設值。若要避免截斷動作
    所需的 `ACCESS EXCLUSIVE` 鎖，將這個選項設為
    false 可能會很有用。若使用了 `FULL` 選項，
    這個選項就會被忽略。

`PARALLEL`
:   使用 *`integer`* 個背景工作程序，
    以平行方式執行 `VACUUM` 的索引清理與索引清潔
    階段（關於各個清理階段的細節，請參閱
    [表 27.46](../../server-administration/monitoring/progress-reporting.md#VACUUM-PHASES)）。
    用來執行此操作的工作程序數量，等於該關聯上支援平行清理
    的索引數量，並受限於（若有指定）`PARALLEL`
    選項所指定的工作程序數，而該數量又進一步受限於
    [max_parallel_maintenance_workers](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS)。
    只有當索引大小超過
    [min_parallel_index_scan_size](../../server-administration/runtime-config/runtime-config-query.md#GUC-MIN-PARALLEL-INDEX-SCAN-SIZE)
    時，該索引才能參與平行清理。請注意，並不保證執行期間
    會使用 *`integer`* 中指定的平行工作程序數量。
    清理有可能使用比指定數量更少的工作程序執行，
    甚至完全不使用任何工作程序。每個索引只能使用一個工作程序。
    因此，只有當資料表中至少有 `2` 個索引時，
    才會啟動平行工作程序。清理用的工作程序會在每個階段開始前
    啟動，並在該階段結束時退出。這些行為在未來版本中可能會改變。
    這個選項不能與 `FULL` 選項一起使用。

`SKIP_DATABASE_STATS`
:   指定 `VACUUM` 應略過更新關於最舊未凍結 XID 的
    資料庫層級統計資訊。一般而言，`VACUUM` 會在
    指令結束時更新這些統計資訊一次。然而，在資料表數量非常多
    的資料庫中，這可能會耗費一些時間，而且除非包含最舊未凍結
    XID 的資料表也在這次清理範圍內，否則不會有任何效果。
    此外，若同時並行發出多個 `VACUUM` 指令，
    一次只能有其中一個更新資料庫層級的統計資訊。因此，
    若應用程式打算依序發出一連串多個 `VACUUM`
    指令，除了最後一個以外，在其餘每個指令中設定這個選項
    會很有幫助；或者也可以在所有指令中都設定這個選項，
    並在之後另外發出一次
    `VACUUM (ONLY_DATABASE_STATS)`。

`ONLY_DATABASE_STATS`
:   指定 `VACUUM` 除了更新關於最舊未凍結 XID 的
    資料庫層級統計資訊之外，不執行任何其他動作。指定這個選項時，
    *`table_and_columns`* 清單必須為空，
    且除了 `VERBOSE` 之外，不能啟用任何其他選項。

`BUFFER_USAGE_LIMIT`
:   指定 `VACUUM` 所使用的
    [*[緩衝區存取策略](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)*](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)
    環狀緩衝區大小。這個大小用來計算此策略中將重複使用的
    共享緩衝區數量。`0` 會停用
    `Buffer Access Strategy` 的使用。若同時指定了
    `ANALYZE`，`BUFFER_USAGE_LIMIT` 的值
    會同時套用於清理與分析兩個階段。這個選項不能與
    `FULL` 選項一起使用，除非同時也指定了
    `ANALYZE`。若未指定這個選項，`VACUUM`
    會使用
    [vacuum_buffer_usage_limit](../../server-administration/runtime-config/runtime-config-resource.md#GUC-VACUUM-BUFFER-USAGE-LIMIT)
    的值。設定較高的值可以讓 `VACUUM` 執行得更快，
    但設定過大的值，可能會導致其他有用的頁面被逐出共享緩衝區。
    最小值為 `128 kB`，最大值為 `16 GB`。

*`boolean`*
:   指定所選選項應開啟或關閉。你可以寫
    `TRUE`、`ON` 或
    `1` 來啟用該選項，寫
    `FALSE`、`OFF` 或
    `0` 來停用它。也可以省略
    *`boolean`* 值，此時會假定為
    `TRUE`。

*`integer`*
:   指定傳遞給所選選項的非負整數值。

*`size`*
:   以千位元組指定記憶體大小。大小也可以指定為一個字串，
    內容為數值大小後接以下任一記憶體單位：
    `B`（位元組）、
    `kB`（千位元組）、`MB`（百萬位元組）、
    `GB`（十億位元組）或 `TB`（兆位元組）。

*`table_name`*
:   要清理的特定資料表或具體化檢視表名稱（可加上結構描述限定）。
    若在資料表名稱前指定了 `ONLY`，則只會清理該資料表。
    若未指定 `ONLY`，則該資料表及其所有繼承子系資料表
    或分割區（若有）也會一併被清理。也可以選擇在資料表名稱後
    指定 `*`，以明確表示要清理繼承子系資料表（或分割區）。

*`column_name`*
:   要分析的特定欄位名稱。預設為所有欄位。若指定了欄位清單，
    則也必須指定 `ANALYZE`。

<a id="id-1.9.3.184.7"></a>

## 輸出

指定 `VERBOSE` 時，`VACUUM` 會發出進度訊息，
指出目前正在處理哪個資料表。同時也會列印關於這些資料表的
各項統計資訊。

<a id="id-1.9.3.184.8"></a>

## 注意事項

要清理一個資料表，通常必須擁有該資料表的 `MAINTAIN`
權限。不過，資料庫擁有者可以清理其資料庫中的所有資料表，
共享目錄除外。`VACUUM` 會略過呼叫端使用者
沒有清理權限的任何資料表。

`VACUUM` 執行期間，
[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH)
會暫時被改為 `pg_catalog, pg_temp`。

`VACUUM` 無法在交易區塊內執行。

對於擁有 GIN 索引的資料表，`VACUUM`（任何形式）
也會完成所有待處理的索引插入，將待處理的索引項目移動到
主要 GIN 索引結構中的適當位置。詳情請參閱
[第 65.4.4.1 節](../../internals/indextypes/gin.md#GIN-FAST-UPDATE)。

我們建議定期清理所有資料庫，以移除死亡資料列。
PostgreSQL 提供了「autovacuum」設施，
可以自動執行例行清理維護工作。關於自動與手動清理的更多資訊，
請參閱[第 24.1 節](../../server-administration/maintenance/routine-vacuuming.md)。

不建議在例行使用中採用 `FULL` 選項，
但在特殊情況下可能會很有用。舉例來說，當你已刪除或更新了
資料表中大部分的資料列，並希望該資料表能實際縮小、
佔用較少磁碟空間、並讓資料表掃描更快時，就適合使用。
`VACUUM FULL` 通常會比單純的 `VACUUM`
更能縮小資料表的大小。

`PARALLEL` 選項僅用於清理用途。若這個選項與
`ANALYZE` 選項一起指定，並不會影響
`ANALYZE`。

`VACUUM` 會導致 I/O 流量大幅增加，這可能會導致
其他活躍工作階段的效能變差。因此，有時建議使用以成本為基礎的
清理延遲功能。在平行清理中，每個工作程序會依其已完成的工作量
按比例休眠。詳情請參閱
[第 19.10.2 節](../../server-administration/runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)。

每個執行不含 `FULL` 選項之 `VACUUM`
的後端程序，都會在 `pg_stat_progress_vacuum`
檢視表中回報其進度。執行 `VACUUM FULL`
的後端程序，則會改在 `pg_stat_progress_cluster`
檢視表中回報進度。詳情請參閱
[第 27.4.5 節](../../server-administration/monitoring/progress-reporting.md#VACUUM-PROGRESS-REPORTING)
與
[第 27.4.2 節](../../server-administration/monitoring/progress-reporting.md#CLUSTER-PROGRESS-REPORTING)。

<a id="id-1.9.3.184.9"></a>

## 範例

清理單一資料表 `onek`，為最佳化工具進行分析，
並印出詳細的清理活動報告：

```

VACUUM (VERBOSE, ANALYZE) onek;
```

<a id="id-1.9.3.184.10"></a>

## 相容性

SQL 標準中沒有 `VACUUM` 陳述式。

以下語法曾在 PostgreSQL 9.0 之前的版本中使用，
目前仍受支援：

```

VACUUM [ FULL ] [ FREEZE ] [ VERBOSE ] [ ANALYZE ] [ table_and_columns [, ...] ]
```

請注意，在這種語法中，選項必須依照上述顯示的順序指定。

<a id="id-1.9.3.184.11"></a>

## 參見

[vacuumdb](../reference-client/app-vacuumdb.md)、[第 19.10.2 節](../../server-administration/runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)、[第 24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)、[第 27.4.5 節](../../server-administration/monitoring/progress-reporting.md#VACUUM-PROGRESS-REPORTING)、[第 27.4.2 節](../../server-administration/monitoring/progress-reporting.md#CLUSTER-PROGRESS-REPORTING)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-vacuum.html)（原文版本：18.6；核對日期：2026-09-30）
