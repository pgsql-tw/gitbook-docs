<a id="SQL-EXPLAIN"></a><a id="id-1.9.3.148.1"></a><a id="id-1.9.3.148.2"></a><a id="id-1.9.3.148.3"></a>

## EXPLAIN

EXPLAIN — 顯示陳述式的執行計畫

<a id="id-1.9.3.148.6"></a>

## 語法

```

EXPLAIN [ ( option [, ...] ) ] statement

where option can be one of:

    ANALYZE [ boolean ]
    VERBOSE [ boolean ]
    COSTS [ boolean ]
    SETTINGS [ boolean ]
    GENERIC_PLAN [ boolean ]
    BUFFERS [ boolean ]
    SERIALIZE [ { NONE | TEXT | BINARY } ]
    WAL [ boolean ]
    TIMING [ boolean ]
    SUMMARY [ boolean ]
    MEMORY [ boolean ]
    FORMAT { TEXT | XML | JSON | YAML }
```

<a id="id-1.9.3.148.7"></a>

## 說明

此命令會顯示 PostgreSQL 規劃器為所提供的陳述式產生的執行計畫。執行計畫會顯示陳述式所引用的資料表將如何被掃描——使用一般的循序掃描、索引掃描等等——以及若引用了多個資料表，將使用哪些連接演算法把每個輸入資料表中所需的資料列結合在一起。

顯示內容中最關鍵的部分是估計的陳述式執行成本，也就是規劃器對執行該陳述式需要多久時間的推測（以任意的成本單位衡量，但慣例上代表磁碟頁面的讀取次數）。實際上會顯示兩個數字：傳回第一筆資料列之前的啟動成本，以及傳回所有資料列的總成本。對大多數查詢而言，重要的是總成本，但在某些情境下，例如 `EXISTS` 中的子查詢，規劃器會選擇啟動成本最小的計畫，而不是總成本最小的計畫（因為執行器在取得一筆資料列之後無論如何都會停止）。此外，若你以 `LIMIT` 子句限制要傳回的資料列數量，規劃器會在端點成本之間進行適當的內插，以估算哪個計畫才真正是最便宜的。

`ANALYZE` 選項會使陳述式被實際執行，而不只是規劃。接著會在顯示內容中加入實際的執行時間統計資訊，包括每個計畫節點內所耗用的總經過時間（以毫秒為單位），以及它實際傳回的資料列總數。這有助於了解規劃器的估計是否接近實際情況。

<a id="id-1.9.3.148.7.5"></a>

### 重要

請記住，使用 `ANALYZE` 選項時，陳述式是真的會被執行的。雖然
`EXPLAIN` 會捨棄
`SELECT` 原本會傳回的任何輸出，但該陳述式的其他副作用仍會照常發生。若你想對
`INSERT`、`UPDATE`、
`DELETE`、`MERGE`、
`CREATE TABLE AS`
或 `EXECUTE` 陳述式使用
`EXPLAIN ANALYZE`，又不想讓該命令影響你的資料，請使用以下做法：

```

BEGIN;
EXPLAIN ANALYZE ...;
ROLLBACK;
```

<a id="id-1.9.3.148.8"></a>

## 參數

`ANALYZE`
:   執行該命令，並顯示實際執行時間與其他統計資訊。
    此參數預設為 `FALSE`。

`VERBOSE`
:   顯示有關計畫的額外資訊。具體而言，包括計畫樹中每個節點的輸出欄位列表、以綱要限定資料表與函式名稱、一律以範圍表（range table）別名標示運算式中的變數，以及一律印出有顯示統計資訊之每個觸發程序的名稱。若已計算查詢識別碼，也會一併顯示；詳細資訊請參閱 [compute_query_id](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID)。此參數預設為 `FALSE`。

`COSTS`
:   包含每個計畫節點的估計啟動成本與總成本資訊，以及估計的資料列數量與每筆資料列的估計寬度。
    此參數預設為 `TRUE`。

