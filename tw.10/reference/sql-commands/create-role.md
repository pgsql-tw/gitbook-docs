# CREATE ROLE

CREATE ROLE — 定義一個新的資料庫角色

### 語法

```text
CREATE ROLE name [ [ WITH ] option [ ... ] ]

where option can be:

      SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT connlimit
    | [ ENCRYPTED ] PASSWORD 'password'
    | VALID UNTIL 'timestamp'
    | IN ROLE role_name [, ...]
    | IN GROUP role_name [, ...]
    | ROLE role_name [, ...]
    | ADMIN role_name [, ...]
    | USER role_name [, ...]
    | SYSID uid
```

### 說明

`CREATE ROLE 將新的角色加到 PostgreSQL 資料庫叢集之中。角色是可以擁有資料庫物件並具有資料庫權限的實體；根據使用方式的不同，角色可以被視為「使用者」、「群組」或是兩者兼具。有關管理使用者和身份驗證的訊息，請參閱`[`第 21 章`](../../server-administration/user-manag/)`和`[`第 20 章`](../../server-administration/20.-shi-yong-zhe-ren-zheng/)`。 您必須具有 CREATEROLE 權限或成為資料庫的超級使用者才能使用此命令。`

請注意，角色是在資料庫叢集等級所定義的，因此在叢集中的所有資料庫中都是有效的。

### 參數

_`name`_

新角色的名稱。

`SUPERUSER`  
`NOSUPERUSER`

這個子句決定新角色是否為「超級使用者」，他可以覆寫資料庫中的所有存取限制。超級使用者的狀態很危險，只能在真正需要時才使用。您必須自己成為超級使用者才能建立新的超級使用者。如果未指定，則 NOSUPERUSER 是預設值。

`CREATEDB`  
`NOCREATEDB`

這個子句定義了角色是否可以建立資料庫。如果指定了 CREATEDB，則被定義的角色將被允許建立新的資料庫。指定 NOCREATEDB 則是不允許建立資料庫的角色。如果未指定，則預設為 NOCREATEDB。

`CREATEROLE`  
`NOCREATEROLE`

這個子句決定是否允許角色建立新角色（即執行CREATE ROLE）。具有CREATEROLE 權限的角色也可以變更和刪除其他角色。如果未指定，則預設為 NOCREATEROLE。

`INHERIT`  
`NOINHERIT`

這個子句決定角色是否「繼承」它所屬角色的特權。具有 INHERIT 屬性的角色可以自動使用已授予其直接或間接成員的所有角色的任何資料庫特權。沒有INHERIT，另一個角色的成員資格只能賦予角色設定其他角色的能力；其他角色的權限僅在完成後才可用。如果未指定，INHERIT 是預設值。

`LOGIN`  
`NOLOGIN`

這個子句決定是否允許角色登入；也就是說，在用戶端連線期間，角色是否可以作為初始連線的授權名稱。具有 LOGIN 屬性的角色可以被認為是一個使用者。沒有此屬性的角色對於管理資料庫權限很有用，但不是一般認知上的使用者。如果未指定，則除了通過其替代指令 [CREATE USER](create-user.md) 使用 CREATE ROLE 時，NOLOGIN 是預設值。

`REPLICATION`  
`NOREPLICATION`

這個子句確定角色是否是可以進行複製工作的角色。角色必須具有此屬性（或成為超級使用者）才能以複製模式（實體或邏輯複製）連線到伺服器，並且能夠建立或刪除複製單元。具有 REPLICATION 屬性的角色是一個非常高權限的角色，只能用於實際用於複製工作的角色。 如果未指定，則預設為 NOREPLICATION。

`BYPASSRLS`  
`NOBYPASSRLS`

These clauses determine whether a role bypasses every row-level security \(RLS\) policy. `NOBYPASSRLS` is the default. Note that pg\_dump will set `row_security` to `OFF` by default, to ensure all contents of a table are dumped out. If the user running pg\_dump does not have appropriate permissions, an error will be returned. The superuser and owner of the table being dumped always bypass RLS.

`CONNECTION LIMIT` _`connlimit`_

If role can log in, this specifies how many concurrent connections the role can make. -1 \(the default\) means no limit. Note that only normal connections are counted towards this limit. Neither prepared transactions nor background worker connections are counted towards this limit.

\[ `ENCRYPTED` \] `PASSWORD` _`password`_

Sets the role's password. \(A password is only of use for roles having the `LOGIN` attribute, but you can nonetheless define one for roles without it.\) If you do not plan to use password authentication you can omit this option. If no password is specified, the password will be set to null and password authentication will always fail for that user. A null password can optionally be written explicitly as `PASSWORD NULL`.

#### Note

Specifying an empty string will also set the password to null, but that was not the case before PostgreSQL version 10. In earlier versions, an empty string could be used, or not, depending on the authentication method and the exact version, and libpq would refuse to use it in any case. To avoid the ambiguity, specifying an empty string should be avoided.

