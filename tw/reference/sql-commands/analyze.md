# ANALYZE

ANALYZE — 收集有關資料庫的統計資訊

### 語法

```text
ANALYZE [ VERBOSE ] [ table_name [ ( column_name [, ...] ) ] ]
```

### 說明

ANALYZE 收集有關資料庫中資料表內容的統計資訊，並將結果儲在在 pg\_statistic 系統目錄中。然後，查詢計劃程序會使用這些統計資訊來幫助決定查詢的最有效執行計劃。

如果沒有參數，ANALYZE 會檢查目前資料庫中的每個資料表。使用參數時，ANALYZE 僅檢查該資料表。還可以輸出欄位名稱列表，在這種情況下，僅收集這些欄位的統計資訊。

### 參數

`VERBOSE`

啟用進度訊息的顯示。

_`table_name`_

要分析的特定資料表的名稱（可以加入綱要名稱）。如果省略，則分析目前資料庫中的所有一般資料表，分割資料表和具體化檢視表（但不包括外部資料表）。如果指定的資料表是分割資料表，則更新分割資料表的繼承統計資訊和各個分割區的統計資訊。

_`column_name`_

要分析特定欄位的名稱。預設為所有欄位。

### 輸出

指定 VERBOSE 時，ANALYZE 會輸出進度訊息以顯示目前正在處理哪個資料表。還會列出有關資料表的各種統計資訊。

### 注意

僅在明確選擇時才會分析外部資料表。並非所有外部資料封裝器都支援 ANALYZE。如果資料表的封裝器不支援 ANALYZE，則該命令只會輸出警告並且不執行任何操作。

在預設的 PostgreSQL 配置中，autovacuum 背景程序（參閱[第 24.1.6 節](../../server-administration/routine-database-maintenance-tasks/routine-vacuuming.md#24-1-6-autovacuum-bei-jing-cheng-xu)）負責在資料表首次載入資料時自動分析資料表，並在整個日常操作中進行變更。停用 autovacuum 時，最好定期運行 ANALYZE，或者在對資料表的內容進行大量變更後運行。準確的統計資訊可以幫助規劃程序選擇最合適的查詢計劃，從而提高查詢處理的效率。讀取主要資料庫的常見策略是在一天的離峰使用時間內每天運行一次 VACUUM 和 ANALYZE。（如果有大量更新活動的話，這是不夠的。）

ANALYZE 只需要對目標資料表執行讀取鎖定，因此它可以與資料表上的其他活動同時運行。

ANALYZE 收集的統計資訊通常包括每欄位中一些最常見值的列表，以及顯示每個欄位中近似資料分佈的直方圖。如果 ANALYZE 認為它們不感興趣（例如，在唯一鍵欄位中，沒有常見值）或者欄位資料型別不支援相應的運算子，則可以省略其中一個或兩個。[第 24 章](../../server-administration/routine-database-maintenance-tasks/)提供了有關統計資訊的更多訊息。

對於大型資料表，ANALYZE 採用資料表內容的隨機樣本，而不是檢查每一個資料列。這允許在很短的時間內分析非常大的資料表。但請注意，統計訊息只是近似值，並且每次運行 ANALYZE 時都會略有變化，即使實際資料表內容沒有變化也是如此。這可能會導致 [EXPLAIN](explain.md) 顯示的計劃程序估算成本發生微小變化。在極少數情況下，這種非確定性會導致計劃程序在運行 ANALYZE 後更改查詢計劃。為避免這種情況，請提高 ANALYZE 收集的統計資料量，如下所述。

可以透過調整 [default\_statistics\_target](../../server-administration/server-configuration/query-planning.md#19-7-4-other-planner-options) 組態變數來控制分析的範圍，或者透過使用[ALTER TABLE](alter-table.md) ... ALTER COLUMN ... SET STATISTICS 設定每個欄位統計訊息目標來達到各欄位控制（參閱 ALTER TABLE）。目標值設定最常用值列表中的最大項目數和直方圖中的最大二進制數。預設目標值為 100，但可以向上或向下調整此值以將計劃器估計的準確性與 ANALYZE 所用的時間和 pg\_statistic 中佔用的空間量進行權衡。特別是，將統計訊息目標設定為零會停用該欄位的統計訊息收集。對於從未用作查詢的 WHERE，GROUP BY 或 ORDER BY 子句的一部分欄位，這樣做可能很有用，因為規劃程序不會使用此類欄位的統計訊息。

被分析欄位中最大的統計目標決定了為準備統計訊息而採樣的資料列數。增加目標會使得進行 ANALYZE 所需的時間和空間成比例增加。

ANALYZE 估計的值之一是每個欄位中出現的不同值的數量。因為只檢查了資料列的子集，所以即使具有最大可能的統計目標，該估計有時也可能非常不準確。如果這種不準確導致錯誤的查詢計劃，可以手動確定更準確的值，然後使用 ALTER TABLE ... ALTER COLUMN ... SET \(n\_distinct = ...\) 進行安裝（參閱 [ALTER TABLE](alter-table.md)）。

如果正在分析的資料表有一個或多個子資料表，ANALYZE 將收集兩次統計訊息：一次僅在父資料表的資料列上，第二次在父資料表的資料列上及其所有子資料表。在規劃遍歷整個繼承樹的查詢時，需要第二組統計訊息。 但是，autovacuum 背景程序在決定是否觸發對該資料表的自動分析時，只會考慮父資料表本身的插入或更新。如果很少插入或更新該資料表，則除非您手動運行 ANALYZE，否則繼承統計訊息將不是最新的。

如果任何子資料表是外部資料封裝器不支援 ANALYZE 的外部資料表，則在收集繼承統計訊息時將忽略這些子資料表。

如果要分析的資料表完全為空，ANALYZE 將不會記錄該資料表的新統計訊息。任何現有統計資訊都會被保留。

### 相容性

SQL 標準中沒有 ANALYZE 語句。

### 參閱

[VACUUM](vacuum.md), [vacuumdb](../client-applications/vacuumdb.md), [Section 19.4.4](../../server-administration/server-configuration/resource-consumption.md#19-4-4-cheng-ben-kao-liang-de-vacuum-yan), [Section 24.1.6](../../server-administration/routine-database-maintenance-tasks/routine-vacuuming.md#24-1-6-autovacuum-bei-jing-cheng-xu)

