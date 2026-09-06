<a id="SQL-ALTEROPERATOR"></a><a id="id-1.9.3.20.1"></a>

# ALTER OPERATOR

ALTER OPERATOR — change the definition of an operator

## Synopsis

```

ALTER OPERATOR name ( { left_type | NONE } , right_type )
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER OPERATOR name ( { left_type | NONE } , right_type )
    SET SCHEMA new_schema

ALTER OPERATOR name ( { left_type | NONE } , right_type )
    SET ( {  RESTRICT = { res_proc | NONE }
           | JOIN = { join_proc | NONE }
         } [, ... ] )
```

<a id="id-1.9.3.20.5"></a>

## Description

`ALTER OPERATOR` changes the definition of an operator.

You must own the operator to use `ALTER OPERATOR`. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the operator's schema. (These restrictions enforce that altering the owner doesn't do anything you couldn't do by dropping and recreating the operator. However, a superuser can alter ownership of any operator anyway.)

<a id="id-1.9.3.20.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name (optionally schema-qualified) of an existing operator.

<em class="replaceable"><code>left&#95;type</code></em>

The data type of the operator's left operand; write `NONE` if the operator has no left operand.

<em class="replaceable"><code>right&#95;type</code></em>

The data type of the operator's right operand.

<em class="replaceable"><code>new&#95;owner</code></em>

The new owner of the operator.

<em class="replaceable"><code>new&#95;schema</code></em>

The new schema for the operator.

<em class="replaceable"><code>res&#95;proc</code></em>

The restriction selectivity estimator function for this operator; write NONE to remove existing selectivity estimator.

<em class="replaceable"><code>join&#95;proc</code></em>

The join selectivity estimator function for this operator; write NONE to remove existing selectivity estimator.

<a id="id-1.9.3.20.7"></a>

## Examples

Change the owner of a custom operator `a @@ b` for type `text`:

```

ALTER OPERATOR @@ (text, text) OWNER TO joe;
```

Change the restriction and join selectivity estimator functions of a custom operator `a && b` for type `int[]`:

```

ALTER OPERATOR && (_int4, _int4) SET (RESTRICT = _int_contsel, JOIN = _int_contjoinsel);
```

<a id="id-1.9.3.20.8"></a>

## Compatibility

There is no `ALTER OPERATOR` statement in the SQL standard.

<a id="id-1.9.3.20.9"></a>

## See Also

[CREATE OPERATOR](create-operator.md), [DROP OPERATOR](drop-operator.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-alteroperator.html)（英文原文，待翻譯）
