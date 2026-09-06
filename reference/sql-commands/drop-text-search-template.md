<a id="SQL-DROPTSTEMPLATE"></a><a id="id-1.9.3.139.1"></a>

# DROP TEXT SEARCH TEMPLATE

DROP TEXT SEARCH TEMPLATE — remove a text search template

## Synopsis

```

DROP TEXT SEARCH TEMPLATE [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.139.5"></a>

## Description

`DROP TEXT SEARCH TEMPLATE` drops an existing text search template. You must be a superuser to use this command.

<a id="id-1.9.3.139.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the text search template does not exist. A notice is issued in this case.

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of an existing text search template.

`CASCADE`

Automatically drop objects that depend on the text search template, and in turn all objects that depend on those objects (see [Section 5.14](../../the-sql-language/ddl/dependency-tracking.md)).

`RESTRICT`

Refuse to drop the text search template if any objects depend on it. This is the default.

<a id="id-1.9.3.139.7"></a>

## Examples

Remove the text search template `thesaurus`:

```

DROP TEXT SEARCH TEMPLATE thesaurus;
```

This command will not succeed if there are any existing text search dictionaries that use the template. Add `CASCADE` to drop such dictionaries along with the template.

<a id="id-1.9.3.139.8"></a>

## Compatibility

There is no `DROP TEXT SEARCH TEMPLATE` statement in the SQL standard.

<a id="id-1.9.3.139.9"></a>

## See Also

[ALTER TEXT SEARCH TEMPLATE](alter-text-search-template.md), [CREATE TEXT SEARCH TEMPLATE](create-text-search-template.md)

---

原文：[PostgreSQL 15.19 Documentation](drop-text-search-template.md)（英文原文，待翻譯）
