<a id="id-1.9.3.109.1"></a>

## DROP DOMAIN

DROP DOMAIN — 移除 domain

## 語法

```

DROP DOMAIN [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.109.5"></a>

## 說明

`DROP DOMAIN` 會移除 domain。只有 domain 的擁有者可以移除它。

<a id="id-1.9.3.109.6"></a>

## 參數

`IF EXISTS`
:   domain 不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有 domain 的名稱（可選擇以 schema 限定）。

`CASCADE`
:   自動移除相依於 domain 的物件（例如資料表欄位），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有物件相依於 domain 則拒絕移除。這是預設行為。

<a id="SQL-DROPDOMAIN-EXAMPLES"></a>

## 範例

若要移除 domain `box`：

```

DROP DOMAIN box;
```

<a id="SQL-DROPDOMAIN-COMPATIBILITY"></a>

## 相容性

此命令符合 SQL 標準，但 `IF EXISTS` 選項是 PostgreSQL 擴充功能。

<a id="SQL-DROPDOMAIN-SEE-ALSO"></a>

## 另請參閱

[CREATE DOMAIN](sql-createdomain.md), [ALTER DOMAIN](sql-alterdomain.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropdomain.html)（原文版本：18.6；核對日期：2026-09-10）
