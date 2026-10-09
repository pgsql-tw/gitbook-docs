<a id="SQL-ALTERROLE"></a><a id="id-1.9.3.26.1"></a>

## ALTER ROLE

ALTER ROLE — 變更資料庫角色

<a id="id-1.9.3.26.4"></a>

## 語法

```

ALTER ROLE role_specification [ WITH ] option [ ... ]

where option can be:

      SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT connlimit
    | [ ENCRYPTED ] PASSWORD 'password' | PASSWORD NULL
    | VALID UNTIL 'timestamp'

ALTER ROLE name RENAME TO new_name

ALTER ROLE { role_specification | ALL } [ IN DATABASE database_name ] SET configuration_parameter { TO | = } { value | DEFAULT }
ALTER ROLE { role_specification | ALL } [ IN DATABASE database_name ] SET configuration_parameter FROM CURRENT
ALTER ROLE { role_specification | ALL } [ IN DATABASE database_name ] RESET configuration_parameter
ALTER ROLE { role_specification | ALL } [ IN DATABASE database_name ] RESET ALL

where role_specification can be:

    role_name
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER
```

<a id="SQL-ALTERROLE-DESC"></a>

## 說明

`ALTER ROLE` 會變更 PostgreSQL 角色的屬性。

語法中列出的此命令第一種變體，可以變更許多可在 [`CREATE ROLE`](sql-createrole.md) 中指定的角色屬性。（所有可能的屬性都涵蓋在內，只是沒有新增或移除成員資格的選項；這方面請使用 [`GRANT`](sql-grant.md) 與 [`REVOKE`](sql-revoke.md)。）命令中未提及的屬性會保留先前的設定。資料庫超級使用者可以為任何角色變更這些設定中的任何一項，但不能變更[*[引導超級使用者（bootstrap superuser）](../../appendixes/glossary/README.md#GLOSSARY-BOOTSTRAP-SUPERUSER)*](../../appendixes/glossary/README.md#GLOSSARY-BOOTSTRAP-SUPERUSER)的 `SUPERUSER` 屬性。具有 `CREATEROLE` 權限的非超級使用者角色可以變更這些屬性中的大部分，但只限於其已被授予 `ADMIN OPTION` 的非超級使用者且非複寫角色。非超級使用者不能變更 `SUPERUSER` 屬性；而只有在自己擁有對應的屬性時，才能變更 `CREATEDB`、`REPLICATION` 與 `BYPASSRLS` 屬性。一般角色只能變更自己的密碼。

第二種變體會變更角色的名稱。資料庫超級使用者可以重新命名任何角色。具有 `CREATEROLE` 權限的角色，可以重新命名其已被授予 `ADMIN OPTION` 的非超級使用者角色。目前的工作階段使用者無法被重新命名。（若需要這麼做，請以另一個使用者身分連線。）由於以 `MD5` 加密的密碼使用角色名稱作為加密用的 salt，若密碼是以 `MD5` 加密的，重新命名角色會清除其密碼。

其餘的變體會變更角色對某個組態變數的工作階段預設值，可以套用到所有資料庫，或在指定 `IN
DATABASE` 子句時，只套用到指定資料庫中的工作階段。若指定 `ALL` 而非角色名稱，則會變更所有角色的設定。將 `ALL` 與 `IN DATABASE` 一起使用，實際上等同於使用命令 `ALTER DATABASE ... SET ...`。

之後每當該角色啟動新的工作階段時，指定的值就會成為工作階段的預設值，覆寫 `postgresql.conf` 中的任何設定，或從 `postgres` 命令列接收到的設定。這只會在登入時發生；執行 [`SET ROLE`](sql-set-role.md) 或 [`SET SESSION AUTHORIZATION`](sql-set-session-authorization.md) 不會使新的組態值被設定。為所有資料庫設定的值，會被附加在角色上的資料庫專屬設定覆寫。針對特定資料庫或特定角色的設定，會覆寫針對所有角色的設定。

超級使用者可以變更任何人的工作階段預設值。具有 `CREATEROLE` 權限的角色，可以變更其已被授予 `ADMIN OPTION` 之非超級使用者角色的預設值。一般角色只能為自己設定預設值。某些組態變數無法以這種方式設定，或只有在由超級使用者發出命令時才能設定。只有超級使用者可以變更所有資料庫中所有角色的設定。

<a id="SQL-ALTERROLE-PARAMS"></a>

## 參數

<a id="SQL-ALTERROLE-PARAMS-NAME"></a>

*`name`* [#](#SQL-ALTERROLE-PARAMS-NAME)
:   要變更其屬性之角色的名稱。
<a id="SQL-ALTERROLE-PARAMS-CURRENT-ROLE"></a>

`CURRENT_ROLE`<br>`CURRENT_USER` [#](#SQL-ALTERROLE-PARAMS-CURRENT-ROLE)
:   變更目前使用者，而不是明確指定的角色。
<a id="SQL-ALTERROLE-PARAMS-SESSION-USER"></a>

`SESSION_USER` [#](#SQL-ALTERROLE-PARAMS-SESSION-USER)
:   變更目前的工作階段使用者，而不是明確指定的角色。
<a id="SQL-ALTERROLE-PARAMS-SUPERUSER"></a>

`SUPERUSER`<br>`NOSUPERUSER`<br>`CREATEDB`<br>`NOCREATEDB`<br>`CREATEROLE`<br>`NOCREATEROLE`<br>`INHERIT`<br>`NOINHERIT`<br>`LOGIN`<br>`NOLOGIN`<br>`REPLICATION`<br>`NOREPLICATION`<br>`BYPASSRLS`<br>`NOBYPASSRLS`<br>`CONNECTION LIMIT` *`connlimit`*<br>[ `ENCRYPTED` ] `PASSWORD` '*`password`*'<br>`PASSWORD NULL`<br>`VALID UNTIL` '*`timestamp`*' [#](#SQL-ALTERROLE-PARAMS-SUPERUSER)
:   這些子句會變更原先由 [`CREATE ROLE`](sql-createrole.md) 設定的屬性。更多資訊請參閱 `CREATE ROLE` 參考頁面。
<a id="SQL-ALTERROLE-PARAMS-NEW-NAME"></a>

*`new_name`* [#](#SQL-ALTERROLE-PARAMS-NEW-NAME)
:   角色的新名稱。
<a id="SQL-ALTERROLE-PARAMS-DATABASE-NAME"></a>

*`database_name`* [#](#SQL-ALTERROLE-PARAMS-DATABASE-NAME)
:   要在其中設定組態變數之資料庫的名稱。
<a id="SQL-ALTERROLE-PARAMS-CONFIGURATION-PARAMETER"></a>

*`configuration_parameter`*<br>*`value`* [#](#SQL-ALTERROLE-PARAMS-CONFIGURATION-PARAMETER)
:   將此角色中指定組態參數的工作階段預設值設為給定的值。若 *`value`* 為 `DEFAULT`，或等效地使用 `RESET`，則會移除角色專屬的變數設定，該角色在新的工作階段中將繼承系統層級的預設設定。使用 `RESET ALL` 可清除所有角色專屬的設定。`SET FROM CURRENT` 會將該參數在工作階段中目前的值儲存為角色專屬的值。若指定了 `IN DATABASE`，則只會針對給定的角色與資料庫設定或移除該組態參數。

    角色專屬的變數設定只在登入時生效；[`SET ROLE`](sql-set-role.md) 與 [`SET SESSION AUTHORIZATION`](sql-set-session-authorization.md) 不會處理角色專屬的變數設定。

    關於允許的參數名稱與值的更多資訊，請參閱 [SET](sql-set.md) 與[第 19 章](../../server-administration/runtime-config/README.md)。

<a id="SQL-ALTERROLE-NOTES"></a>

## 注意事項

使用 [`CREATE ROLE`](sql-createrole.md) 新增角色，使用 [`DROP ROLE`](sql-droprole.md) 移除角色。

`ALTER ROLE` 無法變更角色的成員資格。這方面請使用 [`GRANT`](sql-grant.md) 與 [`REVOKE`](sql-revoke.md)。

以此命令指定未加密的密碼時必須小心。密碼會以明文傳送到伺服器，而且也可能被記錄在用戶端的命令歷史或伺服器日誌中。[psql](../reference-client/app-psql.md) 提供了 `\password` 命令，可用來變更角色的密碼而不暴露明文密碼。

也可以將工作階段預設值綁定到特定資料庫而非角色；請參閱 [ALTER DATABASE](sql-alterdatabase.md)。若有衝突，資料庫與角色專屬的設定會覆寫角色專屬的設定，而角色專屬的設定又會覆寫資料庫專屬的設定。

<a id="SQL-ALTERROLE-EXAMPLES"></a>

## 範例

變更角色的密碼：

```

ALTER ROLE davide WITH PASSWORD 'hu8jmn3';
```

移除角色的密碼：

```

ALTER ROLE davide WITH PASSWORD NULL;
```

變更密碼的到期日，指定密碼應該在 2015 年 5 月 4 日中午到期，並使用比 UTC 快一小時的時區：

```

ALTER ROLE chris VALID UNTIL 'May 4 12:00:00 2015 +1';
```

讓密碼永久有效：

```

ALTER ROLE fred VALID UNTIL 'infinity';
```

賦予角色管理其他角色及建立新資料庫的能力：

```

ALTER ROLE miriam CREATEROLE CREATEDB;
```

為角色設定 [maintenance_work_mem](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM) 參數的非預設值：

```

ALTER ROLE worker_bee SET maintenance_work_mem = 100000;
```

為角色設定 [client_min_messages](../../server-administration/runtime-config/runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) 參數的資料庫專屬非預設值：

```

ALTER ROLE fred IN DATABASE devel SET client_min_messages = DEBUG;
```

<a id="SQL-ALTERROLE-COMPAT"></a>

## 相容性

`ALTER ROLE` 陳述式是 PostgreSQL 的擴充語法。

<a id="SQL-ALTERROLE-SEE"></a>

## 另請參閱

[CREATE ROLE](sql-createrole.md), [DROP ROLE](sql-droprole.md), [ALTER DATABASE](sql-alterdatabase.md), [SET](sql-set.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterrole.html)（原文版本：18.6；核對日期：2026-10-05）
