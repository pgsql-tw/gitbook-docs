<a id="SQL-DROPTSDICTIONARY"></a><a id="id-1.9.3.137.1"></a>

## DROP TEXT SEARCH DICTIONARY

DROP TEXT SEARCH DICTIONARY — 移除文字搜尋字典

<a id="id-1.9.3.137.4"></a>

## 語法

```

DROP TEXT SEARCH DICTIONARY [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.137.5"></a>

## 說明

`DROP TEXT SEARCH DICTIONARY` 會移除現有的文字搜尋字典。要執行此命令，您必須是該字典的擁有者。

<a id="id-1.9.3.137.6"></a>

## 參數

`IF EXISTS`
:   文字搜尋字典不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有文字搜尋字典的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於該文字搜尋字典的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該文字搜尋字典則拒絕移除。這是預設行為。

<a id="id-1.9.3.137.7"></a>

## 範例

移除文字搜尋字典 `english`：

```

DROP TEXT SEARCH DICTIONARY english;
```

若有任何現有的文字搜尋設定使用此字典，這個命令就不會成功。加上 `CASCADE` 即可將這些設定連同字典一起移除。

<a id="id-1.9.3.137.8"></a>

## 相容性

SQL 標準中沒有 `DROP TEXT SEARCH DICTIONARY` 陳述式。

<a id="id-1.9.3.137.9"></a>

## 另請參閱

[ALTER TEXT SEARCH DICTIONARY](sql-altertsdictionary.md), [CREATE TEXT SEARCH DICTIONARY](sql-createtsdictionary.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptsdictionary.html)（原文版本：18.6；核對日期：2026-10-03）
