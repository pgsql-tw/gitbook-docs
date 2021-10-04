# 11.9. Index-Only Scans and Covering Indexes

PostgreSQL 中的所有索引都是次要索引 \(Secondary Index\)，這意味著每個索引都與資料表的主要資料區（在 PostgreSQL 術語中稱為資料表的 heap）分開儲存。也就是說，在一般的索引掃描中，每筆資料檢索都需要從索引和 heap 中取得資料。此外，雖然與給定可索引 WHERE 條件匹配的索引項目通常在索引中會放在一起，但它們連結的資料列可能在 heap 中的任何位置。因此，索引掃描的 heap 存取部分涉及對 heap 的大量隨機存取，這可能會很慢，尤其是在傳統的儲存媒體上。 （如[第 11.5 節](combining-multiple-indexes.md)中所述，bitmap 掃描嘗試透過按排序順序進行 heap 存取來降低這個成本，但這也只是到目前為止唯一所能做的事。）

為了解決此效能問題，PostgreSQL 支援了 Index-only 掃描，此種掃描表示只需要從索引中回覆查詢，而不涉及任何 heap 的存取。基本思想是直接從每個索引項目中回傳值，而不需要查詢關聯的 heap 內容。何時可以使用此方法有兩個基本限制：

1. 索引類型必須支持 Index-only 掃描。B-tree 索引的所有操作都能適用。 GiST 和 SP-GiST 索引支援了某些運算子類別的 Index-only 掃描，但並沒有支援其他的運算子類別。除了上述以外的索引目前不支援此功能。 基本要求是索引必須實體儲存或能夠回傳每個索引項目的原始資料值。作為反例，GIN 索引不能支援 Index-only 掃描，因為每個索引項目通常僅保留原始資料值的一部分。
2. 該查詢必須僅引用儲存在索引中的欄位。例如，在某三個欄位 \(x, y, z\) 的資料表宣告了 x 和 y 欄位上的索引，這些查詢就可以使用 Index-only 掃描：

   ```text
   SELECT x, y FROM tab WHERE x = 'key';
   SELECT x FROM tab WHERE x = 'key' AND y < 42;
   ```

   但是這些查詢就不能使用：

   ```text
   SELECT x, z FROM tab WHERE x = 'key';
   SELECT x FROM tab WHERE x = 'key' AND z < 42;
   ```

   （後續所述的表示式索引和部分索引使會此規則複雜化。）

如果滿足這兩個基本要求，那麼查詢所需的所有資料都可以從索引中獲得，因此實際執行面來說，Index-only 掃描是可能的。但是 PostgreSQL 中的任何資料表掃描還有一個額外的要求：它必須驗證對查詢的 MVCC 快照「可見」每筆檢索到的資料列，如[第 13 章](../concurrency-control/)所述。可見性資訊並不儲存在索引之中，而僅儲存在 heap 之中；因此乍看之下似乎每筆資料檢索都將需要存取 heap。如果資料表最近被修改了，則確實如此。但是，對於很少修改資料的情況，有一種解決此問題的方法。PostgreSQL 針對資料表中的每個頁面追踪該頁面中儲存的所有資料列版本是否足夠舊，以至於所有目前和將來的事務均是可見的。此資訊儲存在資料表的可見性檢視表中。 Index-only 掃描在找到候選索引項目之後，檢查相應 heap 頁面的可見性映射位元。如果已設置，則該筆資料是可見的，因此不需要進一步的工作即可回傳資料。如果未設定，則必須存取 heap 以確認它是否為可見，因此與標準的索引掃描相比，不見得能得到效能優勢。即使在成功的情況下，這種方法也將可見性檢視存取再切換成 heap 存取。但是由於可見性檢視表比它所記錄的 heap 小四個數量級，因此存取它所需的實體 I/O 顯然會少得多。在大多數情況下，可見性檢視表會一直保持快取在記憶體之中。

簡而言之，儘管在滿足兩個基本要求的情況下可以進行 Index-only 掃描，但是只有在資料表的 heap 頁面很大一部分都設定了其所有可見性映射位元的情況下，它才會是可用的。但是，由於普遍上大部分資料列不變的資料表是普遍的情況，所以在實務上中這種掃描會非常有用。

To make effective use of the index-only scan feature, you might choose to create a _covering index_, which is an index specifically designed to include the columns needed by a particular type of query that you run frequently. Since queries typically need to retrieve more columns than just the ones they search on, PostgreSQL allows you to create an index in which some columns are just “payload” and are not part of the search key. This is done by adding an `INCLUDE` clause listing the extra columns. For example, if you commonly run queries like

