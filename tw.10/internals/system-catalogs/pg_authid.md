# 51.8. pg\_authid

目錄 pg\_authid 包含有關資料庫認證識別（角色）的資訊。角色包含「使用者」和「群組」的概念。使用者基本上只是設置了 rolcanlogin 識別的角色。任何角色（無論有或沒有 rolcanlogin）都可以擁有其他角色作為成員；詳見 [pg\_auth\_members](pg_auth_members.md)。

由於此目錄包含密碼，因此不得公開讀取。 [pg\_roles](pg_roles.md) 是 pg\_authid 上的一個公開可讀的檢視表，它隱藏了密碼字串。

[第 21 章](../../server-administration/21.-zi-liao-ku-jiao-se/)包含有關使用者和權限管理的詳細訊息。

由於使用者身份是叢集範圍的，因此 pg\_authid 在叢集的所有資料庫之間共享：每個叢集只有一個 pg\_authid 副本，而不是每個資料庫一個副本。

**Table 51.8. `pg_authid` Columns**

| Name | Type | Description |
| :--- | :--- | :--- |
| `oid` | `oid` | 資料列指標（隱藏屬性；必須明確選擇） |
| `rolname` | `name` | 角色名稱 |
| `rolsuper` | `bool` | 角色具有超級使用者權限 |
| `rolinherit` | `bool` | 角色自動繼承其所屬角色的權限 |
| `rolcreaterole` | `bool` | 角色可以創造更多角色 |
| `rolcreatedb` | `bool` | 角色可以建立資料庫 |
| `rolcanlogin` | `bool` | 角色可以登入。也就是說，此角色可以作為初始連線認證識別 |
| `rolreplication` | `bool` | 角色是複寫角色。複寫角色可以啟動複寫連線並建立和移除複寫槽。 |
| `rolbypassrls` | `bool` | 角色繞過每個資料列級別的安全原則，有關詳細訊息，請參閱[第 5.7 節](../../the-sql-language/ddl/5.7.-zi-liao-lie-an-quan-yuan-ze.md)。 |
| `rolconnlimit` | `int4` | 對於可以登入的角色，這將設定此角色可以進行的最大同時連線數。-1 表示沒有限制。 |
| `rolpassword` | `text` | 密碼（可能是加密的）; 如果沒有則為 null。格式取決於使用的加密形式。 |
| `rolvaliduntil` | `timestamptz` | 密碼到期時間（僅用於密碼驗證）；如果沒有過期，則回傳 null |

對於 MD5 加密密碼，rolpassword 欄位將以字串 md5 開頭，之後跟 32 個字元的十六進位 MD5 hash。MD5 hash 將是使用者的密碼連接到他們的使用者名稱。例如，如果使用者 joe 的密碼為 xyzzy，則 PostgreSQL 將儲存 xyzzyjoe 的 md5 hash 值。

如果使用 SCRAM-SHA-256 加密密碼，則其格式為：

```text
SCRAM-SHA-256$<iteration count>:<salt>$<StoredKey>:<ServerKey>
```

其中 salt，StoredKey 和 ServerKey 採用 Base64 編碼格式。此格式與 RFC 5803 指定的格式相同。

未遵循這些格式之一的密碼就會被認為是未加密的。

