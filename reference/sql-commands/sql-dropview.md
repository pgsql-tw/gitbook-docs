<a id="SQL-DROPVIEW"></a><a id="id-1.9.3.145.1"></a>

## DROP VIEW

DROP VIEW — 移除檢視表

<a id="id-1.9.3.145.4"></a>

## 語法

```

DROP VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.145.5"></a>

## 說明

`DROP VIEW` 會移除現有的檢視表。要執行此命令，您必須是該檢視表的擁有者。

<a id="id-1.9.3.145.6"></a>

## 參數

`IF EXISTS`
:   檢視表不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除之檢視表的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於檢視表的物件（例如其他檢視表），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於檢視表則拒絕移除。這是預設行為。

<a id="id-1.9.3.145.7"></a>

## 範例

此命令會移除名為 `kinds` 的檢視表：

```

DROP VIEW kinds;
```

<a id="id-1.9.3.145.8"></a>

## 相容性

此命令符合 SQL 標準，但標準只允許每個命令移除一個檢視表；此外，`IF EXISTS` 選項是 PostgreSQL 擴充功能。

<a id="id-1.9.3.145.9"></a>

## 另請參閱

[ALTER VIEW](sql-alterview.md), [CREATE VIEW](sql-createview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropview.html)（原文版本：18.6；核對日期：2026-10-03）
