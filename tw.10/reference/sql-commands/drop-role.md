# DROP ROLE

DROP ROLE — remove a database role

### Synopsis

```text
DROP ROLE [ IF EXISTS ] name [, ...]
```

### Description

`DROP ROLE` removes the specified role\(s\). To drop a superuser role, you must be a superuser yourself; to drop non-superuser roles, you must have `CREATEROLE` privilege.

A role cannot be removed if it is still referenced in any database of the cluster; an error will be raised if so. Before dropping the role, you must drop all the objects it owns \(or reassign their ownership\) and revoke any privileges the role has been granted on other objects. The [REASSIGN OWNED](https://www.postgresql.org/docs/10/static/sql-reassign-owned.html) and [DROP OWNED](https://www.postgresql.org/docs/10/static/sql-drop-owned.html) commands can be useful for this purpose; see [Section 21.4](https://www.postgresql.org/docs/10/static/role-removal.html) for more discussion.

However, it is not necessary to remove role memberships involving the role; `DROP ROLE` automatically revokes any memberships of the target role in other roles, and of other roles in the target role. The other roles are not dropped nor otherwise affected.

### Parameters

`IF EXISTS`

Do not throw an error if the role does not exist. A notice is issued in this case._`name`_

The name of the role to remove.

### Notes

PostgreSQL includes a program [dropuser](https://www.postgresql.org/docs/10/static/app-dropuser.html) that has the same functionality as this command \(in fact, it calls this command\) but can be run from the command shell.

### Examples

To drop a role:

```text
DROP ROLE jonathan;
```

### Compatibility

The SQL standard defines `DROP ROLE`, but it allows only one role to be dropped at a time, and it specifies different privilege requirements than PostgreSQL uses.

### See Also

[CREATE ROLE](https://www.postgresql.org/docs/10/static/sql-createrole.html), [ALTER ROLE](https://www.postgresql.org/docs/10/static/sql-alterrole.html), [SET ROLE](https://www.postgresql.org/docs/10/static/sql-set-role.html)

