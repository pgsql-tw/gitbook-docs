<a id="SQL-DROPOPFAMILY"></a><a id="id-1.9.3.121.1"></a>

# DROP OPERATOR FAMILY

DROP OPERATOR FAMILY — remove an operator family

## Synopsis

```

DROP OPERATOR FAMILY [ IF EXISTS ] name USING index_method [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.121.5"></a>

## Description

`DROP OPERATOR FAMILY` drops an existing operator family. To execute this command you must be the owner of the operator family.

`DROP OPERATOR FAMILY` includes dropping any operator classes contained in the family, but it does not drop any of the operators or functions referenced by the family. If there are any indexes depending on operator classes within the family, you will need to specify `CASCADE` for the drop to complete.

<a id="id-1.9.3.121.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the operator family does not exist. A notice is issued in this case.

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of an existing operator family.

<em class="replaceable"><code>index&#95;method</code></em>

The name of the index access method the operator family is for.

`CASCADE`

Automatically drop objects that depend on the operator family, and in turn all objects that depend on those objects (see [Section 5.14](../../the-sql-language/ddl/dependency-tracking.md)).

`RESTRICT`

Refuse to drop the operator family if any objects depend on it. This is the default.

<a id="id-1.9.3.121.7"></a>

## Examples

Remove the B-tree operator family `float_ops`:

```

DROP OPERATOR FAMILY float_ops USING btree;
```

This command will not succeed if there are any existing indexes that use operator classes within the family. Add `CASCADE` to drop such indexes along with the operator family.

<a id="id-1.9.3.121.8"></a>

## Compatibility

There is no `DROP OPERATOR FAMILY` statement in the SQL standard.

<a id="id-1.9.3.121.9"></a>

## See Also

[ALTER OPERATOR FAMILY](alter-operator-family.md), [CREATE OPERATOR FAMILY](create-operator-family.md), [ALTER OPERATOR CLASS](alter-operator-class.md), [CREATE OPERATOR CLASS](create-operator-class.md), [DROP OPERATOR CLASS](drop-operator-class.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-dropopfamily.html)（英文原文，待翻譯）
