# 複寫識別模式

[返回ALTER TABLE](sql-altertable.md)

<a id="SQL-ALTERTABLE-REPLICA-IDENTITY-DEFAULT"></a>

## `DEFAULT` [#](#sql-altertable-replica-identity-default) <a href="#sql-altertable-replica-identity-default" id="sql-altertable-replica-identity-default"></a>

記錄主鍵欄位的舊值。這是非系統資料表的預設值。沒有主鍵時，行為與 `NOTHING` 相同。

<a id="SQL-ALTERTABLE-REPLICA-IDENTITY-USING-INDEX"></a>

## `USING INDEX index_name` [#](#sql-altertable-replica-identity-using-index) <a href="#sql-altertable-replica-identity-using-index" id="sql-altertable-replica-identity-using-index"></a>

記錄所指名索引所涵蓋之欄位的舊值；該索引必須是唯一的、非部分的、不可延遲的，並且只包含標記為 `NOT NULL` 的欄位。若此索引被移除，行為與 `NOTHING` 相同。

<a id="SQL-ALTERTABLE-REPLICA-IDENTITY-FULL"></a>

## `FULL` [#](#sql-altertable-replica-identity-full) <a href="#sql-altertable-replica-identity-full" id="sql-altertable-replica-identity-full"></a>

記錄資料列中所有欄位的舊值。

<a id="SQL-ALTERTABLE-REPLICA-IDENTITY-NOTHING"></a>

## `NOTHING` [#](#sql-altertable-replica-identity-nothing) <a href="#sql-altertable-replica-identity-nothing" id="sql-altertable-replica-identity-nothing"></a>

不記錄任何關於舊資料列的資訊。這是系統資料表的預設值。

[返回ALTER TABLE](sql-altertable.md)

---

本頁內容由父頁分出，沿用其原文版本與核對日期。

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertable.html)（原文版本：18.6；核對日期：2026-10-04）
