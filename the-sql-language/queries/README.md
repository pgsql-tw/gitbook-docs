## 第 7 章 查詢

**目錄**

[7.1. 概觀](queries-overview.md)

[7.2. 資料表運算式](queries-table-expressions.md)
:   [7.2.1. `FROM` 子句](queries-table-expressions.md#QUERIES-FROM)

    [7.2.2. `WHERE` 子句](queries-table-expressions.md#QUERIES-WHERE)

    [7.2.3. `GROUP BY` 與 `HAVING` 子句](queries-table-expressions.md#QUERIES-GROUP)

    [7.2.4. `GROUPING SETS`、`CUBE` 與 `ROLLUP`](queries-table-expressions.md#QUERIES-GROUPING-SETS)

    [7.2.5. Window 函式的處理](queries-table-expressions.md#QUERIES-WINDOW)

[7.3. 選取清單](queries-select-lists.md)
:   [7.3.1. 選取清單項目](queries-select-lists.md#QUERIES-SELECT-LIST-ITEMS)

    [7.3.2. 欄位標籤](queries-select-lists.md#QUERIES-COLUMN-LABELS)

    [7.3.3. `DISTINCT`](queries-select-lists.md#QUERIES-DISTINCT)

[7.4. 組合查詢（`UNION`、`INTERSECT`、`EXCEPT`）](queries-union.md)

[7.5. 排序資料列（`ORDER BY`）](queries-order.md)

[7.6. `LIMIT` 與 `OFFSET`](queries-limit.md)

[7.7. `VALUES` 清單](queries-values.md)

[7.8. `WITH` 查詢（通用資料表運算式）](queries-with.md)
:   [7.8.1. `WITH` 中的 `SELECT`](queries-with.md#QUERIES-WITH-SELECT)

    [7.8.2. 遞迴查詢](queries-with.md#QUERIES-WITH-RECURSIVE)

    [7.8.3. 通用資料表運算式的具體化](queries-with.md#QUERIES-WITH-CTE-MATERIALIZATION)

    [7.8.4. `WITH` 中的資料修改陳述式](queries-with.md#QUERIES-WITH-MODIFYING)

<a id="id-1.5.6.2"></a><a id="id-1.5.6.3"></a>

前面幾章說明了如何建立資料表、如何填入資料，以及如何操作這些資料。現在我們終於要討論如何從資料庫中取出資料。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/queries.html)（原文版本：18.6；核對日期：2026-09-11）
