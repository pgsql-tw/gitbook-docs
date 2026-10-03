<a id="SQL-DROPSEQUENCE"></a><a id="id-1.9.3.130.1"></a>

## DROP SEQUENCE

DROP SEQUENCE — 移除序列

<a id="id-1.9.3.130.4"></a>

## 語法

```

DROP SEQUENCE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.130.5"></a>

## 說明

`DROP SEQUENCE` 會移除序號產生器。序列只能由其擁有者或超級使用者移除。

<a id="id-1.9.3.130.6"></a>

## 參數

`IF EXISTS`
:   序列不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   序列的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於該序列的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該序列則拒絕移除。這是預設行為。

<a id="id-1.9.3.130.7"></a>

## 範例

移除序列 `serial`：

```

DROP SEQUENCE serial;
```

<a id="id-1.9.3.130.8"></a>

## 相容性

`DROP SEQUENCE` 符合 SQL 標準，但有兩點例外：標準只允許每個命令移除一個序列；另外，`IF EXISTS` 選項是 PostgreSQL 的擴充功能。

<a id="id-1.9.3.130.9"></a>

## 另請參閱

[CREATE SEQUENCE](sql-createsequence.md), [ALTER SEQUENCE](sql-altersequence.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropsequence.html)（原文版本：18.6；核對日期：2026-10-03）
