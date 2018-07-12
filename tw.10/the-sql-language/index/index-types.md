---
description: 版本：10
---

# 11.2. 索引型別

PostgreSQL 提供了幾種索引型別：B-tree，Hash，GiST，SP-GiST，GIN 和 BRIN。每種索引型別依適合類型的查詢使用不同的演算法。預設情況下， CREATE INDEX 指令建立適合最常見情況的 B-tree 索引。

B-tree 可以處理為某種排序的資料比較和範圍查詢。特別是，只要使用以下運算子之一進行比較時，PostgreSQL 查詢計劃程序就會考慮使用 B-tree 索引：

| `<` |
| --- | --- | --- | --- | --- |
| `<=` |
| `=` |
| `>=` |
| `>` |

也可以使用 B-tree 索引搜尋來實作等同於這些運算子的組合的語法，例如 BETWEEN 和 IN。此外，索引欄位上的 IS NULL 或 IS NOT NULL 條件也可以與 B-tree 索引一起使用。

對於涉及樣式比對運算子 LIKE 和 ~ 的查詢，最佳化程序也可以使用 B-tree 索引，如果是樣式是常數並且放在字串的開頭的話 - 例如，col LIKE 'foo%' 或 col~' ^ foo'，但 col LIKE '%bar' 就不是。但是，如果您的資料庫不使用 C 語言環境，則需要使用特殊的運算子類建立索引，以支援樣式比對查詢的索引；詳見下面的第 11.9 節。也可以對 ILIKE 和 ~\* 使用 B-tree 索引，但前提是樣式以非字母字元開頭，即不受大/小寫轉換影響的字元。

B-tree 索引也可用於按排序順序檢索資料。這並不一定會比簡單的掃描及排序更快，但通常會很有幫助。

Hash 索引只能處理簡單的相等比較。只要使用 = 運算子在比較中涉及索引欄位，查詢計劃程序就會考慮使用 Hash 索引。以下指令用於建立 Hash 索引：

```text
CREATE INDEX name ON table USING HASH (column);
```

GiST 索引不是一種索引，而是一種可以實作許多不同索引策略的基礎結構。因此，可以使用 GiST 索引的特定運算子根據索引策略（運算子類）而變化。例如，PostgreSQL 的標準版本包括幾個二維幾何資料型別的 GiST 運算子類，它們支援使用這些運算子的索引查詢：

| `<<` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `&<` |
| `&>` |
| `>>` |
| `<<|` |
| `&<|` |
| `|&>` |
| `|>>` |
| `@>` |
| `<@` |
| `~=` |
| `&&` |

（有關這些運算子的含義，請參閱[第 9.11 節](../functions-and-operators/9.11.-di-li-zi-xun-han-shi-ji-yun-suan-zi.md)。）標準版本中包含的 GiST 運算子類記錄在 [Table 62.1](../../internals/gist-indexes/built-in-operator-classes.md#table-62-1-built-in-gist-operator-classes) 中。許多其他 GiST 運算子類在 contrib 套件中可用或作為單獨的專案支援。有關更多訊息，請參閱[第 62 章](../../internals/gist-indexes/)。

GiST 索引還能夠最佳化「最近鄰居」搜尋，例如

```text
SELECT * FROM places ORDER BY location <-> point '(101,456)' LIMIT 10;
```

找到最接近給予目標點的 10 個位置。執行此操作的能力再次取決於所使用的特定運算子類。在 Table 62.1 中，可以以這種方式使用的運算子列在「Ordering Operators」欄位中。

SP-GiST 索引（如 GiST 索引）提供支援各種搜尋的基礎結構。SP-GiST 允許實作各種不同的非平衡的磁碟資料結構，例如 quadtree，k-d tree 和 radix tree。 例如，PostgreSQL 的標準版本包括用於二維空間的 SP-GiST 運算子類，它支援使用這些運算子的索引查詢：

| `<<` |
| --- | --- | --- | --- | --- | --- |
| `>>` |
| `~=` |
| `<@` |
| `<^` |
| `>^` |

\(See [Section 9.11](https://www.postgresql.org/docs/10/static/functions-geometry.html) for the meaning of these operators.\) The SP-GiST operator classes included in the standard distribution are documented in [Table 63.1](https://www.postgresql.org/docs/10/static/spgist-builtin-opclasses.html#SPGIST-BUILTIN-OPCLASSES-TABLE). For more information see [Chapter 63](https://www.postgresql.org/docs/10/static/spgist.html).

GIN indexes are “inverted indexes” which are appropriate for data values that contain multiple component values, such as arrays. An inverted index contains a separate entry for each component value, and can efficiently handle queries that test for the presence of specific component values.

Like GiST and SP-GiST, GIN can support many different user-defined indexing strategies, and the particular operators with which a GIN index can be used vary depending on the indexing strategy. As an example, the standard distribution of PostgreSQL includes a GIN operator class for arrays, which supports indexed queries using these operators:

| `<@` |
| --- | --- | --- | --- |
| `@>` |
| `=` |
| `&&` |

（有關這些運算子的含義，請參閱[第 9.18 節](../functions-and-operators/9.18.-zhen-lie-han-shi-ji-yun-suan-zi.md)。）標準版本中包含的 GIN 運算子類記錄在 [Table 64.1](../../internals/64.-gin-suo-yin/64.2.-built-in-operator-classes.md#table-64-1-built-in-gin-operator-classes) 中。許多其他 GIN 運算子類在 contrib 套件中可用或作為單獨的專案支援。有關更多訊息，請參閱[第 64 章](../../internals/64.-gin-suo-yin/)。

BRIN indexes \(a shorthand for Block Range INdexes\) store summaries about the values stored in consecutive physical block ranges of a table. Like GiST, SP-GiST and GIN, BRIN can support many different indexing strategies, and the particular operators with which a BRIN index can be used vary depending on the indexing strategy. For data types that have a linear sort order, the indexed data corresponds to the minimum and maximum values of the values in the column for each block range. This supports indexed queries using these operators:

| `<` |
| --- | --- | --- | --- | --- |
| `<=` |
| `=` |
| `>=` |
| `>` |

The BRIN operator classes included in the standard distribution are documented in [Table 65.1](https://www.postgresql.org/docs/10/static/brin-builtin-opclasses.html#BRIN-BUILTIN-OPCLASSES-TABLE). For more information see [Chapter 65](https://www.postgresql.org/docs/10/static/brin.html).

