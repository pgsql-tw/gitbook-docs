<a id="id-1.9.3.126.1"></a>

## DROP ROLE

DROP ROLE — remove a database role

## Synopsis

```

DROP ROLE [ IF EXISTS ] name [, ...]
```

<a id="id-1.9.3.126.5"></a>

## Description

`DROP ROLE` removes the specified role(s).
To drop a superuser role, you must be a superuser yourself;
to drop non-superuser roles, you must have `CREATEROLE`
privilege and have been granted `ADMIN OPTION` on the role.

A role cannot be removed if it is still referenced in any database
of the cluster; an error will be raised if so. Before dropping the role,
you must drop all the objects it owns (or reassign their ownership)
and revoke any privileges the role has been granted on other objects.
The [`REASSIGN
OWNED`](sql-reassign-owned.md) and [`DROP
OWNED`](sql-drop-owned.md)
commands can be useful for this purpose; see [Section 21.4](../../server-administration/user-manag/role-removal.md)
for more discussion.

However, it is not necessary to remove role memberships involving
the role; `DROP ROLE` automatically revokes any memberships
of the target role in other roles, and of other roles in the target role.
The other roles are not dropped nor otherwise affected.

<a id="id-1.9.3.126.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the role does not exist. A notice is issued
    in this case.

*`name`*
:   The name of the role to remove.

<a id="id-1.9.3.126.7"></a>

## Notes

PostgreSQL includes a program [dropuser](../reference-client/app-dropuser.md) that has the
same functionality as this command (in fact, it calls this command)
but can be run from the command shell.

<a id="id-1.9.3.126.8"></a>

## Examples

To drop a role:

```

DROP ROLE jonathan;
```

<a id="id-1.9.3.126.9"></a>

## Compatibility

The SQL standard defines `DROP ROLE`, but it allows
only one role to be dropped at a time, and it specifies different
privilege requirements than PostgreSQL uses.

<a id="id-1.9.3.126.10"></a>

## See Also

[CREATE ROLE](sql-createrole.md), [ALTER ROLE](sql-alterrole.md), [SET ROLE](sql-set-role.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droprole.html)（英文原文，待翻譯）
