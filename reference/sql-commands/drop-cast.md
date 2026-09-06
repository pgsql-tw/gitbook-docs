<a id="SQL-DROPCAST"></a><a id="id-1.9.3.105.1"></a>

# DROP CAST

DROP CAST — remove a cast

## Synopsis

```

DROP CAST [ IF EXISTS ] (source_type AS target_type) [ CASCADE | RESTRICT ]
```

<a id="SQL-DROPCAST-DESCRIPTION"></a>

## Description

`DROP CAST` removes a previously defined cast.

To be able to drop a cast, you must own the source or the target data type. These are the same privileges that are required to create a cast.

<a id="id-1.9.3.105.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the cast does not exist. A notice is issued in this case.

<em class="replaceable"><code>source&#95;type</code></em>

The name of the source data type of the cast.

<em class="replaceable"><code>target&#95;type</code></em>

The name of the target data type of the cast.

`CASCADE`<br>`RESTRICT`

These key words do not have any effect, since there are no dependencies on casts.

<a id="SQL-DROPCAST-EXAMPLES"></a>

## Examples

To drop the cast from type `text` to type `int`:

```

DROP CAST (text AS int);
```

<a id="SQL-DROPCAST-COMPAT"></a>

## Compatibility

The `DROP CAST` command conforms to the SQL standard.

<a id="id-1.9.3.105.9"></a>

## See Also

[CREATE CAST](create-cast.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-dropcast.html)（英文原文，待翻譯）
