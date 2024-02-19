# SET SESSION AUTHORIZATION

SET SESSION AUTHORIZATION — 設定連線使用者識別和目前連線的目前使用者識別

### 語法

```
SET [ SESSION | LOCAL ] SESSION AUTHORIZATION user_name
SET [ SESSION | LOCAL ] SESSION AUTHORIZATION DEFAULT
RESET SESSION AUTHORIZATION
```

### 說明

此指令將連線使用者識別和目前 SQL 連線的目前使用者識別設定為 user\_name。使用者名稱可以寫成識別指標或字串文字。例如，使用此指令可以暫時成為非超級使用者，然後再切換回超級使用者。

連線使用者識別最初設定為用戶端提供的（可能經過身份驗證的）使用者名稱。目前使用者識別通常等於連線使用者識別，但可能會在 SECURITY DEFINER 功能和類似機制的情況下暫時改變；它也可以通過 [SET ROLE](set-role.md) 進行變更。目前的使用者識別與權限檢查相關。

只有初始連線使用者（經過身份驗證的用戶）具有超級使用者權限時，才能變更連線使用者識別。否則，該指令僅在指定經過驗證的使用者名稱時才被接受。

SESSION 和 LOCAL 修飾字的作用與一般的 [SET](set.md) 命令相同。

DEFAULT 和 RESET 語法將連線和目前使用者識別重置為最初認證的使用者名稱。這些語法可以由任何使用者執行。

### 注意

SET SESSION AUTHORIZATION 不能用於 SECURITY DEFINER 函數之中。

### 範例

```
SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user 
--------------+--------------
 peter        | peter

SET SESSION AUTHORIZATION 'paul';

SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user 
--------------+--------------
 paul         | paul
```

### 相容性

SQL 標準允許一些其他表示式代替文字 user\_name 出現，但這些選項在實作中並不重要。PostgreSQL 允許標識字語法("username")，但不是 SQL 標準。SQL在交易事務中不允許這個命令；PostgreSQL 則沒有這個限制，因為沒有理由。SESSION 和 LOCAL 修飾字是 PostgreSQL 延伸語法，RESET 語法也是如此。

執行此命令所需的權限由實作定義。

### 參閱

[SET ROLE](set-role.md)
