<a id="SQL-DROPMATERIALIZEDVIEW"></a><a id="id-1.9.3.118.1"></a>

## DROP MATERIALIZED VIEW

DROP MATERIALIZED VIEW — 移除具體化檢視表

<a id="id-1.9.3.118.4"></a>

## 語法

```

DROP MATERIALIZED VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.118.5"></a>

## 說明

`DROP MATERIALIZED VIEW` 會移除現有的具體化檢視表。要執行此命令，您必須是該具體化檢視表的擁有者。

<a id="id-1.9.3.118.6"></a>

## 參數

`IF EXISTS`
:   具體化檢視表不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除之具體化檢視表的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於該具體化檢視表的物件（例如其他具體化檢視表或一般檢視表），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該具體化檢視表則拒絕移除。這是預設行為。

<a id="id-1.9.3.118.7"></a>

## 範例

此命令會移除名為 `order_summary` 的具體化檢視表：

```

DROP MATERIALIZED VIEW order_summary;
```

<a id="id-1.9.3.118.8"></a>

## 相容性

`DROP MATERIALIZED VIEW` 是 PostgreSQL 擴充功能。

<a id="id-1.9.3.118.9"></a>

## 另請參閱

[CREATE MATERIALIZED VIEW](sql-creatematerializedview.md), [ALTER MATERIALIZED VIEW](sql-altermaterializedview.md), [REFRESH MATERIALIZED VIEW](sql-refreshmaterializedview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropmaterializedview.html)（原文版本：18.6；核對日期：2026-10-03）
