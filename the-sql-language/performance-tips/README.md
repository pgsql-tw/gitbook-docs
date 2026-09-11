## 第 14 章 效能提示

**目錄**

[14.1. 使用 `EXPLAIN`](using-explain.md)
:   [14.1.1. `EXPLAIN` 基礎](using-explain.md#USING-EXPLAIN-BASICS)

    [14.1.2. `EXPLAIN ANALYZE`](using-explain.md#USING-EXPLAIN-ANALYZE)

    [14.1.3. 注意事項](using-explain.md#USING-EXPLAIN-CAVEATS)

[14.2. 規劃器使用的統計資訊](planner-stats.md)
:   [14.2.1. 單一欄位統計資訊](planner-stats.md#PLANNER-STATS-SINGLE-COLUMN)

    [14.2.2. 擴充統計資訊](planner-stats.md#PLANNER-STATS-EXTENDED)

[14.3. 以明確的 `JOIN` 子句控制規劃器](explicit-joins.md)

[14.4. 填入資料庫](populate.md)
:   [14.4.1. 停用自動提交](populate.md#DISABLE-AUTOCOMMIT)

    [14.4.2. 使用 `COPY`](populate.md#POPULATE-COPY-FROM)

    [14.4.3. 移除索引](populate.md#POPULATE-RM-INDEXES)

    [14.4.4. 移除外鍵限制條件](populate.md#POPULATE-RM-FKEYS)

    [14.4.5. 增加 `maintenance_work_mem`](populate.md#POPULATE-WORK-MEM)

    [14.4.6. 增加 `max_wal_size`](populate.md#POPULATE-MAX-WAL-SIZE)

    [14.4.7. 停用 WAL 封存與串流複寫](populate.md#POPULATE-PITR)

    [14.4.8. 事後執行 `ANALYZE`](populate.md#POPULATE-ANALYZE)

    [14.4.9. 關於 pg_dump 的一些說明](populate.md#POPULATE-PG-DUMP)

[14.5. 非持久性設定](non-durability.md)

<a id="id-1.5.13.2"></a>

查詢效能可能受到許多因素影響。其中有些可以由使用者控制，有些則是系統底層設計的根本特性。本章提供一些提示，幫助你了解並調校 PostgreSQL 的效能。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/performance-tips.html)（原文版本：18.6；核對日期：2026-09-11）
