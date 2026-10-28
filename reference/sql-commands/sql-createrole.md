<a id="SQL-CREATEROLE"></a><a id="id-1.9.3.78.1"></a>

## CREATE ROLE

CREATE ROLE — 定義新的資料庫角色

<a id="id-1.9.3.78.4"></a>

## 語法

```

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
    | [ ENCRYPTED ] PASSWORD 'password' | PASSWORD NULL
    | VALID UNTIL 'timestamp'
    | IN ROLE role_name [, ...]
    | ROLE role_name [, ...]
    | ADMIN role_name [, ...]
    | SYSID uid
```

<a id="id-1.9.3.78.5"></a>

## 說明

`CREATE ROLE` 會在 PostgreSQL 資料庫叢集中新增一個角色。角色是一種可以擁有資料庫物件並具有資料庫權限的實體；依使用方式而定，角色可以被視為「使用者」、「群組」，或兩者皆是。關於管理使用者與身分驗證的資訊，請參閱[第 21 章](../../server-administration/user-manag/README.md)與[第 20 章](../../server-administration/client-authentication/README.md)。你必須具有 `CREATEROLE` 權限或是資料庫超級使用者，才能使用此命令。

請注意，角色是在資料庫叢集層級定義的，因此在叢集中的所有資料庫內皆有效。

建立角色時，可以立即將新建立的角色指派為某個現有角色的成員，也可以將現有角色指派為新建立角色的成員。初始角色成員資格會啟用哪些選項的規則，在下文的 `IN ROLE`、`ROLE` 與 `ADMIN` 子句中說明。[GRANT](sql-grant.md) 命令在建立成員資格時可以細部控制各選項，並且能在新角色建立之後修改這些選項。

<a id="id-1.9.3.78.6"></a>

## 參數

*`name`*
:   新角色的名稱。

`SUPERUSER`<br>`NOSUPERUSER`
:   這些子句決定新角色是否為「超級使用者」，超級使用者可以覆寫資料庫內的所有存取限制。超級使用者身分具有危險性，應該只在真正需要時使用。你自己必須是超級使用者，才能建立新的超級使用者。若未指定，預設為 `NOSUPERUSER`。

`CREATEDB`<br>`NOCREATEDB`
:   這些子句定義角色建立資料庫的能力。若指定 `CREATEDB`，所定義的角色將被允許建立新的資料庫。指定 `NOCREATEDB` 則會拒絕角色建立資料庫的能力。若未指定，預設為 `NOCREATEDB`。只有超級使用者角色或具有 `CREATEDB` 的角色可以指定 `CREATEDB`。

