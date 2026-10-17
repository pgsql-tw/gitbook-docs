<a id="ROW-ESTIMATION-EXAMPLES"></a>

## 69.1. 資料列估計範例 [#](#ROW-ESTIMATION-EXAMPLES)

<a id="id-1.10.21.4.2"></a>

以下所示的範例使用 PostgreSQL
迴歸測試資料庫中的資料表。
另外也請注意，由於 `ANALYZE` 在產生統計資訊時
使用隨機取樣，因此每次執行新的 `ANALYZE` 之後，
結果都會略有不同。

讓我們從一個非常簡單的查詢開始：

```

EXPLAIN SELECT * FROM tenk1;

                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..458.00 rows=10000 width=244)
```

規劃器如何判斷 `tenk1` 的基數（cardinality），
在[第 14.2 節](../../the-sql-language/performance-tips/planner-stats.md)已有說明，但為了
完整起見在此重述。頁面數與資料列數是從
`pg_class` 中查得的：

```

SELECT relpages, reltuples FROM pg_class WHERE relname = 'tenk1';

 relpages | reltuples
----------+-----------
      358 |     10000
```

這些數字是截至該資料表最後一次 `VACUUM` 或
`ANALYZE` 時的最新值。接著規劃器會取得
資料表目前實際的頁面數（這是成本低廉的操作，
不需要掃描資料表）。如果它與
`relpages` 不同，就會按比例調整
`reltuples`，以得到
目前的資料列數估計值。在上面的範例中，
`relpages` 的值是最新的，因此資料列數估計值
與 `reltuples` 相同。

接下來看一個 `WHERE` 子句中帶有範圍條件的
範例：

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 1000;

                                   QUERY PLAN
-------------------------------------------------------------------​-------------
 Bitmap Heap Scan on tenk1  (cost=24.06..394.64 rows=1007 width=244)
   Recheck Cond: (unique1 < 1000)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..23.80 rows=1007 width=0)
         Index Cond: (unique1 < 1000)
```

規劃器會檢查 `WHERE` 子句的條件，
並在 `pg_operator` 中查詢運算子
`<` 的選擇率函式。
它記錄在 `oprrest` 欄位中，
在此例中該項目為 `scalarltsel`。
`scalarltsel` 函式會從
`pg_statistic` 取得
`unique1` 的直方圖。若是手動查詢，查看較簡單的
`pg_stats` 檢視表會比較
方便：

```

SELECT histogram_bounds FROM pg_stats
WHERE tablename='tenk1' AND attname='unique1';

                   histogram_bounds
------------------------------------------------------
 {0,993,1997,3050,4040,5036,5957,7057,8029,9016,9995}
```

接著計算出直方圖中「< 1000」所占的比例。
這就是選擇率。直方圖會將範圍
劃分為頻率相等的區間（bucket），因此我們只需要找出
我們的值所在的區間，然後計入該區間的*一部分*以及
它之前的*所有*區間。值 1000 顯然落在
第二個區間（993–1997）。假設每個區間內的值
呈線性分布，我們可以將選擇率計算為：

```

selectivity = (1 + (1000 - bucket[2].min)/(bucket[2].max - bucket[2].min))/num_buckets
            = (1 + (1000 - 993)/(1997 - 993))/10
            = 0.100697
```

也就是一整個區間，加上第二個區間的線性比例，再除以
區間數。現在可以將估計資料列數計算為
選擇率與 `tenk1` 基數的
乘積：

```

rows = rel_cardinality * selectivity
     = 10000 * 0.100697
     = 1007  (rounding off)
```

接下來考慮一個 `WHERE` 子句中帶有相等條件的
範例：

```

EXPLAIN SELECT * FROM tenk1 WHERE stringu1 = 'CRAAAA';

                        QUERY PLAN
----------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..483.00 rows=30 width=244)
   Filter: (stringu1 = 'CRAAAA'::name)
```

規劃器同樣會檢查 `WHERE` 子句的條件，
並查詢 `=` 的選擇率函式，也就是
`eqsel`。對於相等條件的估計，直方圖
沒有用處；改為使用*最常見值*
（most common values，MCV）清單來判斷
選擇率。讓我們看看這些 MCV，並附上一些稍後
會用到的額外欄位：

```

SELECT null_frac, n_distinct, most_common_vals, most_common_freqs FROM pg_stats
WHERE tablename='tenk1' AND attname='stringu1';

null_frac         | 0
n_distinct        | 676
most_common_vals  | {EJAAAA,BBAAAA,CRAAAA,FCAAAA,FEAAAA,GSAAAA,​JOAAAA,MCAAAA,NAAAAA,WGAAAA}
most_common_freqs | {0.00333333,0.003,0.003,0.003,0.003,0.003,​0.003,0.003,0.003,0.003}
```

由於 `CRAAAA` 出現在 MCV 清單中，選擇率
就只是最常見頻率（most common frequencies，MCF）清單中
相對應的項目：

```

