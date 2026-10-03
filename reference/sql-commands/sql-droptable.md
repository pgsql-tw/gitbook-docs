<a id="SQL-DROPTABLE"></a><a id="id-1.9.3.134.1"></a>

## DROP TABLE

DROP TABLE — 移除資料表

<a id="id-1.9.3.134.4"></a>

## 語法

```

DROP TABLE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.134.5"></a>

## 說明

`DROP TABLE` 會從資料庫中移除資料表。只有資料表擁有者、綱要擁有者與超級使用者可以移除資料表。若要清空資料表中的資料列而不刪除資料表本身，請使用 [`DELETE`](sql-delete.md) 或 [`TRUNCATE`](sql-truncate.md)。

`DROP TABLE` 一律會移除目標資料表上存在的任何索引、規則、觸發程序與限制條件。不過，若要移除被檢視表或其他資料表的外鍵限制條件所參照的資料表，就必須指定 `CASCADE`。（`CASCADE` 會完整移除相依的檢視表，但在外鍵的情況下，它只會移除外鍵限制條件，而不會完整移除另一個資料表。）

<a id="id-1.9.3.134.6"></a>

## 參數

`IF EXISTS`
:   資料表不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除之資料表的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於資料表的物件（例如檢視表），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於資料表則拒絕移除。這是預設行為。

<a id="id-1.9.3.134.7"></a>

## 範例

若要刪除 `films` 與 `distributors` 這兩個資料表：

```

DROP TABLE films, distributors;
```

<a id="id-1.9.3.134.8"></a>

## 相容性

此命令符合 SQL 標準，但標準只允許每個命令移除一個資料表；此外，`IF EXISTS` 選項是 PostgreSQL 擴充功能。

<a id="id-1.9.3.134.9"></a>

## 另請參閱

[ALTER TABLE](sql-altertable.md), [CREATE TABLE](sql-createtable.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptable.html)（原文版本：18.6；核對日期：2026-10-03）
