<a id="LIBPQ-SSL"></a>

## 32.19. SSL 支援 [#](#libpq-ssl) <a href="#libpq-ssl" id="libpq-ssl"></a>

[32.19.1. 用戶端驗證伺服器憑證](libpq-ssl.md#libq-ssl-certificates)

[32.19.2. 用戶端憑證](libpq-ssl.md#libpq-ssl-clientcert)

[32.19.3. 不同模式所提供的保護](libpq-ssl/libpq-ssl-protection.md#libpq-ssl-protection)

[32.19.4. SSL 用戶端檔案用途](libpq-ssl/libpq-ssl-fileusage.md#libpq-ssl-fileusage)

[32.19.5. SSL 函式庫初始化](libpq-ssl.md#libpq-ssl-initialize)

<a id="id-1.7.3.26.2"></a>

PostgreSQL 原生支援使用 SSL
連線，以 TLS 協定加密用戶端／伺服器之間的通訊，提高安全性。
伺服器端 SSL 功能的詳細資訊請參閱[第 18.9 節](../../server-administration/runtime/ssl-tcp.md)。

libpq 會讀取全系統的
OpenSSL 設定檔。預設情況下，這個
檔案名為 `openssl.cnf`，位於
`openssl version -d` 所回報的目錄中。這項預設值
可以藉由將環境變數
`OPENSSL_CONF` 設定為所需設定檔的名稱來覆寫。

<a id="LIBQ-SSL-CERTIFICATES"></a>

### 32.19.1. 用戶端驗證伺服器憑證 [#](#libq-ssl-certificates) <a href="#libq-ssl-certificates" id="libq-ssl-certificates"></a>

預設情況下，PostgreSQL 不會對伺服器憑證進行任何驗證。
這表示有可能在用戶端不知情的情況下偽冒伺服器身分
（例如修改 DNS 紀錄，或接管伺服器的
IP 位址）。為了防止偽冒，
用戶端必須能夠透過信任鏈驗證伺服器的身分。
信任鏈的建立方式是：在一台電腦上放置根（自我簽署）
憑證授權單位（CA）憑證，並在另一台電腦上放置由該
根憑證*簽署*的葉憑證。也可以使用
由根憑證簽署、並用來簽署葉憑證的「中繼」憑證。

若要讓用戶端驗證伺服器的身分，請在用戶端放置根
憑證，並在伺服器放置由該根憑證簽署的葉憑證。若要讓伺服器驗證
用戶端的身分，請在伺服器放置根憑證，並在用戶端放置由該根憑證簽署的葉
憑證。也可以使用一個或多個
中繼憑證（通常與葉憑證儲存在一起），
將葉憑證連結到根憑證。

信任鏈建立之後，用戶端有兩種方式可以驗證伺服器所傳送的葉憑證。
若參數 `sslmode` 設定為 `verify-ca`，
libpq 會檢查憑證鏈，一路檢查到儲存在用戶端的根憑證，
以驗證伺服器值得信任。
若 `sslmode` 設定為 `verify-full`，
libpq *還會*驗證伺服器主機
名稱是否與伺服器憑證中所儲存的名稱相符。若無法驗證伺服器憑證，
SSL 連線就會失敗。在大多數
重視安全性的環境中，建議使用 `verify-full`。

在 `verify-full` 模式下，主機名稱會與
憑證的主體別名（Subject Alternative Name，SAN）屬性比對；若沒有
`dNSName` 類型的 SAN，則與通用名稱（Common Name）屬性比對。
若憑證的名稱屬性以星號
（`*`）開頭，該星號會被視為
萬用字元，可比對點號
（`.`）*以外*的所有字元。這表示該憑證不會比對到子網域。
若連線是使用 IP 位址而不是主機名稱建立的，
該 IP 位址會（在不進行任何 DNS 查詢的情況下）與
`iPAddress` 或 `dNSName` 類型的 SAN 比對。若既沒有
`iPAddress` SAN，也沒有
相符的 `dNSName` SAN，則以主機 IP 位址
與通用名稱屬性比對。

### 注意

為了與 PostgreSQL 的早期版本保持向後相容性，主機
IP 位址的驗證方式與
[RFC 6125](https://datatracker.ietf.org/doc/html/rfc6125) 不同。
主機 IP 位址一律會與 `dNSName`
SAN 以及 `iPAddress` SAN 比對；若沒有相關的 SAN，
也可能與通用名稱屬性比對。

若要啟用伺服器憑證驗證，必須將一個或多個根憑證
放在使用者家目錄中的 `~/.postgresql/root.crt` 檔案裡。
（在 Microsoft Windows 上，該檔案名為
`%APPDATA%\postgresql\root.crt`。）若需要中繼
憑證來將伺服器所傳送的憑證鏈連結到儲存在用戶端的根憑證，
也應該將這些中繼憑證加入該檔案。

若檔案 `~/.postgresql/root.crl` 存在
（在 Microsoft
Windows 上為 `%APPDATA%\postgresql\root.crl`），
也會檢查憑證撤銷清單（Certificate Revocation List，CRL）項目。

根憑證檔案與 CRL 的位置可以藉由設定
連線參數 `sslrootcert` 與 `sslcrl`，
或環境變數 `PGSSLROOTCERT` 與 `PGSSLCRL` 來變更。
也可以使用 `sslcrldir` 或環境變數 `PGSSLCRLDIR`
指定包含 CRL 檔案的目錄。

### 注意

為了與 PostgreSQL 的早期版本保持向後相容性，若
根 CA 檔案存在，
`sslmode=require` 的行為會與
`verify-ca` 相同，也就是會依據 CA 驗證伺服器憑證。
不建議依賴這項行為；
需要驗證憑證的應用程式應該一律使用
`verify-ca` 或 `verify-full`。

<a id="LIBPQ-SSL-CLIENTCERT"></a>

### 32.19.2. 用戶端憑證 [#](#libpq-ssl-clientcert) <a href="#libpq-ssl-clientcert" id="libpq-ssl-clientcert"></a>

若伺服器藉由要求用戶端提供葉憑證來嘗試驗證
用戶端的身分，
libpq 會傳送儲存在使用者家目錄中
`~/.postgresql/postgresql.crt` 檔案裡的憑證。
這些憑證必須能串連到伺服器所信任的根憑證。
也必須存在相符的
私密金鑰檔案 `~/.postgresql/postgresql.key`。
在 Microsoft Windows 上，這些檔案名為
`%APPDATA%\postgresql\postgresql.crt` 與
`%APPDATA%\postgresql\postgresql.key`。
憑證與金鑰檔案的位置可以由
連線參數 `sslcert`
與 `sslkey`，或由
環境變數 `PGSSLCERT` 與 `PGSSLKEY` 覆寫。

在 Unix 系統上，私密金鑰檔案的權限必須禁止
其他使用者（world）或群組的任何存取；可以使用諸如
`chmod 0600 ~/.postgresql/postgresql.key` 的命令達成。
另一種做法是讓該檔案由 root 擁有，並具有群組讀取權
（也就是 `0640` 權限）。這種設定適用於
由作業系統管理憑證與金鑰檔案的安裝環境。此時應將
libpq 的使用者
加入有權存取這些憑證與金鑰檔案的群組。
（在 Microsoft Windows 上不會檢查檔案權限，
因為 `%APPDATA%\postgresql` 目錄被假定為安全的。）

`postgresql.crt` 中的第一個憑證必須是
用戶端的憑證，因為它必須與用戶端的私密金鑰相符。
可以選擇性地將「中繼」憑證附加到
該檔案中——這樣做可以避免需要在伺服器上儲存中繼
憑證（[ssl_ca_file](../../server-administration/runtime-config/runtime-config-connection.md#GUC-SSL-CA-FILE)）。

憑證與金鑰可以是 PEM 或 ASN.1 DER 格式。

金鑰可以
以明文儲存，或以 OpenSSL 所支援的任何演算法（例如 AES-128）
搭配密碼短語（passphrase）加密。若金鑰
以加密形式儲存，則可以在
[sslpassword](libpq-paramkeywords.md#libpq-connect-sslpassword) 連線選項中提供密碼短語。若提供了
加密的金鑰，而 `sslpassword` 選項
未指定或為空白，且有 TTY 可用，
OpenSSL 會以
`Enter PEM pass phrase:` 提示以互動方式要求輸入密碼。
應用程式可以提供自己的
金鑰密碼回呼函式，以覆寫用戶端憑證的提示以及
`sslpassword` 參數的處理方式；請參閱
[`PQsetSSLKeyPassHook_OpenSSL`](libpq-connect.md#libpq-pqsetsslkeypasshook-openssl)。

關於建立憑證的說明，請參閱[第 18.9.5 節](../../server-administration/runtime/ssl-tcp.md#ssl-certificate-creation)。

### 32.19.3. 不同模式所提供的保護 [#](#libpq-ssl-protection) <a href="#libpq-ssl-protection" id="libpq-ssl-protection"></a>

完整內容請見 [32.19.3. 不同模式所提供的保護](libpq-ssl/libpq-ssl-protection.md#libpq-ssl-protection)。

### 32.19.4. SSL 用戶端檔案用途 [#](#libpq-ssl-fileusage) <a href="#libpq-ssl-fileusage" id="libpq-ssl-fileusage"></a>

完整內容請見 [32.19.4. SSL 用戶端檔案用途](libpq-ssl/libpq-ssl-fileusage.md#libpq-ssl-fileusage)。

<a id="LIBPQ-SSL-INITIALIZE"></a>

### 32.19.5. SSL 函式庫初始化 [#](#libpq-ssl-initialize) <a href="#libpq-ssl-initialize" id="libpq-ssl-initialize"></a>

需要與較舊版本的
PostgreSQL 相容、並使用 OpenSSL
1.0.2 或更舊版本的應用程式，需要在使用 SSL 函式庫之前先將其初始化。
會初始化 `libssl` 和／或
`libcrypto` 函式庫的應用程式，應該呼叫
[`PQinitOpenSSL`](libpq-ssl.md#LIBPQ-PQINITOPENSSL)，告知 libpq
`libssl` 和／或 `libcrypto` 函式庫
已由你的應用程式初始化，如此
libpq 就不會再初始化這些函式庫。
不過，使用 OpenSSL
1.1.0 或更新版本時就不需要這麼做，因為重複初始化已不再造成問題。

關於其用法的詳細資訊，請參閱你所針對之 PostgreSQL 版本的
文件。

<a id="LIBPQ-PQINITOPENSSL"></a>

`PQinitOpenSSL`<a id="id-1.7.3.26.9.4.1.1.1.2"></a> [#](#LIBPQ-PQINITOPENSSL)

讓應用程式選擇要初始化哪些安全性函式庫。

```

    void PQinitOpenSSL(int do_ssl, int do_crypto);
```

此函式已棄用，僅為了向後相容性而存在，
它不會執行任何動作。

<a id="LIBPQ-PQINITSSL"></a>

`PQinitSSL`<a id="id-1.7.3.26.9.4.1.2.1.2"></a> [#](#LIBPQ-PQINITSSL)

讓應用程式選擇要初始化哪些安全性函式庫。

```

    void PQinitSSL(int do_ssl);
```

此函式等同於
`PQinitOpenSSL(do_ssl, do_ssl)`。
此函式已棄用，僅為了向後相容性而存在，
它不會執行任何動作。

[`PQinitSSL`](libpq-ssl.md#LIBPQ-PQINITSSL) 與 [`PQinitOpenSSL`](libpq-ssl.md#LIBPQ-PQINITOPENSSL)
為了向後相容性而保留，但自
PostgreSQL 18 起已不再需要。
[`PQinitSSL`](libpq-ssl.md#LIBPQ-PQINITSSL) 自
PostgreSQL 8.0 起就已存在，而 [`PQinitOpenSSL`](libpq-ssl.md#LIBPQ-PQINITOPENSSL)
是在 PostgreSQL 8.4 才加入，因此對於需要與較舊版本
libpq 搭配運作的應用程式，[`PQinitSSL`](libpq-ssl.md#LIBPQ-PQINITSSL)
可能較為合適。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-ssl.html)（原文版本：18.6；核對日期：2026-10-17）
