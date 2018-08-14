---
description: 版本：10
---

# 11.2. 索引型別

PostgreSQL 提供了幾種索引型別：B-tree，Hash，GiST，SP-GiST，GIN 和 BRIN。每種索引型別依適合類型的查詢使用不同的演算法。預設情況下， CREATE INDEX 指令建立適合最常見情況的 B-tree 索引。

B-tree 可以處理為某種排序的資料比較和範圍查詢。特別是，只要使用以下運算子之一進行比較時，PostgreSQL 查詢計劃程序就會考慮使用 B-tree 索引：

| `<` |
| :--- |
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
| :--- |
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
| :--- |
| `>>` |
| `~=` |
| `<@` |
| `<^` |
| `>^` |

（有關這些運算子的含義，請參閱[第 9.11 節](../functions-and-operators/9.11.-di-li-zi-xun-han-shi-ji-yun-suan-zi.md)。）標準版本中包含的 SP-GiST 運算子類記錄在[ Table 63.1 ](../../internals/sp-gist-indexes/built-in-operator-classes.md#table-63-1-built-in-sp-gist-operator-classes)中。有關更多訊息，請參閱[第 63 章](../../internals/sp-gist-indexes/)。

GIN 索引是「反向索引」，適用於包含多個值的組合的資料值，例如陣列。反向索引包含每個組合值的單獨項目，並且可以有效地處理測試特定組合值是否存在的查詢。

與 GiST 和 SP-GiST 一樣，GIN 可以支援許多不同的使用者定義的索引策略，並且可以使用 GIN 索引的特定運算子根據索引策略而有所不同。例如，PostgreSQL 的標準發行版包括一個陣列的 GIN 運算子類，它支援使用這些運算子的索引查詢：

| `<@` |
| :--- |
| `@>` |
| `=` |
| `&&` |

（有關這些運算子的含義，請參閱[第 9.18 節](../functions-and-operators/9.18.-zhen-lie-han-shi-ji-yun-suan-zi.md)。）標準版本中包含的 GIN 運算子類記錄在 [Table 64.1](../../internals/gin-indexes/64.2.-built-in-operator-classes.md#table-64-1-built-in-gin-operator-classes) 中。許多其他 GIN 運算子類在 contrib 套件中可用或作為單獨的專案支援。有關更多訊息，請參閱[第 64 章](../../internals/gin-indexes/)。

BRIN 索引（Block Range Indexes 的簡寫）儲存關於儲存在資料表的連續物理區塊範圍中值的摘要。與 GiST，SP-GiST 和 GIN 一樣，BRIN 可以支援許多不同的索引策略，並且可以使用 BRIN 索引的特定運算子根據索引策略而變化。對於具有線性排序順序的資料類型，索引數據對應於每個區塊範圍的欄位中值的最小值和最大值。這支援使用這些運算子的索引查詢：

| `<` |
| :--- |
| `<=` |
| `=` |
| `>=` |
| `>` |

[Table 65.1](../../internals/brin/built-in-operator-classes.md#table-65-1-built-in-brin-operator-classes) 中記錄了標準發行版中包含的 BRIN 運算子類。有關更多訊息，請參閱[第 65 章](../../internals/brin/)。

