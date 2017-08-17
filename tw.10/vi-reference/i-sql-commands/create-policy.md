# CREATE POLICY[^1]

CREATE POLICY — define a new row level security policy for a table

## Synopsis

```
CREATE POLICY 
name
 ON 
table_name

    [ AS { PERMISSIVE | RESTRICTIVE } ]
    [ FOR { ALL | SELECT | INSERT | UPDATE | DELETE } ]
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

The`CREATE POLICY`command defines a new row-level security policy for a table. Note that row-level security must be enabled on the table \(using`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`\) in order for created policies to be applied.

A policy grants the permission to select, insert, update, or delete rows that match the relevant policy expression. Existing table rows are checked against the expression specified in`USING`, while new rows that would be created via`INSERT`or`UPDATE`are checked against the expression specified in`WITH CHECK`. When a`USING`expression returns true for a given row then that row is visible to the user, while if false or null is returned then the row is not visible. When a`WITH CHECK`expression returns true for a row then that row is inserted or updated, while if false or null is returned then an error occurs.

For`INSERT`and`UPDATE`statements,`WITH CHECK`expressions are enforced after`BEFORE`triggers are fired, and before any actual data modifications are made. Thus a`BEFORE ROW`trigger may modify the data to be inserted, affecting the result of the security policy check.`WITH CHECK`expressions are enforced before any other constraints.

Policy names are per-table. Therefore, one policy name can be used for many different tables and have a definition for each table which is appropriate to that table.

Policies can be applied for specific commands or for specific roles. The default for newly created policies is that they apply for all commands and roles, unless otherwise specified. If multiple policies apply to a given statement, they will be combined using OR \(although`ON CONFLICT DO UPDATE`and`INSERT`policies are not combined in this way, but rather enforced as noted at each stage of`ON CONFLICT`execution\).

For commands that can have both`USING`and`WITH CHECK`policies \(`ALL`and`UPDATE`\), if no`WITH CHECK`policy is defined, then the`USING`policy will be used both for which rows are visible \(normal`USING`case\) and for which rows will be allowed to be added \(`WITH CHECK`case\).

If row-level security is enabled for a table, but no applicable policies exist, a“default deny”policy is assumed, so that no rows will be visible or updatable.

## Parameters

_`name`_

The name of the policy to be created. This must be distinct from the name of any other policy for the table.

_`table_name`_

The name \(optionally schema-qualified\) of the table the policy applies to.

`PERMISSIVE`

Specify that the policy is to be created as a permissive policy. All permissive policies which are applicable to a given query will be combined together using the Boolean“OR”operator. By creating permissive policies, administrators can add to the set of records which can be accessed. Policies are permissive by default.

`RESTRICTIVE`

Specify that the policy is to be created as a restrictive policy. All restrictive policies which are applicable to a given query will be combined together using the Boolean“AND”operator. By creating restrictive policies, administrators can reduce the set of records which can be accessed as all restrictive policies must be passed for each record.

_`command`_

The command to which the policy applies. Valid options are`ALL`,`SELECT`,`INSERT`,`UPDATE`, and`DELETE`.`ALL`is the default. See below for specifics regarding how these are applied.

_`role_name`_

The role\(s\) to which the policy is to be applied. The default is`PUBLIC`, which will apply the policy to all roles.

_`using_expression`_

AnySQLconditional expression \(returning`boolean`\). The conditional expression cannot contain any aggregate or window functions. This expression will be added to queries that refer to the table if row level security is enabled. Rows for which the expression returns true will be visible. Any rows for which the expression returns false or null will not be visible to the user \(in a`SELECT`\), and will not be available for modification \(in an`UPDATE`or`DELETE`\). Such rows are silently suppressed; no error is reported.

_`check_expression`_

AnySQLconditional expression \(returning`boolean`\). The conditional expression cannot contain any aggregate or window functions. This expression will be used in`INSERT`and`UPDATE`queries against the table if row level security is enabled. Only rows for which the expression evaluates to true will be allowed. An error will be thrown if the expression evaluates to false or null for any of the records inserted or any of the records that result from the update. Note that the_`check_expression`_is evaluated against the proposed new contents of the row, not the original contents.

### Per-Command Policies

`ALL`

Using`ALL`for a policy means that it will apply to all commands, regardless of the type of command. If an`ALL`policy exists and more specific policies exist, then both the`ALL`policy and the more specific policy \(or policies\) will be combined using OR, as usual for overlapping policies. Additionally,`ALL`policies will be applied to both the selection side of a query and the modification side, using the`USING`expression for both cases if only a`USING`expression has been defined.

As an example, if an`UPDATE`is issued, then the`ALL`policy will be applicable both to what the`UPDATE`will be able to select as rows to be updated \(applying the`USING`expression\), and to the resulting updated rows, to check if they are permitted to be added to the table \(applying the`WITH CHECK`expression, if defined, and the`USING`expression otherwise\). If an`INSERT`or`UPDATE`command attempts to add rows to the table that do not pass the`ALL`policy's`WITH CHECK`expression, the entire command will be aborted.

`SELECT`

Using`SELECT`for a policy means that it will apply to`SELECT`queries and whenever`SELECT`permissions are required on the relation the policy is defined for. The result is that only those records from the relation that pass the`SELECT`policy will be returned during a`SELECT`query, and that queries that require`SELECT`permissions, such as`UPDATE`, will also only see those records that are allowed by the`SELECT`policy. A`SELECT`policy cannot have a`WITH CHECK`expression, as it only applies in cases where records are being retrieved from the relation.

`INSERT`

Using`INSERT`for a policy means that it will apply to`INSERT`commands. Rows being inserted that do not pass this policy will result in a policy violation error, and the entire`INSERT`command will be aborted. An`INSERT`policy cannot have a`USING`expression, as it only applies in cases where records are being added to the relation.

Note that`INSERT`with`ON CONFLICT DO UPDATE`checks`INSERT`policies'`WITH CHECK`expressions only for rows appended to the relation by the`INSERT`path.

`UPDATE`

Using`UPDATE`for a policy means that it will apply to`UPDATE`commands \(or auxiliary`ON CONFLICT DO UPDATE`clauses of`INSERT`commands\). Since`UPDATE`involves pulling an existing record and then making changes to some portion \(but possibly not all\) of the record,`UPDATE`policies accept both a`USING`expression and a`WITH CHECK`expression. The`USING`expression determines which records the`UPDATE`command will see to operate against, while the`WITH CHECK`expression defines which modified rows are allowed to be stored back into the relation.

When an`UPDATE`command is used with a`WHERE`clause or a`RETURNING`clause,`SELECT`rights are also required on the relation being updated and the appropriate`SELECT`and`ALL`policies will be combined \(using OR for any overlapping`SELECT`related policies found\) with the`USING`clause of the`UPDATE`policy using AND. Therefore, in order for a user to be able to`UPDATE`specific rows, the user must have access to the row\(s\) through a`SELECT`or`ALL`policy and the row\(s\) must pass the`UPDATE`policy's`USING`expression.

Any rows whose updated values do not pass the`WITH CHECK`expression will cause an error, and the entire command will be aborted. If only a`USING`clause is specified, then that clause will be used for both`USING`and`WITH CHECK`cases.

Note, however, that`INSERT`with`ON CONFLICT DO UPDATE`requires that an`UPDATE`policy`USING`expression always be enforced as a`WITH CHECK`expression. This`UPDATE`policy must always pass when the`UPDATE`path is taken. Any existing row that necessitates that the`UPDATE`path be taken must pass the \(`UPDATE`or`ALL`\)`USING`qualifications \(combined using OR\), which are always enforced as`WITH CHECK`options in this context. \(The`UPDATE`path will_never_be silently avoided; an error will be thrown instead.\) Finally, the final row appended to the relation must pass any`WITH CHECK`options that a conventional`UPDATE`is required to pass.

`DELETE`

Using`DELETE`for a policy means that it will apply to`DELETE`commands. Only rows that pass this policy will be seen by a`DELETE`command. There can be rows that are visible through a`SELECT`that are not available for deletion, if they do not pass the`USING`expression for the`DELETE`policy.

When a`DELETE`command is used with a`WHERE`clause or a`RETURNING`clause,`SELECT`rights are also required on the relation being updated and the appropriate`SELECT`and`ALL`policies will be combined \(using OR for any overlapping`SELECT`related policies found\) with the`USING`clause of the`DELETE`policy using AND. Therefore, in order for a user to be able to`DELETE`specific rows, the user must have access to the row\(s\) through a`SELECT`or`ALL`policy and the row\(s\) must pass the`DELETE`policy's`USING`expression.

A`DELETE`policy cannot have a`WITH CHECK`expression, as it only applies in cases where records are being deleted from the relation, so that there is no new row to check.

## Notes

You must be the owner of a table to create or change policies for it.

While policies will be applied for explicit queries against tables in the database, they are not applied when the system is performing internal referential integrity checks or validating constraints. This means there are indirect ways to determine that a given value exists. An example of this is attempting to insert a duplicate value into a column that is a primary key or has a unique constraint. If the insert fails then the user can infer that the value already exists. \(This example assumes that the user is permitted by policy to insert records which they are not allowed to see.\) Another example is where a user is allowed to insert into a table which references another, otherwise hidden table. Existence can be determined by the user inserting values into the referencing table, where success would indicate that the value exists in the referenced table. These issues can be addressed by carefully crafting policies to prevent users from being able to insert, delete, or update records at all which might possibly indicate a value they are not otherwise able to see, or by using generated values \(e.g., surrogate keys\) instead of keys with external meanings.

Note that there needs to be at least one permissive policy to grant access to records before restrictive policies can be usefully used to reduce that access. If only restrictive policies exist, then no records will be accessible. When a mix of permissive and restrictive policies are present, a record is only accessible if at least one of the permissive policies passes, in addition to all the restrictive policies.

Generally, the system will enforce filter conditions imposed using security policies prior to qualifications that appear in user queries, in order to prevent inadvertent exposure of the protected data to user-defined functions which might not be trustworthy. However, functions and operators marked by the system \(or the system administrator\) as`LEAKPROOF`may be evaluated before policy expressions, as they are assumed to be trustworthy.

Since policy expressions are added to the user's query directly, they will be run with the rights of the user running the overall query. Therefore, users who are using a given policy must be able to access any tables or functions referenced in the expression or they will simply receive a permission denied error when attempting to query the table that has row-level security enabled. This does not change how views work, however. As with normal queries and views, permission checks and policies for the tables which are referenced by a view will use the view owner's rights and any policies which apply to the view owner.

Additional discussion and practical examples can be found in[Section 5.7](https://www.postgresql.org/docs/devel/static/ddl-rowsecurity.html).

## Compatibility

`CREATE POLICY`is aPostgreSQLextension.

## See Also

[ALTER POLICY](https://www.postgresql.org/docs/devel/static/sql-alterpolicy.html)

,

[DROP POLICY](https://www.postgresql.org/docs/devel/static/sql-droppolicy.html)

,

[ALTER TABLE](https://www.postgresql.org/docs/devel/static/sql-altertable.html)

---



[^1]:  [PostgreSQL: Documentation: devel: CREATE POLICY](https://www.postgresql.org/docs/devel/static/sql-createpolicy.html)

