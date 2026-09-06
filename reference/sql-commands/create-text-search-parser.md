<a id="SQL-CREATETSPARSER"></a><a id="id-1.9.3.90.1"></a>

# CREATE TEXT SEARCH PARSER

CREATE TEXT SEARCH PARSER — define a new text search parser

## Synopsis

```

CREATE TEXT SEARCH PARSER name (
    START = start_function ,
    GETTOKEN = gettoken_function ,
    END = end_function ,
    LEXTYPES = lextypes_function
    [, HEADLINE = headline_function ]
)
```

<a id="id-1.9.3.90.5"></a>

## Description

`CREATE TEXT SEARCH PARSER` creates a new text search parser. A text search parser defines a method for splitting a text string into tokens and assigning types (categories) to the tokens. A parser is not particularly useful by itself, but must be bound into a text search configuration along with some text search dictionaries to be used for searching.

If a schema name is given then the text search parser is created in the specified schema. Otherwise it is created in the current schema.

You must be a superuser to use `CREATE TEXT SEARCH PARSER`. (This restriction is made because an erroneous text search parser definition could confuse or even crash the server.)

Refer to [Chapter 12](../../the-sql-language/12.-quan-wen-jian-suo/README.md) for further information.

<a id="id-1.9.3.90.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name of the text search parser to be created. The name can be schema-qualified.

<em class="replaceable"><code>start&#95;function</code></em>

The name of the start function for the parser.

<em class="replaceable"><code>gettoken&#95;function</code></em>

The name of the get-next-token function for the parser.

<em class="replaceable"><code>end&#95;function</code></em>

The name of the end function for the parser.

<em class="replaceable"><code>lextypes&#95;function</code></em>

The name of the lextypes function for the parser (a function that returns information about the set of token types it produces).

<em class="replaceable"><code>headline&#95;function</code></em>

The name of the headline function for the parser (a function that summarizes a set of tokens).

The function names can be schema-qualified if necessary. Argument types are not given, since the argument list for each type of function is predetermined. All except the headline function are required.

The arguments can appear in any order, not only the one shown above.

<a id="id-1.9.3.90.7"></a>

## Compatibility

There is no `CREATE TEXT SEARCH PARSER` statement in the SQL standard.

<a id="id-1.9.3.90.8"></a>

## See Also

[ALTER TEXT SEARCH PARSER](alter-text-search-parser.md), [DROP TEXT SEARCH PARSER](drop-text-search-parser.md)

---

原文：[PostgreSQL 15.19 Documentation](create-text-search-parser.md)（英文原文，待翻譯）
