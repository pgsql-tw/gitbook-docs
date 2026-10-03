<a id="SQL-DROPSCHEMA"></a><a id="id-1.9.3.129.1"></a>

## DROP SCHEMA

DROP SCHEMA — 移除綱要

<a id="id-1.9.3.129.4"></a>

## 語法

```

DROP SCHEMA [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.129.5"></a>

## 說明

`DROP SCHEMA` 會從資料庫中移除綱要。

綱要只能由其擁有者或超級使用者移除。請注意，即使擁有者並不擁有綱要內的某些物件，擁有者仍可以移除該綱要（並因此移除其中包含的所有物件）。

<a id="id-1.9.3.129.6"></a>

## 參數

`IF EXISTS`
:   綱要不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   綱要的名稱。

`CASCADE`
:   自動移除綱要中包含的物件（資料表、函式等），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若綱要包含任何物件則拒絕移除。這是預設行為。

<a id="id-1.9.3.129.7"></a>

## 注意事項

使用 `CASCADE` 選項可能使命令除了移除所指名的綱要之外，也移除其他綱要中的物件。

<a id="id-1.9.3.129.8"></a>

## 範例

若要從資料庫中移除綱要 `mystuff` 及其包含的所有內容：

```

DROP SCHEMA mystuff CASCADE;
```

<a id="id-1.9.3.129.9"></a>

## 相容性

`DROP SCHEMA` 完全符合 SQL 標準，但標準只允許每個命令移除一個綱要，此外 `IF EXISTS` 選項是 PostgreSQL 擴充功能。

<a id="id-1.9.3.129.10"></a>

## 另請參閱

[ALTER SCHEMA](sql-alterschema.md), [CREATE SCHEMA](sql-createschema.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropschema.html)（原文版本：18.6；核對日期：2026-10-03）
