---
description: 版本：10
---

# 14.1. 善用EXPLAIN

PostgreSQL 會為它收到的每個查詢設計一個查詢計劃。選擇正確的計劃以搭配查詢結構和資料屬性對於提高效能至關重要，所以系統包含一個複雜的計劃程序，試圖選擇好的計劃。您可以使用 [EXPLAIN](../../reference/sql-commands/explain.md) 指令查看計劃程序為每一個查詢所建立的查詢計劃。計劃內容閱讀是一門需要掌握一定經驗的藝術，但本部分主要涵蓋基本知識。

本節中的範例是在使用 9.3 開發原始碼進行 VACUUM ANALYZE 後進行迴歸測試資料庫中提取的。如果您自己嘗試這些範例，應該能夠獲得類似的結果，但您的估計成本和行數可能略有不同，因為 ANALYZE 的統計資訊是隨機樣本而不是精確的，而且因為成本本質上與平台有關。

這些範例使用 EXPLAIN 的預設「文字」輸出格式，該格式緊湊且便於人類閱讀。 如果要將 EXPLAIN 的輸出提供給程式以進行進一步分析，則應使用其機器可讀輸出格式之一（XML、JSON 或 YAML）。

## 14.1.1. `EXPLAIN` 基本概念

查詢計劃的結構是計劃節點樹。樹底層的節點是掃描節點：它們從資料表中回傳原始資料列。對於不同的資料表存取方法，存在不同類型的掃描節點：循序掃描、索引掃描和 bitmap 索引掃描。還有非資料表的來源，例如 VALUES 中的 VALUES 子句和 set-returns 函數，它們有自己的掃描節點類型。如果查詢需要對原始資料列進行交叉查詢、彙總、排序或其他操作，則掃描節點上方將有其他節點來執行這些操作。同樣，通常有多種可能的方法來執行這些操作，因此這裡也可以顯示不同的節點類型。EXPLAIN 的輸出對於計劃樹中的每個節點都有一行，顯示基本節點類型以及計劃程序為執行該計劃節點所做的成本估算。可能會顯示從節點的摘要行縮進的其他行，以顯示節點的其他屬性。第一行（最頂層節點的摘要行）具有計劃的估計總執行成本；計劃程序會試圖最小化這個數字。

這裡有一個簡單的例子，只是為了顯示輸出的樣子：

```text
EXPLAIN SELECT * FROM tenk1;

                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..458.00 rows=10000 width=244)
```

由於此查詢沒有 WHERE 子句，因此它必須掃描資料表的所有資料列，因此規劃程序選擇使用簡單的循序掃描計劃。括號中引用的數字是（從左到右）：

* 估計的啟動成本。這是在輸出階段開始之前花費的時間，例如，在排序節點中進行排序的時間。
* 估計總成本。這是在假設計劃節點執行完成，即檢索所有可用資料列的情況下評估的。實際上，節點的父節點可能會停止讀取所有可用的資料列（請參閱下面的 LIMIT 範例）。
* 此計劃節點輸出的估計資料列數量。同樣地，假定節點完全執行。
* 此計劃節點輸出的資料列估計的平均資料大小（以 byte 為單位）。

