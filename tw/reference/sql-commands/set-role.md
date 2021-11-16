# SET ROLE

SET ROLE — 設定目前連線的目前使用者識別

### 語法

```
SET [ SESSION | LOCAL ] ROLE role_name
SET [ SESSION | LOCAL ] ROLE NONE
RESET ROLE
```

### 說明

此命令將目前 SQL 連線的目前使用者識別指定為 role\_name。角色名稱可以寫為識別字或字串文字。在 SET ROLE 之後，執行 SQL 命令的權限檢查，就如同指定角色是最初登入的角色一樣。

指定的 role\_name 必須是目前連線角色所屬的角色。（如果連線使用者是超級使用者，則可以選擇任何角色。）

SESSION 和 LOCAL 修飾字的作用與一般 [SET](set.md) 命令的作用相同。

NONE 和 RESET 語法將目前使用者識別字重置為目前連線使用者的識別字。這些語法可以由任何使用者執行。

### 注意

使用此命令，可以增加權限或限制其權限。如果連線使用者角色具有 INHERITS 屬性，則它自動擁有它可以設定為 ROLE 的每個角色所有權限；在這種情況下，SET ROLE 有效地刪除了直接分配給連線使用者以及它所屬的其他角色的所有權限，只留下指定角色可用的權限。另一方面，如果連線使用者角色具有 NOINHERITS 屬性，則 SET ROLE 將刪除直接分配給連線使用者的權限，而是獲取指定角色可用的權限。

特別是，當超級使用者選擇將 SET ROLE 設定為非超級使用者角色時，他們將失去超級使用者權限。

SET ROLE 具有與 [SET SESSION AUTHORIZATION](set-session-authorization.md) 相當的效果，但涉及的權限檢查完全不同。此外，SET SESSION AUTHORIZATION 決定哪些角色可用於以後的 SET ROLE命令，而使用 SET ROLE 變更角色不會更改允許用於以後的 SET ROLE 的角色集合。

SET ROLE 不處理角色由 [ALTER ROLE](alter-role.md) 指定的連線變數；這只發生在登入期間。

SET ROLE 不能在 SECURITY DEFINER 功能中使用。

### 範例

```
SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user 
--------------+--------------
 peter        | peter

SET ROLE 'paul';

SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user 
--------------+--------------
 peter        | paul
```

### 相容性

PostgreSQL 允許使用識別字語法（“rolename”），而 SQL 標準要求將角色名稱寫為字串文字。SQL 在事務期間不允許此命令；PostgreSQL 則沒有這個限制，因為沒有理由限制。SESSION 和 LOCAL 修飾字是 PostgreSQL 延伸功能，RESET 語法也是。

### 參閱

[SET SESSION AUTHORIZATION](set-session-authorization.md)
