<a id="SQL-DROPOPCLASS"></a><a id="id-1.9.3.120.1"></a>

# DROP OPERATOR CLASS

DROP OPERATOR CLASS — remove an operator class

## Synopsis

```

DROP OPERATOR CLASS [ IF EXISTS ] name USING index_method [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.120.5"></a>

## Description

`DROP OPERATOR CLASS` drops an existing operator class. To execute this command you must be the owner of the operator class.

`DROP OPERATOR CLASS` does not drop any of the operators or functions referenced by the class. If there are any indexes depending on the operator class, you will need to specify `CASCADE` for the drop to complete.

<a id="id-1.9.3.120.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the operator class does not exist. A notice is issued in this case.

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of an existing operator class.

<em class="replaceable"><code>index&#95;method</code></em>

The name of the index access method the operator class is for.

`CASCADE`

Automatically drop objects that depend on the operator class (such as indexes), and in turn all objects that depend on those objects (see [Section 5.14](../../the-sql-language/ddl/dependency-tracking.md)).

`RESTRICT`

Refuse to drop the operator class if any objects depend on it. This is the default.

<a id="id-1.9.3.120.7"></a>

## Notes

`DROP OPERATOR CLASS` will not drop the operator family containing the class, even if there is nothing else left in the family (in particular, in the case where the family was implicitly created by `CREATE OPERATOR CLASS`). An empty operator family is harmless, but for the sake of tidiness you might wish to remove the family with `DROP OPERATOR FAMILY`; or perhaps better, use `DROP OPERATOR FAMILY` in the first place.

<a id="id-1.9.3.120.8"></a>

## Examples

Remove the B-tree operator class `widget_ops`:

```

DROP OPERATOR CLASS widget_ops USING btree;
```

This command will not succeed if there are any existing indexes that use the operator class. Add `CASCADE` to drop such indexes along with the operator class.

<a id="id-1.9.3.120.9"></a>

## Compatibility

There is no `DROP OPERATOR CLASS` statement in the SQL standard.

<a id="id-1.9.3.120.10"></a>

## See Also

[ALTER OPERATOR CLASS](alter-operator-class.md), [CREATE OPERATOR CLASS](create-operator-class.md), [DROP OPERATOR FAMILY](drop-operator-family.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-dropopclass.html)（英文原文，待翻譯）
