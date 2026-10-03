<a id="SQL-DROPFOREIGNTABLE"></a><a id="id-1.9.3.113.1"></a>

## DROP FOREIGN TABLE

DROP FOREIGN TABLE — 移除外部資料表

<a id="id-1.9.3.113.4"></a>

## 語法

```

DROP FOREIGN TABLE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.113.5"></a>

## 說明

`DROP FOREIGN TABLE` 會移除外部資料表。只有外部資料表的擁有者可以移除它。

<a id="id-1.9.3.113.6"></a>

## 參數

`IF EXISTS`
:   外部資料表不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除之外部資料表的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於外部資料表的物件（例如檢視表），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於外部資料表則拒絕移除。這是預設行為。

<a id="id-1.9.3.113.7"></a>

## 範例

若要刪除 `films` 與 `distributors` 這兩個外部資料表：

```

DROP FOREIGN TABLE films, distributors;
```

<a id="id-1.9.3.113.8"></a>

## 相容性

此命令符合 ISO/IEC 9075-9（SQL/MED），但標準只允許每個命令移除一個外部資料表；此外，`IF EXISTS` 選項是 PostgreSQL 擴充功能。

<a id="id-1.9.3.113.9"></a>

## 另請參閱

[ALTER FOREIGN TABLE](sql-alterforeigntable.md), [CREATE FOREIGN TABLE](sql-createforeigntable.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropforeigntable.html)（原文版本：18.6；核對日期：2026-10-03）
