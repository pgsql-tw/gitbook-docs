---
description: 版本：10
---

# 11.4. 索引與ORDER BY

這裡增加說明一個查詢的 ORDER BY 原則，毋須單獨的排序步驟即可獲得。目前 PostgreSQL 支援的索引類型中，只有 B-tree 可以產生有序輸出 - 其他索引類型以未指定的，依賴於實作上的順序回傳符合的資料列。

規劃程予將考慮透過掃描與語法符合的可用索引，或者透過按儲存循序掃描資料表並進行明確的排序來滿足 ORDER BY 語法。對於需要掃描資料表的大部分的查詢，明確的排序中一個重要的特殊情況是 ORDER BY 與 LIMIT n 結合使用：必須對所有資料完全排序，以取得前 n 筆資料，但如果存在與 ORDER BY 符合的索引，則可以直接檢索前 n 筆資料，而不掃描剩餘的資料列。

預設情況下，B-tree 索引按升羃儲存其項目，最後為空。這樣産生的索引是 x 欄位上索引的正向掃描，產生的輸出滿足 ORDER BY x（或者更詳細，ORDER BY x ASC NULLS LAST）。也可以向後掃描，產生滿足 ORDER BY x DESC 的輸出（或者更詳細地說，ORDER BY x DESC NULLS FIRST，因為 NULLS FIRST 是ORDER BY DESC 的預設值）。

您可以透過在建笠索引時包含選項 ASC，DESC，NULLS FIRST 或 NULLS LAST來調整 B-tree 索引的順序；例如：

```text
CREATE INDEX test2_info_nulls_low ON test2 (info NULLS FIRST);
CREATE INDEX test3_desc_index ON test3 (id DESC NULLS LAST);
```

首先以空值以升羃儲存的索引可以滿足 ORDER BY x ASC NULLS FIRST 或 ORDER BY x DESC NULLS LAST，具體取決於掃描的方向。

您可能想知道為什麼還要提供所有四個選項，當兩個選項和後向掃描的可能性將覆蓋 ORDER BY 的所有變形時。在單欄位索引中，選項確實是多餘的，但在多欄位索引中它們可能很有用。 考慮 \(x, y\) 上的兩欄位索引：如果我們向前掃描，這可以滿足 ORDER BY x,y，如果我們向後掃描，則可以滿足 ORDER BY x DESC, y DESC。但可能是應用程序經常需要使用 ORDER BY x ASC, y DESC。無法從普通索引獲取該排序，但如果索引定義為 \(x ASC, y DESC\) 或 \(x DESC, y ASC\)，則可能。

顯然，具有非隱含排序順序的索引是一個相當專業的功能，但有時它們可以為某些查詢產生巨大的加速。是否值得維護這樣的索引取決於您使用需要特殊排序順序的查詢的頻率。

