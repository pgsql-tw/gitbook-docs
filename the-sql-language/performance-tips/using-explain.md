<a id="USING-EXPLAIN"></a>

## 14.1. 使用 `EXPLAIN` [#](#USING-EXPLAIN)

[14.1.1. `EXPLAIN` 基礎](using-explain.md#USING-EXPLAIN-BASICS)

[14.1.2. `EXPLAIN ANALYZE`](using-explain.md#USING-EXPLAIN-ANALYZE)

[14.1.3. 注意事項](using-explain.md#USING-EXPLAIN-CAVEATS)

<a id="id-1.5.13.4.2"></a><a id="id-1.5.13.4.3"></a>

PostgreSQL 會為它收到的每個查詢擬定一個*查詢計畫*（query plan）。選擇與查詢結構及資料特性相符的正確計畫，對良好的效能至關重要，因此系統包含了一個複雜的*規劃器*（planner），試圖選出好的計畫。你可以使用 [`EXPLAIN`](../../reference/sql-commands/sql-explain.md) 命令，查看規劃器為任何查詢建立了什麼樣的查詢計畫。解讀計畫是一門需要一些經驗才能掌握的藝術，但本節會試著介紹基礎知識。

本節中的範例取自執行過 `VACUUM ANALYZE` 之後的迴歸測試資料庫，使用的是 v18 的開發版原始碼。如果你自己嘗試這些範例，應該能得到類似的結果，但估計的成本與資料列數可能會略有不同，因為 `ANALYZE` 的統計資訊是隨機取樣而非精確值，而且成本本質上多少與平台相關。

這些範例使用 `EXPLAIN` 預設的「text」輸出格式，這種格式精簡，便於人類閱讀。如果你想將 `EXPLAIN` 的輸出交給程式做進一步分析，應該改用它的其中一種機器可讀輸出格式（XML、JSON 或 YAML）。

<a id="USING-EXPLAIN-BASICS"></a>

### 14.1.1. `EXPLAIN` 基礎 [#](#USING-EXPLAIN-BASICS)

查詢計畫的結構是一棵由*計畫節點*（plan node）組成的樹。樹最底層的節點是掃描節點：它們從資料表回傳原始的資料列。不同的資料表存取方法有不同類型的掃描節點：循序掃描、索引掃描與點陣圖索引掃描。此外也有非資料表的資料列來源，例如 `VALUES` 子句與 `FROM` 中的集合回傳函式，它們有自己的掃描節點類型。如果查詢需要對原始資料列進行聯結、彙總、排序或其他操作，那麼在掃描節點之上就會有額外的節點來執行這些操作。同樣地，執行這些操作的方式通常不只一種，因此這裡也可能出現不同的節點類型。`EXPLAIN` 的輸出中，計畫樹的每個節點各占一行，顯示基本的節點類型，以及規劃器為執行該計畫節點所做的成本估計。可能還會出現額外的幾行，從節點的摘要行縮排，用來顯示節點的其他屬性。最開頭的第一行（最上層節點的摘要行）是該計畫估計的總執行成本；規劃器試圖最小化的正是這個數字。

以下是一個非常簡單的範例，只是為了展示輸出的樣子：

```

EXPLAIN SELECT * FROM tenk1;

                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..445.00 rows=10000 width=244)
```

由於這個查詢沒有 `WHERE` 子句，它必須掃描資料表中的所有資料列，因此規劃器選擇使用簡單的循序掃描計畫。括號中列出的數字（由左至右）分別是：

* 估計的啟動成本。這是在輸出階段能夠開始之前所花費的時間，例如在排序節點中進行排序的時間。
* 估計的總成本。這是在假設計畫節點會執行到完成（也就是取得所有可用的資料列）的前提下所得出的。實際上，節點的上層節點可能會在讀取完所有可用資料列之前就停止（請參閱下面的 `LIMIT` 範例）。
* 估計這個計畫節點輸出的資料列數。同樣地，這是假設節點會執行到完成。
* 估計這個計畫節點輸出之資料列的平均寬度（以位元組為單位）。

成本是以由規劃器成本參數所決定的任意單位來衡量的（請參閱[第 19.7.2 節](../../server-administration/runtime-config/runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)）。傳統的做法是以磁碟頁面擷取次數為單位來衡量成本；也就是說，[seq_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-SEQ-PAGE-COST) 慣例上設為 `1.0`，而其他成本參數則相對於它來設定。本節中的範例都是使用預設的成本參數執行的。

重要的是要了解，上層節點的成本包含了其所有子節點的成本。同樣重要的是要明白，成本只反映規劃器在意的事情。特別是，成本並未考慮將輸出值轉換為文字形式或傳送給用戶端所花費的時間，而這些可能是實際經過時間中的重要因素；但規劃器會忽略這些成本，因為它無法藉由改變計畫來改變它們。（我們相信，每個正確的計畫都會輸出相同的資料列集合。）

`rows` 值有點微妙，因為它不是計畫節點處理或掃描的資料列數，而是該節點輸出的資料列數。由於在該節點上套用的任何 `WHERE` 子句條件會進行過濾，這個數字通常會少於掃描的資料列數。理想情況下，最上層的資料列數估計會接近查詢實際回傳、更新或刪除的資料列數。

回到我們的範例：

```

EXPLAIN SELECT * FROM tenk1;

                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..445.00 rows=10000 width=244)
```

這些數字的推導方式非常直接。如果你執行：

```

SELECT relpages, reltuples FROM pg_class WHERE relname = 'tenk1';
```

你會發現 `tenk1` 有 345 個磁碟頁面與 10000 筆資料列。估計的成本計算方式為（讀取的磁碟頁面數 \* [seq_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-SEQ-PAGE-COST)）+（掃描的資料列數 \* [cpu_tuple_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-CPU-TUPLE-COST)）。預設情況下，`seq_page_cost` 為 1.0，`cpu_tuple_cost` 為 0.01，因此估計的成本為 (345 \* 1.0) + (10000 \* 0.01) = 445。

現在，讓我們修改查詢，加上一個 `WHERE` 條件：

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 7000;

                         QUERY PLAN
------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..470.00 rows=7000 width=244)
   Filter: (unique1 < 7000)
```

請注意，`EXPLAIN` 的輸出顯示 `WHERE` 子句被當作附加在 Seq Scan 計畫節點上的「filter」（過濾）條件套用。這表示該計畫節點會對它掃描的每一筆資料列檢查這個條件，並只輸出通過條件的資料列。由於 `WHERE` 子句的關係，輸出資料列數的估計減少了。不過，掃描仍然必須走訪全部 10000 筆資料列，因此成本並沒有降低；事實上，成本還略微上升了（確切地說，增加了 10000 \* [cpu_operator_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-CPU-OPERATOR-COST)），以反映檢查 `WHERE` 條件所花費的額外 CPU 時間。

這個查詢實際會選取的資料列數是 7000，但 `rows` 估計只是近似值。如果你試著重現這個實驗，很可能會得到略有不同的估計值；此外，它在每次執行 `ANALYZE` 命令之後都可能改變，因為 `ANALYZE` 所產生的統計資訊取自資料表的隨機樣本。

現在，讓我們把條件設得更嚴格：

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100;

                                  QUERY PLAN
-------------------------------------------------------------------​-----------
 Bitmap Heap Scan on tenk1  (cost=5.06..224.98 rows=100 width=244)
   Recheck Cond: (unique1 < 100)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
         Index Cond: (unique1 < 100)
```

在這裡，規劃器決定使用兩步驟的計畫：子計畫節點會走訪索引，找出符合索引條件之資料列的位置，然後上層計畫節點再實際從資料表本身擷取這些資料列。個別擷取資料列比循序讀取它們要昂貴得多，但由於不需要走訪資料表的所有頁面，這仍然比循序掃描便宜。（使用兩個計畫層級的原因是，上層計畫節點會先將索引所找出的資料列位置依實體順序排序，然後再讀取它們，以將個別擷取的成本降到最低。節點名稱中提到的「bitmap」（點陣圖），就是進行這項排序的機制。）

現在，讓我們在 `WHERE` 子句中再加上一個條件：

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND stringu1 = 'xxx';

                                  QUERY PLAN
-------------------------------------------------------------------​-----------
 Bitmap Heap Scan on tenk1  (cost=5.04..225.20 rows=1 width=244)
   Recheck Cond: (unique1 < 100)
   Filter: (stringu1 = 'xxx'::name)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
         Index Cond: (unique1 < 100)
```

新增的條件 `stringu1 = 'xxx'` 降低了輸出資料列數的估計，但沒有降低成本，因為我們仍然必須走訪相同的資料列集合。這是因為 `stringu1` 子句無法作為索引條件套用，因為這個索引只建立在 `unique1` 欄位上。取而代之的是，它會被當作過濾條件，套用在使用索引取得的資料列上。因此，成本實際上略微上升，以反映這項額外的檢查。

在某些情況下，規劃器會偏好「簡單的」索引掃描計畫：

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 = 42;

                                 QUERY PLAN
-------------------------------------------------------------------​----------
 Index Scan using tenk1_unique1 on tenk1  (cost=0.29..8.30 rows=1 width=244)
   Index Cond: (unique1 = 42)
```

在這種計畫中，資料表的資料列是依索引順序擷取的，這使得讀取它們的成本更高，但由於資料列非常少，不值得為排序資料列位置付出額外的成本。你最常在只擷取單一資料列的查詢中看到這種計畫類型。它也經常用於具有與索引順序相符之 `ORDER BY` 條件的查詢，因為這樣就不需要額外的排序步驟來滿足 `ORDER BY`。在這個範例中，加上 `ORDER BY unique1` 會使用相同的計畫，因為索引本身已經隱含地提供了所要求的順序。

規劃器可能會以數種方式實作 `ORDER BY` 子句。上面的範例顯示，這樣的排序子句可以隱含地實作。規劃器也可能加入明確的 `Sort` 步驟：

```

EXPLAIN SELECT * FROM tenk1 ORDER BY unique1;

                            QUERY PLAN
-------------------------------------------------------------------
 Sort  (cost=1109.39..1134.39 rows=10000 width=244)
   Sort Key: unique1
   ->  Seq Scan on tenk1  (cost=0.00..445.00 rows=10000 width=244)
```

如果計畫中的某個部分保證了所需排序鍵之前綴的順序，規劃器可能會改為決定使用 `Incremental Sort`（遞增排序）步驟：

```

EXPLAIN SELECT * FROM tenk1 ORDER BY hundred, ten LIMIT 100;

                                              QUERY PLAN
-------------------------------------------------------------------​-----------------------------
 Limit  (cost=19.35..39.49 rows=100 width=244)
   ->  Incremental Sort  (cost=19.35..2033.39 rows=10000 width=244)
         Sort Key: hundred, ten
         Presorted Key: hundred
         ->  Index Scan using tenk1_hundred on tenk1  (cost=0.29..1574.20 rows=10000 width=244)
```

與一般排序相比，遞增排序允許在整個結果集排序完成之前就回傳 tuple，這特別能夠讓 `LIMIT` 查詢進行最佳化。它也可能降低記憶體用量，以及排序溢出到磁碟的可能性，但代價是將結果集拆分成多個排序批次所增加的額外負擔。

如果在 `WHERE` 中參照的數個欄位上各有獨立的索引，規劃器可能會選擇使用這些索引的 AND 或 OR 組合：

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000;

                                     QUERY PLAN
-------------------------------------------------------------------​------------------
 Bitmap Heap Scan on tenk1  (cost=25.07..60.11 rows=10 width=244)
   Recheck Cond: ((unique1 < 100) AND (unique2 > 9000))
   ->  BitmapAnd  (cost=25.07..25.07 rows=10 width=0)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
               Index Cond: (unique1 < 100)
         ->  Bitmap Index Scan on tenk1_unique2  (cost=0.00..19.78 rows=999 width=0)
               Index Cond: (unique2 > 9000)
```

但這需要走訪兩個索引，因此與只使用一個索引、並將另一個條件當作過濾條件相比，不一定比較划算。如果你改變所涉及的範圍，就會看到計畫隨之改變。

以下是一個展示 `LIMIT` 效果的範例：

```

EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000 LIMIT 2;

                                     QUERY PLAN
-------------------------------------------------------------------​------------------
 Limit  (cost=0.29..14.28 rows=2 width=244)
   ->  Index Scan using tenk1_unique2 on tenk1  (cost=0.29..70.27 rows=10 width=244)
         Index Cond: (unique2 > 9000)
         Filter: (unique1 < 100)
```

這與上面的查詢相同，但我們加上了 `LIMIT`，因此不需要取得所有的資料列，於是規劃器改變了它的做法。請注意，Index Scan 節點的總成本與資料列數，是以假設它會執行到完成的方式顯示的。不過，Limit 節點預期在只取得其中五分之一的資料列之後就會停止，因此它的總成本只有五分之一，而這才是該查詢實際的估計成本。之所以偏好這個計畫，而不是在前一個計畫上加一個 Limit 節點，是因為 Limit 無法避免支付點陣圖掃描的啟動成本，因此採用那種做法的總成本會超過 25 個單位。

讓我們試著使用我們一直在討論的欄位來聯結兩個資料表：

```

EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t1.unique2 = t2.unique2;

                                      QUERY PLAN
-------------------------------------------------------------------​-------------------
 Nested Loop  (cost=4.65..118.50 rows=10 width=488)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.38 rows=10 width=244)
         Recheck Cond: (unique1 < 10)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0)
               Index Cond: (unique1 < 10)
   ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..7.90 rows=1 width=244)
         Index Cond: (unique2 = t1.unique2)
