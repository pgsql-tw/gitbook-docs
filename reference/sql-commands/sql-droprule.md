<a id="id-1.9.3.128.1"></a>

## DROP RULE

DROP RULE — 移除重寫規則

## 語法

```

DROP RULE [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.128.5"></a>

## 說明

`DROP RULE` 會移除重寫規則。

<a id="id-1.9.3.128.6"></a>

## 參數

`IF EXISTS`
:   規則不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除的規則名稱。

*`table_name`*
:   套用該規則的資料表或檢視表名稱（可選擇以 schema 限定）。

`CASCADE`
:   自動移除相依於該規則的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有物件相依於規則則拒絕移除。這是預設行為。

<a id="id-1.9.3.128.7"></a>

## 範例

若要移除重寫規則 `newrule`：

```

DROP RULE newrule ON mytable;
```

<a id="id-1.9.3.128.8"></a>

## 相容性

`DROP RULE` 是 PostgreSQL 語言擴充功能，如同整個查詢重寫系統。

<a id="id-1.9.3.128.9"></a>

## 另請參閱

[CREATE RULE](sql-createrule.md), [ALTER RULE](sql-alterrule.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droprule.html)（原文版本：18.6；核對日期：2026-09-10）
