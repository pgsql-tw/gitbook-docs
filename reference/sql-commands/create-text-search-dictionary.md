<a id="SQL-CREATETSDICTIONARY"></a><a id="id-1.9.3.89.1"></a>

# CREATE TEXT SEARCH DICTIONARY

CREATE TEXT SEARCH DICTIONARY — define a new text search dictionary

## Synopsis

```

CREATE TEXT SEARCH DICTIONARY name (
    TEMPLATE = template
    [, option = value [, ... ]]
)
```

<a id="id-1.9.3.89.5"></a>

## Description

`CREATE TEXT SEARCH DICTIONARY` creates a new text search dictionary. A text search dictionary specifies a way of recognizing interesting or uninteresting words for searching. A dictionary depends on a text search template, which specifies the functions that actually perform the work. Typically the dictionary provides some options that control the detailed behavior of the template's functions.

If a schema name is given then the text search dictionary is created in the specified schema. Otherwise it is created in the current schema.

The user who defines a text search dictionary becomes its owner.

Refer to [Chapter 12](../../the-sql-language/12.-quan-wen-jian-suo/README.md) for further information.

<a id="id-1.9.3.89.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name of the text search dictionary to be created. The name can be schema-qualified.

<em class="replaceable"><code>template</code></em>

The name of the text search template that will define the basic behavior of this dictionary.

<em class="replaceable"><code>option</code></em>

The name of a template-specific option to be set for this dictionary.

<em class="replaceable"><code>value</code></em>

The value to use for a template-specific option. If the value is not a simple identifier or number, it must be quoted (but you can always quote it, if you wish).

The options can appear in any order.

<a id="id-1.9.3.89.7"></a>

## Examples

The following example command creates a Snowball-based dictionary with a nonstandard list of stop words.

```

CREATE TEXT SEARCH DICTIONARY my_russian (
    template = snowball,
    language = russian,
    stopwords = myrussian
);
```

<a id="id-1.9.3.89.8"></a>

## Compatibility

There is no `CREATE TEXT SEARCH DICTIONARY` statement in the SQL standard.

<a id="id-1.9.3.89.9"></a>

## See Also

[ALTER TEXT SEARCH DICTIONARY](alter-text-search-dictionary.md), [DROP TEXT SEARCH DICTIONARY](drop-text-search-dictionary.md)

---

原文：[PostgreSQL 15.19 Documentation](create-text-search-dictionary.md)（英文原文，待翻譯）
