<a id="INDEXES-TYPES"></a>

## 11.2. 索引類型 [#](#INDEXES-TYPES)

[11.2.1. B-Tree](indexes-types.md#INDEXES-TYPES-BTREE)

[11.2.2. Hash](indexes-types.md#INDEXES-TYPES-HASH)

[11.2.3. GiST](indexes-types.md#INDEXES-TYPE-GIST)

[11.2.4. SP-GiST](indexes-types.md#INDEXES-TYPE-SPGIST)

[11.2.5. GIN](indexes-types.md#INDEXES-TYPES-GIN)

[11.2.6. BRIN](indexes-types.md#INDEXES-TYPES-BRIN)

PostgreSQL 提供了數種索引類型：B-tree、Hash、GiST、SP-GiST、GIN、BRIN，以及擴充功能 [bloom](../../appendixes/contrib/bloom.md)。每種索引類型都使用不同的演算法，各自最適合不同類型的可索引子句。預設情況下，[`CREATE INDEX`](../../reference/sql-commands/sql-createindex.md) 命令會建立 B-tree 索引，它適用於最常見的情況。其他索引類型則是藉由寫出關鍵字 `USING`，後面接著索引類型名稱來選用。例如，要建立 Hash 索引：

```

CREATE INDEX name ON table USING HASH (column);
```

<a id="INDEXES-TYPES-BTREE"></a>

### 11.2.1. B-Tree [#](#INDEXES-TYPES-BTREE)

<a id="id-1.5.10.5.3.2"></a><a id="id-1.5.10.5.3.3"></a>

B-tree 可以處理可排序成某種順序之資料上的相等與範圍查詢。特別是，每當被索引的欄位涉及使用下列其中一個運算子的比較時，PostgreSQL 查詢規劃器就會考慮使用 B-tree 索引：

```

<   <=   =   >=   >
```

與這些運算子之組合等價的結構，例如 `BETWEEN` 與 `IN`，也可以用 B-tree 索引搜尋來實作。此外，索引欄位上的 `IS NULL` 或 `IS NOT NULL` 條件也可以搭配 B-tree 索引使用。

對於涉及模式比對運算子 `LIKE` 與 `~` 的查詢，最佳化器也可以使用 B-tree 索引，*前提是*模式是常數，而且錨定在字串的開頭——例如 `col LIKE 'foo%'` 或 `col ~ '^foo'`，但不包括 `col LIKE '%bar'`。不過，如果你的資料庫不使用 C 語系，就需要以特殊的運算子類別建立索引，才能支援模式比對查詢的索引；請參閱下面的[第 11.10 節](indexes-opclass.md)。B-tree 索引也可以用於 `ILIKE` 與 `~*`，但前提是模式以非字母字元開頭，也就是不受大小寫轉換影響的字元。

B-tree 索引也可以用來依排序後的順序取得資料。這不一定總是比簡單的掃描加排序更快，但通常很有幫助。

<a id="INDEXES-TYPES-HASH"></a>

### 11.2.2. Hash [#](#INDEXES-TYPES-HASH)

<a id="id-1.5.10.5.4.2"></a><a id="id-1.5.10.5.4.3"></a>

Hash 索引儲存的是由被索引欄位的值所推導出的 32 位元雜湊碼。因此，這類索引只能處理簡單的相等比較。每當被索引的欄位涉及使用等號運算子的比較時，查詢規劃器就會考慮使用 Hash 索引：

```

=
```

<a id="INDEXES-TYPE-GIST"></a>

### 11.2.3. GiST [#](#INDEXES-TYPE-GIST)

<a id="id-1.5.10.5.5.2"></a><a id="id-1.5.10.5.5.3"></a>

GiST 索引並不是單一種類的索引，而是一套基礎架構，可以在其中實作許多不同的索引策略。相應地，GiST 索引可以搭配使用的具體運算子，會依索引策略（*運算子類別*）而有所不同。舉例來說，PostgreSQL 的標準發行版本中包含了用於數種二維幾何資料型別的 GiST 運算子類別，支援使用下列運算子的索引查詢：

```

<<   &<   &>   >>   <<|   &<|   |&>   |>>   @>   <@   ~=   &&
```

（這些運算子的意義請參閱[第 9.11 節](../functions/functions-geometry.md)。）標準發行版本中所包含的 GiST 運算子類別，記載於[表 65.1](../../internals/indextypes/gist.md#GIST-BUILTIN-OPCLASSES-TABLE)。還有許多其他的 GiST 運算子類別，可以在 `contrib` 集合中或以獨立專案的形式取得。更多資訊請參閱[第 65.2 節](../../internals/indextypes/gist.md)。

GiST 索引也能夠最佳化「最近鄰」（nearest-neighbor）搜尋，例如

```

SELECT * FROM places ORDER BY location <-> point '(101,456)' LIMIT 10;
```

它會找出距離指定目標點最近的十個地點。能否做到這一點，同樣取決於所使用的運算子類別。在[表 65.1](../../internals/indextypes/gist.md#GIST-BUILTIN-OPCLASSES-TABLE) 中，可以用於這種方式的運算子列在「Ordering Operators」（排序運算子）欄位中。

<a id="INDEXES-TYPE-SPGIST"></a>

### 11.2.4. SP-GiST [#](#INDEXES-TYPE-SPGIST)

<a id="id-1.5.10.5.6.2"></a><a id="id-1.5.10.5.6.3"></a>

SP-GiST 索引就像 GiST 索引一樣，提供了一套支援各種搜尋的基礎架構。SP-GiST 允許實作各種不同的非平衡、以磁碟為基礎的資料結構，例如四元樹（quadtree）、k-d 樹與基數樹（radix tree，trie）。舉例來說，PostgreSQL 的標準發行版本中包含了用於二維點的 SP-GiST 運算子類別，支援使用下列運算子的索引查詢：

```

<<   >>   ~=   <@   <<|   |>>
```

（這些運算子的意義請參閱[第 9.11 節](../functions/functions-geometry.md)。）標準發行版本中所包含的 SP-GiST 運算子類別，記載於[表 65.2](../../internals/indextypes/spgist.md#SPGIST-BUILTIN-OPCLASSES-TABLE)。更多資訊請參閱[第 65.3 節](../../internals/indextypes/spgist.md)。

與 GiST 一樣，SP-GiST 也支援「最近鄰」搜尋。對於支援距離排序的 SP-GiST 運算子類別，對應的運算子列在[表 65.2](../../internals/indextypes/spgist.md#SPGIST-BUILTIN-OPCLASSES-TABLE) 的「Ordering Operators」欄位中。

<a id="INDEXES-TYPES-GIN"></a>

### 11.2.5. GIN [#](#INDEXES-TYPES-GIN)

<a id="id-1.5.10.5.7.2"></a><a id="id-1.5.10.5.7.3"></a>

GIN 索引是「反向索引」（inverted index），適用於包含多個組成值的資料值，例如陣列。反向索引會為每個組成值各保存一個項目，可以有效率地處理檢驗特定組成值是否存在的查詢。

與 GiST 及 SP-GiST 一樣，GIN 可以支援許多不同的使用者自訂索引策略，而 GIN 索引可以搭配使用的具體運算子，會依索引策略而有所不同。舉例來說，PostgreSQL 的標準發行版本中包含了用於陣列的 GIN 運算子類別，支援使用下列運算子的索引查詢：

```

<@   @>   =   &&
```

（這些運算子的意義請參閱[第 9.19 節](../functions/functions-array.md)。）標準發行版本中所包含的 GIN 運算子類別，記載於[表 65.3](../../internals/indextypes/gin.md#GIN-BUILTIN-OPCLASSES-TABLE)。還有許多其他的 GIN 運算子類別，可以在 `contrib` 集合中或以獨立專案的形式取得。更多資訊請參閱[第 65.4 節](../../internals/indextypes/gin.md)。

<a id="INDEXES-TYPES-BRIN"></a>

### 11.2.6. BRIN [#](#INDEXES-TYPES-BRIN)

<a id="id-1.5.10.5.8.2"></a><a id="id-1.5.10.5.8.3"></a>

BRIN 索引（Block Range INdexes，區塊範圍索引的簡稱）儲存的是資料表中連續實體區塊範圍內所儲存之值的摘要。因此，對於其值與資料表資料列實體順序高度相關的欄位，它們最為有效。與 GiST、SP-GiST 及 GIN 一樣，BRIN 可以支援許多不同的索引策略，而 BRIN 索引可以搭配使用的具體運算子，會依索引策略而有所不同。對於具有線性排序順序的資料型別，被索引的資料對應於每個區塊範圍內該欄位值的最小值與最大值。這支援使用下列運算子的索引查詢：

```

<   <=   =   >=   >
```

標準發行版本中所包含的 BRIN 運算子類別，記載於[表 65.4](../../internals/indextypes/brin.md#BRIN-BUILTIN-OPCLASSES-TABLE)。更多資訊請參閱[第 65.5 節](../../internals/indextypes/brin.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-types.html)（原文版本：18.6；核對日期：2026-09-11）
