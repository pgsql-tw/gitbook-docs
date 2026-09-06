<a id="SQL-DROPSERVER"></a><a id="id-1.9.3.131.1"></a>

# DROP SERVER

DROP SERVER — remove a foreign server descriptor

## Synopsis

```

DROP SERVER [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.131.5"></a>

## Description

`DROP SERVER` removes an existing foreign server descriptor. To execute this command, the current user must be the owner of the server.

<a id="id-1.9.3.131.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the server does not exist. A notice is issued in this case.

<em class="replaceable"><code>name</code></em>

The name of an existing server.

`CASCADE`

Automatically drop objects that depend on the server (such as user mappings), and in turn all objects that depend on those objects (see [Section 5.14](../../the-sql-language/ddl/dependency-tracking.md)).

`RESTRICT`

Refuse to drop the server if any objects depend on it. This is the default.

<a id="id-1.9.3.131.7"></a>

## Examples

Drop a server `foo` if it exists:

```

DROP SERVER IF EXISTS foo;
```

<a id="id-1.9.3.131.8"></a>

## Compatibility

`DROP SERVER` conforms to ISO/IEC 9075-9 (SQL/MED). The `IF EXISTS` clause is a PostgreSQL extension.

<a id="id-1.9.3.131.9"></a>

## See Also

[CREATE SERVER](create-server.md), [ALTER SERVER](alter-server.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-dropserver.html)（英文原文，待翻譯）
