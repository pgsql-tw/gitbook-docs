## 11.6. 唯一值索引 [#](#INDEXES-UNIQUE)

<a id="id-1.5.10.9.2"></a>

索引也可用來強制欄位值唯一，或強制多個欄位組合值唯一。

```

CREATE UNIQUE INDEX name ON table (column [, ...]) [ NULLS [ NOT ] DISTINCT ];
```

目前只有 B-tree 索引可宣告為唯一值索引。

將索引宣告為唯一值索引後，不允許多筆資料表資料列具有相同索引值。預設情況下，唯一欄位中的 null 值不視為相等，因此欄位可包含多個 null。`NULLS NOT DISTINCT` 選項會改變此行為，讓索引將 null 視為相等。多欄位唯一值索引只會拒絕多筆資料列中所有已建立索引欄位皆相等的情況。

在資料表上定義唯一限制條件或主鍵時，PostgreSQL 會自動建立唯一值索引。該索引涵蓋組成主鍵或唯一限制條件的欄位（必要時為多欄位索引），並藉此強制執行限制條件。

### 注意

無須手動在唯一欄位上建立索引；這只會複製自動建立的索引。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-unique.html)（原文版本：18.6；核對日期：2026-09-10）