```text
SELECT y FROM tab WHERE x = 'key';
```

the traditional approach to speeding up such queries would be to create an index on `x` only. However, an index defined as

```text
CREATE INDEX tab_x_y ON tab(x) INCLUDE (y);
```

could handle these queries as index-only scans, because `y` can be obtained from the index without visiting the heap.

Because column `y` is not part of the index's search key, it does not have to be of a data type that the index can handle; it's merely stored in the index and is not interpreted by the index machinery. Also, if the index is a unique index, that is

```text
CREATE UNIQUE INDEX tab_x_y ON tab(x) INCLUDE (y);
```

the uniqueness condition applies to just column `x`, not to the combination of `x` and `y`. \(An `INCLUDE` clause can also be written in `UNIQUE` and `PRIMARY KEY` constraints, providing alternative syntax for setting up an index like this.\)

It's wise to be conservative about adding non-key payload columns to an index, especially wide columns. If an index tuple exceeds the maximum size allowed for the index type, data insertion will fail. In any case, non-key columns duplicate data from the index's table and bloat the size of the index, thus potentially slowing searches. And remember that there is little point in including payload columns in an index unless the table changes slowly enough that an index-only scan is likely to not need to access the heap. If the heap tuple must be visited anyway, it costs nothing more to get the column's value from there. Other restrictions are that expressions are not currently supported as included columns, and that only B-tree and GiST indexes currently support included columns.

Before PostgreSQL had the `INCLUDE` feature, people sometimes made covering indexes by writing the payload columns as ordinary index columns, that is writing

```text
CREATE INDEX tab_x_y ON tab(x, y);
```

even though they had no intention of ever using `y` as part of a `WHERE` clause. This works fine as long as the extra columns are trailing columns; making them be leading columns is unwise for the reasons explained in [Section 11.3](https://www.postgresql.org/docs/13/indexes-multicolumn.html). However, this method doesn't support the case where you want the index to enforce uniqueness on the key column\(s\).

_Suffix truncation_ always removes non-key columns from upper B-Tree levels. As payload columns, they are never used to guide index scans. The truncation process also removes one or more trailing key column\(s\) when the remaining prefix of key column\(s\) happens to be sufficient to describe tuples on the lowest B-Tree level. In practice, covering indexes without an `INCLUDE` clause often avoid storing columns that are effectively payload in the upper levels. However, explicitly defining payload columns as non-key columns _reliably_ keeps the tuples in upper levels small.

In principle, index-only scans can be used with expression indexes. For example, given an index on `f(x)` where `x` is a table column, it should be possible to execute

```text
SELECT f(x) FROM tab WHERE f(x) < 1;
```

as an index-only scan; and this is very attractive if `f()` is an expensive-to-compute function. However, PostgreSQL's planner is currently not very smart about such cases. It considers a query to be potentially executable by index-only scan only when all _columns_ needed by the query are available from the index. In this example, `x` is not needed except in the context `f(x)`, but the planner does not notice that and concludes that an index-only scan is not possible. If an index-only scan seems sufficiently worthwhile, this can be worked around by adding `x` as an included column, for example

```text
CREATE INDEX tab_f_x ON tab (f(x)) INCLUDE (x);
```

An additional caveat, if the goal is to avoid recalculating `f(x)`, is that the planner won't necessarily match uses of `f(x)` that aren't in indexable `WHERE` clauses to the index column. It will usually get this right in simple queries such as shown above, but not in queries that involve joins. These deficiencies may be remedied in future versions of PostgreSQL.

Partial indexes also have interesting interactions with index-only scans. Consider the partial index shown in [Example 11.3](https://www.postgresql.org/docs/13/indexes-partial.html#INDEXES-PARTIAL-EX3):

```text
CREATE UNIQUE INDEX tests_success_constraint ON tests (subject, target)
    WHERE success;
```

In principle, we could do an index-only scan on this index to satisfy a query like

```text
SELECT target FROM tests WHERE subject = 'some-subject' AND success;
```

But there's a problem: the `WHERE` clause refers to `success` which is not available as a result column of the index. Nonetheless, an index-only scan is possible because the plan does not need to recheck that part of the `WHERE` clause at run time: all entries found in the index necessarily have `success = true` so this need not be explicitly checked in the plan. PostgreSQL versions 9.6 and later will recognize such cases and allow index-only scans to be generated, but older versions will not.  


