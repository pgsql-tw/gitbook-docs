<a id="SQL-DROPCONVERSION"></a><a id="id-1.9.3.107.1"></a>

# DROP CONVERSION

DROP CONVERSION — remove a conversion

## Synopsis

```

DROP CONVERSION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="SQL-DROPCONVERSION-DESCRIPTION"></a>

## Description

`DROP CONVERSION` removes a previously defined conversion. To be able to drop a conversion, you must own the conversion.

<a id="id-1.9.3.107.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the conversion does not exist. A notice is issued in this case.

<em class="replaceable"><code>name</code></em>

The name of the conversion. The conversion name can be schema-qualified.

`CASCADE`<br>`RESTRICT`

These key words do not have any effect, since there are no dependencies on conversions.

<a id="SQL-DROPCONVERSION-EXAMPLES"></a>

## Examples

To drop the conversion named `myname`:

```

DROP CONVERSION myname;
```

<a id="SQL-DROPCONVERSION-COMPAT"></a>

## Compatibility

There is no `DROP CONVERSION` statement in the SQL standard, but a `DROP TRANSLATION` statement that goes along with the `CREATE TRANSLATION` statement that is similar to the `CREATE CONVERSION` statement in PostgreSQL.

<a id="id-1.9.3.107.9"></a>

## See Also

[ALTER CONVERSION](alter-conversion.md), [CREATE CONVERSION](create-conversion.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-dropconversion.html)（英文原文，待翻譯）
