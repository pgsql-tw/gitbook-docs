<a id="SQL-ALTEROPCLASS"></a><a id="id-1.9.3.21.1"></a>

# ALTER OPERATOR CLASS

ALTER OPERATOR CLASS — change the definition of an operator class

## Synopsis

```

ALTER OPERATOR CLASS name USING index_method
    RENAME TO new_name

ALTER OPERATOR CLASS name USING index_method
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER OPERATOR CLASS name USING index_method
    SET SCHEMA new_schema
```

<a id="id-1.9.3.21.5"></a>

## Description

`ALTER OPERATOR CLASS` changes the definition of an operator class.

You must own the operator class to use `ALTER OPERATOR CLASS`. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the operator class's schema. (These restrictions enforce that altering the owner doesn't do anything you couldn't do by dropping and recreating the operator class. However, a superuser can alter ownership of any operator class anyway.)

<a id="id-1.9.3.21.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of an existing operator class.

<em class="replaceable"><code>index&#95;method</code></em>

The name of the index method this operator class is for.

<em class="replaceable"><code>new&#95;name</code></em>

The new name of the operator class.

<em class="replaceable"><code>new&#95;owner</code></em>

The new owner of the operator class.

<em class="replaceable"><code>new&#95;schema</code></em>

The new schema for the operator class.

<a id="id-1.9.3.21.7"></a>

## Compatibility

There is no `ALTER OPERATOR CLASS` statement in the SQL standard.

<a id="id-1.9.3.21.8"></a>

## See Also

[CREATE OPERATOR CLASS](create-operator-class.md), [DROP OPERATOR CLASS](drop-operator-class.md), [ALTER OPERATOR FAMILY](alter-operator-family.md)

---

原文：[PostgreSQL 15.19 Documentation](alter-operator-class.md)（英文原文，待翻譯）