```

在這個計畫中，有一個巢狀迴圈聯結節點，它以兩個資料表掃描作為輸入，也就是子節點。節點摘要行的縮排反映了計畫樹的結構。聯結的第一個子節點，也就是「外部」（outer）子節點，是一個與我們之前看過的類似的點陣圖掃描。它的成本與資料列數，與我們從 `SELECT ... WHERE unique1 < 10` 所得到的相同，因為我們在該節點上套用了 `WHERE` 子句 `unique1 < 10`。`t1.unique2 = t2.unique2` 子句在這時還不相關，因此不會影響外部掃描的資料列數。巢狀迴圈聯結節點會對從外部子節點取得的每一筆資料列，各執行一次它的第二個子節點，也就是「內部」（inner）子節點。目前外部資料列的欄位值可以代入內部掃描；在這裡，可以使用外部資料列的 `t1.unique2` 值，因此我們得到的計畫與成本，類似於上面看到的簡單 `SELECT ... WHERE t2.unique2 = constant` 情況。（由於預期在重複對 `t2` 進行索引掃描時會發生快取，估計的成本實際上比上面看到的略低一些。）接著，迴圈節點的成本是根據外部掃描的成本，加上每一筆外部資料列各重複一次內部掃描的成本（這裡是 10 \* 7.90），再加上一點用於聯結處理的 CPU 時間來設定的。

在這個範例中，聯結的輸出資料列數與兩個掃描之資料列數的乘積相同，但並非所有情況都是如此，因為可能還有其他同時提及兩個資料表的 `WHERE` 子句，這些子句只能在聯結點套用，而無法套用到任一個輸入掃描上。以下是一個範例：

```

EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t2.unique2 < 10 AND t1.hundred < t2.hundred;

                                         QUERY PLAN
-------------------------------------------------------------------​--------------------------
 Nested Loop  (cost=4.65..49.36 rows=33 width=488)
   Join Filter: (t1.hundred < t2.hundred)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.38 rows=10 width=244)
         Recheck Cond: (unique1 < 10)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0)
               Index Cond: (unique1 < 10)
   ->  Materialize  (cost=0.29..8.51 rows=10 width=244)
         ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..8.46 rows=10 width=244)
               Index Cond: (unique2 < 10)
```

條件 `t1.hundred < t2.hundred` 無法在 `tenk2_unique2` 索引中檢驗，因此它會在聯結節點上套用。這降低了聯結節點估計的輸出資料列數，但不會改變任何一個輸入掃描。

請注意，這裡的規劃器選擇了將聯結的內部關聯「實體化」（materialize），方法是在其上方放置一個 Materialize 計畫節點。這表示 `t2` 的索引掃描只會執行一次，即使巢狀迴圈聯結節點需要讀取該資料十次（外部關聯的每一筆資料列各一次）。Materialize 節點會在讀取資料時將它保存在記憶體中，然後在之後的每一輪都從記憶體回傳資料。

處理外部聯結時，你可能會看到同時附加了「Join Filter」與一般「Filter」條件的聯結計畫節點。Join Filter 條件來自外部聯結的 `ON` 子句，因此不符合 Join Filter 條件的資料列，仍然可能被當作以 null 延伸的資料列輸出。但一般的 Filter 條件是在外部聯結規則之後才套用的，因此會無條件地移除資料列。在內部聯結中，這兩種過濾條件在語意上沒有差別。

如果我們稍微改變查詢的選擇率，可能會得到非常不同的聯結計畫：

```

EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Hash Join  (cost=226.23..709.73 rows=100 width=488)
   Hash Cond: (t2.unique2 = t1.unique2)
   ->  Seq Scan on tenk2 t2  (cost=0.00..445.00 rows=10000 width=244)
   ->  Hash  (cost=224.98..224.98 rows=100 width=244)
         ->  Bitmap Heap Scan on tenk1 t1  (cost=5.06..224.98 rows=100 width=244)
               Recheck Cond: (unique1 < 100)
               ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
                     Index Cond: (unique1 < 100)