`SETTINGS`
:   包含組態參數的相關資訊。具體而言，包括影響查詢規劃、且值與內建預設值不同的選項。此參數預設為 `FALSE`。

`GENERIC_PLAN`
:   允許陳述式包含像
    `$1` 這樣的參數預留位置，並產生不相依於這些參數值的通用計畫。
    有關通用計畫以及支援參數的陳述式類型的詳細資訊，請參閱 [`PREPARE`](sql-prepare.md)。
    此參數不能與 `ANALYZE` 一起使用。
    它預設為 `FALSE`。

`BUFFERS`
:   包含緩衝區使用情況的資訊。具體而言，包括共享區塊的命中、讀取、弄髒與寫入數量，本地區塊的命中、讀取、弄髒與寫入數量，暫存區塊的讀取與寫入數量，以及若已啟用
    [track_io_timing](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING)，讀取與寫入資料檔案區塊、本地區塊及暫存檔案區塊所花費的時間（以毫秒為單位）。
    *命中*（hit）表示因為需要時該區塊已在快取中，所以避免了一次讀取。
    共享區塊包含來自一般資料表與索引的資料；
    本地區塊包含來自暫存資料表與索引的資料；
    而暫存區塊則包含排序、雜湊、Materialize 計畫節點及類似情況中所使用的短期工作資料。
    *弄髒*（dirtied）的區塊數量，表示此查詢所變更之先前未被修改的區塊數量；而*寫入*（written）的區塊數量，表示此後端在查詢處理期間從快取中逐出的先前已被弄髒的區塊數量。
    上層節點所顯示的區塊數量，包含其所有子節點所使用的區塊。在文字格式中，只會印出非零的值。使用 `ANALYZE` 時，會自動包含緩衝區資訊。

`SERIALIZE`
:   包含*序列化*（serializing）查詢輸出資料之成本的相關資訊，也就是將其轉換為文字或二進位格式以傳送給用戶端的成本。
    若資料型別的輸出函式代價高昂，或必須從行外儲存擷取經 TOAST 處理的值，這可能會佔查詢一般執行所需時間的相當大部分。`EXPLAIN` 的預設行為 `SERIALIZE NONE` 不會執行這些轉換。若指定了 `SERIALIZE TEXT`
    或 `SERIALIZE BINARY`，就會執行適當的轉換，並測量執行轉換所花費的時間（除非指定了 `TIMING OFF`）。若同時也指定了
    `BUFFERS` 選項，則轉換中涉及的任何緩衝區存取也會被計入。
    不過，在任何情況下 `EXPLAIN` 都不會真正將結果資料傳送給用戶端；因此無法以這種方式調查網路傳輸成本。
    只有在同時啟用 `ANALYZE` 時才能啟用序列化。若寫了 `SERIALIZE` 而未加引數，則假定為 `TEXT`。

`WAL`
:   包含 WAL 紀錄產生的相關資訊。具體而言，包括紀錄數量、完整頁面映像（fpi）的數量、以位元組為單位所產生的 WAL 量，以及 WAL 緩衝區變滿的次數。
    在文字格式中，只會印出非零的值。
    此參數只能在同時啟用 `ANALYZE` 時使用。它預設為 `FALSE`。

`TIMING`
:   在輸出中包含實際的啟動時間，以及在每個節點中所花費的時間。
    在某些系統上，重複讀取系統時鐘的額外負擔可能會大幅拖慢查詢，因此當只需要實際的資料列數量、而不需要精確時間時，將此參數設為 `FALSE` 可能會有用。即使以此選項關閉了節點層級的計時，整個陳述式的執行時間仍一律會被測量。
    此參數只能在同時啟用 `ANALYZE` 時使用。它預設為 `TRUE`。

