<a id="SQL-DROPFOREIGNDATAWRAPPER"></a><a id="id-1.9.3.112.1"></a>

# DROP FOREIGN DATA WRAPPER

DROP FOREIGN DATA WRAPPER — remove a foreign-data wrapper

## Synopsis

```

DROP FOREIGN DATA WRAPPER [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.112.5"></a>

## Description

`DROP FOREIGN DATA WRAPPER` removes an existing foreign-data wrapper. To execute this command, the current user must be the owner of the foreign-data wrapper.

<a id="id-1.9.3.112.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the foreign-data wrapper does not exist. A notice is issued in this case.

<em class="replaceable"><code>name</code></em>

The name of an existing foreign-data wrapper.

`CASCADE`

Automatically drop objects that depend on the foreign-data wrapper (such as foreign tables and servers), and in turn all objects that depend on those objects (see [Section 5.14](../../the-sql-language/ddl/dependency-tracking.md)).

`RESTRICT`

Refuse to drop the foreign-data wrapper if any objects depend on it. This is the default.

<a id="id-1.9.3.112.7"></a>

## Examples

Drop the foreign-data wrapper `dbi`:

```

DROP FOREIGN DATA WRAPPER dbi;
```

<a id="id-1.9.3.112.8"></a>

## Compatibility

`DROP FOREIGN DATA WRAPPER` conforms to ISO/IEC 9075-9 (SQL/MED). The `IF EXISTS` clause is a PostgreSQL extension.

<a id="id-1.9.3.112.9"></a>

## See Also

[CREATE FOREIGN DATA WRAPPER](create-foreign-data-wrapper.md), [ALTER FOREIGN DATA WRAPPER](alter-foreign-data-wrapper.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-dropforeigndatawrapper.html)（英文原文，待翻譯）
