<a id="GSSAPI-AUTH"></a>

## 20.6. GSSAPI 驗證 [#](#gssapi-auth) <a href="#gssapi-auth" id="gssapi-auth"></a>

<a id="id-1.6.7.13.2"></a>

GSSAPI 是一種用於安全驗證的業界標準協定，
定義於
[RFC 2743](https://datatracker.ietf.org/doc/html/rfc2743)。
PostgreSQL
支援將 GSSAPI 用於驗證、
通訊加密，或兩者兼用。
對於支援 GSSAPI 的系統，它可提供自動驗證
（單一登入）。驗證本身是安全的。若使用了 GSSAPI 加密
或 SSL 加密，經由資料庫連線傳送的資料就會加密；
否則就不會加密。

建置 PostgreSQL 時必須啟用 GSSAPI 支援；
詳情請參閱[第 17 章](../installation/README.md)。

當 GSSAPI 使用
Kerberos 時，它會使用標準的服務
主體（principal，即驗證身分）名稱，格式為
`servicename/hostname@realm`。
特定安裝所使用的主體名稱，不會以任何方式編碼在
PostgreSQL 伺服器中；而是指定在伺服器
為了判定自身身分而讀取的 *keytab* 檔案中。若
keytab 檔案中列出了多個主體，伺服器會接受其中任何一個。
伺服器的領域（realm）名稱，是伺服器可存取的 Kerberos
設定檔中所指定的偏好領域。

連線時，用戶端必須知道它打算連線之伺服器的主體名稱。
主體的 *`servicename`*
部分通常是 `postgres`，
但可以透過 libpq 的
[krbsrvname](../../client-interfaces/libpq/libpq-paramkeywords.md#libpq-connect-krbsrvname) 連線參數選擇其他值。
*`hostname`* 部分是 libpq 被指示要連線的
主機的完整網域名稱（fully qualified host name）。
領域名稱是用戶端可存取的 Kerberos
設定檔中所指定的偏好領域。

用戶端也會有一個代表其自身身分的主體名稱
（而且它必須持有此主體的有效票證）。若要
使用 GSSAPI 進行驗證，用戶端
主體必須與某個
PostgreSQL 資料庫使用者名稱相關聯。
可以使用 `pg_ident.conf` 設定檔
將主體對應到使用者名稱；例如，
`pgusername@realm` 可以只對應到 `pgusername`。
或者，你也可以不做任何對應，直接將完整的 `username@realm` 主體
作為 PostgreSQL 中的角色名稱。

PostgreSQL 也支援只從主體中去除領域，
藉此將用戶端主體對應到使用者名稱。此方法是為了
向後相容性而支援，強烈不建議使用，因為這樣就無法區分
使用者名稱相同、但來自不同領域的不同使用者。若要啟用此方法，
請將 `include_realm` 設為 0。對於簡單的單一領域
安裝，這麼做並同時設定
`krb_realm` 參數（它會檢查主體的領域是否與
`krb_realm` 參數中的值完全相符），
仍然是安全的；但相較於在
`pg_ident.conf` 中指定明確的對應，這是一種功能較有限的做法。

伺服器 keytab 檔案的位置由 [krb_server_keyfile](../runtime-config/runtime-config-connection.md#GUC-KRB-SERVER-KEYFILE) 設定參數指定。
基於安全考量，建議只為
PostgreSQL 伺服器使用一個獨立的 keytab，
而不要讓伺服器讀取系統的 keytab 檔案。
請確認你的伺服器 keytab 檔案可由 PostgreSQL
伺服器帳號讀取（最好是只能讀取，不可寫入）。（另請參閱[第 18.1 節](../runtime/postgres-user.md)。）

keytab 檔案是使用 Kerberos 軟體產生的；詳情請參閱
Kerberos 文件。下列範例示範如何使用
MIT Kerberos 的 kadmin 工具
完成這項工作：

```

kadmin% addprinc -randkey postgres/server.my.domain.org
kadmin% ktadd -k krb5.keytab postgres/server.my.domain.org
```

GSSAPI 驗證方法支援下列
驗證選項：

`include_realm`
:   若設為 0，已驗證使用者主體中的領域名稱會在
    傳入使用者名稱對應
    （[第 20.2 節](auth-username-maps.md)）之前被去除。不建議這麼做，
    此選項主要是為了向後相容性而提供，因為除非同時使用
    `krb_realm`，否則在多領域環境中並不安全。
    建議將 `include_realm` 保持為預設值（1），
    並在 `pg_ident.conf` 中提供明確的對應，
    將主體名稱轉換為 PostgreSQL 使用者名稱。

`map`
:   允許從用戶端主體對應到資料庫使用者名稱。詳情請參閱
    [第 20.2 節](auth-username-maps.md)。對於 GSSAPI／Kerberos
    主體，例如 `username@EXAMPLE.COM`（或較
    少見的 `username/hostbased@EXAMPLE.COM`），
    用於對應的使用者名稱是
    `username@EXAMPLE.COM`（或分別為
    `username/hostbased@EXAMPLE.COM`），
    除非 `include_realm` 已設為 0；在這種情況下，
    對應時所看到的系統使用者名稱是 `username`
    （或 `username/hostbased`）。

`krb_realm`
:   設定用來比對使用者主體名稱的領域。若設定了此參數，
    只會接受該領域的使用者。若未設定，
    任何領域的使用者都可以連線，但須受所執行的任何使用者名稱
    對應所約束。

除了這些可以依不同 `pg_hba.conf` 項目而有所不同的設定之外，
還有一個伺服器層級的
[krb_caseins_users](../runtime-config/runtime-config-connection.md#GUC-KRB-CASEINS-USERS) 設定
參數。若將其設為 true，用戶端主體會以不區分大小寫的方式
與使用者對應項目比對。`krb_realm` 若有設定，
也會以不區分大小寫的方式比對。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/gssapi-auth.html)（原文版本：18.6；核對日期：2026-10-10）
