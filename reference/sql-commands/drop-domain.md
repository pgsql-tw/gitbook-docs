<a id="SQL-DROPDOMAIN"></a><a id="id-1.9.3.109.1"></a>

# DROP DOMAIN

DROP DOMAIN — remove a domain

## Synopsis

```

DROP DOMAIN [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.109.5"></a>

## Description

`DROP DOMAIN` removes a domain. Only the owner of a domain can remove it.

<a id="id-1.9.3.109.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the domain does not exist. A notice is issued in this case.

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of an existing domain.

`CASCADE`

Automatically drop objects that depend on the domain (such as table columns), and in turn all objects that depend on those objects (see [Section 5.14](../../the-sql-language/ddl/dependency-tracking.md)).

`RESTRICT`

Refuse to drop the domain if any objects depend on it. This is the default.

<a id="SQL-DROPDOMAIN-EXAMPLES"></a>

## Examples

To remove the domain `box`:

```

DROP DOMAIN box;
```

<a id="SQL-DROPDOMAIN-COMPATIBILITY"></a>

## Compatibility

This command conforms to the SQL standard, except for the `IF EXISTS` option, which is a PostgreSQL extension.

<a id="SQL-DROPDOMAIN-SEE-ALSO"></a>

## See Also

[CREATE DOMAIN](create-domain.md), [ALTER DOMAIN](alter-domain.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-dropdomain.html)（英文原文，待翻譯）