selectivity = mcf[3]
            = 0.003
```

和前面一樣，估計資料列數就是這個值與
`tenk1` 基數的乘積：

```

rows = 10000 * 0.003
     = 30
```

現在考慮同一個查詢，但使用一個不在
MCV 清單中的常數：

```

EXPLAIN SELECT * FROM tenk1 WHERE stringu1 = 'xxx';

                        QUERY PLAN
----------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..483.00 rows=15 width=244)
   Filter: (stringu1 = 'xxx'::name)
```

這是相當不同的問題：當值*不*在 MCV 清單中時，
該如何估計選擇率。
做法是利用該值不在清單中這項事實，
再結合所有
MCV 的頻率資訊：

```

selectivity = (1 - sum(mcv_freqs))/(num_distinct - num_mcv)
            = (1 - (0.00333333 + 0.003 + 0.003 + 0.003 + 0.003 + 0.003 +
                    0.003 + 0.003 + 0.003 + 0.003))/(676 - 10)
            = 0.0014559
```

也就是把所有 MCV 的頻率加總，
再用 1 減去這個總和，然後
除以*其他*相異值的數量。
這相當於假設欄位中不屬於任何
MCV 的那部分，平均分布在所有其他相異值之間。
請注意，這裡沒有 null 值，因此不必考慮它們
（否則還要從分子中減去 null 值比例）。
接著照常計算估計資料列數：

```

rows = 10000 * 0.0014559
     = 15  (rounding off)
```

前面 `unique1 < 1000` 的範例，
把 `scalarltsel` 實際所做的事過度簡化了；
既然我們已經看過使用 MCV 的範例，就可以補充
更多細節。就該範例所涵蓋的範圍而言，它是正確的，因為
`unique1` 是唯一值欄位，所以它沒有 MCV（顯然，沒有任何
值比其他值更常見）。對於非唯一值
欄位，通常同時會有直方圖與 MCV 清單，而且
*直方圖不包含欄位母體中
由 MCV 所代表的部分*。我們這樣做是因為
它能做出更精確的估計。在這種情況下，
`scalarltsel` 會直接將條件（例如
「< 1000」）套用到 MCV 清單中的每個值，並加總
使條件成立之 MCV 的頻率。這樣就能
精確估計資料表中屬於 MCV 那部分的
選擇率。接著以和上面相同的方式使用直方圖，
估計資料表中不屬於
MCV 那部分的選擇率，再將這兩個數字組合起來，估計整體的
選擇率。例如，請看

```

EXPLAIN SELECT * FROM tenk1 WHERE stringu1 < 'IAAAAA';

                         QUERY PLAN
------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..483.00 rows=3077 width=244)
   Filter: (stringu1 < 'IAAAAA'::name)
```

我們已經看過 `stringu1` 的 MCV 資訊，
以下是它的直方圖：

```

SELECT histogram_bounds FROM pg_stats
WHERE tablename='tenk1' AND attname='stringu1';

                                histogram_bounds
-------------------------------------------------------------------​-------------
 {AAAAAA,CQAAAA,FRAAAA,IBAAAA,KRAAAA,NFAAAA,PSAAAA,SGAAAA,VAAAAA,​XLAAAA,ZZAAAA}
```

檢查 MCV 清單後，我們發現條件 `stringu1 <
'IAAAAA'` 對前六個項目成立，對後四個項目不成立，
因此母體中 MCV 部分的選擇率為

```

selectivity = sum(relevant mvfs)
            = 0.00333333 + 0.003 + 0.003 + 0.003 + 0.003 + 0.003
            = 0.01833333
```

加總所有 MCF 也可以得知，MCV 所代表的母體
總比例為 0.03033333，因此
直方圖所代表的比例為 0.96966667（同樣地，這裡
沒有 null 值，否則就必須在此將它們排除）。我們可以看出，
值 `IAAAAA` 幾乎落在
第三個直方圖區間的末端。規劃器根據一些關於
不同字元出現頻率、相當粗略的假設，
估計直方圖母體中
小於 `IAAAAA` 的部分為 0.298387。接著我們將
MCV 母體與非 MCV 母體的估計值組合起來：

```

selectivity = mcv_selectivity + histogram_selectivity * histogram_fraction
            = 0.01833333 + 0.298387 * 0.96966667
            = 0.307669

rows        = 10000 * 0.307669
            = 3077  (rounding off)
```

在這個特定範例中，來自 MCV 清單的修正相當
小，因為該欄位的分布其實相當平坦（
統計資訊顯示這些特定值比其他值更常見，
主要是取樣誤差造成的）。在較典型的情況下，
某些值明顯比其他值更常見，此時這個複雜的
過程能有效提升準確度，因為最常見值的
選擇率是精確求得的。

現在來看一個 `WHERE` 子句中有超過一個
條件的情況：

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 1000 AND stringu1 = 'xxx';

                                   QUERY PLAN
-------------------------------------------------------------------​-------------
 Bitmap Heap Scan on tenk1  (cost=23.80..396.91 rows=1 width=244)
   Recheck Cond: (unique1 < 1000)
   Filter: (stringu1 = 'xxx'::name)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..23.80 rows=1007 width=0)
         Index Cond: (unique1 < 1000)
```

