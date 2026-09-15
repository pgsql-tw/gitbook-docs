## 第 11 章 索引

**目錄**

[11.1. 簡介](indexes-intro.md)

[11.2. 索引類型](indexes-types.md)
:   [11.2.1. B-Tree](indexes-types.md#INDEXES-TYPES-BTREE)

    [11.2.2. Hash](indexes-types.md#INDEXES-TYPES-HASH)

    [11.2.3. GiST](indexes-types.md#INDEXES-TYPE-GIST)

    [11.2.4. SP-GiST](indexes-types.md#INDEXES-TYPE-SPGIST)

    [11.2.5. GIN](indexes-types.md#INDEXES-TYPES-GIN)

    [11.2.6. BRIN](indexes-types.md#INDEXES-TYPES-BRIN)

[11.3. 多欄位索引](indexes-multicolumn.md)

[11.4. 索引與 `ORDER BY`](indexes-ordering.md)

[11.5. 組合多個索引](indexes-bitmap-scans.md)

[11.6. 唯一值索引](indexes-unique.md)

[11.7. 運算式索引](indexes-expressional.md)

[11.8. 部分索引](indexes-partial.md)

[11.9. 僅索引掃描與涵蓋索引](indexes-index-only-scans.md)

[11.10. 運算子類別與運算子族系](indexes-opclass.md)

[11.11. 索引與定序](indexes-collations.md)

[11.12. 檢查索引的使用情形](indexes-examine.md)

<a id="id-1.5.10.2"></a>

索引是提升資料庫效能的常見方法。索引讓資料庫伺服器能夠比沒有索引時更快地找出並取得特定的資料列。但索引也會為整個資料庫系統增加額外負擔，因此應該審慎地使用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes.html)（原文版本：18.6；核對日期：2026-09-13）
