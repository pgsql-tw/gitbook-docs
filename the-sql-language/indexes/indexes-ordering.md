<a id="INDEXES-ORDERING"></a>

## 11.4. 索引與 `ORDER BY` [#](#INDEXES-ORDERING)

<a id="id-1.5.10.7.2"></a>

除了單純找出查詢要回傳的資料列之外，索引也可能能夠以特定的排序順序提供這些資料列。這讓查詢的 `ORDER BY` 規格可以在沒有額外排序步驟的情況下得到滿足。在 PostgreSQL 目前支援的索引類型中，只有 B-tree 能產生排序過的輸出——其他索引類型會以未指定、取決於實作的順序回傳相符的資料列。

規劃器會考慮兩種滿足 `ORDER BY` 規格的方式：掃描一個符合該規格的可用索引，或是依實體順序掃描資料表並進行明確的排序。對於需要掃描資料表大部分內容的查詢，明確排序很可能比使用索引更快，因為它遵循循序存取模式，所需的磁碟 I/O 較少。當只需要擷取少數幾筆資料列時，索引會比較有用。一個重要的特例是 `ORDER BY` 搭配 `LIMIT` *`n`*：明確排序必須處理所有資料才能找出前 *`n`* 筆資料列，但如果有一個符合 `ORDER BY` 的索引，就能直接取得前 *`n`* 筆資料列，完全不必掃描其餘部分。

預設情況下，B-tree 索引以遞增順序儲存其項目，並將 null 值放在最後（在其他方面都相等的項目之間，資料表的 TID 會被當作決勝欄位）。這表示對欄位 `x` 上的索引進行正向掃描，會產生滿足 `ORDER BY x`（或者寫得更完整一點，`ORDER BY x ASC NULLS LAST`）的輸出。這個索引也可以反向掃描，產生滿足 `ORDER BY x DESC` 的輸出（或者寫得更完整一點，`ORDER BY x DESC NULLS FIRST`，因為 `NULLS FIRST` 是 `ORDER BY DESC` 的預設值）。

你可以在建立索引時加上 `ASC`、`DESC`、`NULLS FIRST` 和／或 `NULLS LAST` 選項，來調整 B-tree 索引的排序方式；例如：

```

CREATE INDEX test2_info_nulls_low ON test2 (info NULLS FIRST);
CREATE INDEX test3_desc_index ON test3 (id DESC NULLS LAST);
```

以遞增順序且 null 值在前的方式儲存的索引，視掃描方向而定，可以滿足 `ORDER BY x ASC NULLS FIRST` 或 `ORDER BY x DESC NULLS LAST`。

你可能會納悶，既然兩個選項再加上反向掃描的可能性，就能涵蓋 `ORDER BY` 的所有變化，為什麼還要提供全部四個選項。在單一欄位索引中，這些選項確實是多餘的，但在多欄位索引中，它們可能很有用。考慮一個建立在 `(x, y)` 上的雙欄位索引：如果正向掃描，它可以滿足 `ORDER BY x, y`；如果反向掃描，則可以滿足 `ORDER BY x DESC, y DESC`。但應用程式可能經常需要使用 `ORDER BY x ASC, y DESC`。一般的索引無法提供這種順序，但如果索引定義為 `(x ASC, y DESC)` 或 `(x DESC, y ASC)`，就可以做到。

顯然，使用非預設排序順序的索引是相當特殊的功能，但有時它們能讓某些查詢大幅加速。是否值得維護這樣的索引，取決於你有多常使用需要特殊排序順序的查詢。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-ordering.html)（原文版本：18.6；核對日期：2026-09-13）
