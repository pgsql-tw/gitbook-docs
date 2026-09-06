<a id="SQL-ALTERTSTEMPLATE"></a><a id="id-1.9.3.40.1"></a>

# ALTER TEXT SEARCH TEMPLATE

ALTER TEXT SEARCH TEMPLATE — change the definition of a text search template

## Synopsis

```

ALTER TEXT SEARCH TEMPLATE name RENAME TO new_name
ALTER TEXT SEARCH TEMPLATE name SET SCHEMA new_schema
```

<a id="id-1.9.3.40.5"></a>

## Description

`ALTER TEXT SEARCH TEMPLATE` changes the definition of a text search template. Currently, the only supported functionality is to change the template's name.

You must be a superuser to use `ALTER TEXT SEARCH TEMPLATE`.

<a id="id-1.9.3.40.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of an existing text search template.

<em class="replaceable"><code>new&#95;name</code></em>

The new name of the text search template.

<em class="replaceable"><code>new&#95;schema</code></em>

The new schema for the text search template.

<a id="id-1.9.3.40.7"></a>

## Compatibility

There is no `ALTER TEXT SEARCH TEMPLATE` statement in the SQL standard.

<a id="id-1.9.3.40.8"></a>

## See Also

[CREATE TEXT SEARCH TEMPLATE](create-text-search-template.md), [DROP TEXT SEARCH TEMPLATE](drop-text-search-template.md)

---

原文：[PostgreSQL 15.19 Documentation](alter-text-search-template.md)（英文原文，待翻譯）
