<a id="SQL-DROPFOREIGNDATAWRAPPER"></a><a id="id-1.9.3.112.1"></a>

## DROP FOREIGN DATA WRAPPER

DROP FOREIGN DATA WRAPPER — 移除外部資料包裝器

<a id="id-1.9.3.112.4"></a>

## 語法

```

DROP FOREIGN DATA WRAPPER [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.112.5"></a>

## 說明

`DROP FOREIGN DATA WRAPPER` 會移除現有的外部資料包裝器。要執行此命令，目前使用者必須是該外部資料包裝器的擁有者。

<a id="id-1.9.3.112.6"></a>

## 參數

`IF EXISTS`
:   外部資料包裝器不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有外部資料包裝器的名稱。

`CASCADE`
:   自動移除相依於該外部資料包裝器的物件（例如外部資料表與外部伺服器），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該外部資料包裝器則拒絕移除。這是預設行為。

<a id="id-1.9.3.112.7"></a>

## 範例

移除外部資料包裝器 `dbi`：

```

DROP FOREIGN DATA WRAPPER dbi;
```

<a id="id-1.9.3.112.8"></a>

## 相容性

`DROP FOREIGN DATA WRAPPER` 符合 ISO/IEC 9075-9（SQL/MED）。`IF EXISTS` 子句是 PostgreSQL 擴充功能。

<a id="id-1.9.3.112.9"></a>

## 另請參閱

[CREATE FOREIGN DATA WRAPPER](sql-createforeigndatawrapper.md), [ALTER FOREIGN DATA WRAPPER](sql-alterforeigndatawrapper.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropforeigndatawrapper.html)（原文版本：18.6；核對日期：2026-10-03）