```

在這裡，規劃器選擇使用雜湊聯結，也就是將一個資料表的資料列放入記憶體中的雜湊表，然後掃描另一個資料表，並針對每一筆資料列在雜湊表中探查相符的項目。同樣請注意縮排如何反映計畫結構：對 `tenk1` 的點陣圖掃描是 Hash 節點的輸入，Hash 節點會建構雜湊表。雜湊表接著會回傳給 Hash Join 節點，該節點會從它的外部子計畫讀取資料列，並針對每一筆資料列搜尋雜湊表。

另一種可能的聯結類型是合併聯結，如下所示：

```

EXPLAIN SELECT *
FROM tenk1 t1, onek t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Merge Join  (cost=0.56..233.49 rows=10 width=488)
   Merge Cond: (t1.unique2 = t2.unique2)
   ->  Index Scan using tenk1_unique2 on tenk1 t1  (cost=0.29..643.28 rows=100 width=244)
         Filter: (unique1 < 100)
   ->  Index Scan using onek_unique2 on onek t2  (cost=0.28..166.28 rows=1000 width=244)
```

合併聯結要求其輸入資料依聯結鍵排序。在這個範例中，每個輸入都是藉由使用索引掃描、依正確的順序走訪資料列來排序的；但也可以使用循序掃描加排序。（在排序大量資料列時，循序掃描加排序往往勝過索引掃描，因為索引掃描需要非循序的磁碟存取。）

查看替代計畫的一種方法，是使用[第 19.7.1 節](../../server-administration/runtime-config/runtime-config-query.md#RUNTIME-CONFIG-QUERY-ENABLE)所述的啟用／停用旗標，強制規劃器捨棄它認為最便宜的策略。（這是一個粗略但有用的工具。另請參閱[第 14.3 節](explicit-joins.md)。）例如，如果我們不確定合併聯結是否是上一個範例的最佳聯結類型，可以嘗試

```

SET enable_mergejoin = off;

EXPLAIN SELECT *
FROM tenk1 t1, onek t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Hash Join  (cost=226.23..344.08 rows=10 width=488)
   Hash Cond: (t2.unique2 = t1.unique2)
   ->  Seq Scan on onek t2  (cost=0.00..114.00 rows=1000 width=244)
   ->  Hash  (cost=224.98..224.98 rows=100 width=244)
         ->  Bitmap Heap Scan on tenk1 t1  (cost=5.06..224.98 rows=100 width=244)
               Recheck Cond: (unique1 < 100)
               ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
                     Index Cond: (unique1 < 100)
```

這顯示出規劃器認為，在這種情況下雜湊聯結的成本會比合併聯結高出將近 50%。當然，接下來的問題是它的判斷是否正確。我們可以使用 `EXPLAIN ANALYZE` 來調查這一點，如[下面](using-explain.md#USING-EXPLAIN-ANALYZE)所述。

使用啟用／停用旗標來停用計畫節點類型時，許多旗標只會抑制對應計畫節點的使用，而不會完全禁止規劃器使用該計畫節點類型。這是刻意的設計，讓規劃器仍然保有為給定查詢產生計畫的能力。當產生的計畫包含已停用的節點時，`EXPLAIN` 的輸出會指出這個事實。

```

SET enable_seqscan = off;
EXPLAIN SELECT * FROM unit;

                       QUERY PLAN
---------------------------------------------------------
 Seq Scan on unit  (cost=0.00..21.30 rows=1130 width=44)
   Disabled: true
```

由於 `unit` 資料表沒有任何索引，沒有其他方法可以讀取該資料表的資料，因此循序掃描是查詢規劃器唯一可用的選項。

<a id="id-1.5.13.4.7.31.1"></a>
有些查詢計畫涉及*子計畫*（subplan），它們源自原始查詢中的子 `SELECT`。這類查詢有時可以轉換為一般的聯結計畫，但當無法轉換時，我們會得到像這樣的計畫：

```

EXPLAIN VERBOSE SELECT unique1
FROM tenk1 t
WHERE t.ten < ALL (SELECT o.ten FROM onek o WHERE o.four = t.four);

                               QUERY PLAN
-------------------------------------------------------------------​------
 Seq Scan on public.tenk1 t  (cost=0.00..586095.00 rows=5000 width=4)
   Output: t.unique1
   Filter: (ALL (t.ten < (SubPlan 1).col1))
   SubPlan 1
     ->  Seq Scan on public.onek o  (cost=0.00..116.50 rows=250 width=4)
           Output: o.ten
           Filter: (o.four = t.four)
```

這個相當刻意的範例是為了說明幾個要點：外部計畫層級的值可以向下傳入子計畫（這裡傳入的是 `t.four`），而子查詢的結果可供外部計畫使用。`EXPLAIN` 會以類似 `(subplan_name).colN` 的表示法顯示這些結果值，它指的是子 `SELECT` 的第 *`N`* 個輸出欄位。

<a id="id-1.5.13.4.7.32.1"></a>
在上面的範例中，`ALL` 運算子會針對外部查詢的每一筆資料列再次執行子計畫（這也是估計成本很高的原因）。有些查詢可以使用*雜湊子計畫*（hashed subplan）來避免這種情況：

```

EXPLAIN SELECT *
FROM tenk1 t
WHERE t.unique1 NOT IN (SELECT o.unique1 FROM onek o);

                                         QUERY PLAN
-------------------------------------------------------------------​-------------------------
 Seq Scan on tenk1 t  (cost=61.77..531.77 rows=5000 width=244)
   Filter: (NOT (ANY (unique1 = (hashed SubPlan 1).col1)))
   SubPlan 1
     ->  Index Only Scan using onek_unique1 on onek o  (cost=0.28..59.27 rows=1000 width=4)
