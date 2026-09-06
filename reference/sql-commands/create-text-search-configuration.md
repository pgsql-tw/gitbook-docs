<a id="SQL-CREATETSCONFIG"></a><a id="id-1.9.3.88.1"></a>

# CREATE TEXT SEARCH CONFIGURATION

CREATE TEXT SEARCH CONFIGURATION — define a new text search configuration

## Synopsis

```

CREATE TEXT SEARCH CONFIGURATION name (
    PARSER = parser_name |
    COPY = source_config
)
```

<a id="id-1.9.3.88.5"></a>

## Description

`CREATE TEXT SEARCH CONFIGURATION` creates a new text search configuration. A text search configuration specifies a text search parser that can divide a string into tokens, plus dictionaries that can be used to determine which tokens are of interest for searching.

If only the parser is specified, then the new text search configuration initially has no mappings from token types to dictionaries, and therefore will ignore all words. Subsequent `ALTER TEXT SEARCH CONFIGURATION` commands must be used to create mappings to make the configuration useful. Alternatively, an existing text search configuration can be copied.

If a schema name is given then the text search configuration is created in the specified schema. Otherwise it is created in the current schema.

The user who defines a text search configuration becomes its owner.

Refer to [Chapter 12](../../the-sql-language/12.-quan-wen-jian-suo/README.md) for further information.

<a id="id-1.9.3.88.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name of the text search configuration to be created. The name can be schema-qualified.

<em class="replaceable"><code>parser&#95;name</code></em>

The name of the text search parser to use for this configuration.

<em class="replaceable"><code>source&#95;config</code></em>

The name of an existing text search configuration to copy.

<a id="id-1.9.3.88.7"></a>

## Notes

The `PARSER` and `COPY` options are mutually exclusive, because when an existing configuration is copied, its parser selection is copied too.

<a id="id-1.9.3.88.8"></a>

## Compatibility

There is no `CREATE TEXT SEARCH CONFIGURATION` statement in the SQL standard.

<a id="id-1.9.3.88.9"></a>

## See Also

[ALTER TEXT SEARCH CONFIGURATION](alter-text-search-configuration.md), [DROP TEXT SEARCH CONFIGURATION](drop-text-search-configuration.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-createtsconfig.html)（英文原文，待翻譯）
