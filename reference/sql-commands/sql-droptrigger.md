<a id="SQL-DROPTRIGGER"></a><a id="id-1.9.3.141.1"></a>

## DROP TRIGGER

DROP TRIGGER — 移除觸發程序

<a id="id-1.9.3.141.4"></a>

## 語法

```

DROP TRIGGER [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.141.5"></a>

## 說明

`DROP TRIGGER` 會移除現有的觸發程序定義。要執行此命令，目前使用者必須是定義該觸發程序之資料表的擁有者。

<a id="id-1.9.3.141.6"></a>

## 參數

`IF EXISTS`
:   觸發程序不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除之觸發程序的名稱。

*`table_name`*
:   定義該觸發程序之資料表的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於觸發程序的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於觸發程序則拒絕移除。這是預設行為。

<a id="SQL-DROPTRIGGER-EXAMPLES"></a>

## 範例

刪除資料表 `films` 上的觸發程序 `if_dist_exists`：

```

DROP TRIGGER if_dist_exists ON films;
```

<a id="SQL-DROPTRIGGER-COMPATIBILITY"></a>

## 相容性

PostgreSQL 中的 `DROP TRIGGER` 陳述式與 SQL 標準不相容。在 SQL 標準中，觸發程序名稱並不是各資料表區域性的，因此該命令就只是 `DROP TRIGGER
name`。

<a id="id-1.9.3.141.9"></a>

## 另請參閱

[CREATE TRIGGER](sql-createtrigger.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptrigger.html)（原文版本：18.6；核對日期：2026-10-03）