(4 rows)
```

在這裡，子計畫只會執行一次，其輸出會被載入記憶體中的雜湊表，然後由外部的 `ANY` 運算子進行探查。這要求子 `SELECT` 不參照外部查詢的任何變數，而且 `ANY` 的比較運算子必須適合進行雜湊。

<a id="id-1.5.13.4.7.33.1"></a>
如果子 `SELECT` 除了不參照外部查詢的任何變數之外，也不會回傳超過一筆資料列，那麼它可能會改以*初始計畫*（initplan）來實作：

```

EXPLAIN VERBOSE SELECT unique1
FROM tenk1 t1 WHERE t1.ten = (SELECT (random() * 10)::integer);

                             QUERY PLAN
------------------------------------------------------------​--------
 Seq Scan on public.tenk1 t1  (cost=0.02..470.02 rows=1000 width=4)
   Output: t1.unique1
   Filter: (t1.ten = (InitPlan 1).col1)
   InitPlan 1
     ->  Result  (cost=0.00..0.02 rows=1 width=4)
           Output: ((random() * '10'::double precision))::integer
```

初始計畫在外部計畫每次執行時只會執行一次，其結果會被保存下來，供外部計畫之後的資料列重複使用。因此在這個範例中，`random()` 只會被評估一次，而 `t1.ten` 的所有值都會與同一個隨機選出的整數比較。這與沒有使用子 `SELECT` 結構時會發生的情況大不相同。

<a id="USING-EXPLAIN-ANALYZE"></a>

### 14.1.2. `EXPLAIN ANALYZE` [#](#USING-EXPLAIN-ANALYZE)

使用 `EXPLAIN` 的 `ANALYZE` 選項，可以檢查規劃器估計的準確度。使用這個選項時，`EXPLAIN` 會實際執行查詢，然後顯示每個計畫節點中累計的真實資料列數與真實執行時間，以及一般 `EXPLAIN` 所顯示的相同估計值。例如，我們可能會得到像這樣的結果：

```

EXPLAIN ANALYZE SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t1.unique2 = t2.unique2;

                                                           QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------------------
 Nested Loop  (cost=4.65..118.50 rows=10 width=488) (actual time=0.017..0.051 rows=10.00 loops=1)
   Buffers: shared hit=36 read=6
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.38 rows=10 width=244) (actual time=0.009..0.017 rows=10.00 loops=1)
         Recheck Cond: (unique1 < 10)
         Heap Blocks: exact=10
         Buffers: shared hit=3 read=5 written=4
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0) (actual time=0.004..0.004 rows=10.00 loops=1)
               Index Cond: (unique1 < 10)
               Index Searches: 1
               Buffers: shared hit=2
   ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..7.90 rows=1 width=244) (actual time=0.003..0.003 rows=1.00 loops=10)
         Index Cond: (unique2 = t1.unique2)
         Index Searches: 10
         Buffers: shared hit=24 read=6
 Planning:
   Buffers: shared hit=15 dirtied=9
 Planning Time: 0.485 ms
 Execution Time: 0.073 ms
```

請注意，「actual time」（實際時間）的值是以實際時間的毫秒為單位，而 `cost` 估計值則以任意單位表示；因此它們不太可能相符。通常最需要注意的是，估計的資料列數是否合理地接近實際情況。在這個範例中，估計值全都完全正確，但這在實務上相當少見。

在某些查詢計畫中，子計畫節點有可能被執行不只一次。例如，在上面的巢狀迴圈計畫中，內部的索引掃描會針對每一筆外部資料列各執行一次。在這種情況下，`loops` 值會回報該節點的總執行次數，而所顯示的實際時間與資料列值則是每次執行的平均值。這樣做是為了讓這些數字能與成本估計的顯示方式相互比較。將它們乘以 `loops` 值，就能得到實際花在該節點上的總時間。在上面的範例中，我們總共花了 0.030 毫秒執行對 `tenk2` 的索引掃描。

在某些情況下，`EXPLAIN ANALYZE` 除了計畫節點的執行時間與資料列數之外，還會顯示額外的執行統計資訊。例如，Sort 與 Hash 節點會提供額外的資訊：

```

EXPLAIN ANALYZE SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2 ORDER BY t1.fivethous;

                                                                 QUERY PLAN
-------------------------------------------------------------------​-------------------------------------------------------------------​------
 Sort  (cost=713.05..713.30 rows=100 width=488) (actual time=2.995..3.002 rows=100.00 loops=1)
   Sort Key: t1.fivethous
   Sort Method: quicksort  Memory: 74kB
   Buffers: shared hit=440
   ->  Hash Join  (cost=226.23..709.73 rows=100 width=488) (actual time=0.515..2.920 rows=100.00 loops=1)
         Hash Cond: (t2.unique2 = t1.unique2)
         Buffers: shared hit=437
         ->  Seq Scan on tenk2 t2  (cost=0.00..445.00 rows=10000 width=244) (actual time=0.026..1.790 rows=10000.00 loops=1)
               Buffers: shared hit=345
         ->  Hash  (cost=224.98..224.98 rows=100 width=244) (actual time=0.476..0.477 rows=100.00 loops=1)
               Buckets: 1024  Batches: 1  Memory Usage: 35kB
               Buffers: shared hit=92
               ->  Bitmap Heap Scan on tenk1 t1  (cost=5.06..224.98 rows=100 width=244) (actual time=0.030..0.450 rows=100.00 loops=1)
                     Recheck Cond: (unique1 < 100)
                     Heap Blocks: exact=90
                     Buffers: shared hit=92
                     ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.013..0.013 rows=100.00 loops=1)
                           Index Cond: (unique1 < 100)
                           Index Searches: 1
                           Buffers: shared hit=2
 Planning:
   Buffers: shared hit=12
 Planning Time: 0.187 ms
 Execution Time: 3.036 ms
