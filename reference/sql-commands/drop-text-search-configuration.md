<a id="SQL-DROPTSCONFIG"></a><a id="id-1.9.3.136.1"></a>

# DROP TEXT SEARCH CONFIGURATION

DROP TEXT SEARCH CONFIGURATION — remove a text search configuration

## Synopsis

```

DROP TEXT SEARCH CONFIGURATION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.136.5"></a>

## Description

`DROP TEXT SEARCH CONFIGURATION` drops an existing text search configuration. To execute this command you must be the owner of the configuration.

<a id="id-1.9.3.136.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the text search configuration does not exist. A notice is issued in this case.

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of an existing text search configuration.

`CASCADE`

Automatically drop objects that depend on the text search configuration, and in turn all objects that depend on those objects (see [Section 5.14](../../the-sql-language/ddl/dependency-tracking.md)).

`RESTRICT`

Refuse to drop the text search configuration if any objects depend on it. This is the default.

<a id="id-1.9.3.136.7"></a>

## Examples

Remove the text search configuration `my_english`:

```

DROP TEXT SEARCH CONFIGURATION my_english;
```

This command will not succeed if there are any existing indexes that reference the configuration in `to_tsvector` calls. Add `CASCADE` to drop such indexes along with the text search configuration.

<a id="id-1.9.3.136.8"></a>

## Compatibility

There is no `DROP TEXT SEARCH CONFIGURATION` statement in the SQL standard.

<a id="id-1.9.3.136.9"></a>

## See Also

[ALTER TEXT SEARCH CONFIGURATION](alter-text-search-configuration.md), [CREATE TEXT SEARCH CONFIGURATION](create-text-search-configuration.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-droptsconfig.html)（英文原文，待翻譯）
