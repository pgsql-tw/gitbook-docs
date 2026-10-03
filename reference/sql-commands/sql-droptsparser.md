<a id="SQL-DROPTSPARSER"></a><a id="id-1.9.3.138.1"></a>

## DROP TEXT SEARCH PARSER

DROP TEXT SEARCH PARSER — 移除文字搜尋剖析器

<a id="id-1.9.3.138.4"></a>

## 語法

```

DROP TEXT SEARCH PARSER [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.138.5"></a>

## 說明

`DROP TEXT SEARCH PARSER` 會移除現有的文字搜尋剖析器。你必須是超級使用者才能使用此命令。

<a id="id-1.9.3.138.6"></a>

## 參數

`IF EXISTS`
:   文字搜尋剖析器不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有文字搜尋剖析器的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於該文字搜尋剖析器的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該文字搜尋剖析器則拒絕移除。這是預設行為。

<a id="id-1.9.3.138.7"></a>

## 範例

移除文字搜尋剖析器 `my_parser`：

```

DROP TEXT SEARCH PARSER my_parser;
```

若有任何現有的文字搜尋設定使用此剖析器，此命令將不會成功。加上 `CASCADE` 可將這些設定連同剖析器一併移除。

<a id="id-1.9.3.138.8"></a>

## 相容性

SQL 標準中沒有 `DROP TEXT SEARCH PARSER` 陳述式。

<a id="id-1.9.3.138.9"></a>

## 另請參閱

[ALTER TEXT SEARCH PARSER](sql-altertsparser.md), [CREATE TEXT SEARCH PARSER](sql-createtsparser.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptsparser.html)（原文版本：18.6；核對日期：2026-10-03）
