<a id="SQL-DROPTSTEMPLATE"></a><a id="id-1.9.3.139.1"></a>

## DROP TEXT SEARCH TEMPLATE

DROP TEXT SEARCH TEMPLATE — 移除文字搜尋範本

<a id="id-1.9.3.139.4"></a>

## 語法

```

DROP TEXT SEARCH TEMPLATE [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.139.5"></a>

## 說明

`DROP TEXT SEARCH TEMPLATE` 會移除現有的文字搜尋範本。您必須是超級使用者才能使用此命令。

<a id="id-1.9.3.139.6"></a>

## 參數

`IF EXISTS`
:   文字搜尋範本不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有文字搜尋範本的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於文字搜尋範本的物件，以及相依於這些物件的所有物件
    （請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於文字搜尋範本則拒絕移除。這是預設行為。

<a id="id-1.9.3.139.7"></a>

## 範例

移除文字搜尋範本 `thesaurus`：

```

DROP TEXT SEARCH TEMPLATE thesaurus;
```

若有任何現有的文字搜尋字典使用該範本，此命令將不會成功。加上 `CASCADE` 即可將這些字典連同範本一併移除。

<a id="id-1.9.3.139.8"></a>

## 相容性

SQL 標準中沒有 `DROP TEXT SEARCH TEMPLATE` 陳述式。

<a id="id-1.9.3.139.9"></a>

## 另請參閱

[ALTER TEXT SEARCH TEMPLATE](sql-altertstemplate.md), [CREATE TEXT SEARCH TEMPLATE](sql-createtstemplate.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptstemplate.html)（原文版本：18.6；核對日期：2026-10-03）