成本按照規劃程序的成本參數決定的各個單位計量（見[第 19.7.2 節](../../server-administration/server-configuration/19.7.-cha-xun-gui-hua.md#19-7-2-planner-cost-constants)）。傳統做法是以磁碟頁面讀取為單位來衡量成本；也就是說，[seq\_page\_cost](../../server-administration/server-configuration/19.7.-cha-xun-gui-hua.md#19-7-2-planner-cost-constants) 通常設定為 1.0，其他成本參數相對於此來設定。本節中的範例使用預設的成本參數進行。

很重要的是要了解上層節點的成本包括其所有子節點的成本。同樣重要的是要意識到成本只反映了計劃程序所關心的事情。特別是，成本不考慮將結果資料列傳輸到用戶端所花費的時間，這可能是實際經過時間的一個重要因素；但是計劃者忽略了它，因為它不能透過改變計劃來改善它。（我們相信，每個正確的計劃都會輸出相同的資料列集合。）

資料列的數目有點棘手，因為它不是計劃節點處理或掃描的數量，而是節點發出的資料列數量。這通常小於掃描的數量，這是透過在節點上套用的任何 WHHERE 子句條件進行過濾的結果。理想情況下，最上層級資料列數量估計值將近似於查詢實際回傳、更新或刪除的資料列數目。

回到我們的例子：

```text
EXPLAIN SELECT * FROM tenk1;

                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..458.00 rows=10000 width=244)
```

這些數字非常直觀。如果你這樣做：

```text
SELECT relpages, reltuples FROM pg_class WHERE relname = 'tenk1';
```

你會發現 tenk1 有 358 個磁碟頁面和 10000 個資料列。估計的成本計算為（磁碟頁讀取  _\*_ [seq\_page\_cost](../../server-administration/server-configuration/19.7.-cha-xun-gui-hua.md#19-7-2-planner-cost-constants)）+（資料列掃描 \* [cpu\_tuple\_cost](../../server-administration/server-configuration/19.7.-cha-xun-gui-hua.md#19-7-2-planner-cost-constants)）。預設的情況下，seq\_page\_cost 為 1.0，cpu\_tuple\_cost 為 0.01，因此估計成本為（358 \*  __1.0）+（10000 \* 0.01）= 458。

現在讓我們修改查詢加入 WHERE 條件：

```text
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 7000;

                         QUERY PLAN
------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..483.00 rows=7001 width=244)
   Filter: (unique1 < 7000)
```

請注意，EXPLAIN 輸出顯示 WHERE 子句作為附加到 Seq Scan 計劃節點的「filter」條件應用。這意味著計劃節點檢查它掃描的每一筆資料的條件，並僅輸出通過該條件的那些資料列。由於 WHERE 子句，輸出資料列的估計已經減少。只是，掃描仍然需要讀取所有 10000 筆資料，因此成本並沒有降低；實際上它已經上升了一點（確切地說是 10000 \* [cpu\_operator\_cost](../../server-administration/server-configuration/19.7.-cha-xun-gui-hua.md#19-7-2-planner-cost-constants)）以反映檢查 WHERE 條件所花費的額外 CPU 時間。

此查詢將回傳的實際筆數為 7000，但筆數估計值僅為近似值。如果您嘗試複製此實驗，您可能會得到略微不同的估計；此外，它可能在每個 ANALYZE 指令之後改變，因為 ANALYZE 産成的統計訊息來自於資料表的隨機樣本。

現在，我們加上更多條件限制：

```text
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100;

                                  QUERY PLAN
------------------------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=5.07..229.20 rows=101 width=244)
   Recheck Cond: (unique1 < 100)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=101 width=0)
         Index Cond: (unique1 < 100)
```

規劃程序決定使用兩個步驟的計劃：子計劃節點讀取索引以查詢與索引條件匹配的資料列位置，然後上層計劃節點實際從資料表本身中提取這些資料列。單獨獲取資料列比按順序讀取它們要昂貴得多，但由於不是必須讀取該資料表的所有頁面，因此這仍然比循序掃描便宜。（使用兩個計劃層級的原因是上層計劃節點在讀取之前將索引標示的資料列位置排序為物理順序，以最小化單獨提取的成本。節點名稱中提到的「bitmap」是排序機制。）

現在讓我們為 WHERE 子句增加另一個條件：

```text
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND stringu1 = 'xxx';

                                  QUERY PLAN
------------------------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=5.04..229.43 rows=1 width=244)
   Recheck Cond: (unique1 < 100)
   Filter: (stringu1 = 'xxx'::name)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=101 width=0)
         Index Cond: (unique1 < 100)
```

增加的條件 stringu1 ='xxx' 減少了輸出資料列數的估計，但不是成本，因為我們仍然必須讀取同一組資料列。請注意，stringu1 子句無法作為索引條件套用，因為此索引僅在 unique1 欄位上。而是將其作為過濾器套用於索引檢索的資料列。因此，成本實際上略有上升，以反映這種額外的檢查。

在某些情況下，規劃程序更喜歡「簡單」的索引掃描計劃：

```text
EXPLAIN SELECT * FROM tenk1 WHERE unique1 = 42;

                                 QUERY PLAN
-----------------------------------------------------------------------------
 Index Scan using tenk1_unique1 on tenk1  (cost=0.29..8.30 rows=1 width=244)
   Index Cond: (unique1 = 42)
```

在這種類型的計劃中，資料列按索引順序讀取，這使得它們讀取起來更加昂貴，但是很少有人覺得資料列位置進行排序的額外成本是不值得的。對於只獲取一個資料列的查詢，您通常會看到此計劃類型。它也經常用於具有與索引順序匹配的 ORDER BY 條件的查詢，因為這樣就不需要額外的排序步驟來滿足 ORDER BY。

如果在 WHERE 中引用的幾個欄位上有單獨的索引，則查詢規劃器可能會選擇使用索引的 AND 及 OR 組合：

```text
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000;

                                     QUERY PLAN
-------------------------------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=25.08..60.21 rows=10 width=244)
   Recheck Cond: ((unique1 < 100) AND (unique2 > 9000))
   ->  BitmapAnd  (cost=25.08..25.08 rows=10 width=0)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=101 width=0)
               Index Cond: (unique1 < 100)
         ->  Bitmap Index Scan on tenk1_unique2  (cost=0.00..19.78 rows=999 width=0)
               Index Cond: (unique2 > 9000)
```

但這需要存取兩個索引，因此與僅使用一個索引並將另一個條件視為過濾器相比，它不一定更好。如果您改變所涉及的範圍，您將看到相應的計劃變更。

以下是顯示 LIMIT 效果的範例：

```text
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000 LIMIT 2;

                                     QUERY PLAN
-------------------------------------------------------------------------------------
 Limit  (cost=0.29..14.48 rows=2 width=244)
   ->  Index Scan using tenk1_unique2 on tenk1  (cost=0.29..71.27 rows=10 width=244)
         Index Cond: (unique2 > 9000)
         Filter: (unique1 < 100)
```

這是與上面相同的查詢，但是我們增加了一個 LIMIT，以便不需要檢索所有資料列，並且計劃程序改變了想要做什麼的想法。請注意，「索引掃描」節點的總成本和資料列數量顯示為執行完成。但是，限制節點預計僅檢索這些資料列中的五分之一後停止，因此其總成本僅為五分之一，這是查詢的實際估計成本。此計劃優於將 Limit 節點加到上一個計劃，因為 Limit 無法避免支付 bitmap 掃描的啟動成本，因此使用該方法的總成本將超過 25 個單位。

讓我們嘗試使用我們一直在討論的欄位來交叉查詢兩個資料表：

```text
EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t1.unique2 = t2.unique2;

                                      QUERY PLAN
--------------------------------------------------------------------------------------
 Nested Loop  (cost=4.65..118.62 rows=10 width=488)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.47 rows=10 width=244)
         Recheck Cond: (unique1 < 10)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0)
               Index Cond: (unique1 < 10)
   ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..7.91 rows=1 width=244)
         Index Cond: (unique2 = t1.unique2)
```

在此計劃中，我們有一個巢狀循環的交叉查詢節點，其中有兩個資料表掃描作為輸入或子節點。節點摘要行的縮進反映了計劃樹狀結構。交叉查詢的第一個或「外部」子節點是一個類似於我們之前看到的 bitmap 掃描。它的成本和行數與我們從SELECT ... WHERE unique1 &lt;10 得到的相同，因為我們在該節點上使用了WHERE 子句 unique1 &lt;10。 t1.unique2 = t2.unique2 子句尚未相關，因此它不會影響外部掃描的行數。巢狀循環交叉查詢節點將為從外部子節點獲取的每一行運行其第二個或“內部”子節點一次。來自當下外部交叉查詢資料列的欄位值可以插入內部掃瞄；在這裡，來自外部交叉查詢資料列的 t1.unique2 值是可用的，因此我們得到一個類似於我們在上面看到的簡單「SELECT ... WHERE t2.unique2 = 常數」的情況。 （估計的成本實際上比上面看到的要低一些，因為在 t2 上重複索引掃描期間預計會發生快取。）然後根據成本確定循環節點的成本。外部交叉查詢掃描，每個外部交叉查詢資料列重複一次內部交叉查詢掃描（此處為10 \* 7.91），加上一點 CPU 時間進行交叉查詢處理。

在此範例中，交叉查詢的輸出資料列計數與兩個掃描的資料列計數的乘積相同，但在所有情況下都不是這樣，因為可以有其他 WHERE 子句提及兩個資料表，因此只會用於交叉查詢的節點，不論其他輸入任何掃描。這是一個例子：

```text
EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t2.unique2 < 10 AND t1.hundred < t2.hundred;

                                         QUERY PLAN
---------------------------------------------------------------------------------------------
 Nested Loop  (cost=4.65..49.46 rows=33 width=488)
   Join Filter: (t1.hundred < t2.hundred)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.47 rows=10 width=244)
         Recheck Cond: (unique1 < 10)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0)
               Index Cond: (unique1 < 10)
   ->  Materialize  (cost=0.29..8.51 rows=10 width=244)
         ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..8.46 rows=10 width=244)
               Index Cond: (unique2 < 10)
```

The condition `t1.hundred < t2.hundred` can't be tested in the `tenk2_unique2` index, so it's applied at the join node. This reduces the estimated output row count of the join node, but does not change either input scan.

Notice that here the planner has chosen to “materialize” the inner relation of the join, by putting a Materialize plan node atop it. This means that the `t2` index scan will be done just once, even though the nested-loop join node needs to read that data ten times, once for each row from the outer relation. The Materialize node saves the data in memory as it's read, and then returns the data from memory on each subsequent pass.

When dealing with outer joins, you might see join plan nodes with both “Join Filter” and plain “Filter” conditions attached. Join Filter conditions come from the outer join's `ON` clause, so a row that fails the Join Filter condition could still get emitted as a null-extended row. But a plain Filter condition is applied after the outer-join rules and so acts to remove rows unconditionally. In an inner join there is no semantic difference between these types of filters.

If we change the query's selectivity a bit, we might get a very different join plan:

```text
EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Hash Join  (cost=230.47..713.98 rows=101 width=488)
   Hash Cond: (t2.unique2 = t1.unique2)
   ->  Seq Scan on tenk2 t2  (cost=0.00..445.00 rows=10000 width=244)
   ->  Hash  (cost=229.20..229.20 rows=101 width=244)
         ->  Bitmap Heap Scan on tenk1 t1  (cost=5.07..229.20 rows=101 width=244)
               Recheck Cond: (unique1 < 100)
               ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=101 width=0)
                     Index Cond: (unique1 < 100)
```

Here, the planner has chosen to use a hash join, in which rows of one table are entered into an in-memory hash table, after which the other table is scanned and the hash table is probed for matches to each row. Again note how the indentation reflects the plan structure: the bitmap scan on `tenk1` is the input to the Hash node, which constructs the hash table. That's then returned to the Hash Join node, which reads rows from its outer child plan and searches the hash table for each one.

Another possible type of join is a merge join, illustrated here:

```text
EXPLAIN SELECT *
FROM tenk1 t1, onek t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Merge Join  (cost=198.11..268.19 rows=10 width=488)
   Merge Cond: (t1.unique2 = t2.unique2)
   ->  Index Scan using tenk1_unique2 on tenk1 t1  (cost=0.29..656.28 rows=101 width=244)
         Filter: (unique1 < 100)
   ->  Sort  (cost=197.83..200.33 rows=1000 width=244)
         Sort Key: t2.unique2
         ->  Seq Scan on onek t2  (cost=0.00..148.00 rows=1000 width=244)
```

Merge join requires its input data to be sorted on the join keys. In this plan the `tenk1` data is sorted by using an index scan to visit the rows in the correct order, but a sequential scan and sort is preferred for `onek`, because there are many more rows to be visited in that table. \(Sequential-scan-and-sort frequently beats an index scan for sorting many rows, because of the nonsequential disk access required by the index scan.\)

One way to look at variant plans is to force the planner to disregard whatever strategy it thought was the cheapest, using the enable/disable flags described in [Section 19.7.1](https://www.postgresql.org/docs/10/static/runtime-config-query.html#RUNTIME-CONFIG-QUERY-ENABLE). \(This is a crude tool, but useful. See also [Section 14.3](https://www.postgresql.org/docs/10/static/explicit-joins.html).\) For example, if we're unconvinced that sequential-scan-and-sort is the best way to deal with table `onek` in the previous example, we could try

```text
SET enable_sort = off;

EXPLAIN SELECT *
FROM tenk1 t1, onek t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Merge Join  (cost=0.56..292.65 rows=10 width=488)
   Merge Cond: (t1.unique2 = t2.unique2)
   ->  Index Scan using tenk1_unique2 on tenk1 t1  (cost=0.29..656.28 rows=101 width=244)
         Filter: (unique1 < 100)
   ->  Index Scan using onek_unique2 on onek t2  (cost=0.28..224.79 rows=1000 width=244)
```

which shows that the planner thinks that sorting `onek` by index-scanning is about 12% more expensive than sequential-scan-and-sort. Of course, the next question is whether it's right about that. We can investigate that using`EXPLAIN ANALYZE`, as discussed below.

## 14.1.2. `EXPLAIN ANALYZE`

可以使用 EXPLAIN 的 ANALYZE 選項檢查計劃員估算的準確性。 使用此選項，EXPLAIN 實際執行查詢，然後顯示每個計劃節點中累積的真實資料列計數和真實執行時間，以及簡單 EXPLAIN 顯示的相同估計值。例如，我們可能得到這樣的結果：

```text
EXPLAIN ANALYZE SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t1.unique2 = t2.unique2;

                                                           QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------
 Nested Loop  (cost=4.65..118.62 rows=10 width=488) (actual time=0.128..0.377 rows=10 loops=1)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.47 rows=10 width=244) (actual time=0.057..0.121 rows=10 loops=1)
         Recheck Cond: (unique1 < 10)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0) (actual time=0.024..0.024 rows=10 loops=1)
               Index Cond: (unique1 < 10)
   ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..7.91 rows=1 width=244) (actual time=0.021..0.022 rows=1 loops=10)
         Index Cond: (unique2 = t1.unique2)
 Planning time: 0.181 ms
 Execution time: 0.501 ms
```

注意，「實際時間」值是實際執行的時間，以毫秒為單位，而成本估算會以任意單位表示；所以他們不太可能匹配。通常最重要的事情是估計的資料列數量是否與現實相當接近。在這個例子中，估計都是死的，但這在實務上很不尋常。

In some query plans, it is possible for a subplan node to be executed more than once. For example, the inner index scan will be executed once per outer row in the above nested-loop plan. In such cases, the `loops` value reports the total number of executions of the node, and the actual time and rows values shown are averages per-execution. This is done to make the numbers comparable with the way that the cost estimates are shown. Multiply by the `loops`value to get the total time actually spent in the node. In the above example, we spent a total of 0.220 milliseconds executing the index scans on `tenk2`.

In some cases `EXPLAIN ANALYZE` shows additional execution statistics beyond the plan node execution times and row counts. For example, Sort and Hash nodes provide extra information:

```text
EXPLAIN ANALYZE SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2 ORDER BY t1.fivethous;

                                                                 QUERY PLAN
--------------------------------------------------------------------------------------------------------------------------------------------
 Sort  (cost=717.34..717.59 rows=101 width=488) (actual time=7.761..7.774 rows=100 loops=1)
   Sort Key: t1.fivethous
   Sort Method: quicksort  Memory: 77kB
   ->  Hash Join  (cost=230.47..713.98 rows=101 width=488) (actual time=0.711..7.427 rows=100 loops=1)
         Hash Cond: (t2.unique2 = t1.unique2)
         ->  Seq Scan on tenk2 t2  (cost=0.00..445.00 rows=10000 width=244) (actual time=0.007..2.583 rows=10000 loops=1)
         ->  Hash  (cost=229.20..229.20 rows=101 width=244) (actual time=0.659..0.659 rows=100 loops=1)
               Buckets: 1024  Batches: 1  Memory Usage: 28kB
               ->  Bitmap Heap Scan on tenk1 t1  (cost=5.07..229.20 rows=101 width=244) (actual time=0.080..0.526 rows=100 loops=1)
                     Recheck Cond: (unique1 < 100)
                     ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=101 width=0) (actual time=0.049..0.049 rows=100 loops=1)
                           Index Cond: (unique1 < 100)
 Planning time: 0.194 ms
 Execution time: 8.008 ms
```

The Sort node shows the sort method used \(in particular, whether the sort was in-memory or on-disk\) and the amount of memory or disk space needed. The Hash node shows the number of hash buckets and batches as well as the peak amount of memory used for the hash table. \(If the number of batches exceeds one, there will also be disk space usage involved, but that is not shown.\)

Another type of extra information is the number of rows removed by a filter condition:

```text
EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE ten < 7;

                                               QUERY PLAN
---------------------------------------------------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..483.00 rows=7000 width=244) (actual time=0.016..5.107 rows=7000 loops=1)
   Filter: (ten < 7)
   Rows Removed by Filter: 3000
 Planning time: 0.083 ms
 Execution time: 5.905 ms
```

These counts can be particularly valuable for filter conditions applied at join nodes. The “Rows Removed” line only appears when at least one scanned row, or potential join pair in the case of a join node, is rejected by the filter condition.

A case similar to filter conditions occurs with “lossy” index scans. For example, consider this search for polygons containing a specific point:

```text
EXPLAIN ANALYZE SELECT * FROM polygon_tbl WHERE f1 @> polygon '(0.5,2.0)';

                                              QUERY PLAN
------------------------------------------------------------------------------------------------------
 Seq Scan on polygon_tbl  (cost=0.00..1.05 rows=1 width=32) (actual time=0.044..0.044 rows=0 loops=1)
   Filter: (f1 @> '((0.5,2))'::polygon)
   Rows Removed by Filter: 4
 Planning time: 0.040 ms
 Execution time: 0.083 ms
```

The planner thinks \(quite correctly\) that this sample table is too small to bother with an index scan, so we have a plain sequential scan in which all the rows got rejected by the filter condition. But if we force an index scan to be used, we see:

```text
SET enable_seqscan TO off;

EXPLAIN ANALYZE SELECT * FROM polygon_tbl WHERE f1 @> polygon '(0.5,2.0)';

                                                        QUERY PLAN
--------------------------------------------------------------------------------------------------------------------------
 Index Scan using gpolygonind on polygon_tbl  (cost=0.13..8.15 rows=1 width=32) (actual time=0.062..0.062 rows=0 loops=1)
   Index Cond: (f1 @> '((0.5,2))'::polygon)
   Rows Removed by Index Recheck: 1
 Planning time: 0.034 ms
 Execution time: 0.144 ms
```

Here we can see that the index returned one candidate row, which was then rejected by a recheck of the index condition. This happens because a GiST index is “lossy” for polygon containment tests: it actually returns the rows with polygons that overlap the target, and then we have to do the exact containment test on those rows.

`EXPLAIN` has a `BUFFERS` option that can be used with `ANALYZE` to get even more run time statistics:

```text
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000;

                                                           QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=25.08..60.21 rows=10 width=244) (actual time=0.323..0.342 rows=10 loops=1)
   Recheck Cond: ((unique1 < 100) AND (unique2 > 9000))
   Buffers: shared hit=15
   ->  BitmapAnd  (cost=25.08..25.08 rows=10 width=0) (actual time=0.309..0.309 rows=0 loops=1)
         Buffers: shared hit=7
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=101 width=0) (actual time=0.043..0.043 rows=100 loops=1)
               Index Cond: (unique1 < 100)
               Buffers: shared hit=2
         ->  Bitmap Index Scan on tenk1_unique2  (cost=0.00..19.78 rows=999 width=0) (actual time=0.227..0.227 rows=999 loops=1)
               Index Cond: (unique2 > 9000)
               Buffers: shared hit=5
 Planning time: 0.088 ms
 Execution time: 0.423 ms
```

The numbers provided by `BUFFERS` help to identify which parts of the query are the most I/O-intensive.

Keep in mind that because `EXPLAIN ANALYZE` actually runs the query, any side-effects will happen as usual, even though whatever results the query might output are discarded in favor of printing the `EXPLAIN` data. If you want to analyze a data-modifying query without changing your tables, you can roll the command back afterwards, for example:

```text
BEGIN;

EXPLAIN ANALYZE UPDATE tenk1 SET hundred = hundred + 1 WHERE unique1 < 100;

                                                           QUERY PLAN
--------------------------------------------------------------------------------------------------------------------------------
 Update on tenk1  (cost=5.07..229.46 rows=101 width=250) (actual time=14.628..14.628 rows=0 loops=1)
   ->  Bitmap Heap Scan on tenk1  (cost=5.07..229.46 rows=101 width=250) (actual time=0.101..0.439 rows=100 loops=1)
         Recheck Cond: (unique1 < 100)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=101 width=0) (actual time=0.043..0.043 rows=100 loops=1)
               Index Cond: (unique1 < 100)
 Planning time: 0.079 ms
 Execution time: 14.727 ms

ROLLBACK;
```

As seen in this example, when the query is an `INSERT`, `UPDATE`, or `DELETE` command, the actual work of applying the table changes is done by a top-level Insert, Update, or Delete plan node. The plan nodes underneath this node perform the work of locating the old rows and/or computing the new data. So above, we see the same sort of bitmap table scan we've seen already, and its output is fed to an Update node that stores the updated rows. It's worth noting that although the data-modifying node can take a considerable amount of run time \(here, it's consuming the lion's share of the time\), the planner does not currently add anything to the cost estimates to account for that work. That's because the work to be done is the same for every correct query plan, so it doesn't affect planning decisions.

When an `UPDATE` or `DELETE` command affects an inheritance hierarchy, the output might look like this:

```text
EXPLAIN UPDATE parent SET f2 = f2 + 1 WHERE f1 = 101;
                                    QUERY PLAN
-----------------------------------------------------------------------------------
 Update on parent  (cost=0.00..24.53 rows=4 width=14)
   Update on parent
   Update on child1
   Update on child2
   Update on child3
   ->  Seq Scan on parent  (cost=0.00..0.00 rows=1 width=14)
         Filter: (f1 = 101)
   ->  Index Scan using child1_f1_key on child1  (cost=0.15..8.17 rows=1 width=14)
         Index Cond: (f1 = 101)
   ->  Index Scan using child2_f1_key on child2  (cost=0.15..8.17 rows=1 width=14)
         Index Cond: (f1 = 101)
   ->  Index Scan using child3_f1_key on child3  (cost=0.15..8.17 rows=1 width=14)
         Index Cond: (f1 = 101)
```

In this example the Update node needs to consider three child tables as well as the originally-mentioned parent table. So there are four input scanning subplans, one per table. For clarity, the Update node is annotated to show the specific target tables that will be updated, in the same order as the corresponding subplans. \(These annotations are new as of PostgreSQL 9.5; in prior versions the reader had to intuit the target tables by inspecting the subplans.\)

The `Planning time` shown by `EXPLAIN ANALYZE` is the time it took to generate the query plan from the parsed query and optimize it. It does not include parsing or rewriting.

The `Execution time` shown by `EXPLAIN ANALYZE` includes executor start-up and shut-down time, as well as the time to run any triggers that are fired, but it does not include parsing, rewriting, or planning time. Time spent executing `BEFORE` triggers, if any, is included in the time for the related Insert, Update, or Delete node; but time spent executing `AFTER` triggers is not counted there because `AFTER` triggers are fired after completion of the whole plan. The total time spent in each trigger \(either `BEFORE` or `AFTER`\) is also shown separately. Note that deferred constraint triggers will not be executed until end of transaction and are thus not considered at all by `EXPLAIN ANALYZE`.

## 14.1.3. 注意事項

EXPLAIN ANALYZE 測量的執行時間有兩種主要情況可能偏離同一查詢的實際執行。首先，由於沒有輸出資料列傳送到客戶端，因此不包括網路傳輸成本和 I/O 轉換成本。其次，EXPLAIN ANALYZE 增加的測量開銷可能很大，特別是在具有較慢 gettimeofday\(\) 作業系統的機器上。您可以使用 [pg\_test\_timing](../../reference/server-applications/pg_test_timing.md) 工具來衡量系統計時的成本。

EXPLAIN 結果不應該推斷到與您實際測試的情況大不相同的情況；例如，不能假設小型資料表上的結果適用於大型資料表。規劃程序的成本估算不是線性的，因此可能會為更大或更小的資料表選擇不同的計劃。一個極端的例子是，在只佔用一個磁碟頁面的資料表上，無論索引是否可用，您幾乎總能獲得循順掃描計劃。規劃程序在任何情況下都會讀取一個磁碟頁面來處理資料表，因此在延伸額外的頁面讀取以查看索引時就沒有任何價值。（我們在上面的 polygon\_tbl 範例中看到了這種情況。）

在某些情況下，實際值和估計值不能很好地對應，但沒有什麼是真正的錯誤。當計劃節點執行由 LIMIT 或類似效果停止時，就會發生這種情況。例如，在我們之前使用的 LIMIT 查詢中，

```text
EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000 LIMIT 2;

                                                          QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.29..14.71 rows=2 width=244) (actual time=0.177..0.249 rows=2 loops=1)
   ->  Index Scan using tenk1_unique2 on tenk1  (cost=0.29..72.42 rows=10 width=244) (actual time=0.174..0.244 rows=2 loops=1)
         Index Cond: (unique2 > 9000)
         Filter: (unique1 < 100)
         Rows Removed by Filter: 287
 Planning time: 0.096 ms
 Execution time: 0.336 ms
```

索引掃描節點的估計成本和資料列數目顯示為執行完成。但實際上，Limit 節點在獲得兩個資料列後停止請求，因此實際資料列數目僅為 2，執行時間小於成本估算所顯示的。這不是估計誤差，只是估計值和真實值顯示方式有所差異。

交叉查詢也有測量工具，也可能産生混淆。如果一個輸入耗盡了另一個輸入，並且一個輸入中的下一個鍵值大於另一個輸入的最後一個鍵值，則交叉查詢將停止讀取一個輸入；在這種情況下，不可能再有匹配，因此不需要掃描第一個輸入的其餘部分。這導致不讀取所有下一個子項，結果如 LIMIT 所述。此外，如果外部（第一個）子項包含具有重複鍵值的資料列，則內部（第二個）子項將被備份並重新掃描其與該鍵值匹配資料列的部分。EXPLAIN ANALYZE 計算相同內部資料列的這些重複映射，就好像它們是真正的附加資料列一樣。當存在許多外部重複項時，內部子計劃節點的報告實際資料列數目可能明顯大於內部關連中實際存在的資料列數目。

由於實作限制，BitmapAnd 和 BitmapOr 節點始終將其實際資料列計數回報為零。

