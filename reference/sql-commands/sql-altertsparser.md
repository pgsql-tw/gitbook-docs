<a id="id-1.9.3.39.1"></a>

## ALTER TEXT SEARCH PARSER

ALTER TEXT SEARCH PARSER — 變更文字搜尋剖析器的定義

## 語法

```

ALTER TEXT SEARCH PARSER name RENAME TO new_name
ALTER TEXT SEARCH PARSER name SET SCHEMA new_schema
```

<a id="id-1.9.3.39.5"></a>

## 說明

`ALTER TEXT SEARCH PARSER` 會變更文字搜尋剖析器的定義。目前唯一支援的功能是變更剖析器名稱。

你必須是超級使用者，才能使用 `ALTER TEXT SEARCH PARSER`。

<a id="id-1.9.3.39.6"></a>

## 參數

*`name`*
:   既有文字搜尋剖析器的名稱（可加上 schema 名稱限定）。

*`new_name`*
:   文字搜尋剖析器的新名稱。

*`new_schema`*
:   文字搜尋剖析器的新 schema。

<a id="id-1.9.3.39.7"></a>

## 相容性

SQL 標準中沒有 `ALTER TEXT SEARCH PARSER` 陳述式。

<a id="id-1.9.3.39.8"></a>

## 另請參閱

[CREATE TEXT SEARCH PARSER](sql-createtsparser.md), [DROP TEXT SEARCH PARSER](sql-droptsparser.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertsparser.html)（原文版本：18.6；核對日期：2026-09-07）
