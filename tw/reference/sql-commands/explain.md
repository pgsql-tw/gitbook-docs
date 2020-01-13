# EXPLAIN

EXPLAIN — 顯示執行計劃的內容

### 語法

```text
EXPLAIN [ ( option [, ...] ) ] statement
EXPLAIN [ ANALYZE ] [ VERBOSE ] statement

where option can be one of:

    ANALYZE [ boolean ]
    VERBOSE [ boolean ]
    COSTS [ boolean ]
    BUFFERS [ boolean ]
    TIMING [ boolean ]
    SUMMARY [ boolean ]
    FORMAT { TEXT | XML | JSON | YAML }
```

### 說明

此命令顯示 PostgreSQL 計劃程序為所提供的查詢語句設計的執行計劃。執行計劃顯示查詢語句如何掃瞄其所引用的資料表 - 通過簡單循序掃描、索引掃描等 - 如果引用了多個資料表，將使用哪些交叉查詢的演算法將每個資料表所需的資料列匯集在一起。

顯示這些資訊的最關鍵部分是估計查詢語句的執行成本，這是計劃程序猜測執行行語句需要多長時間（以成本單位測量，是任何面向的，但通常意味著磁碟頁面讀取）。實際上顯示了兩個數字：可以回傳第一個資料列之前的啟動成本，以及回傳所有資料列的總成本。對於大多數查詢而言，總成本是重要的，但在諸如 EXISTS 中的子查詢之類的查詢中，規劃程序將選擇最小的啟動成本而不是最小的總成本（因為執行程序會在獲得一個資料列之後將停止）。此外，如果使用 LIMIT 子句限制要回傳的資料列數量，則計劃程序會在兩端的成本之間進行適當的插值，以估計哪個計劃確實成本較低。

ANALYZE 選項讓語句實際執行，而不僅僅是計劃而已。然後將實際運行時的統計資訊加到顯示結果中，包括每個計劃節點中消耗的總耗用時間（以毫秒為單位）以及實際回傳的總資料列數。這對於了解規劃程序的估計是否接近現實非常有用。

#### 重點

請記住，當使用 ANALYZE 選項時，實際上會執行該語句。儘管 EXPLAIN 將丟棄 SELECT 回傳的任何輸出，但該語句的其他副作用將照常發生。如果您希望在 INSERT、UPDATE、DELETE、CREATE TABLE AS 或 EXECUTE 語句上使用 EXPLAIN ANALYZE 而不讓命令影響您的資料，請使用以下方法：

```text
BEGIN;
EXPLAIN ANALYZE ...;
ROLLBACK;
```

在未括號的語法中，只有 ANALYZE 和 VERBOSE 選項可以使用，而且也只能依次序使用。在 PostgreSQL 9.0 之前，沒有括號的語法是唯一受支援的語法。預計所有新選項僅在括號語法中受支援。

### 參數

`ANALYZE`

執行命令並顯示實際運行時間和其他統計訊息。此參數預設為 FALSE。

`VERBOSE`

顯示有關計劃的其他訊息。具體來說，包括計劃樹中每個節點的輸出欄位列表， schema-qualify 資料表和函數名稱，始終在表示式中使用其範圍資料表別名標記，並始終輸出顯示統計訊息的每個觸發器的名稱。此參數預設為 FALSE。

`COSTS`

包括有關每個計劃節點的估計啟動和總成本的訊息，以及估計的資料列數和每個資料列的估計寬度。此參數預設為 TRUE。

`BUFFERS`

加入顯示有關緩衝區使用的訊息。具體來說，包括命中、讀取、弄髒和寫入的共享塊的數量，命中、讀取、弄髒和寫入的本地區塊的數量，以及讀取和寫入的臨時區塊的數量。命中意味著避免了讀取，因為在需要時已經在緩衝區中找到了區塊。共享區塊包含來自一般資料表和索引的資料；本地區塊包含臨時資料表和索引的資料；臨時區塊包含用於排序、映射、具體化計劃節點和類似情況的短期工作資料。髒污的區塊數表示此查詢更改的先前未修改的區塊數量；而寫入的區塊數表示在查詢處理期間由該後端從緩衝區中讀出的先前髒污區塊的數量。為上層節點顯示的塊數包括其所有子節點使用的塊數。在文字格式中，僅輸出非零的值。僅當啟用 ANALYZE 時，才能使用此參數。它預設為 FALSE。

`TIMING`

包括輸出中每個節點花費的實際啟動時間和總時間。重複讀取系統時鐘的開銷可能會在某些系統上顯著減慢查詢速度，因此當僅需要實際資料列計數而非精確時間時，將此參數設定為 FALSE 可能會很有用。即使使用此選項關閉節點級時序，也始終會測量整個語句的執行時間。僅當啟用 ANALYZE 時，才能使用此參數。 它預設為 TRUE。

`SUMMARY`

在查詢計劃之後顯示摘要訊息（例如，總計的時間訊息）。使用 ANALYZE 時預設會包含摘要訊息，但一般預設的情況下不包括摘要信息，不過可以使用此選項啟用。EXPLAIN EXECUTE 中的計劃時間包括從緩衝區中取得計劃所需的時間以及必要時重新計劃所需的時間。

`FORMAT`

指定輸出格式，可以是 TEXT、XML、JSON 或 YAML。非文字輸出格式包含與文字輸出格式相同的訊息，但能讓程式更容易解析。此參數預設為 TEXT。

_`boolean`_

指定是應打開還是關閉所選選項。您可以寫入 TRUE、ON 或 1 以啟用該選項，使用 FALSE、OFF 或 0 來停用它。布林值也可以省略，在這種情況下假定為 TRUE。