The password is always stored encrypted in the system catalogs. The `ENCRYPTED` keyword has no effect, but is accepted for backwards compatibility. The method of encryption is determined by the configuration parameter [password\_encryption](https://www.postgresql.org/docs/10/static/runtime-config-connection.html#GUC-PASSWORD-ENCRYPTION). If the presented password string is already in MD5-encrypted or SCRAM-encrypted format, then it is stored as-is regardless of `password_encryption` \(since the system cannot decrypt the specified encrypted password string, to encrypt it in a different format\). This allows reloading of encrypted passwords during dump/restore.

`VALID UNTIL` '_`timestamp`_'

The `VALID UNTIL` clause sets a date and time after which the role's password is no longer valid. If this clause is omitted the password will be valid for all time.

`IN ROLE` _`role_name`_

The `IN ROLE` clause lists one or more existing roles to which the new role will be immediately added as a new member. \(Note that there is no option to add the new role as an administrator; use a separate `GRANT` command to do that.\)

`IN GROUP` _`role_name`_

`IN GROUP` is an obsolete spelling of `IN ROLE`.

`ROLE` _`role_name`_

The `ROLE` clause lists one or more existing roles which are automatically added as members of the new role. \(This in effect makes the new role a “group”.\)

`ADMIN` _`role_name`_

The `ADMIN` clause is like `ROLE`, but the named roles are added to the new role `WITH ADMIN OPTION`, giving them the right to grant membership in this role to others.

`USER` _`role_name`_

The `USER` clause is an obsolete spelling of the `ROLE` clause.

`SYSID` _`uid`_

The `SYSID` clause is ignored, but is accepted for backwards compatibility.

### Notes

Use [ALTER ROLE](https://www.postgresql.org/docs/10/static/sql-alterrole.html) to change the attributes of a role, and [DROP ROLE](https://www.postgresql.org/docs/10/static/sql-droprole.html) to remove a role. All the attributes specified by `CREATE ROLE` can be modified by later `ALTER ROLE` commands.

The preferred way to add and remove members of roles that are being used as groups is to use [GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html) and [REVOKE](https://www.postgresql.org/docs/10/static/sql-revoke.html).

The `VALID UNTIL` clause defines an expiration time for a password only, not for the role _per se_. In particular, the expiration time is not enforced when logging in using a non-password-based authentication method.

The `INHERIT` attribute governs inheritance of grantable privileges \(that is, access privileges for database objects and role memberships\). It does not apply to the special role attributes set by `CREATE ROLE` and `ALTER ROLE`. For example, being a member of a role with `CREATEDB`privilege does not immediately grant the ability to create databases, even if `INHERIT` is set; it would be necessary to become that role via [SET ROLE](https://www.postgresql.org/docs/10/static/sql-set-role.html) before creating a database.

The `INHERIT` attribute is the default for reasons of backwards compatibility: in prior releases of PostgreSQL, users always had access to all privileges of groups they were members of. However, `NOINHERIT` provides a closer match to the semantics specified in the SQL standard.

Be careful with the `CREATEROLE` privilege. There is no concept of inheritance for the privileges of a `CREATEROLE`-role. That means that even if a role does not have a certain privilege but is allowed to create other roles, it can easily create another role with different privileges than its own \(except for creating roles with superuser privileges\). For example, if the role “user” has the `CREATEROLE` privilege but not the `CREATEDB` privilege, nonetheless it can create a new role with the `CREATEDB` privilege. Therefore, regard roles that have the `CREATEROLE` privilege as almost-superuser-roles.

PostgreSQL includes a program [createuser](https://www.postgresql.org/docs/10/static/app-createuser.html) that has the same functionality as `CREATE ROLE` \(in fact, it calls this command\) but can be run from the command shell.

The `CONNECTION LIMIT` option is only enforced approximately; if two new sessions start at about the same time when just one connection “slot” remains for the role, it is possible that both will fail. Also, the limit is never enforced for superusers.

Caution must be exercised when specifying an unencrypted password with this command. The password will be transmitted to the server in cleartext, and it might also be logged in the client's command history or the server log. The command [createuser](https://www.postgresql.org/docs/10/static/app-createuser.html), however, transmits the password encrypted. Also, [psql](https://www.postgresql.org/docs/10/static/app-psql.html) contains a command `\password` that can be used to safely change the password later.

### Examples

Create a role that can log in, but don't give it a password:

```text
CREATE ROLE jonathan LOGIN;
```

Create a role with a password:

```text
CREATE USER davide WITH PASSWORD 'jw8s0F4';
```

\(`CREATE USER` is the same as `CREATE ROLE` except that it implies `LOGIN`.\)

Create a role with a password that is valid until the end of 2004. After one second has ticked in 2005, the password is no longer valid.

```text
CREATE ROLE miriam WITH LOGIN PASSWORD 'jw8s0F4' VALID UNTIL '2005-01-01';
```

Create a role that can create databases and manage roles:

```text
CREATE ROLE admin WITH CREATEDB CREATEROLE;
```

### Compatibility

The `CREATE ROLE` statement is in the SQL standard, but the standard only requires the syntax

```text
CREATE ROLE name [ WITH ADMIN role_name ]
```

Multiple initial administrators, and all the other options of `CREATE ROLE`, are PostgreSQL extensions.

The SQL standard defines the concepts of users and roles, but it regards them as distinct concepts and leaves all commands defining users to be specified by each database implementation. In PostgreSQL we have chosen to unify users and roles into a single kind of entity. Roles therefore have many more optional attributes than they do in the standard.

The behavior specified by the SQL standard is most closely approximated by giving users the `NOINHERIT` attribute, while roles are given the `INHERIT` attribute.

### See Also

[SET ROLE](set-role.md), [ALTER ROLE](alter-role.md), [DROP ROLE](drop-role.md), [GRANT](grant.md), [REVOKE](revoke.md), [createuser](../client/createuser.md)