```

Sort 節點會顯示所使用的排序方法（特別是排序是在記憶體中還是在磁碟上進行），以及所需的記憶體或磁碟空間量。Hash 節點會顯示雜湊桶與批次的數量，以及雜湊表所使用的記憶體峰值。（如果批次數量超過一個，也會涉及磁碟空間的使用，但這不會顯示出來。）

Index Scan 節點（以及 Bitmap Index Scan 與 Index-Only Scan 節點）會顯示一行「Index Searches」（索引搜尋），回報在該節點*所有*執行次數／`loops` 中的索引搜尋總次數：

```

EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE thousand IN (1, 500, 700, 999);
                                                            QUERY PLAN
-------------------------------------------------------------------​---------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=9.45..73.44 rows=40 width=244) (actual time=0.012..0.028 rows=40.00 loops=1)
   Recheck Cond: (thousand = ANY ('{1,500,700,999}'::integer[]))
   Heap Blocks: exact=39
   Buffers: shared hit=47
   ->  Bitmap Index Scan on tenk1_thous_tenthous  (cost=0.00..9.44 rows=40 width=0) (actual time=0.009..0.009 rows=40.00 loops=1)
         Index Cond: (thousand = ANY ('{1,500,700,999}'::integer[]))
         Index Searches: 4
         Buffers: shared hit=8
 Planning Time: 0.029 ms
 Execution Time: 0.034 ms
```

在這裡，我們看到一個需要 4 次個別索引搜尋的 Bitmap Index Scan 節點。對於述詞的 `IN` 結構中的每一個 `integer` 值，這個掃描都必須從 `tenk1_thous_tenthous` 索引的根頁面搜尋一次索引。不過，索引搜尋的次數往往不會與查詢述詞有如此簡單的對應關係：

```

EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE thousand IN (1, 2, 3, 4);
                                                            QUERY PLAN
-------------------------------------------------------------------​---------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=9.45..73.44 rows=40 width=244) (actual time=0.009..0.019 rows=40.00 loops=1)
   Recheck Cond: (thousand = ANY ('{1,2,3,4}'::integer[]))
   Heap Blocks: exact=38
   Buffers: shared hit=40
   ->  Bitmap Index Scan on tenk1_thous_tenthous  (cost=0.00..9.44 rows=40 width=0) (actual time=0.005..0.005 rows=40.00 loops=1)
         Index Cond: (thousand = ANY ('{1,2,3,4}'::integer[]))
         Index Searches: 1
         Buffers: shared hit=2
 Planning Time: 0.029 ms
 Execution Time: 0.026 ms
```

我們這個 `IN` 查詢的變化形式只執行了 1 次索引搜尋。它走訪索引所花的時間（與原本的查詢相比）較少，因為它的 `IN` 結構所使用的值，對應到的索引 tuple 彼此相鄰地儲存在同一個 `tenk1_thous_tenthous` 索引葉頁面上。

對於套用*跳躍掃描*（skip scan）最佳化、以更有效率地走訪索引的 B-tree 索引掃描，「Index Searches」這一行也很有用：

```

EXPLAIN ANALYZE SELECT four, unique1 FROM tenk1 WHERE four BETWEEN 1 AND 3 AND unique1 = 42;
                                                              QUERY PLAN
-------------------------------------------------------------------​---------------------------------------------------------------
 Index Only Scan using tenk1_four_unique1_idx on tenk1  (cost=0.29..6.90 rows=1 width=8) (actual time=0.006..0.007 rows=1.00 loops=1)
   Index Cond: ((four >= 1) AND (four <= 3) AND (unique1 = 42))
   Heap Fetches: 0
   Index Searches: 3
   Buffers: shared hit=7
 Planning Time: 0.029 ms
 Execution Time: 0.012 ms
```

在這裡，我們看到一個使用 `tenk1_four_unique1_idx` 的 Index-Only Scan 節點，這是建立在 `tenk1` 資料表之 `four` 與 `unique1` 欄位上的多欄位索引。這個掃描執行了 3 次搜尋，每次各讀取一個索引葉頁面：「`four = 1 AND unique1 = 42`」、「`four = 2 AND unique1 = 42`」與「`four = 3 AND unique1 = 42`」。這個索引一般而言是跳躍掃描的良好對象，因為如[第 11.3 節](../indexes/indexes-multicolumn.md)所述，它的前導欄位（`four` 欄位）只包含 4 個相異值，而它的第二個／最後一個欄位（`unique1` 欄位）則包含許多相異值。

另一種額外資訊，是被過濾條件移除的資料列數：

```

EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE ten < 7;

                                               QUERY PLAN
-------------------------------------------------------------------​--------------------------------------
 Seq Scan on tenk1  (cost=0.00..470.00 rows=7000 width=244) (actual time=0.030..1.995 rows=7000.00 loops=1)
   Filter: (ten < 7)
   Rows Removed by Filter: 3000
   Buffers: shared hit=345
 Planning Time: 0.102 ms
 Execution Time: 2.145 ms
```

對於在聯結節點上套用的過濾條件，這些計數可能特別有價值。只有在至少有一筆被掃描的資料列（或在聯結節點的情況下，至少有一個可能的聯結配對）被過濾條件排除時，才會出現「Rows Removed」這一行。

與過濾條件類似的情況，也會發生在「有損」（lossy）的索引掃描中。例如，考慮下面這個搜尋包含特定點之多邊形的查詢：

```

EXPLAIN ANALYZE SELECT * FROM polygon_tbl WHERE f1 @> polygon '(0.5,2.0)';

                                              QUERY PLAN
-------------------------------------------------------------------​-----------------------------------
 Seq Scan on polygon_tbl  (cost=0.00..1.09 rows=1 width=85) (actual time=0.023..0.023 rows=0.00 loops=1)
   Filter: (f1 @> '((0.5,2))'::polygon)
   Rows Removed by Filter: 7
   Buffers: shared hit=1
 Planning Time: 0.039 ms
 Execution Time: 0.033 ms
