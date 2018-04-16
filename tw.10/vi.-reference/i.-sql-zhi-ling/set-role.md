# SET ROLE

SET ROLE — set the current user identifier of the current session

## Synopsis

```text
SET [ SESSION | LOCAL ] ROLE 
role_name

SET [ SESSION | LOCAL ] ROLE NONE
RESET ROLE
```

## Description

This command sets the current user identifier of the current SQL session to be`role_name`. The role name can be written as either an identifier or a string literal. After`SET ROLE`, permissions checking for SQL commands is carried out as though the named role were the one that had logged in originally.

The specified\_`role_name`\_must be a role that the current session user is a member of. \(If the session user is a superuser, any role can be selected.\)

The`SESSION`and`LOCAL`modifiers act the same as for the regular[SET](https://www.postgresql.org/docs/10/static/sql-set.html)command.

The`NONE`and`RESET`forms reset the current user identifier to be the current session user identifier. These forms can be executed by any user.

## Notes

Using this command, it is possible to either add privileges or restrict one's privileges. If the session user role has the`INHERITS`attribute, then it automatically has all the privileges of every role that it could`SET ROLE`to; in this case`SET ROLE`effectively drops all the privileges assigned directly to the session user and to the other roles it is a member of, leaving only the privileges available to the named role. On the other hand, if the session user role has the`NOINHERITS`attribute,`SET ROLE`drops the privileges assigned directly to the session user and instead acquires the privileges available to the named role.

In particular, when a superuser chooses to`SET ROLE`to a non-superuser role, they lose their superuser privileges.

`SET ROLE`has effects comparable to[SET SESSION AUTHORIZATION](https://www.postgresql.org/docs/10/static/sql-set-session-authorization.html), but the privilege checks involved are quite different. Also,`SET SESSION AUTHORIZATION`determines which roles are allowable for later`SET ROLE`commands, whereas changing roles with`SET ROLE`does not change the set of roles allowed to a later`SET ROLE`.

`SET ROLE`does not process session variables as specified by the role's[ALTER ROLE](https://www.postgresql.org/docs/10/static/sql-alterrole.html)settings; this only happens during login.

`SET ROLE`cannot be used within a`SECURITY DEFINER`function.

## Examples

```text
SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user 
--------------+--------------
 peter        | peter

SET ROLE 'paul';

SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user 
--------------+--------------
 peter        | paul
```

## Compatibility

PostgreSQLallows identifier syntax \(`"rolename`"\), while the SQL standard requires the role name to be written as a string literal. SQL does not allow this command during a transaction;PostgreSQLdoes not make this restriction because there is no reason to. The`SESSION`and`LOCAL`modifiers are aPostgreSQLextension, as is the`RESET`syntax.

## See Also

[SET SESSION AUTHORIZATION](https://www.postgresql.org/docs/10/static/sql-set-session-authorization.html)

