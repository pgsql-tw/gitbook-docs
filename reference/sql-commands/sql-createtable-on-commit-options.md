# CREATE TABLE：ON COMMIT 選項

[返回 CREATE TABLE 主頁](sql-createtable.md)。

<a id="SQL-CREATETABLE-PARMS-ON-COMMIT-PRESERVE-ROWS"></a>

## `PRESERVE ROWS` [#](#sql-createtable-parms-on-commit-preserve-rows) <a href="#sql-createtable-parms-on-commit-preserve-rows" id="sql-createtable-parms-on-commit-preserve-rows"></a>

在交易結束時不採取任何特殊動作。這是預設行為。
<a id="SQL-CREATETABLE-PARMS-ON-COMMIT-DELETE-ROWS"></a>

## `DELETE ROWS` [#](#sql-createtable-parms-on-commit-delete-rows) <a href="#sql-createtable-parms-on-commit-delete-rows" id="sql-createtable-parms-on-commit-delete-rows"></a>

暫存資料表中的所有資料列會在每個交易區塊結束時被刪除。基本上，每次提交時都會自動執行一次 [`TRUNCATE`](sql-truncate.md)。用在分割資料表上時，此動作不會串聯到其分割區。
<a id="SQL-CREATETABLE-PARMS-ON-COMMIT-DROP"></a>

## `DROP` [#](#sql-createtable-parms-on-commit-drop) <a href="#sql-createtable-parms-on-commit-drop" id="sql-createtable-parms-on-commit-drop"></a>

暫存資料表會在目前交易區塊結束時被移除。用在分割資料表上時，此動作會移除其分割區；用在具有繼承子資料表的資料表上時，則會移除相依的子資料表。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtable.html)（原文版本：18.6；核對日期：2026-10-04）
