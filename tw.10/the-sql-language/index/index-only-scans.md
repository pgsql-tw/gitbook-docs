---
description: 版本：10
---

# 11.11. 索引限定查詢（Index-only scan）

PostgreSQL 中的所有索引都是二級索引，這意味著每個索引都與資料的主資料區域（在 PostgreSQL 術語中稱為資料表的 heap）分開儲存。這意味著在普通索引掃描中，每個資料列檢索都需要從索引和堆中獲取資料。此外，雖然與給予可索引 WHERE 條件匹配的索引項目通常在索引中靠近在一起，但它們引用的資料列可能在 heap 中的任何位置。因此，索引掃描 heap 部分涉及大量隨機存取，這可能很慢，特別是在傳統的磁碟媒體上。（如第 11.5 節所述，bitmap 掃描嘗試透過按排序循序執行 heap 存取來減輕此成本，但這只是到目前為止而已。）

為了解決這個效能問題，PostgreSQL 支援索引限定掃描，它可以單獨回答索引中的查詢而毋須任何 heap 存取。基本思維是直接從每個索引項目中回傳值，而不是查詢相關的 heap 項目。何時可以使用此方法有兩個基本限制：

1. 索引類型必須支援僅索引掃描。B-tree 索引能做到，GiST 和 SP-GiST 索引支援某些運算子類的僅索引掃描，但不支持其他運算子類。其他索引類型則沒有支援。 基本要求是索引必須物理儲存或能夠重建每個索引項目的原始資料值。作為一個反例，GIN 索引不支援索引限定掃描，因為每個索引項目通常只包含原始資料值的一部分。
2. 查詢必須僅引用儲存在索引中的欄位。例如，給予一個也有欄位 z 的資料表欄位 x 和 y 的索引，這些查詢可以使用索引限定掃描：

   ```text
   SELECT x, y FROM tab WHERE x = 'key';
   SELECT x FROM tab WHERE x = 'key' AND y < 42;
   ```

   但這些查詢不能：

   ```text
   SELECT x, z FROM tab WHERE x = 'key';
   SELECT x FROM tab WHERE x = 'key' AND z < 42;
   ```

   （表示式索引和部分索引使此規則複雜化，如下所述。）

If these two fundamental requirements are met, then all the data values required by the query are available from the index, so an index-only scan is physically possible. But there is an additional requirement for any table scan in PostgreSQL: it must verify that each retrieved row be “visible” to the query's MVCC snapshot, as discussed in [Chapter 13](https://www.postgresql.org/docs/10/static/mvcc.html). Visibility information is not stored in index entries, only in heap entries; so at first glance it would seem that every row retrieval would require a heap access anyway. And this is indeed the case, if the table row has been modified recently. However, for seldom-changing data there is a way around this problem. PostgreSQL tracks, for each page in a table's heap, whether all rows stored in that page are old enough to be visible to all current and future transactions. This information is stored in a bit in the table's _visibility map_. An index-only scan, after finding a candidate index entry, checks the visibility map bit for the corresponding heap page. If it's set, the row is known visible and so the data can be returned with no further work. If it's not set, the heap entry must be visited to find out whether it's visible, so no performance advantage is gained over a standard index scan. Even in the successful case, this approach trades visibility map accesses for heap accesses; but since the visibility map is four orders of magnitude smaller than the heap it describes, far less physical I/O is needed to access it. In most situations the visibility map remains cached in memory all the time.

In short, while an index-only scan is possible given the two fundamental requirements, it will be a win only if a significant fraction of the table's heap pages have their all-visible map bits set. But tables in which a large fraction of the rows are unchanging are common enough to make this type of scan very useful in practice.

To make effective use of the index-only scan feature, you might choose to create indexes in which only the leading columns are meant to match `WHERE` clauses, while the trailing columns hold “payload” data to be returned by a query. For example, if you commonly run queries like

```text
SELECT y FROM tab WHERE x = 'key';
```

the traditional approach to speeding up such queries would be to create an index on `x` only. However, an index on `(x, y)` would offer the possibility of implementing this query as an index-only scan. As previously discussed, such an index would be larger and hence more expensive than an index on `x` alone, so this is attractive only if the table is known to be mostly static. Note it's important that the index be declared on `(x, y)` not `(y, x)`, as for most index types \(particularly B-trees\) searches that do not constrain the leading index columns are not very efficient.

In principle, index-only scans can be used with expression indexes. For example, given an index on `f(x)` where `x` is a table column, it should be possible to execute

```text
SELECT f(x) FROM tab WHERE f(x) < 1;
```

as an index-only scan; and this is very attractive if `f()` is an expensive-to-compute function. However, PostgreSQL's planner is currently not very smart about such cases. It considers a query to be potentially executable by index-only scan only when all _columns_ needed by the query are available from the index. In this example, `x` is not needed except in the context `f(x)`, but the planner does not notice that and concludes that an index-only scan is not possible. If an index-only scan seems sufficiently worthwhile, this can be worked around by declaring the index to be on `(f(x), x)`, where the second column is not expected to be used in practice but is just there to convince the planner that an index-only scan is possible. An additional caveat, if the goal is to avoid recalculating `f(x)`, is that the planner won't necessarily match uses of `f(x)` that aren't in indexable `WHERE` clauses to the index column. It will usually get this right in simple queries such as shown above, but not in queries that involve joins. These deficiencies may be remedied in future versions of PostgreSQL.

Partial indexes also have interesting interactions with index-only scans. Consider the partial index shown in [Example 11.3](https://www.postgresql.org/docs/10/static/indexes-partial.html#INDEXES-PARTIAL-EX3):

```text
CREATE UNIQUE INDEX tests_success_constraint ON tests (subject, target)
    WHERE success;
```

In principle, we could do an index-only scan on this index to satisfy a query like

```text
SELECT target FROM tests WHERE subject = 'some-subject' AND success;
```

But there's a problem: the `WHERE` clause refers to `success` which is not available as a result column of the index. Nonetheless, an index-only scan is possible because the plan does not need to recheck that part of the `WHERE` clause at run time: all entries found in the index necessarily have `success = true` so this need not be explicitly checked in the plan. PostgreSQL versions 9.6 and later will recognize such cases and allow index-only scans to be generated, but older versions will not.

