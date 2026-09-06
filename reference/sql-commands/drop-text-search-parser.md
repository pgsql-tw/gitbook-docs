<a id="SQL-DROPTSPARSER"></a><a id="id-1.9.3.138.1"></a>

# DROP TEXT SEARCH PARSER

DROP TEXT SEARCH PARSER — remove a text search parser

## Synopsis

```

DROP TEXT SEARCH PARSER [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.138.5"></a>

## Description

`DROP TEXT SEARCH PARSER` drops an existing text search parser. You must be a superuser to use this command.

<a id="id-1.9.3.138.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the text search parser does not exist. A notice is issued in this case.

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of an existing text search parser.

`CASCADE`

Automatically drop objects that depend on the text search parser, and in turn all objects that depend on those objects (see [Section 5.14](../../the-sql-language/ddl/dependency-tracking.md)).

`RESTRICT`

Refuse to drop the text search parser if any objects depend on it. This is the default.

<a id="id-1.9.3.138.7"></a>

## Examples

Remove the text search parser `my_parser`:

```

DROP TEXT SEARCH PARSER my_parser;
```

This command will not succeed if there are any existing text search configurations that use the parser. Add `CASCADE` to drop such configurations along with the parser.

<a id="id-1.9.3.138.8"></a>

## Compatibility

There is no `DROP TEXT SEARCH PARSER` statement in the SQL standard.

<a id="id-1.9.3.138.9"></a>

## See Also

[ALTER TEXT SEARCH PARSER](alter-text-search-parser.md), [CREATE TEXT SEARCH PARSER](create-text-search-parser.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-droptsparser.html)（英文原文，待翻譯）
