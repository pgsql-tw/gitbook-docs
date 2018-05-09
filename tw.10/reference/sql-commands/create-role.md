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

這個子句決定角色是否可以繞過每個資料列級安全（RLS）原則檢查。 NOBYPASSRLS 是預設值。請注意，預設情況下，pg\_dump 會將 row\_security 設定為 OFF，以確保資料表中的所有內容都被匯出。如果執行 pg\_dump 的使用者沒有適當的權限，則會回報錯誤。超級使用者和匯出資料表的擁有者總是能夠繞過 RLS。

`CONNECTION LIMIT` _`connlimit`_

如果角色可以登入，則指定該角色可以建立多少個同時連線。-1（預設值）表示沒有限制。請注意，只有正常連線才會計入此限制。預備交易和後端服務連線都不計入此限制。

\[ `ENCRYPTED` \] `PASSWORD` _`password`_

設定角色的密碼。（密碼僅用於具有 LOGIN 屬性的角色，但您可以為沒有密碼的角色定義密碼。）如果您不打算使用密碼驗證，則可以省略此選項。如果未指定密碼，則密碼將設定為 NULL，而該使用者的密碼驗證將始終失敗。可以選擇將空密碼明確寫為PASSWORD NULL。

#### 提醒

**指定一個空字串也會將密碼設定為 NULL，但 PostgreSQL 版本 10 之前並不是這種情況。在早期版本中，可以使用或不使用空字串，具體取決於身份驗證方法和確切版本，libpq 會拒絕在任何情況下使用它。為避免歧義，應避免指定空字串。**

密碼總是會以加密方式儲存在系統目錄中。ENCRYPTED 關鍵字不起作用，但為了相容性而被接受。加密方法由配置參數 password\_encryption 決定。如果提供的密碼字串已經以 MD5 加密或 SCRAM 加密的格式存在，則無論使用password\_encryption 為何（因為系統無法解密指定的加密密碼字符串，如果以不同的格式對其進行加密的話），它都會按原樣儲存。 這允許在轉存/恢復期間重新載入加密的密碼。

`VALID UNTIL` '_`timestamp`_'

VALID UNTIL 子句設定角色密碼不再有效的日期和時間。 如果省略此項，則密碼將始終有效。

`IN ROLE` _`role_name`_

IN ROLE 子句列出一個或多個新角色將立即添加為新成員的現有角色。（請注意，不能選擇以管理員身份增加新角色；請使用單獨的 GRANT 指令來執行此操作。）

`IN GROUP` _`role_name`_

`IN GROUP 是 IN ROLE 的過時選項。`

`ROLE` _`role_name`_

ROLE 子句列出了一個或多個自動增加為新角色成員的現有角色。 （這實際上使新角色成為「群組」。）

`ADMIN` _`role_name`_

ADMIN 子句與 ROLE 類似，但已命名的角色被新增到新角色 WITH ADMIN OPTION 中，賦予他們將此角色的成員身份授予其他人的權利。

`USER` _`role_name`_

USER 子句是 ROLE 子句的過時寫法。

`SYSID` _`uid`_

SYSID 子句會被忽略，但為了相容性而被接受。

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

