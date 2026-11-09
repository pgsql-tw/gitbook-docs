# 29.4.3. UPDATE 轉換

<a id="LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS"></a>

## 29.4.3. UPDATE 轉換 [#](#logical-replication-row-filter-transformations) <a href="#logical-replication-row-filter-transformations" id="logical-replication-row-filter-transformations"></a>

每當處理一筆 `UPDATE` 時，會分別以更新前與更新後的資料列（即舊資料與新資料）來求值資料列篩選運算式。若兩者求值結果皆為 `true`，則複寫該筆 `UPDATE` 異動。若兩者求值結果皆為 `false`，則不複寫該筆異動。若只有其中一筆（舊資料或新資料）符合資料列篩選運算式，則該筆 `UPDATE` 會被轉換為 `INSERT` 或 `DELETE`，以避免資料不一致。訂閱者上的資料列應反映發布者上資料列篩選運算式所定義的結果。

若舊資料列滿足篩選運算式（因此已送至訂閱者），但新資料列不滿足，則從資料一致性的角度來看，應將該舊資料列從訂閱者移除。因此該 `UPDATE` 會被轉換為 `DELETE`。

若舊資料列不滿足篩選運算式（因此未送至訂閱者），但新資料列滿足，則從資料一致性的角度來看，應將該新資料列加入訂閱者。因此該 `UPDATE` 會被轉換為 `INSERT`。

[表 29.1](#logical-replication-row-filter-transformations-summary) 彙整了套用的轉換規則。

<a id="LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS-SUMMARY"></a>

### 表 29.1. `UPDATE` 轉換彙整 [#](#logical-replication-row-filter-transformations-summary) <a href="#logical-replication-row-filter-transformations-summary" id="logical-replication-row-filter-transformations-summary"></a>

<table border="1" class="table" summary="UPDATE 轉換摘要"><colgroup><col/><col/><col/></colgroup><thead><tr><th>舊資料列</th><th>新資料列</th><th>轉換方式</th></tr></thead><tbody><tr><td>不符合</td><td>不符合</td><td>不複寫</td></tr><tr><td>不符合</td><td>符合</td><td><code class="literal">INSERT</code></td></tr><tr><td>符合</td><td>不符合</td><td><code class="literal">DELETE</code></td></tr><tr><td>符合</td><td>符合</td><td><code class="literal">UPDATE</code></td></tr></tbody></table>

<br>

[返回 29.4. 資料列篩選器](../logical-replication-row-filter.md#logical-replication-row-filter)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-row-filter.html)（原文版本：18.6；核對日期：2026-09-25）