`CREATEROLE`<br>`NOCREATEROLE`
:   這些子句決定角色是否被允許建立、修改、移除其他角色，為其他角色加上註解，以及變更其他角色的安全標籤。關於此權限所賦予之能力的更多細節，請參閱[角色建立](../../server-administration/user-manag/role-attributes.md#ROLE-CREATION)。若未指定，預設為 `NOCREATEROLE`。

`INHERIT`<br>`NOINHERIT`

這會影響此角色被加入為另一個角色之成員時的成員資格繼承狀態，包括在本命令與日後的命令中。具體而言，它控制以本命令的 `IN ROLE` 子句所加入之成員資格，以及在之後的命令中以 `ROLE` 子句所加入之成員資格的繼承狀態。使用 `GRANT` 命令將此角色加入為成員時，它也會被當作預設的繼承狀態。若未指定，預設為 `INHERIT`。

在 PostgreSQL 16 之前的版本中，繼承是角色層級的屬性，控制該角色在執行期間的所有成員資格檢查。

`LOGIN`<br>`NOLOGIN`
:   這些子句決定角色是否被允許登入；也就是說，該角色是否可以在用戶端連線時作為初始的工作階段授權名稱。具有 `LOGIN` 屬性的角色可以被視為使用者。沒有此屬性的角色可用於管理資料庫權限，但並非一般意義上的使用者。若未指定，預設為 `NOLOGIN`，但透過其替代寫法 [`CREATE USER`](sql-createuser.md) 呼叫 `CREATE ROLE` 時除外。

`REPLICATION`<br>`NOREPLICATION`
:   這些子句決定角色是否為複寫角色。角色必須具有此屬性（或是超級使用者），才能以複寫模式（實體或邏輯複寫）連線到伺服器，以及建立或移除複寫插槽。具有 `REPLICATION` 屬性的角色是權限非常高的角色，應該只用在實際用於複寫的角色上。若未指定，預設為 `NOREPLICATION`。只有超級使用者角色或具有 `REPLICATION` 的角色可以指定 `REPLICATION`。

`BYPASSRLS`<br>`NOBYPASSRLS`

這些子句決定角色是否略過所有資料列層級安全性（RLS）政策。預設為 `NOBYPASSRLS`。只有超級使用者角色或具有 `BYPASSRLS` 的角色可以指定 `BYPASSRLS`。

請注意，pg_dump 預設會將 `row_security` 設為 `OFF`，以確保資料表的所有內容都被傾印出來。若執行 pg_dump 的使用者沒有適當的權限，將會傳回錯誤。不過，超級使用者與被傾印之資料表的擁有者一律會略過 RLS。

`CONNECTION LIMIT` *`connlimit`*
:   若角色可以登入，此選項指定該角色可以建立多少個並行連線。-1（預設值）表示沒有限制。請注意，只有一般連線會計入此限制。此限制既不計入預備交易，也不計入背景工作程序連線。

[ `ENCRYPTED` ] `PASSWORD` '*`password`*'<br>`PASSWORD NULL`
:   設定角色的密碼。（密碼只對具有 `LOGIN` 屬性的角色有用，但你仍然可以為沒有此屬性的角色定義密碼。）若你不打算使用密碼身分驗證，可以省略此選項。若未指定密碼，密碼將被設為 null，且該使用者的密碼身分驗證一律會失敗。null 密碼也可以選擇明確寫成 `PASSWORD NULL`。

    <a id="id-1.9.3.78.6.2.10.2.2"></a>

    ### 注意

    指定空字串也會將密碼設為 null，但在 PostgreSQL 10 版之前並非如此。在較早的版本中，依身分驗證方法與確切版本而定，空字串可能可以使用，也可能不行，而且 libpq 在任何情況下都會拒絕使用它。為了避免歧義，應該避免指定空字串。

    密碼一律以加密形式儲存在系統目錄中。`ENCRYPTED` 關鍵字沒有作用，但為了向後相容性而仍被接受。加密方法由設定參數 [password_encryption](../../server-administration/runtime-config/runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION) 決定。若提供的密碼字串已經是 MD5 加密或 SCRAM 加密格式，則不論 `password_encryption` 為何，都會原樣儲存（因為系統無法解密所指定的已加密密碼字串，也就無法將它以不同格式加密）。這使得在傾印／還原期間可以重新載入已加密的密碼。

    <a id="id-1.9.3.78.6.2.10.2.4"></a>

    ### 警告

    對 MD5 加密密碼的支援已被棄用，並將在 PostgreSQL 的未來版本中移除。關於遷移到其他密碼類型的細節，請參閱[第 20.5 節](../../server-administration/client-authentication/auth-password.md)。

`VALID UNTIL` '*`timestamp`*'
:   `VALID UNTIL` 子句設定一個日期與時間，在此之後角色的密碼便不再有效。若省略此子句，密碼將永久有效。

`IN ROLE` *`role_name`*
:   `IN ROLE` 子句使新角色自動被加入為所指定之現有角色的成員。新的成員資格將啟用 `SET` 選項，並停用 `ADMIN` 選項。除非指定了 `NOINHERIT` 選項，否則將啟用 `INHERIT` 選項。

`ROLE` *`role_name`*
:   `ROLE` 子句使一個或多個所指定的現有角色自動被加入為成員，並啟用 `SET` 選項。這實際上使新角色成為一個「群組」。在此子句中列出、且具有角色層級 `INHERIT` 屬性的角色，其新的成員資格將啟用 `INHERIT` 選項。新的成員資格將停用 `ADMIN` 選項。

`ADMIN` *`role_name`*
:   `ADMIN` 子句的效果與 `ROLE` 相同，但所列出的角色會在啟用 `ADMIN` 的情況下被加入為新角色的成員，使它們有權將新角色的成員資格授予他人。

`SYSID` *`uid`*
:   `SYSID` 子句會被忽略，但為了向後相容性而仍被接受。

<a id="id-1.9.3.78.7"></a>

## 注意事項

使用 [`ALTER ROLE`](sql-alterrole.md) 變更角色的屬性，使用 [`DROP ROLE`](sql-droprole.md) 移除角色。由 `CREATE ROLE` 指定的所有屬性，都可以在之後以 `ALTER ROLE` 命令修改。

對於當作群組使用的角色，新增與移除其成員的建議方式是使用 [`GRANT`](sql-grant.md) 與 [`REVOKE`](sql-revoke.md)。

`VALID UNTIL` 子句只為密碼定義到期時間，而不是為角色本身定義。特別是，使用非密碼型的身分驗證方法登入時，不會強制套用此到期時間。

此處定義的角色屬性是不可繼承的；也就是說，成為具有例如 `CREATEDB` 之角色的成員，並不會允許該成員建立新的資料庫，即使該成員資格授予具有 `INHERIT` 選項也一樣。當然，若成員資格授予具有 `SET` 選項，成員角色就能夠以 [`SET ROLE`](sql-set-role.md) 切換為該 createdb 角色，然後建立新的資料庫。

由 `IN ROLE`、`ROLE` 與 `ADMIN` 子句建立的成員資格授予，會以執行此命令的角色作為授予者。

`INHERIT` 屬性之所以是預設值，是出於向後相容性的考量：在 PostgreSQL 先前的版本中，使用者一律可以存取其所屬群組的所有權限。不過，`NOINHERIT` 更貼近 SQL 標準所規定的語意。

PostgreSQL 提供一個程式 [createuser](../reference-client/app-createuser.md)，其功能與 `CREATE ROLE` 相同（事實上，它會呼叫此命令），但可以從命令 shell 執行。

`CONNECTION LIMIT` 選項只會大約地強制執行；若在角色只剩一個連線「插槽」時，有兩個新的工作階段約在同一時間啟動，兩者可能都會失敗。此外，此限制永遠不會對超級使用者強制執行。

以此命令指定未加密的密碼時必須謹慎。密碼將以明文傳送到伺服器，而且也可能被記錄在用戶端的命令歷史或伺服器日誌中。不過，[createuser](../reference-client/app-createuser.md) 命令會以加密形式傳送密碼。此外，[psql](../reference-client/app-psql.md) 包含一個 `\password` 命令，可用於之後安全地變更密碼。

<a id="id-1.9.3.78.8"></a>

## 範例

建立一個可以登入、但不給予密碼的角色：

```

CREATE ROLE jonathan LOGIN;
```

建立一個具有密碼的角色：

```

CREATE USER davide WITH PASSWORD 'jw8s0F4';
```

（`CREATE USER` 與 `CREATE ROLE` 相同，只是它隱含 `LOGIN`。）

建立一個具有密碼的角色，該密碼的有效期限到 2004 年底為止。進入 2005 年的第一秒之後，該密碼便不再有效。

```

CREATE ROLE miriam WITH LOGIN PASSWORD 'jw8s0F4' VALID UNTIL '2005-01-01';
```

建立一個可以建立資料庫並管理角色的角色：

```

CREATE ROLE admin WITH CREATEDB CREATEROLE;
```

<a id="id-1.9.3.78.9"></a>

## 相容性

`CREATE ROLE` 陳述式屬於 SQL 標準，但標準只要求以下語法

```

CREATE ROLE name [ WITH ADMIN role_name ]
```

多個初始管理者，以及 `CREATE ROLE` 的所有其他選項，都是 PostgreSQL 的擴充語法。

SQL 標準定義了使用者與角色的概念，但將兩者視為不同的概念，並將所有定義使用者的命令留給各資料庫實作自行規定。在 PostgreSQL 中，我們選擇將使用者與角色統一為單一種類的實體。因此，角色擁有的選用屬性比標準中的多得多。

要最接近 SQL 標準所規定的行為，做法是將 SQL 標準的使用者建立為具有 `NOINHERIT` 選項的 PostgreSQL 角色，並將 SQL 標準的角色建立為具有 `INHERIT` 選項的 PostgreSQL 角色。

`USER` 子句的行為與 `ROLE` 相同，但已被棄用：

```

USER role_name [, ...]
```

`IN GROUP` 子句的行為與 `IN ROLE` 相同，但已被棄用：

```

IN GROUP role_name [, ...]
```

<a id="id-1.9.3.78.10"></a>

## 另請參閱

[SET ROLE](sql-set-role.md), [ALTER ROLE](sql-alterrole.md), [DROP ROLE](sql-droprole.md), [GRANT](sql-grant.md), [REVOKE](sql-revoke.md), [createuser](../reference-client/app-createuser.md), [createrole_self_grant](../../server-administration/runtime-config/runtime-config-client.md#GUC-CREATEROLE-SELF-GRANT)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createrole.html)（原文版本：18.6；核對日期：2026-10-04）
