<a id="SQL-ALTERGROUP"></a><a id="id-1.9.3.15.1"></a>

# ALTER GROUP

ALTER GROUP — change role name or membership

## Synopsis

```

ALTER GROUP role_specification ADD USER user_name [, ... ]
ALTER GROUP role_specification DROP USER user_name [, ... ]

where role_specification can be:

    role_name
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER

ALTER GROUP group_name RENAME TO new_name
```

<a id="id-1.9.3.15.5"></a>

## Description

`ALTER GROUP` changes the attributes of a user group. This is an obsolete command, though still accepted for backwards compatibility, because groups (and users too) have been superseded by the more general concept of roles.

The first two variants add users to a group or remove them from a group. (Any role can play the part of either a “user” or a “group” for this purpose.) These variants are effectively equivalent to granting or revoking membership in the role named as the “group”; so the preferred way to do this is to use [`GRANT`](grant.md) or [`REVOKE`](revoke.md).

The third variant changes the name of the group. This is exactly equivalent to renaming the role with [`ALTER ROLE`](alter-role.md).

<a id="id-1.9.3.15.6"></a>

## Parameters

<em class="replaceable"><code>group&#95;name</code></em>

The name of the group (role) to modify.

<em class="replaceable"><code>user&#95;name</code></em>

Users (roles) that are to be added to or removed from the group. The users must already exist; `ALTER GROUP` does not create or drop users.

<em class="replaceable"><code>new&#95;name</code></em>

The new name of the group.

<a id="id-1.9.3.15.7"></a>

## Examples

Add users to a group:

```

ALTER GROUP staff ADD USER karl, john;
```

Remove a user from a group:

```

ALTER GROUP workers DROP USER beth;
```

<a id="id-1.9.3.15.8"></a>

## Compatibility

There is no `ALTER GROUP` statement in the SQL standard.

<a id="id-1.9.3.15.9"></a>

## See Also

[GRANT](grant.md), [REVOKE](revoke.md), [ALTER ROLE](alter-role.md)

---

原文：[PostgreSQL 15.19 Documentation](alter-group.md)（英文原文，待翻譯）