規劃器假設這兩個條件彼此獨立，因此
各子句的選擇率可以相乘：

```

selectivity = selectivity(unique1 < 1000) * selectivity(stringu1 = 'xxx')
            = 0.100697 * 0.0014559
            = 0.0001466

rows        = 10000 * 0.0001466
            = 1  (rounding off)
```

請注意，估計由點陣圖索引掃描傳回的資料列數
只反映了與索引搭配使用的條件；這一點
很重要，因為它會影響後續從堆積擷取資料的
成本估計。

最後，我們來檢視一個涉及連接的查詢：

```

EXPLAIN SELECT * FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 50 AND t1.unique2 = t2.unique2;

                                      QUERY PLAN
-------------------------------------------------------------------​-------------------
 Nested Loop  (cost=4.64..456.23 rows=50 width=488)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.64..142.17 rows=50 width=244)
         Recheck Cond: (unique1 < 50)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.63 rows=50 width=0)
               Index Cond: (unique1 < 50)
   ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.00..6.27 rows=1 width=244)
         Index Cond: (unique2 = t1.unique2)
```

`tenk1` 上的限制條件
`unique1 < 50`
會在巢狀迴圈連接之前進行求值。
其處理方式與前面的範圍範例類似。這次
值 50 落在
`unique1` 直方圖的第一個區間：

```

selectivity = (0 + (50 - bucket[1].min)/(bucket[1].max - bucket[1].min))/num_buckets
            = (0 + (50 - 0)/(993 - 0))/10
            = 0.005035

rows        = 10000 * 0.005035
            = 50  (rounding off)
```

連接的限制條件是 `t2.unique2 = t1.unique2`。
運算子就是
我們熟悉的 `=`，不過選擇率函式是
從 `pg_operator` 的 `oprjoin` 欄位
取得的，也就是 `eqjoinsel`。
`eqjoinsel` 會查詢
`tenk2` 與 `tenk1` 兩者的統計資訊：

```

SELECT tablename, null_frac,n_distinct, most_common_vals FROM pg_stats
WHERE tablename IN ('tenk1', 'tenk2') AND attname='unique2';

tablename  | null_frac | n_distinct | most_common_vals
-----------+-----------+------------+------------------
 tenk1     |         0 |         -1 |
 tenk2     |         0 |         -1 |
```

在此例中，`unique2` 沒有 MCV 資訊，
而且所有值看起來都是
唯一的（n_distinct = -1），因此我們使用一種演算法，它依據兩個關聯的
資料列數估計值（num_rows，未顯示，但為 "tenk"），
再加上欄位的 null 值比例（兩者皆為零）：

```

selectivity = (1 - null_frac1) * (1 - null_frac2) / max(num_rows1, num_rows2)
            = (1 - 0) * (1 - 0) / max(10000, 10000)
            = 0.0001
```

也就是說，對每個關聯分別用 1 減去 null 值比例，
再除以較大關聯的資料列數（在非唯一的情況下，
這個值確實會按比例調整）。
連接可能輸出的資料列數，
計算方式是兩個輸入之笛卡兒積的基數，乘以
選擇率：

```

rows = (outer_cardinality * inner_cardinality) * selectivity
     = (50 * 10000) * 0.0001
     = 50
```

如果這兩個欄位有 MCV 清單，
`eqjoinsel` 就會直接比較 MCV
清單，來判斷欄位母體中由 MCV 所代表
那部分的連接選擇率。母體其餘部分的估計，
則採用此處所示的相同方法。

請注意，我們將 `inner_cardinality` 表示為 10000，也就是
`tenk2` 未經修改的大小。從
`EXPLAIN` 輸出看來，連接資料列數的估計值
似乎是來自 50 \* 1，也就是外層資料列數乘以
每次對 `tenk2` 進行內層索引掃描所得到的估計資料列數。
但事實並非如此：連接關聯的大小
是在考慮任何特定連接計畫之前就估計好的。如果
一切運作正常，這兩種估計連接大小的方式
會得出大致相同的答案，但由於捨入誤差及
其他因素，它們有時會出現顯著的差異。

對更多細節有興趣的人可以參考：資料表大小的估計
（在套用任何 `WHERE` 子句之前）是在
`src/backend/optimizer/util/plancat.c` 中完成的。子句選擇率的
通用邏輯位於
`src/backend/optimizer/path/clausesel.c`。
運算子專屬的選擇率函式大多位於
`src/backend/utils/adt/selfuncs.c`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/row-estimation-examples.html)（原文版本：18.6；核對日期：2026-10-12）