`SUMMARY`
:   在查詢計畫之後包含摘要資訊（例如加總的計時資訊）。使用
    `ANALYZE` 時預設會包含摘要資訊，其他情況下預設不包含，但可以使用此選項啟用。`EXPLAIN EXECUTE` 中的規劃時間，包含從快取中擷取計畫所需的時間，以及必要時重新規劃所需的時間。

`MEMORY`
:   包含查詢規劃階段記憶體消耗的相關資訊。
    具體而言，包括規劃器記憶體內結構所使用的精確儲存量，以及考量配置額外負擔後的總記憶體量。
    此參數預設為 `FALSE`。

`FORMAT`
:   指定輸出格式，可以是 TEXT、XML、JSON 或 YAML。
    非文字輸出所包含的資訊與文字輸出格式相同，但較容易讓程式剖析。此參數預設為
    `TEXT`。

*`boolean`*
:   指定所選的選項應該開啟還是關閉。
    你可以寫 `TRUE`、`ON` 或
    `1` 來啟用該選項，寫 `FALSE`、
    `OFF` 或 `0` 來停用它。也可以省略
    *`boolean`* 值，此時會假定為 `TRUE`。

*`statement`*
:   你想查看其執行計畫的任何 `SELECT`、`INSERT`、`UPDATE`、
    `DELETE`、`MERGE`、
    `VALUES`、`EXECUTE`、
    `DECLARE`、`CREATE TABLE AS` 或
    `CREATE MATERIALIZED VIEW AS` 陳述式。

<a id="id-1.9.3.148.9"></a>

## 輸出

此命令的結果是對 *`statement`* 所選計畫的文字描述，並可選擇附上執行統計資訊。
[第 14.1 節](../../the-sql-language/performance-tips/using-explain.md)說明了所提供的資訊。


<a id="id-1.9.3.148.10"></a>

## 注意事項

為了讓 PostgreSQL 查詢規劃器在最佳化查詢時能做出合理且有根據的決策，查詢中所使用之所有資料表的 [`pg_statistic`](../../internals/catalogs/catalog-pg-statistic.md)
資料應該是最新的。通常
[autovacuum 常駐程式](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)會自動處理這件事。但若某個資料表的內容最近有大幅變更，你可能需要手動執行
[`ANALYZE`](sql-analyze.md)，而不是等待 autovacuum 跟上這些變更。

為了測量執行計畫中每個節點的執行時間成本，目前 `EXPLAIN
ANALYZE` 的實作會在查詢執行中加入剖析（profiling）的額外負擔。
因此，對查詢執行 `EXPLAIN ANALYZE`
有時可能會比正常執行該查詢花費明顯更長的時間。額外負擔的多寡取決於查詢的性質以及所使用的平台。最糟的情況發生在本身每次執行只需要極少時間的計畫節點上，以及取得目前時間之作業系統呼叫相對緩慢的機器上。

<a id="id-1.9.3.148.11"></a>

## 範例

顯示對一個只有單一
`integer` 欄位、含 10000 筆資料列之資料表的簡單查詢計畫：

```

EXPLAIN SELECT * FROM foo;

                       QUERY PLAN
---------------------------------------------------------
 Seq Scan on foo  (cost=0.00..155.00 rows=10000 width=4)
(1 row)
```

以下是同一個查詢，採用 JSON 輸出格式：

```

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

若有索引，而我們使用了帶有可使用索引之
`WHERE` 條件的查詢，`EXPLAIN`
可能會顯示不同的計畫：

```

EXPLAIN SELECT * FROM foo WHERE i = 4;

                         QUERY PLAN
--------------------------------------------------------------
 Index Scan using fi on foo  (cost=0.00..5.98 rows=1 width=4)
   Index Cond: (i = 4)
(2 rows)
```

以下是同一個查詢，但採用 YAML 格式：

```

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

XML 格式就留給讀者作為練習。

以下是抑制成本估計後的同一個計畫：