_`statement`_

任何 SELECT，INSERT，UPDATE，DELETE，VALUES，EXECUTE，DECLARE，CREATE TABLE AS 或 CREATE MATERIALIZED VIEW AS 語句，您希望查看其執行計劃。

### 輸出

命令的結果是為語句選擇計劃的文字描述，可選擇使用執行統計訊息加以註釋。[第 14.1 節](../../the-sql-language/performance-tips/using-explain.md)描述了其所提供的訊息。

### 注意

為了使 PostgreSQL 查詢規劃器在優化查詢時做出合理的明智決策，[pg\_statistic](../../internals/system-catalogs/pg_statistic.md) 資料應該是查詢中使用的所有資料表的最新數據。通常，[autovacuum](../../server-administration/routine-database-maintenance-tasks/routine-vacuuming.md#24-1-6-the-autovacuum-daemon) 背景程序會自動處理。但是如果資料表的內容最近發生了重大變化，您可能需要手動 [ANALYZE](analyze.md) 而不是等待 autovacuum 來趕上變化。

為了測量執行計劃中每個節點的執行時成本，EXPLAIN ANALYZE 的目前實作為查詢執行加入了開銷分析。因此，對查詢執行 EXPLAIN ANALYZE 有時會比正常執行查詢花費更長的時間。開銷量取決於查詢的性質以及所使用的平台。最糟糕的情況發生在計劃節點上，這些節點本身每次執行只需要很少的時間，而且在作業系統呼相對較慢以獲取時間的主機上。

### 範例

要顯示具有單個整數欄位和 10000 個資料列的資料表的簡單查詢計劃：

```text
EXPLAIN SELECT * FROM foo;

                       QUERY PLAN
---------------------------------------------------------
 Seq Scan on foo  (cost=0.00..155.00 rows=10000 width=4)
(1 row)
```

這是相同的查詢，使用 JSON 輸出格式：

```text
EXPLAIN (FORMAT JSON) SELECT * FROM foo;
           QUERY PLAN
--------------------------------
 [                             +
   {                           +
     "Plan": {                 +
       "Node Type": "Seq Scan",+
       "Relation Name": "foo", +
       "Alias": "foo",         +
       "Startup Cost": 0.00,   +
       "Total Cost": 155.00,   +
       "Plan Rows": 10000,     +
       "Plan Width": 4         +
     }                         +
   }                           +
 ]
(1 row)
```

如果索引存在並且我們使用具有可索引的 WHERE 條件查詢，則 EXPLAIN 可能會顯示不同的計劃：

```text
EXPLAIN SELECT * FROM foo WHERE i = 4;

                         QUERY PLAN
--------------------------------------------------------------
 Index Scan using fi on foo  (cost=0.00..5.98 rows=1 width=4)
   Index Cond: (i = 4)
(2 rows)
```

這是相同的查詢，但是採用 YAML 格式：

```text
EXPLAIN (FORMAT YAML) SELECT * FROM foo WHERE i='4';
          QUERY PLAN
-------------------------------
 - Plan:                      +
     Node Type: "Index Scan"  +
     Scan Direction: "Forward"+
     Index Name: "fi"         +
     Relation Name: "foo"     +
     Alias: "foo"             +
     Startup Cost: 0.00       +
     Total Cost: 5.98         +
     Plan Rows: 1             +
     Plan Width: 4            +
     Index Cond: "(i = 4)"    
(1 row)
```

XML 格式留給讀者練習。

以下是同一計劃，其成本估算被停用：

```text
EXPLAIN (COSTS FALSE) SELECT * FROM foo WHERE i = 4;

        QUERY PLAN
----------------------------
 Index Scan using fi on foo
   Index Cond: (i = 4)
(2 rows)
```

以下是使用彙總函數查詢的查詢計劃範例：

```text
EXPLAIN SELECT sum(i) FROM foo WHERE i < 10;

                             QUERY PLAN
---------------------------------------------------------------------
 Aggregate  (cost=23.93..23.93 rows=1 width=4)
   ->  Index Scan using fi on foo  (cost=0.00..23.92 rows=6 width=4)
         Index Cond: (i < 10)
(3 rows)
```

以下是使用 EXPLAIN EXECUTE 顯示準備好的查詢執行計劃範例：

```text
PREPARE query(int, int) AS SELECT sum(bar) FROM test
    WHERE id > $1 AND id < $2
    GROUP BY foo;

EXPLAIN ANALYZE EXECUTE query(100, 200);

                                                       QUERY PLAN                                                       
------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=9.54..9.54 rows=1 width=8) (actual time=0.156..0.161 rows=11 loops=1)
   Group Key: foo
   ->  Index Scan using test_pkey on test  (cost=0.29..9.29 rows=50 width=8) (actual time=0.039..0.091 rows=99 loops=1)
         Index Cond: ((id > $1) AND (id < $2))
 Planning time: 0.197 ms
 Execution time: 0.225 ms
(6 rows)
```

當然，此處顯示的具體數字取決於所涉及資料表的實際內容。另請注意，由於計劃程序的改進，PostgreSQL 版本之間的數字甚至選定的查詢策略可能會有所不同。此外，ANALYZE 指令使用隨機採樣來估計數據統計；因此，即使資料表中資料的實際分佈沒有改變，也可能在全新的 ANALYZE 之後改變成本估算。

### 相容性

SQL 標準中並沒有定義 EXPLAIN 語句。

### 參閱

[ANALYZE](analyze.md)

