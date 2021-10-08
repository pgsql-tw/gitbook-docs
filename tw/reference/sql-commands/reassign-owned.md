# REASSIGN OWNED

REASSIGN OWNED — change the ownership of database objects owned by a database role

## Synopsis

```text
REASSIGN OWNED BY { old_role | CURRENT_USER | SESSION_USER } [, ...]
               TO { new_role | CURRENT_USER | SESSION_USER }
```

## Description

`REASSIGN OWNED` instructs the system to change the ownership of database objects owned by any of the _`old_roles`_ to _`new_role`_.

## Parameters

_`old_role`_

The name of a role. The ownership of all the objects within the current database, and of all shared objects \(databases, tablespaces\), owned by this role will be reassigned to _`new_role`_._`new_role`_

The name of the role that will be made the new owner of the affected objects.

## Notes

`REASSIGN OWNED` is often used to prepare for the removal of one or more roles. Because `REASSIGN OWNED` does not affect objects within other databases, it is usually necessary to execute this command in each database that contains objects owned by a role that is to be removed.

`REASSIGN OWNED` requires privileges on both the source role\(s\) and the target role.

The [DROP OWNED](https://www.postgresql.org/docs/10/static/sql-drop-owned.html) command is an alternative that simply drops all the database objects owned by one or more roles.

The `REASSIGN OWNED` command does not affect any privileges granted to the _`old_roles`_ for objects that are not owned by them. Use `DROP OWNED` to revoke such privileges.

See [Section 21.4](https://www.postgresql.org/docs/10/static/role-removal.html) for more discussion.

## Compatibility

The `REASSIGN OWNED` command is a PostgreSQL extension.

## See Also

[DROP OWNED](https://www.postgresql.org/docs/10/static/sql-drop-owned.html), [DROP ROLE](https://www.postgresql.org/docs/10/static/sql-droprole.html), [ALTER DATABASE](https://www.postgresql.org/docs/10/static/sql-alterdatabase.html)