```

EXPLAIN (COSTS FALSE) SELECT * FROM foo WHERE i = 4;

        QUERY PLAN
----------------------------
 Index Scan using fi on foo
   Index Cond: (i = 4)
(2 rows)
```

以下是使用彙總函式之查詢的查詢計畫範例：

```

EXPLAIN SELECT sum(i) FROM foo WHERE i < 10;

                             QUERY PLAN
-------------------------------------------------------------------​--
 Aggregate  (cost=23.93..23.93 rows=1 width=4)
   ->  Index Scan using fi on foo  (cost=0.00..23.92 rows=6 width=4)
         Index Cond: (i < 10)
(3 rows)
```

以下是使用 `EXPLAIN EXECUTE` 顯示預備查詢之執行計畫的範例：

```

PREPARE query(int, int) AS SELECT sum(bar) FROM test
    WHERE id > $1 AND id < $2
    GROUP BY foo;

EXPLAIN ANALYZE EXECUTE query(100, 200);

                                                       QUERY PLAN
-------------------------------------------------------------------​------------------------------------------------------
 HashAggregate  (cost=10.77..10.87 rows=10 width=12) (actual time=0.043..0.044 rows=10.00 loops=1)
   Group Key: foo
   Batches: 1  Memory Usage: 24kB
   Buffers: shared hit=4
   ->  Index Scan using test_pkey on test  (cost=0.29..10.27 rows=99 width=8) (actual time=0.009..0.025 rows=99.00 loops=1)
         Index Cond: ((id > 100) AND (id < 200))
         Index Searches: 1
         Buffers: shared hit=4
 Planning Time: 0.244 ms
 Execution Time: 0.073 ms
(10 rows)
```

當然，此處顯示的具體數字取決於所涉及資料表的實際內容。另請注意，由於規劃器的改進，這些數字，甚至所選擇的查詢策略，都可能因
PostgreSQL 版本而異。此外，`ANALYZE` 命令使用隨機取樣來估計資料統計資訊；因此，即使資料表中資料的實際分布沒有改變，重新執行一次
`ANALYZE` 之後，成本估計也有可能改變。

請注意，前一個範例顯示的是針對 `EXECUTE` 中給定之特定參數值的「自訂」計畫。
我們可能也會想查看參數化查詢的通用計畫，這可以使用 `GENERIC_PLAN` 達成：

```

EXPLAIN (GENERIC_PLAN)
  SELECT sum(bar) FROM test
    WHERE id > $1 AND id < $2
    GROUP BY foo;

                                  QUERY PLAN
-------------------------------------------------------------------​------------
 HashAggregate  (cost=26.79..26.89 rows=10 width=12)
   Group Key: foo
   ->  Index Scan using test_pkey on test  (cost=0.29..24.29 rows=500 width=8)
         Index Cond: ((id > $1) AND (id < $2))
(4 rows)
```

在此例中，剖析器正確地推斷出 `$1`
與 `$2` 應該與
`id` 具有相同的資料型別，因此缺少來自 `PREPARE` 的參數型別資訊並不構成問題。在其他情況下，可能需要明確指定參數符號的型別，這可以透過對它們進行轉型來達成，例如：

```

EXPLAIN (GENERIC_PLAN)
  SELECT sum(bar) FROM test
    WHERE id > $1::integer AND id < $2::integer
    GROUP BY foo;
```

<a id="id-1.9.3.148.12"></a>

## 相容性

SQL 標準中沒有定義 `EXPLAIN` 陳述式。

以下語法在 PostgreSQL
9.0 版之前使用，目前仍受支援：

```

EXPLAIN [ ANALYZE ] [ VERBOSE ] statement
```

請注意，在此語法中，選項必須完全依照所示的順序指定。

<a id="id-1.9.3.148.13"></a>

## 另請參閱

[ANALYZE](sql-analyze.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-explain.html)（原文版本：18.6；核對日期：2026-10-03）