```

規劃器認為（相當正確地）這個範例資料表太小，不值得使用索引掃描，因此我們得到一個簡單的循序掃描，其中所有的資料列都被過濾條件排除了。但如果我們強制使用索引掃描，會看到：

```

SET enable_seqscan TO off;

EXPLAIN ANALYZE SELECT * FROM polygon_tbl WHERE f1 @> polygon '(0.5,2.0)';

                                                        QUERY PLAN
-------------------------------------------------------------------​-------------------------------------------------------
 Index Scan using gpolygonind on polygon_tbl  (cost=0.13..8.15 rows=1 width=85) (actual time=0.074..0.074 rows=0.00 loops=1)
   Index Cond: (f1 @> '((0.5,2))'::polygon)
   Rows Removed by Index Recheck: 1
   Index Searches: 1
   Buffers: shared hit=1
 Planning Time: 0.039 ms
 Execution Time: 0.098 ms
```

在這裡我們可以看到，索引回傳了一筆候選資料列，接著它在重新檢查索引條件時被排除了。之所以會這樣，是因為對於多邊形包含測試，GiST 索引是「有損」的：它實際上會回傳多邊形與目標重疊的資料列，然後我們必須對這些資料列進行精確的包含測試。

`EXPLAIN` 有一個 `BUFFERS` 選項，可以提供在規劃與執行給定查詢期間所進行之 I/O 操作的額外細節。所顯示的緩衝區數字，是給定節點及其所有子節點命中、讀取、弄髒與寫入的緩衝區計數（不排除重複）。`ANALYZE` 選項會隱含地啟用 `BUFFERS` 選項。如果不希望這樣，可以明確地停用 `BUFFERS`：

```

EXPLAIN (ANALYZE, BUFFERS OFF) SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000;

                                                           QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=25.07..60.11 rows=10 width=244) (actual time=0.105..0.114 rows=10.00 loops=1)
   Recheck Cond: ((unique1 < 100) AND (unique2 > 9000))
   Heap Blocks: exact=10
   ->  BitmapAnd  (cost=25.07..25.07 rows=10 width=0) (actual time=0.100..0.101 rows=0.00 loops=1)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.027..0.027 rows=100.00 loops=1)
               Index Cond: (unique1 < 100)
               Index Searches: 1
         ->  Bitmap Index Scan on tenk1_unique2  (cost=0.00..19.78 rows=999 width=0) (actual time=0.070..0.070 rows=999.00 loops=1)
               Index Cond: (unique2 > 9000)
               Index Searches: 1
 Planning Time: 0.162 ms
 Execution Time: 0.143 ms
```

請記住，由於 `EXPLAIN ANALYZE` 會實際執行查詢，任何副作用都會照常發生，即使查詢可能輸出的任何結果都會被捨棄，改為印出 `EXPLAIN` 的資料。如果你想分析一個修改資料的查詢，又不想改變你的資料表，可以在事後回復該命令，例如：

```

BEGIN;

EXPLAIN ANALYZE UPDATE tenk1 SET hundred = hundred + 1 WHERE unique1 < 100;

                                                           QUERY PLAN
-------------------------------------------------------------------​-------------------------------------------------------------
 Update on tenk1  (cost=5.06..225.23 rows=0 width=0) (actual time=1.634..1.635 rows=0.00 loops=1)
   ->  Bitmap Heap Scan on tenk1  (cost=5.06..225.23 rows=100 width=10) (actual time=0.065..0.141 rows=100.00 loops=1)
         Recheck Cond: (unique1 < 100)
         Heap Blocks: exact=90
         Buffers: shared hit=4 read=2
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.031..0.031 rows=100.00 loops=1)
               Index Cond: (unique1 < 100)
               Index Searches: 1
               Buffers: shared read=2
 Planning Time: 0.151 ms
 Execution Time: 1.856 ms

ROLLBACK;
```

如這個範例所示，當查詢是 `INSERT`、`UPDATE`、`DELETE` 或 `MERGE` 命令時，套用資料表變更的實際工作，是由最上層的 Insert、Update、Delete 或 Merge 計畫節點完成的。這個節點底下的計畫節點負責找出舊的資料列和／或計算新的資料。因此在上面，我們看到的是與先前相同類型的點陣圖資料表掃描，而它的輸出會傳給一個儲存更新後資料列的 Update 節點。值得注意的是，雖然修改資料的節點可能會花費相當多的執行時間（在這裡，它占用了大部分的時間），但規劃器目前並不會在成本估計中加入任何東西來計入這項工作。這是因為對於每個正確的查詢計畫，要做的工作都是相同的，因此不會影響規劃決策。

當 `UPDATE`、`DELETE` 或 `MERGE` 命令影響到分割資料表或繼承階層時，輸出可能如下所示：

```

EXPLAIN UPDATE gtest_parent SET f1 = CURRENT_DATE WHERE f2 = 101;

                                       QUERY PLAN
-------------------------------------------------------------------​---------------------
 Update on gtest_parent  (cost=0.00..3.06 rows=0 width=0)
   Update on gtest_child gtest_parent_1
   Update on gtest_child2 gtest_parent_2
   Update on gtest_child3 gtest_parent_3
   ->  Append  (cost=0.00..3.06 rows=3 width=14)
         ->  Seq Scan on gtest_child gtest_parent_1  (cost=0.00..1.01 rows=1 width=14)
               Filter: (f2 = 101)
         ->  Seq Scan on gtest_child2 gtest_parent_2  (cost=0.00..1.01 rows=1 width=14)
               Filter: (f2 = 101)
         ->  Seq Scan on gtest_child3 gtest_parent_3  (cost=0.00..1.01 rows=1 width=14)
               Filter: (f2 = 101)
