<a id="SQL-DROPCOLLATION"></a><a id="id-1.9.3.106.1"></a>

## DROP COLLATION

DROP COLLATION — 移除定序

<a id="id-1.9.3.106.4"></a>

## 語法

```

DROP COLLATION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="SQL-DROPCOLLATION-DESCRIPTION"></a>

## 說明

`DROP COLLATION` 會移除先前定義的定序。
要能移除定序，您必須擁有該定序。

<a id="id-1.9.3.106.6"></a>

## 參數

`IF EXISTS`
:   定序不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   定序的名稱。定序名稱可以用綱要限定。

`CASCADE`
:   自動移除相依於定序的物件，以及相依於這些物件的所有物件
    （請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於定序則拒絕移除。這是預設行為。

<a id="SQL-DROPCOLLATION-EXAMPLES"></a>

## 範例

移除名為 `german` 的定序：

```

DROP COLLATION german;
```

<a id="SQL-DROPCOLLATION-COMPAT"></a>

## 相容性

`DROP COLLATION` 命令符合 SQL 標準，但 `IF
EXISTS` 選項除外，它是 PostgreSQL 擴充功能。

<a id="id-1.9.3.106.9"></a>

## 另請參閱

[ALTER COLLATION](sql-altercollation.md), [CREATE COLLATION](sql-createcollation.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropcollation.html)（原文版本：18.6；核對日期：2026-10-03）
