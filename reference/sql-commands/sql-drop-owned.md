<a id="SQL-DROP-OWNED"></a><a id="id-1.9.3.122.1"></a>

## DROP OWNED

DROP OWNED — 移除資料庫角色所擁有的資料庫物件

<a id="id-1.9.3.122.4"></a>

## 語法

```

DROP OWNED BY { name | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.122.5"></a>

## 說明

`DROP OWNED` 會移除目前資料庫中由任一指定角色所擁有的所有物件。在目前資料庫中的物件上或共用物件（資料庫、資料表空間、組態參數）上授予給這些角色的任何權限也會被撤銷。

<a id="id-1.9.3.122.6"></a>

## 參數

*`name`*
:   某個角色的名稱；該角色的物件將被移除，其權限也將被撤銷。

`CASCADE`
:   自動移除相依於受影響物件的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何其他資料庫物件相依於任一受影響物件，則拒絕移除該角色所擁有的物件。這是預設行為。

<a id="id-1.9.3.122.7"></a>

## 注意事項

`DROP OWNED` 常用於為移除一個或多個角色做準備。由於 `DROP OWNED` 只影響目前資料庫中的物件，因此通常必須在每個包含待移除角色所擁有物件的資料庫中執行此命令。

使用 `CASCADE` 選項可能使命令遞迴到其他使用者所擁有的物件。

[`REASSIGN OWNED`](sql-reassign-owned.md) 命令是另一種選擇，它會重新指派一個或多個角色所擁有之所有資料庫物件的擁有權。不過，`REASSIGN OWNED` 不會處理其他物件的權限。

這些角色所擁有的資料庫與資料表空間不會被移除。

更多討論請參閱[第 21.4 節](../../server-administration/user-manag/role-removal.md)。

<a id="id-1.9.3.122.8"></a>

## 相容性

`DROP OWNED` 命令是 PostgreSQL 擴充功能。

<a id="id-1.9.3.122.9"></a>

## 另請參閱

[REASSIGN OWNED](sql-reassign-owned.md), [DROP ROLE](sql-droprole.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-drop-owned.html)（原文版本：18.6；核對日期：2026-10-03）