```

在這個範例中，Update 節點需要考慮三個子資料表，但不需要考慮原本提到的分割資料表（因為它從不儲存任何資料）。因此有三個輸入掃描子計畫，每個資料表各一個。為了清楚起見，Update 節點會加上註記，依照與對應子計畫相同的順序，顯示將被更新的具體目標資料表。

`EXPLAIN ANALYZE` 所顯示的 `Planning time`，是從剖析後的查詢產生查詢計畫並將其最佳化所花費的時間。它不包括剖析或改寫的時間。

`EXPLAIN ANALYZE` 所顯示的 `Execution time`，包括執行器的啟動與關閉時間，以及執行任何被觸發之觸發程序的時間，但不包括剖析、改寫或規劃的時間。執行 `BEFORE` 觸發程序（如果有的話）所花費的時間，會計入相關的 Insert、Update 或 Delete 節點的時間中；但執行 `AFTER` 觸發程序所花費的時間不會計入其中，因為 `AFTER` 觸發程序是在整個計畫完成之後才觸發的。每個觸發程序（無論是 `BEFORE` 還是 `AFTER`）所花費的總時間，也會另外顯示。請注意，延遲的限制條件觸發程序要到交易結束時才會執行，因此 `EXPLAIN ANALYZE` 完全不會將它們納入考量。

最上層節點所顯示的時間，不包括將查詢的輸出資料轉換為可顯示形式，或將其傳送給用戶端所需的任何時間。雖然 `EXPLAIN ANALYZE` 永遠不會將資料傳送給用戶端，但可以藉由指定 `SERIALIZE` 選項，要求它將查詢的輸出資料轉換為可顯示的形式，並量測所需的時間。該時間會另外顯示，而且也會包含在總 `Execution time` 中。

<a id="USING-EXPLAIN-CAVEATS"></a>

### 14.1.3. 注意事項 [#](#USING-EXPLAIN-CAVEATS)

`EXPLAIN ANALYZE` 量測到的執行時間，可能在兩個重要方面偏離同一個查詢的正常執行。第一，由於沒有任何輸出資料列傳送給用戶端，因此不包括網路傳輸成本。除非指定了 `SERIALIZE`，否則也不包括 I/O 轉換成本。第二，`EXPLAIN ANALYZE` 所增加的量測額外負擔可能相當可觀，特別是在 `gettimeofday()` 作業系統呼叫很慢的機器上。你可以使用 [pg_test_timing](../../reference/reference-server/pgtesttiming.md) 工具，量測你系統上計時的額外負擔。

不應將 `EXPLAIN` 的結果外推到與你實際測試的情況相差甚遠的情況；例如，不能假設在玩具大小之資料表上的結果也適用於大型資料表。規劃器的成本估計並非線性的，因此對於較大或較小的資料表，它可能會選擇不同的計畫。一個極端的例子是，在只占用一個磁碟頁面的資料表上，無論是否有可用的索引，你幾乎總是會得到循序掃描計畫。規劃器明白，無論如何處理該資料表都需要讀取一個磁碟頁面，因此花費額外的頁面讀取去查看索引並沒有價值。（我們在上面的 `polygon_tbl` 範例中看到了這種情況。）

在某些情況下，實際值與估計值不太相符，但其實並沒有任何問題。其中一種情況，是計畫節點的執行因 `LIMIT` 或類似的效果而提前停止。例如，在我們先前使用的 `LIMIT` 查詢中，

```

EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000 LIMIT 2;

                                                          QUERY PLAN
-------------------------------------------------------------------​------------------------------------------------------------
 Limit  (cost=0.29..14.33 rows=2 width=244) (actual time=0.051..0.071 rows=2.00 loops=1)
   Buffers: shared hit=16
   ->  Index Scan using tenk1_unique2 on tenk1  (cost=0.29..70.50 rows=10 width=244) (actual time=0.051..0.070 rows=2.00 loops=1)
         Index Cond: (unique2 > 9000)
         Filter: (unique1 < 100)
         Rows Removed by Filter: 287
         Index Searches: 1
         Buffers: shared hit=16
 Planning Time: 0.077 ms
 Execution Time: 0.086 ms
```

Index Scan 節點估計的成本與資料列數，是以假設它會執行到完成的方式顯示的。但實際上，Limit 節點在取得兩筆資料列之後就停止要求資料列了，因此實際的資料列數只有 2，而執行時間也比成本估計所暗示的少。這不是估計錯誤，只是估計值與真實值的顯示方式有所差異。

合併聯結也有一些可能讓不留意的人感到困惑的量測假象。如果合併聯結已經讀完其中一個輸入，而另一個輸入中的下一個鍵值大於前一個輸入的最後一個鍵值，它就會停止讀取該輸入；在這種情況下，不可能再有相符的項目，因此不需要掃描第一個輸入的其餘部分。這會導致沒有讀取某個子節點的全部內容，產生的結果就如同 `LIMIT` 所提到的那樣。此外，如果外部（第一個）子節點包含具有重複鍵值的資料列，內部（第二個）子節點就會倒回並重新掃描其資料列中與該鍵值相符的部分。`EXPLAIN ANALYZE` 會將這些重複輸出的相同內部資料列，當作真正額外的資料列來計算。當外部有許多重複值時，內部子計畫節點所回報的實際資料列數，可能會明顯大於內部關聯中實際存在的資料列數。

由於實作上的限制，BitmapAnd 與 BitmapOr 節點回報的實際資料列數一律為零。

通常，`EXPLAIN` 會顯示規劃器所建立的每一個計畫節點。不過，在某些情況下，執行器可以根據在規劃時尚無法取得的參數值，判斷某些節點由於不可能產生任何資料列而不需要執行。（目前這只會發生在正在掃描分割資料表之 Append 或 MergeAppend 節點的子節點上。）發生這種情況時，這些計畫節點會從 `EXPLAIN` 的輸出中省略，並改為出現 `Subplans Removed: N` 註記。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/using-explain.html)（原文版本：18.6；核對日期：2026-09-11）
