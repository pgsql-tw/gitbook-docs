<a id="SSL-TCP"></a>

## 18.9. 使用 SSL 的安全 TCP/IP 連線 [#](#SSL-TCP)

[18.9.1. 基本設定](ssl-tcp.md#SSL-SETUP)

[18.9.2. OpenSSL 組態設定](ssl-tcp.md#SSL-OPENSSL-CONFIG)

[18.9.3. 使用用戶端憑證](ssl-tcp.md#SSL-CLIENT-CERTIFICATES)

[18.9.4. SSL 伺服器檔案的使用](ssl-tcp.md#SSL-SERVER-FILES)

[18.9.5. 建立憑證](ssl-tcp.md#SSL-CERTIFICATE-CREATION)

<a id="id-1.6.5.12.2"></a>

PostgreSQL 原生支援使用 SSL 連線，
為用戶端與伺服器之間的通訊加密，以提升安全性。
這要求用戶端與伺服器系統上，都必須安裝 OpenSSL，
並且必須在建置時，啟用 PostgreSQL 中對此的支援
（請參閱[第 17 章](../installation/README.md)）。

SSL 與 TLS 這兩個術語，經常交替使用，
用來指稱使用 TLS 協定的安全加密連線。
SSL 協定是 TLS 協定的前身，
即使 SSL 協定本身已不再受到支援，
SSL 這個術語，仍然沿用來指稱加密連線。
在 PostgreSQL 中，SSL 與 TLS
是交替使用的。

<a id="SSL-SETUP"></a>

### 18.9.1. 基本設定 [#](#SSL-SETUP)

在已編譯進 SSL 支援的情況下，只要在
`postgresql.conf` 中，將參數
[ssl](../runtime-config/runtime-config-connection.md#GUC-SSL) 設定為 `on`，
即可啟動支援使用 TLS 協定加密連線的 PostgreSQL 伺服器。
伺服器會在同一個 TCP 連接埠上，
同時聆聽一般連線與 SSL 連線，並會與任何連線中的用戶端，
協商是否要使用 SSL。依預設，這是由用戶端決定的；
關於如何設定伺服器，讓部分或所有連線，
都要求使用 SSL，請參閱
[20.1 節](../client-authentication/auth-pg-hba-conf.md)。

若要以 SSL 模式啟動，必須存在包含伺服器憑證與
私密金鑰的檔案。依預設，系統預期這些檔案，
會分別位於伺服器資料目錄中，並命名為
`server.crt` 與 `server.key`，
不過您也可以使用組態參數
[ssl_cert_file](../runtime-config/runtime-config-connection.md#GUC-SSL-CERT-FILE)
與 [ssl_key_file](../runtime-config/runtime-config-connection.md#GUC-SSL-KEY-FILE)，
指定其他名稱與位置。

在 Unix 系統上，`server.key` 的權限，
必須禁止其他人與群組存取；可透過
`chmod 0600 server.key` 指令達成。
此外，該檔案也可以由 root 擁有，並允許群組讀取
（也就是 `0640` 權限）。這種設定方式，
適用於憑證與金鑰檔案由作業系統管理的安裝環境。
執行 PostgreSQL 伺服器的使用者，
則應加入具有這些憑證與金鑰檔案存取權的群組中。

若資料目錄允許群組讀取存取，為符合上述安全性要求，
憑證檔案可能需要放置於資料目錄之外。一般而言，
啟用群組存取，是為了讓非特殊權限的使用者，
能夠備份資料庫，在這種情況下，
備份軟體將無法讀取憑證檔案，很可能會發生錯誤。

若私密金鑰受密碼短語（passphrase）保護，
伺服器會提示輸入該密碼短語，
並且在輸入完成之前不會啟動。依預設，
使用密碼短語，會停用在不重新啟動伺服器的情況下，
變更伺服器 SSL 組態的能力，
但請參閱
[ssl_passphrase_command_supports_reload](../runtime-config/runtime-config-connection.md#GUC-SSL-PASSPHRASE-COMMAND-SUPPORTS-RELOAD)。
此外，在 Windows 上完全無法使用受密碼短語保護的
私密金鑰。

`server.crt` 中的第一張憑證，
必須是伺服器的憑證，因為它必須與伺服器的私密金鑰相符。
「中繼」憑證授權單位的憑證，也可以附加到該檔案中。
假設根憑證與中繼憑證，都是以 `v3_ca`
延伸項目建立的，這麼做能避免必須在用戶端上，
儲存中繼憑證。（這會將憑證的基本限制
`CA` 設為 `true`。）
這讓中繼憑證更容易到期。

並不需要將根憑證，加入 `server.crt` 中。
相反地，用戶端必須具備伺服器憑證鏈中的根憑證。

<a id="SSL-OPENSSL-CONFIG"></a>

### 18.9.2. OpenSSL 組態設定 [#](#SSL-OPENSSL-CONFIG)

PostgreSQL 會讀取系統層級的 OpenSSL 組態檔。
依預設，此檔案命名為 `openssl.cnf`，
位於 `openssl version -d` 所回報的目錄中。
您可以透過設定環境變數 `OPENSSL_CONF`
為所需組態檔的名稱，覆寫此預設值。

OpenSSL 支援種類繁多、強度各異的加密演算法
（cipher）與驗證演算法。雖然可以在 OpenSSL
組態檔中，指定一份加密演算法清單，但您也可以透過修改
`postgresql.conf` 中的
[ssl_ciphers](../runtime-config/runtime-config-connection.md#GUC-SSL-CIPHERS)，
專門為資料庫伺服器，指定要使用的加密演算法。

### 注意

透過使用 `NULL-SHA` 或 `NULL-MD5`
加密演算法，可以在不承擔加密額外負擔的情況下，
達成驗證。不過，中間人可能會讀取並轉發用戶端與伺服器之間的
通訊內容。此外，相較於驗證的額外負擔，加密的額外負擔
其實相當小。基於這些原因，不建議使用 NULL 加密演算法。

<a id="SSL-CLIENT-CERTIFICATES"></a>

### 18.9.3. 使用用戶端憑證 [#](#SSL-CLIENT-CERTIFICATES)

若要求用戶端提供受信任的憑證，請將您信任的根憑證授權單位
（CA）憑證，放入資料目錄中的某個檔案，
在 `postgresql.conf` 中，將參數
[ssl_ca_file](../runtime-config/runtime-config-connection.md#GUC-SSL-CA-FILE)，
設定為該新檔案的名稱，並在 `pg_hba.conf`
中對應的 `hostssl` 行，加上驗證選項
`clientcert=verify-ca` 或
`clientcert=verify-full`。如此一來，
在 SSL 連線啟動期間，就會向用戶端要求提供憑證。
（關於如何在用戶端設定憑證的說明，
請參閱[32.19 節](../../client-interfaces/libpq/libpq-ssl.md)。）

對於設有 `clientcert=verify-ca` 的
`hostssl` 項目，伺服器會驗證用戶端的憑證，
是否由其中一個受信任的憑證授權單位所簽署。若指定了
`clientcert=verify-full`，伺服器不僅會驗證憑證鏈，
還會檢查使用者名稱或其對應項，
是否與所提供憑證的 `cn`（Common Name）相符。
請注意，使用 `cert` 驗證方式時，
系統一律會確保進行憑證鏈驗證
（請參閱[20.12 節](../client-authentication/auth-cert.md)）。

若您希望避免將中繼憑證，儲存在用戶端上，
只要根憑證與中繼憑證，都是以 `v3_ca`
延伸項目建立的，這類能鏈結至既有根憑證的中繼憑證，
也可以出現在
[ssl_ca_file](../runtime-config/runtime-config-connection.md#GUC-SSL-CA-FILE) 檔案中。
若已設定參數
[ssl_crl_file](../runtime-config/runtime-config-connection.md#GUC-SSL-CRL-FILE)
或 [ssl_crl_dir](../runtime-config/runtime-config-connection.md#GUC-SSL-CRL-DIR)，
系統也會檢查憑證撤銷清單（CRL）項目。

`clientcert` 驗證選項，適用於所有驗證方式，
但僅限於在 `pg_hba.conf` 中指定為
`hostssl` 的行。若未指定 `clientcert`，
伺服器只有在用戶端有提供憑證、且已設定 CA 的情況下，
才會依其 CA 檔案，驗證用戶端憑證。

要強制要求使用者在登入期間提供憑證，有兩種做法。

第一種做法，是針對 `pg_hba.conf` 中的
`hostssl` 項目，使用 `cert` 驗證方式，
如此一來，憑證本身，就會同時用於驗證，
並提供 SSL 連線安全性。詳情請參閱
[20.12 節](../client-authentication/auth-cert.md)。
（使用 `cert` 驗證方式時，
不需要明確指定任何 `clientcert` 選項。）
在這種情況下，系統會將憑證中提供的
`cn`（Common Name），對照使用者名稱或
適用的對應項目進行檢查。

第二種做法，是透過將 `clientcert` 驗證選項，
設定為 `verify-ca` 或 `verify-full`，
將任何驗證方式，與用戶端憑證的驗證結合使用，
用於 `hostssl` 項目。前者僅強制要求
憑證有效，而後者則會另外確保，
憑證中的 `cn`（Common Name），
與使用者名稱或適用的對應項目相符。

<a id="SSL-SERVER-FILES"></a>

### 18.9.4. SSL 伺服器檔案的使用 [#](#SSL-SERVER-FILES)

[表 18.2](ssl-tcp.md#SSL-FILE-USAGE) 彙整了與伺服器上
SSL 設定相關的檔案。（所示的檔案名稱為預設名稱，
本機設定的名稱可能有所不同。）

<a id="SSL-FILE-USAGE"></a>

**表 18.2. SSL 伺服器檔案的使用**

<table border="1" class="table" summary="SSL Server File Usage"><colgroup><col/><col/><col/></colgroup><thead><tr><th>檔案</th><th>內容</th><th>作用</th></tr></thead><tbody><tr><td><a class="xref" href="../runtime-config/runtime-config-connection.md#GUC-SSL-CERT-FILE">ssl_cert_file</a> (<code class="filename">$PGDATA/server.crt</code>)</td><td>伺服器憑證</td><td>傳送給用戶端，用以表明伺服器的身分</td></tr><tr><td><a class="xref" href="../runtime-config/runtime-config-connection.md#GUC-SSL-KEY-FILE">ssl_key_file</a> (<code class="filename">$PGDATA/server.key</code>)</td><td>伺服器私密金鑰</td><td>證明伺服器憑證確實是由擁有者傳送的；但不代表
      該憑證擁有者值得信任</td></tr><tr><td><a class="xref" href="../runtime-config/runtime-config-connection.md#GUC-SSL-CA-FILE">ssl_ca_file</a></td><td>受信任的憑證授權單位</td><td>檢查用戶端憑證
      是否由受信任的憑證授權單位所簽署</td></tr><tr><td><a class="xref" href="../runtime-config/runtime-config-connection.md#GUC-SSL-CRL-FILE">ssl_crl_file</a></td><td>已由憑證授權單位撤銷的憑證</td><td>用戶端憑證不得出現在此清單中</td></tr></tbody></table>

<br>

伺服器會在啟動時，以及每次重新載入伺服器組態時，
讀取這些檔案。在 Windows 系統上，
每當為新的用戶端連線衍生出新的後端程序時，
這些檔案也會被重新讀取。

若在伺服器啟動時，偵測到這些檔案中有錯誤，
伺服器將拒絕啟動。但若是在組態重新載入期間，
偵測到錯誤，則會忽略這些檔案，繼續使用舊有的
SSL 組態。在 Windows 系統上，若在後端啟動時，
偵測到這些檔案中有錯誤，該後端將無法
建立 SSL 連線。在所有這些情況下，
錯誤狀況都會記錄於伺服器日誌中。

<a id="SSL-CERTIFICATE-CREATION"></a>

### 18.9.5. 建立憑證 [#](#SSL-CERTIFICATE-CREATION)

若要為伺服器，建立一份有效期為 365 天的簡易自簽憑證，
請使用以下 OpenSSL 指令，並將
*`dbhost.yourdomain.com`* 換成伺服器的
主機名稱：

```

openssl req -new -x509 -days 365 -nodes -text -out server.crt \
  -keyout server.key -subj "/CN=dbhost.yourdomain.com"
```

接著，執行：

```

chmod og-rwx server.key
```

因為若該檔案的權限，比這更寬鬆，
伺服器就會拒絕該檔案。關於如何建立
伺服器私密金鑰與憑證的更多細節，
請參閱 OpenSSL 的相關文件。

雖然自簽憑證可用於測試，但在正式環境中，
應該使用由憑證授權單位（CA，通常是
企業層級的根 CA）所簽署的憑證。

若要建立一份身分可由用戶端驗證的伺服器憑證，
請先建立一份憑證簽署請求（CSR），
以及一組公開／私密金鑰檔案：

```

openssl req -new -nodes -text -out root.csr \
  -keyout root.key -subj "/CN=root.yourdomain.com"
chmod og-rwx root.key
```

接著，使用該金鑰，簽署此請求，
以建立一個根憑證授權單位
（此處使用 Linux 上 OpenSSL 組態檔的預設位置）：

```

openssl x509 -req -in root.csr -text -days 3650 \
  -extfile /etc/ssl/openssl.cnf -extensions v3_ca \
  -signkey root.key -out root.crt
```

最後，建立一份由此新的根憑證授權單位所簽署的
伺服器憑證：

```

openssl req -new -nodes -text -out server.csr \
  -keyout server.key -subj "/CN=dbhost.yourdomain.com"
chmod og-rwx server.key

openssl x509 -req -in server.csr -text -days 365 \
  -CA root.crt -CAkey root.key -CAcreateserial \
  -out server.crt
```

`server.crt` 與 `server.key`，
應儲存在伺服器上，而 `root.crt`，
則應儲存在用戶端上，讓用戶端能夠驗證伺服器的葉憑證，
確實是由其信任的根憑證所簽署。
`root.key` 應離線儲存，
以供日後建立憑證時使用。

您也可以建立包含中繼憑證的信任鏈：

```

# root
openssl req -new -nodes -text -out root.csr \
  -keyout root.key -subj "/CN=root.yourdomain.com"
chmod og-rwx root.key
openssl x509 -req -in root.csr -text -days 3650 \
  -extfile /etc/ssl/openssl.cnf -extensions v3_ca \
  -signkey root.key -out root.crt

# intermediate
openssl req -new -nodes -text -out intermediate.csr \
  -keyout intermediate.key -subj "/CN=intermediate.yourdomain.com"
chmod og-rwx intermediate.key
openssl x509 -req -in intermediate.csr -text -days 1825 \
  -extfile /etc/ssl/openssl.cnf -extensions v3_ca \
  -CA root.crt -CAkey root.key -CAcreateserial \
  -out intermediate.crt

# leaf
openssl req -new -nodes -text -out server.csr \
  -keyout server.key -subj "/CN=dbhost.yourdomain.com"
chmod og-rwx server.key
openssl x509 -req -in server.csr -text -days 365 \
  -CA intermediate.crt -CAkey intermediate.key -CAcreateserial \
  -out server.crt
```

`server.crt` 與
`intermediate.crt`，應串接成一份憑證檔案包，
並儲存在伺服器上。`server.key`，
也應儲存在伺服器上。`root.crt`，
則應儲存在用戶端上，讓用戶端能夠驗證伺服器的葉憑證，
確實是由鏈結至其信任根憑證的憑證鏈所簽署。
`root.key` 與 `intermediate.key`，
應離線儲存，以供日後建立憑證時使用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ssl-tcp.html)（原文版本：18.6；核對日期：2026-09-24）
