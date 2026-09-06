<a id="id-1.9.3.161.1"></a>

## REASSIGN OWNED

REASSIGN OWNED — change the ownership of database objects owned by a database role

## Synopsis

```

REASSIGN OWNED BY { old_role | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...]
               TO { new_role | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

<a id="id-1.9.3.161.5"></a>

## Description

`REASSIGN OWNED` instructs the system to change
the ownership of database objects owned by any of the
*`old_roles`* to
*`new_role`*.

<a id="id-1.9.3.161.6"></a>

## Parameters

*`old_role`*
:   The name of a role. The ownership of all the objects within the
    current database, and of all shared objects (databases, tablespaces),
    owned by this role will be reassigned to
    *`new_role`*.

*`new_role`*
:   The name of the role that will be made the new owner of the
    affected objects.

<a id="id-1.9.3.161.7"></a>

## Notes

`REASSIGN OWNED` is often used to prepare for the
removal of one or more roles. Because `REASSIGN
OWNED` does not affect objects within other databases,
it is usually necessary to execute this command in each database
that contains objects owned by a role that is to be removed.

`REASSIGN OWNED` requires membership on both the
source role(s) and the target role.

The [`DROP OWNED`](sql-drop-owned.md) command is an alternative that
simply drops all the database objects owned by one or more roles.

The `REASSIGN OWNED` command does not affect any
privileges granted to
the *`old_roles`* on objects
that are not owned by them. Likewise, it does not affect default
privileges created with `ALTER DEFAULT PRIVILEGES`.
Use `DROP OWNED` to revoke such privileges.

See [Section 21.4](../../server-administration/user-manag/role-removal.md) for more discussion.

<a id="id-1.9.3.161.8"></a>

## Compatibility

The `REASSIGN OWNED` command is a
PostgreSQL extension.

<a id="id-1.9.3.161.9"></a>

## See Also

[DROP OWNED](sql-drop-owned.md), [DROP ROLE](sql-droprole.md), [ALTER DATABASE](sql-alterdatabase.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-reassign-owned.html)（英文原文，待翻譯）
