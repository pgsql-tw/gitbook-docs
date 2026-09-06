<a id="id-1.9.3.39.1"></a>

## ALTER TEXT SEARCH PARSER

ALTER TEXT SEARCH PARSER — change the definition of a text search parser

## Synopsis

```

ALTER TEXT SEARCH PARSER name RENAME TO new_name
ALTER TEXT SEARCH PARSER name SET SCHEMA new_schema
```

<a id="id-1.9.3.39.5"></a>

## Description

`ALTER TEXT SEARCH PARSER` changes the definition of
a text search parser. Currently, the only supported functionality
is to change the parser's name.

You must be a superuser to use `ALTER TEXT SEARCH PARSER`.

<a id="id-1.9.3.39.6"></a>

## Parameters

*`name`*
:   The name (optionally schema-qualified) of an existing text search parser.

*`new_name`*
:   The new name of the text search parser.

*`new_schema`*
:   The new schema for the text search parser.

<a id="id-1.9.3.39.7"></a>

## Compatibility

There is no `ALTER TEXT SEARCH PARSER` statement in
the SQL standard.

<a id="id-1.9.3.39.8"></a>

## See Also

[CREATE TEXT SEARCH PARSER](sql-createtsparser.md), [DROP TEXT SEARCH PARSER](sql-droptsparser.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertsparser.html)（英文原文，待翻譯）
