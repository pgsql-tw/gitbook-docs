<a id="SQL-DROPTYPE"></a><a id="id-1.9.3.142.1"></a>

## DROP TYPE

DROP TYPE — 移除資料型別

<a id="id-1.9.3.142.4"></a>

## 語法

```

DROP TYPE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.142.5"></a>

## 說明

`DROP TYPE` 會移除使用者定義的資料型別。只有型別的擁有者可以移除它。

<a id="id-1.9.3.142.6"></a>

## 參數

`IF EXISTS`
:   型別不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除之資料型別的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於該型別的物件（例如資料表欄位、函式與運算子），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該型別則拒絕移除。這是預設行為。

<a id="SQL-DROPTYPE-EXAMPLES"></a>

## 範例

若要移除資料型別 `box`：

```

DROP TYPE box;
```

<a id="SQL-DROPTYPE-COMPATIBILITY"></a>

## 相容性

此命令與 SQL 標準中對應的命令類似，但 `IF EXISTS` 選項是 PostgreSQL 擴充功能。不過請注意，PostgreSQL 中 `CREATE TYPE` 命令的大部分內容以及資料型別擴充機制都與 SQL 標準不同。

<a id="SQL-DROPTYPE-SEE-ALSO"></a>

## 另請參閱

[ALTER TYPE](sql-altertype.md), [CREATE TYPE](sql-createtype.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptype.html)（原文版本：18.6；核對日期：2026-10-03）
