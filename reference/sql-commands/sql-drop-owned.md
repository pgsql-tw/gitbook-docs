<a id="id-1.9.3.122.1"></a>

## DROP OWNED

DROP OWNED — remove database objects owned by a database role

## Synopsis

```

DROP OWNED BY { name | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.122.5"></a>

## Description

`DROP OWNED` drops all the objects within the current
database that are owned by one of the specified roles. Any
privileges granted to the given roles on objects in the current
database or on shared objects (databases, tablespaces, configuration
parameters) will also be revoked.

<a id="id-1.9.3.122.6"></a>

## Parameters

*`name`*
:   The name of a role whose objects will be dropped, and whose
    privileges will be revoked.

`CASCADE`
:   Automatically drop objects that depend on the affected objects,
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the objects owned by a role if any other database
    objects depend on one of the affected objects. This is the default.

<a id="id-1.9.3.122.7"></a>

## Notes

`DROP OWNED` is often used to prepare for the
removal of one or more roles. Because `DROP OWNED`
only affects the objects in the current database, it is usually
necessary to execute this command in each database that contains
objects owned by a role that is to be removed.

Using the `CASCADE` option might make the command
recurse to objects owned by other users.

The [`REASSIGN OWNED`](sql-reassign-owned.md) command is an alternative that
reassigns the ownership of all the database objects owned by one or
more roles. However, `REASSIGN OWNED` does not deal with
privileges for other objects.

Databases and tablespaces owned by the role(s) will not be removed.

See [Section 21.4](../../server-administration/user-manag/role-removal.md) for more discussion.

<a id="id-1.9.3.122.8"></a>

## Compatibility

The `DROP OWNED` command is a
PostgreSQL extension.

<a id="id-1.9.3.122.9"></a>

## See Also

[REASSIGN OWNED](sql-reassign-owned.md), [DROP ROLE](sql-droprole.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-drop-owned.html)（英文原文，待翻譯）
