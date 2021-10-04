# 21.5. Default Roles

PostgreSQL 提供了一組預設的角色，這些角色提供對某些經常需要的特定權限功能和資訊的存取。資料庫管理員可以將這些角色授予其環境中的其他角色，使這些使用者可以存取或使用指定的功能和資訊。

[Table 21.1](default-roles.md#table-21-1-default-roles) 中列出了預設的角色。請注意，隨著其他功能的增加，未來每個預設角色的權限可能也會變更。資料庫管理員應隨時確認說明文件中的內容。

#### **Table 21.1. Default Roles**

| Role | Allowed Access |
| :--- | :--- |
| pg\_read\_all\_settings | Read all configuration variables, even those normally visible only to superusers. |
| pg\_read\_all\_stats | Read all pg\_stat\_\* views and use various statistics related extensions, even those normally visible only to superusers. |
| pg\_stat\_scan\_tables | Execute monitoring functions that may take `ACCESS SHARE` locks on tables, potentially for a long time. |
| pg\_monitor | Read/execute various monitoring views and functions. This role is a member of `pg_read_all_settings`, `pg_read_all_stats` and `pg_stat_scan_tables`. |
| pg\_signal\_backend | Signal another backend to cancel a query or terminate its session. |
| pg\_read\_server\_files | Allow reading files from any location the database can access on the server with COPY and other file-access functions. |
| pg\_write\_server\_files | Allow writing to files in any location the database can access on the server with COPY and other file-access functions. |
| pg\_execute\_server\_program | Allow executing programs on the database server as the user the database runs as with COPY and other functions which allow executing a server-side program. |

pg\_monitor、pg\_read\_all\_settings、pg\_read\_all\_stats 和 pg\_stat\_scan\_tables 角色旨在使資料管理員可以輕鬆地配置角色以監控資料庫伺服器。它們授予一組通用的特殊權限，允許角色讀取各種有用的組態配置、統計資訊與其他通常限於超級使用者才能取得的系統資訊。

pg\_signal\_backend 角色旨在允許資料庫管理員啟用受信任的非超級使用者角色，以將 SIGNAL 發送到其他後端程序。目前，此角色可發送 SIGNAL，以取消另一個後端程序上的查詢或終止其連線。但是，被授予此角色的使用者無法將 SIGNAL 發送到超級使用者所擁有的後端程序。詳見[第 9.27.2 節](../../the-sql-language/functions-and-operators/system-administration.md#9-27-2-server-signaling-functions)。

pg\_read\_server\_files、pg\_write\_server\_files 和 pg\_execute\_server\_program 角色旨在允許資料管理員擁有可信任的角色，但非超級使用者角色。這些角色能夠以資料庫執行使用者的身份存取檔案並在資料庫伺服器上執行程序。由於這些角色可以存取伺務器檔案系統上的任何檔案，因此它們在直接存取檔案時會繞過所有資料庫層級的權限檢查，並且它們可用於取得超級使用者層級的存取權限，因此在授予這些角色以使用這些權限時應格外小心。

授予這些角色時應格外小心，以確保僅在需要時才使用它們，並應了解這些角色會授予對特權資訊的存取權限。

資料庫管理員可以使用 GRANT 指令向使用者授予對這些角色的存取權限，例如：

```text
GRANT pg_signal_backend TO admin_user;
```

