# 51.81 pg\_roles

pg\_roles 這個 view 提供對資料庫角色的資訊。 這只是 pg\_authid 的一個公共可讀的 view，它將密碼部份予以屏蔽。

此 view 列出底層的 OID 欄位，因此可能需要執行與其他目錄的交叉查詢。

**Table 51.82. `pg_roles` 欄位**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `rolname` | `name` |   | 角色名稱 |
| `rolsuper` | `bool` |   | 角色具有超級使用者權限 |
| `rolinherit` | `bool` |   | 角色自動繼承它所屬角色的權限 |
| `rolcreaterole` | `bool` |   | 角色可以建立更多角色 |
| `rolcreatedb` | `bool` |   | 角色可以建立資料庫 |
| `rolcanlogin` | `bool` |   | 角色可以登入。也就是說，可以將此角色作為初始連線認證使用 |
| `rolreplication` | `bool` |   | 角色是可以進行資料複寫的角色。複寫角色表示可以啟動資料複寫連線並建立和刪除複寫對象。 |
| `rolconnlimit` | `int4` |   | 對於可以登入的角色，這個設定此角色可以建立的最大同時連線數。 -1 意味著沒有限制。 |
| `rolpassword` | `text` |   | 不是密碼（讀出來都是\*\*\*\*\*\*\*\*） |
| `rolvaliduntil` | `timestamptz` |   | 密碼到期時間（僅用於密碼驗證）; 如果沒有到期時間，則顯示 null |
| `rolbypassrls` | `bool` |   | 角色繞過每一個資料列層級的安全原則，參閱[第 5.7 節](../../sql/5.-ding-yi-zi-liao-jie-gou/5.7.-zi-liao-lie-an-quan-yuan-ze.md)了解更多訊息。 |
| `rolconfig` | `text[]` |   | 執行環境時用於角色的組態預設值 |
| `oid` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | 角色的 ID |

