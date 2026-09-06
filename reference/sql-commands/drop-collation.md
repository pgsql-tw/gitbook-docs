<a id="SQL-DROPCOLLATION"></a><a id="id-1.9.3.106.1"></a>

# DROP COLLATION

DROP COLLATION — remove a collation

## Synopsis

```

DROP COLLATION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="SQL-DROPCOLLATION-DESCRIPTION"></a>

## Description

`DROP COLLATION` removes a previously defined collation. To be able to drop a collation, you must own the collation.

<a id="id-1.9.3.106.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the collation does not exist. A notice is issued in this case.

<em class="replaceable"><code>name</code></em>

The name of the collation. The collation name can be schema-qualified.

`CASCADE`

Automatically drop objects that depend on the collation, and in turn all objects that depend on those objects (see [Section 5.14](../../the-sql-language/ddl/dependency-tracking.md)).

`RESTRICT`

Refuse to drop the collation if any objects depend on it. This is the default.

<a id="SQL-DROPCOLLATION-EXAMPLES"></a>

## Examples

To drop the collation named `german`:

```

DROP COLLATION german;
```

<a id="SQL-DROPCOLLATION-COMPAT"></a>

## Compatibility

The `DROP COLLATION` command conforms to the SQL standard, apart from the `IF EXISTS` option, which is a PostgreSQL extension.

<a id="id-1.9.3.106.9"></a>

## See Also

[ALTER COLLATION](alter-collation.md), [CREATE COLLATION](create-collation.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-dropcollation.html)（英文原文，待翻譯）
