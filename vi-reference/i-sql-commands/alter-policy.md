# ALTER POLICY[^1]

ALTER POLICY — change the definition of a row level security policy

## Synopsis

```
ALTER POLICY 
name
 ON 
table_name
 RENAME TO 
new_name


ALTER POLICY 
name
 ON 
table_name

    [ TO { 
role_name
 | PUBLIC | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( 
using_expression
 ) ]
    [ WITH CHECK ( 
check_expression
 ) ]

```

## Description

`ALTER POLICY`changes the definition of an existing row-level security policy. Note that`ALTER POLICY`only allows the set of roles to which the policy applies and the`USING`and`WITH CHECK`expressions to be modified. To change other properties of a policy, such as the command to which it applies or whether it is permissive or restrictive, the policy must be dropped and recreated.

To use`ALTER POLICY`, you must own the table that the policy applies to.

In the second form of`ALTER POLICY`, the role list,_`using_expression`_, and_`check_expression`_are replaced independently if specified. When one of those clauses is omitted, the corresponding part of the policy is unchanged.

## Parameters

_`name`_

The name of an existing policy to alter.

_`table_name`_

The name \(optionally schema-qualified\) of the table that the policy is on.

_`new_name`_

The new name for the policy.

_`role_name`_

The role\(s\) to which the policy applies. Multiple roles can be specified at one time. To apply the policy to all roles, use`PUBLIC`.

_`using_expression`_

The`USING`expression for the policy. See[CREATE POLICY](https://www.postgresql.org/docs/devel/static/sql-createpolicy.html)for details.

_`check_expression`_

The`WITH CHECK`expression for the policy. See[CREATE POLICY](https://www.postgresql.org/docs/devel/static/sql-createpolicy.html)for details.

## Compatibility

`ALTER POLICY`is aPostgreSQLextension.

## See Also

[CREATE POLICY](https://www.postgresql.org/docs/devel/static/sql-createpolicy.html)

,

[DROP POLICY](https://www.postgresql.org/docs/devel/static/sql-droppolicy.html)

---



[^1]:  [PostgreSQL: Documentation: devel: ALTER POLICY](https://www.postgresql.org/docs/devel/static/sql-alterpolicy.html)

