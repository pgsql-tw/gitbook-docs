# ALTER ROLE

ALTER ROLE — 變更資料庫角色

### 語法

```text
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
  | CURRENT_USER
  | SESSION_USER
```

### 說明

ALTER ROLE 變更 PostgreSQL 角色的屬性。

語法中列出的此指令的第一種語法樣式可以變更可在 [CREATE ROLE](create-role.md) 中指定的許多角色屬性。（所有可能的屬性都會被覆寫，除了沒有增加或移除成員資格的選項之外，應使用 [GRANT](grant.md) 和 [REVOKE](revoke.md)。）指令中未提及的屬性保留其先前的設定。資料庫超級使用者可以變更任何角色的任何設定。具有 CREATEROLE 權限的角色可以變更任何的這些設定，但僅適用於非超級使用者和非複寫角色。普通角色只能變更自己的密碼。

第二種語法樣式用於變更角色的名稱。資料庫超級使用者可以重新命名任何角色。具有 CREATEROLE 權限的角色可以重新命名非超級使用者角色。無法重新命名目前連線使用者。（如果需要，請以其他使用者身份進行連線。）由於 MD5 加密的密碼使用角色名稱作為加密 salt，因此如果密碼是 MD5 加密的，則重新命名角色會重置其加密密碼。

其餘語法樣式則是變更組態變數的角色連線預設值，或者為所有資料庫更改，或者在指定 IN DATABASE 子句時，僅針對指定名稱資料庫中的連線。如果指定了 ALL 而不是角色名稱，則會變更所有角色的設定。使用 ALL 與 IN DATABASE 實際上與使用指令 ALTER DATABASE ... SET .... 相同。

每當角色隨後啟動一個新連線時，指定的值將成為連線預設值，覆寫 postgresql.conf 中存在的任何設定或已從 postgres 命令列接收。這只發生在登入時；執行 [SET ROLE](set-role.md) 或 [SET SESSION AUTHORIZATION](set-session-authorization.md) 不會設定新的組態值。為所有資料庫的設定將由附加到角色的特定於資料庫的設定覆寫。特定資料庫或特定角色的設定會覆寫所有角色的設定。

超級使用者可以變更任何人的連線預設值。具有 CREATEROLE 權限的角色可以變更非超級使用者角色的預設值。普通角色只能為自己設定預設值。某些組態變數不能以這種方式設定，或者只能在超級使用者發出命令時設定。只有超級使用者才能變更所有資料庫中所有角色的設定。

### 參數

_`name`_

要變更其屬性的角色名稱。

`CURRENT_USER`

變更目前使用者而不是指定的角色。

`SESSION_USER`

變更目前連線使用者而不是指定的角色。

 `SUPERUSER`  
`NOSUPERUSER`  
`CREATEDB`  
`NOCREATEDB`  
`CREATEROLE`  
`NOCREATEROLE`  
`INHERIT`  
`NOINHERIT`  
`LOGIN`  
`NOLOGIN`  
`REPLICATION`  
`NOREPLICATION`  
`BYPASSRLS`  
`NOBYPASSRLS`  
`CONNECTION LIMIT` _`connlimit`_  
\[ `ENCRYPTED` \] `PASSWORD` '_`password`_'  
`PASSWORD NULL`  
`VALID UNTIL` '_`timestamp`_'

這些子句變更 CREATE ROLE 最初設定的屬性。有關更多訊息，請參閱 [CREATE ROLE](create-role.md) 參考頁面。

_`new_name`_

角色的新名稱。

_`database_name`_

應在其中設定組態變數的資料庫名稱。

_`configuration_parameter`_  
_`value`_

將使指定組態參數覆寫此角色的連線預設值。如果 value 為 DEFAULT，或者等效地使用 RESET，則會移除特定於角色的組態參數，因此該角色將在新連線中繼承系統範圍的預設設定。使用 RESET ALL 清除所有特定於角色的設定。SET FROM CURRENT 將連線當下參數值保存為特定於角色的值。如果指定了 IN DATABASE，則僅為給定角色和資料庫設定或移除組態參數。

特定於角色的組態變數設定僅在登入時生效；[SET ROLE](set-role.md) 和 [SET SESSION AUTHORIZATION](set-session-authorization.md) 不處理特定於角色的組態變數設定。

有關可使用的參數名稱和內容的更多訊息，請參閱 [SET](set.md) 和[第 19 章](../../server-administration/server-configuration/)。

### 注意

使用 [CREATE ROLE](create-role.md) 增加新角色，使用 [DROP ROLE](drop-role.md) 移除角色。

ALTER ROLE 無法變更角色的成員資格。請使用 [GRANT](grant.md) 和 [REVOKE](revoke.md) 來做到這一點。

使用此指令指定未加密的密碼時必須小心。密碼將以明文形式傳輸到伺服器，也可能記錄在用戶端的指令歷史記錄或伺服器日誌中。psql 包含一個指令 \password，可用於變更角色的密碼而不暴露明文密碼。

也可以將連線預設值綁定到特定資料庫而不是角色；請參閱 ALTER DATABASE。 如果存在衝突，則特定於資料庫角色的設定會覆蓋特定於角色的設定，而這些設定又會覆蓋特定於資料庫的設定。

### 範例

變更角色的密碼：

```text
ALTER ROLE davide WITH PASSWORD 'hu8jmn3';
```

移除角色的密碼：

```text
ALTER ROLE davide WITH PASSWORD NULL;
```

變更密碼到期日期，指定密碼將於 2015 年 5 月 4 日中午到期，使用比 UTC 提前一小時的時區：

```text
ALTER ROLE chris VALID UNTIL 'May 4 12:00:00 2015 +1';
```

使密碼永久有效：

```text
ALTER ROLE fred VALID UNTIL 'infinity';
```

賦予角色建立其他角色和新資料庫的能力：

```text
ALTER ROLE miriam CREATEROLE CREATEDB;
```

讓某個角色的 [maintenance\_work\_mem](../../server-administration/server-configuration/resource-consumption.md#19-4-1) 參數使用非預設值：

```text
ALTER ROLE worker_bee SET maintenance_work_mem = 100000;
```

為 [client\_min\_messages ](../../server-administration/server-configuration/error-reporting-and-logging.md#client_min_messages-enum)參數指定一個非預設的，特定於某資料庫的設定：

```text
ALTER ROLE fred IN DATABASE devel SET client_min_messages = DEBUG;
```

### 相容性

ALTER ROLE 語句是 PostgreSQL 的延伸功能。

### 參閱

[CREATE ROLE](create-role.md), [DROP ROLE](drop-role.md), [ALTER DATABASE](alter-database.md), [SET](set.md)

