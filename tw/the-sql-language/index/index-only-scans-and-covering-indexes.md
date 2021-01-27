# 11.9. Index-Only Scans and Covering Indexes

PostgreSQL 中的所有索引都是輔助性的，這意味著每個索引都與資料表的主要資料區（在 PostgreSQL 術語中稱為資料表的 heap）分開儲存。這代表著在一般的索引掃描中，每筆資料檢索都需要從索引和 heap 中取得資料。此外，雖然與給定可索引 WHERE 條件匹配的索引項目通常在索引中會放在一起，但它們連結的資料列可能在 heap 中的任何位置。因此，索引掃描的 heap 存取部分涉及對 heap 的大量隨機存取，這可能會很慢，尤其是在傳統的儲存媒體上。 （如[第 11.5 節](combining-multiple-indexes.md)中所述，bitmap 掃描嘗試透過按排序順序進行 heap 存取來降低這個成本，但這也只是到目前為止唯一所能做的事。）

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

If these two fundamental requirements are met, then all the data values required by the query are available from the index, so an index-only scan is physically possible. But there is an additional requirement for any table scan in PostgreSQL: it must verify that each retrieved row be “visible” to the query's MVCC snapshot, as discussed in [Chapter 13](https://www.postgresql.org/docs/13/mvcc.html). Visibility information is not stored in index entries, only in heap entries; so at first glance it would seem that every row retrieval would require a heap access anyway. And this is indeed the case, if the table row has been modified recently. However, for seldom-changing data there is a way around this problem. PostgreSQL tracks, for each page in a table's heap, whether all rows stored in that page are old enough to be visible to all current and future transactions. This information is stored in a bit in the table's _visibility map_. An index-only scan, after finding a candidate index entry, checks the visibility map bit for the corresponding heap page. If it's set, the row is known visible and so the data can be returned with no further work. If it's not set, the heap entry must be visited to find out whether it's visible, so no performance advantage is gained over a standard index scan. Even in the successful case, this approach trades visibility map accesses for heap accesses; but since the visibility map is four orders of magnitude smaller than the heap it describes, far less physical I/O is needed to access it. In most situations the visibility map remains cached in memory all the time.

In short, while an index-only scan is possible given the two fundamental requirements, it will be a win only if a significant fraction of the table's heap pages have their all-visible map bits set. But tables in which a large fraction of the rows are unchanging are common enough to make this type of scan very useful in practice.

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


