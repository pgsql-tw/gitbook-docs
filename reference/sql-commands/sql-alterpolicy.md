<a id="id-1.9.3.23.1"></a>

## ALTER POLICY

ALTER POLICY — change the definition of a row-level security policy

## Synopsis

```

ALTER POLICY name ON table_name RENAME TO new_name

ALTER POLICY name ON table_name
    [ TO { role_name | PUBLIC | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( using_expression ) ]
    [ WITH CHECK ( check_expression ) ]
```

<a id="id-1.9.3.23.5"></a>

## Description

`ALTER POLICY` changes the definition of an existing
row-level security policy. Note that `ALTER POLICY`
only allows the set of roles to which the policy applies and the
`USING` and `WITH CHECK` expressions to
be modified. To change other properties of a policy, such as the command
to which it applies or whether it is permissive or restrictive, the policy
must be dropped and recreated.

To use `ALTER POLICY`, you must own the table that
the policy applies to.

In the second form of `ALTER POLICY`, the role list,
*`using_expression`*, and
*`check_expression`* are replaced
independently if specified. When one of those clauses is omitted, the
corresponding part of the policy is unchanged.

<a id="id-1.9.3.23.6"></a>

## Parameters

*`name`*
:   The name of an existing policy to alter.

*`table_name`*
:   The name (optionally schema-qualified) of the table that the
    policy is on.

*`new_name`*
:   The new name for the policy.

*`role_name`*
:   The role(s) to which the policy applies. Multiple roles can be
    specified at one time. To apply the policy to all roles,
    use `PUBLIC`.

*`using_expression`*
:   The `USING` expression for the policy.
    See [CREATE POLICY](sql-createpolicy.md) for details.

*`check_expression`*
:   The `WITH CHECK` expression for the policy.
    See [CREATE POLICY](sql-createpolicy.md) for details.

<a id="id-1.9.3.23.7"></a>

## Compatibility

`ALTER POLICY` is a PostgreSQL extension.

<a id="id-1.9.3.23.8"></a>

## See Also

[CREATE POLICY](sql-createpolicy.md), [DROP POLICY](sql-droppolicy.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterpolicy.html)（英文原文，待翻譯）
