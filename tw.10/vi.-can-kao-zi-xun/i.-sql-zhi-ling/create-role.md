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

`CREATE ROLE 將新的角色加到 PostgreSQL 資料庫叢集之中。角色是可以擁有資料庫物件並具有資料庫權限的實體；根據使用方式的不同，角色可以被視為「使用者」、「群組」或是兩者兼具。有關管理使用者和身份驗證的訊息，請參閱`[`第 21 章`](../../iii.-xi-tong-guan-li/21.-zi-liao-ku-jiao-se/)`和`[`第 20 章`](../../iii.-xi-tong-guan-li/20.-shi-yong-zhe-ren-zheng/)`。 您必須具有 CREATEROLE 權限或成為資料庫的超級使用者才能使用此命令。`

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

### 注意

使用 [ALTER ROLE](alter-role.md) 變更改角色的屬性，使用 [DROP ROLE](drop-role.md) 刪除角色。所有由CREATE ROLE 指定的屬性都可以在後面的 ALTER ROLE 命令中修改。

從群組加入和移出角色成員的首選方法是使用 [GRANT](grant.md) 和 [REVOKE](revoke.md)。

VALID UNTIL 子句僅定義密碼的到期時間，而不是角色本身。特別要注意的是，使用基於非密碼的身份驗證方法登錄時，不會強制實施到期的時間。

INHERIT 屬性管理可授予權限的繼承（即資料庫物件和角色成員的存取權限）。它不適用於由 CREATE ROLE 和 ALTER ROLE 設定的特殊角色屬性。例如，即使設定了INHERIT，作為 CREATEDB 權限角色的成員也不會立即授予建立資料庫的能力；在建立資料庫之前，有必要通過 SET ROLE 來扮演這個角色。

出於相容性的原因，INHERIT 屬性是預設屬性：在 PostgreSQL 的以前版本中，使用者總是可以存取它們所屬的群組的所有特權。但是，NOINHERIT 提供了與 SQL 標準中指定的語義更接近的設定。

請小心使用 CREATEROLE 權限。對於 CREATEROLE 角色的權限並沒有繼承的概念。這意味著即使角色沒有特定的權限但允許建立其他角色，也可以使用不同於自己的權限輕鬆建立另一個角色（除了使用超級使用者權限建立角色）。例如，如果角色「使用者」具有 CREATEROLE 權限但不具有 CREATEDB 權限，但它可以使用 CREATEDB 權限建立新角色。 因此，將具有 CREATEROLE 權限的角色視為幾乎是超級使用者的角色。

PostgreSQL 包含一個工具 [createuser](../ii.-postgresql-yong-hu-duan-gong-ju/createuser.md)，它具有與 CREATE ROLE 相同的功能（實際上，它也使用此命令），但可以從命令列終端機中執行。

CONNECTION LIMIT 選項只是大略地執行；如果兩個新的連線幾乎同時啟動，但只剩下連線留給該角色的話，也可能兩個都失敗。 此外，此限制不會限制超級使用者。

使用此命令指定未加密的密碼時必須謹慎行事。密碼將以明文形式傳輸到伺服器，並且還可能會記錄在用戶端的命令歷史記錄或伺服器日誌中。但是，[createuser](../ii.-postgresql-yong-hu-duan-gong-ju/createuser.md) 指令會傳輸加密的密碼。此外，[psql](../ii.-postgresql-yong-hu-duan-gong-ju/psql.md) 還包含一個命令 \password，可用於安全地更改密碼。

### 範例

建立一個可以登入的角色，但不要給它一個密碼：

```text
CREATE ROLE jonathan LOGIN;
```

建立角色同時設定一個密碼：

```text
CREATE USER davide WITH PASSWORD 'jw8s0F4';
```

（CREATE USER 與 CREATE ROLE 相同，但它暗示著 LOGIN。）

使用一個有效的密碼建立一個角色，直到 2004 年底。在 2005 年的第一秒之後，密碼就不再有效。

```text
CREATE ROLE miriam WITH LOGIN PASSWORD 'jw8s0F4' VALID UNTIL '2005-01-01';
```

建立一個可以建立資料庫和管理角色的角色：

```text
CREATE ROLE admin WITH CREATEDB CREATEROLE;
```

### 相容性

CREATE ROLE 語句在 SQL 標準中，只有簡單的語法標準。

```text
CREATE ROLE name [ WITH ADMIN role_name ]
```

多個初始管理員和 CREATE ROLE 的所有其他選項都是 PostgreSQL 延伸功能。

SQL 標準定義了使用者和角色的概念，且將它們視為不同的概念，並將所有定義使用者的命令留在每個資料庫的實作中。在 PostgreSQL 中，我們選擇將使用者和角色統一為單一類型的實體。因此，角色擁有比標準更多的可選屬性。

由 SQL 標準指定的行為最接近於給予使用者 NOINHERIT 屬性，而角色則賦予了 INHERIT 屬性。

### 參閱

[SET ROLE](set-role.md), [ALTER ROLE](alter-role.md), [DROP ROLE](drop-role.md), [GRANT](grant.md), [REVOKE](revoke.md), [createuser](../ii.-postgresql-yong-hu-duan-gong-ju/createuser.md)

