<a id="MULTIVARIATE-STATISTICS-EXAMPLES"></a>

## 69.2. 多變量統計資訊範例 [#](#multivariate-statistics-examples) <a href="#multivariate-statistics-examples" id="multivariate-statistics-examples"></a>

[69.2.1. 函數相依性](multivariate-statistics-examples.md#FUNCTIONAL-DEPENDENCIES)

[69.2.2. 多變量相異值計數](multivariate-statistics-examples.md#MULTIVARIATE-NDISTINCT-COUNTS)

[69.2.3. MCV 清單](multivariate-statistics-examples.md#MCV-LISTS)

<a id="id-1.10.21.5.2"></a>

<a id="FUNCTIONAL-DEPENDENCIES"></a>

### 69.2.1. 函數相依性 [#](#FUNCTIONAL-DEPENDENCIES)

多變量相關性可以用一個非常簡單的資料集來示範
——一個有兩個欄位、且兩個欄位包含相同值的資料表：

```

CREATE TABLE t (a INT, b INT);
INSERT INTO t SELECT i % 100, i % 100 FROM generate_series(1, 10000) s(i);
ANALYZE t;
```

如[第 14.2 節](../../the-sql-language/performance-tips/planner-stats.md)所述，規劃器可以使用從 `pg_class`
取得的頁面數與資料列數，判斷 `t` 的基數（cardinality）：

```

SELECT relpages, reltuples FROM pg_class WHERE relname = 't';

 relpages | reltuples
----------+-----------
       45 |     10000
```

資料分布非常單純；每個欄位中只有 100 個相異值，
而且均勻分布。

下面的範例顯示對 `a` 欄位上的 `WHERE`
條件進行估計的結果：

```

EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a = 1;
                                 QUERY PLAN
-------------------------------------------------------------------​------------
 Seq Scan on t  (cost=0.00..170.00 rows=100 width=8) (actual rows=100.00 loops=1)
   Filter: (a = 1)
   Rows Removed by Filter: 9900
```

規劃器檢查該條件，並判定此子句的選擇率
為 1%。比較這個估計值與實際的
資料列數，可以看出估計非常準確
（事實上是完全正確，因為這個資料表非常小）。若將
`WHERE` 條件改為使用 `b` 欄位，會產生
相同的計畫。但請觀察，如果我們對兩個欄位套用相同的
條件，並以 `AND` 將它們組合起來，會發生什麼事：

```

EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a = 1 AND b = 1;
                                 QUERY PLAN
-------------------------------------------------------------------​----------
 Seq Scan on t  (cost=0.00..195.00 rows=1 width=8) (actual rows=100.00 loops=1)
   Filter: ((a = 1) AND (b = 1))
   Rows Removed by Filter: 9900
```

規劃器會個別估計每個條件的選擇率，
得到與上面相同的 1% 估計值。接著它假設這些
條件彼此獨立，因此將它們的選擇率相乘，
得到最終只有 0.01% 的選擇率估計值。
這是明顯的低估，因為實際符合這些條件的資料列數
（100）高出了兩個數量級。

這個問題可以透過建立一個統計資訊物件來解決，
該物件指示 `ANALYZE` 對這兩個欄位計算函數相依性
多變量統計資訊：

```

CREATE STATISTICS stts (dependencies) ON a, b FROM t;
ANALYZE t;
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a = 1 AND b = 1;
                                  QUERY PLAN
-------------------------------------------------------------------​------------
 Seq Scan on t  (cost=0.00..195.00 rows=100 width=8) (actual rows=100.00 loops=1)
   Filter: ((a = 1) AND (b = 1))
   Rows Removed by Filter: 9900
```

<a id="MULTIVARIATE-NDISTINCT-COUNTS"></a>

### 69.2.2. 多變量相異值計數 [#](#MULTIVARIATE-NDISTINCT-COUNTS)

估計多個欄位所構成之集合的基數時，也會發生類似的問題，
例如 `GROUP BY` 子句會產生的群組數量。當 `GROUP BY`
只列出單一欄位時，相異值（n-distinct）估計值（可以從 HashAggregate
節點的估計傳回資料列數看到）非常
準確：

```

EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT COUNT(*) FROM t GROUP BY a;
                                       QUERY PLAN
-------------------------------------------------------------------​----------------------
 HashAggregate  (cost=195.00..196.00 rows=100 width=12) (actual rows=100.00 loops=1)
   Group Key: a
   ->  Seq Scan on t  (cost=0.00..145.00 rows=10000 width=4) (actual rows=10000.00 loops=1)
```

但若沒有多變量統計資訊，對於像下面範例這樣
在 `GROUP BY` 中有兩個欄位的查詢，群組數量的
估計值就會差了一個數量級：

```

EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT COUNT(*) FROM t GROUP BY a, b;
                                       QUERY PLAN
-------------------------------------------------------------------​-------------------------
 HashAggregate  (cost=220.00..230.00 rows=1000 width=16) (actual rows=100.00 loops=1)
   Group Key: a, b
   ->  Seq Scan on t  (cost=0.00..145.00 rows=10000 width=8) (actual rows=10000.00 loops=1)
```

將統計資訊物件重新定義為包含這兩個欄位的相異值計數後，
估計值大幅改善：

```

DROP STATISTICS stts;
CREATE STATISTICS stts (dependencies, ndistinct) ON a, b FROM t;
ANALYZE t;
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT COUNT(*) FROM t GROUP BY a, b;
                                       QUERY PLAN
-------------------------------------------------------------------​-------------------------
 HashAggregate  (cost=220.00..221.00 rows=100 width=16) (actual rows=100.00 loops=1)
   Group Key: a, b
   ->  Seq Scan on t  (cost=0.00..145.00 rows=10000 width=8) (actual rows=10000.00 loops=1)
```

<a id="MCV-LISTS"></a>

### 69.2.3. MCV 清單 [#](#MCV-LISTS)

如[第 69.2.1 節](multivariate-statistics-examples.md#FUNCTIONAL-DEPENDENCIES)所述，函數
相依性是一種成本非常低廉且有效率的統計資訊，但其
主要限制在於其全域性質（只在欄位層級追蹤相依性，
而不是在個別欄位值之間追蹤）。

本節介紹 MCV
（most-common values，最常見值）清單的多變量版本，它是對[第 69.1 節](row-estimation-examples.md)所述之逐欄
統計資訊的直接擴充。這類
統計資訊藉由儲存個別值來解決上述限制，但它
自然也比較昂貴，無論是在 `ANALYZE` 中建立統計資訊、
儲存空間，還是規劃時間方面皆是如此。

讓我們再看一次[第 69.2.1 節](multivariate-statistics-examples.md#FUNCTIONAL-DEPENDENCIES)中的查詢，
但這次是在同一組欄位上建立 MCV 清單
（請務必移除函數相依性，
以確保規劃器使用新建立的統計資訊）。

```

DROP STATISTICS stts;
CREATE STATISTICS stts2 (mcv) ON a, b FROM t;
ANALYZE t;
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a = 1 AND b = 1;
                                   QUERY PLAN
-------------------------------------------------------------------​------------
 Seq Scan on t  (cost=0.00..195.00 rows=100 width=8) (actual rows=100.00 loops=1)
   Filter: ((a = 1) AND (b = 1))
   Rows Removed by Filter: 9900
```

估計值與使用函數相依性時一樣準確，這主要
歸功於資料表相當小，而且分布單純、
相異值數量少。在查看第二個查詢
（函數相依性處理得並不特別好的那一個）之前，
我們先稍微檢視一下 MCV 清單。

可以使用 `pg_mcv_list_items` 這個傳回集合的函式
來檢視 MCV 清單。

```

SELECT m.* FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid),
                pg_mcv_list_items(stxdmcv) m WHERE stxname = 'stts2';
 index |  values  | nulls | frequency | base_frequency
-------+----------+-------+-----------+----------------
     0 | {0, 0}   | {f,f} |      0.01 |         0.0001
     1 | {1, 1}   | {f,f} |      0.01 |         0.0001
   ...
    49 | {49, 49} | {f,f} |      0.01 |         0.0001
    50 | {50, 50} | {f,f} |      0.01 |         0.0001
   ...
    97 | {97, 97} | {f,f} |      0.01 |         0.0001
    98 | {98, 98} | {f,f} |      0.01 |         0.0001
    99 | {99, 99} | {f,f} |      0.01 |         0.0001
(100 rows)
```

這證實了這兩個欄位中有 100 種相異的組合，而且
它們出現的可能性大致相同（每一種的頻率都是 1%）。
基本頻率（base frequency）是根據逐欄統計資訊計算出的頻率，就好像
沒有多欄統計資訊一樣。如果任一欄位中有任何 null 值，
就會在 `nulls` 欄位中標示出來。

估計選擇率時，規劃器會將所有條件套用到
MCV 清單中的項目上，然後加總符合項目的
頻率。詳細內容請參閱 `src/backend/statistics/mcv.c`
中的 `mcv_clauselist_selectivity`。

與函數相依性相比，MCV 清單有兩項
主要優點。第一，清單中儲存的是實際的值，因此可以
判斷哪些組合是相容的。

```

EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a = 1 AND b = 10;
                                 QUERY PLAN
-------------------------------------------------------------------​--------
 Seq Scan on t  (cost=0.00..195.00 rows=1 width=8) (actual rows=0.00 loops=1)
   Filter: ((a = 1) AND (b = 10))
   Rows Removed by Filter: 10000
```

第二，MCV 清單能處理範圍更廣的子句類型，
而不像函數相依性那樣只能處理相等子句。例如，
請看下面對同一個資料表的範圍查詢：

```

EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a <= 49 AND b > 49;
                                QUERY PLAN
-------------------------------------------------------------------​--------
 Seq Scan on t  (cost=0.00..195.00 rows=1 width=8) (actual rows=0.00 loops=1)
   Filter: ((a <= 49) AND (b > 49))
   Rows Removed by Filter: 10000
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/multivariate-statistics-examples.html)（原文版本：18.6；核對日期：2026-10-12）
