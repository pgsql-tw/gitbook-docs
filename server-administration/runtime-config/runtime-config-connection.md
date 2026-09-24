<a id="RUNTIME-CONFIG-CONNECTION"></a>

## 19.3. 連線與驗證 [#](#RUNTIME-CONFIG-CONNECTION)

[19.3.1. 連線設定](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-SETTINGS)

[19.3.2. TCP 設定](runtime-config-connection.md#RUNTIME-CONFIG-TCP-SETTINGS)

[19.3.3. 驗證](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-AUTHENTICATION)

[19.3.4. SSL](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-SSL)

<a id="RUNTIME-CONFIG-CONNECTION-SETTINGS"></a>

### 19.3.1. 連線設定 [#](#RUNTIME-CONFIG-CONNECTION-SETTINGS)

<a id="GUC-LISTEN-ADDRESSES"></a>

`listen_addresses` (`string`) <a id="id-1.6.6.6.2.2.1.1.3"></a> [#](#GUC-LISTEN-ADDRESSES)
:   指定伺服器要監聽來自用戶端應用程式連線的
    TCP/IP 位址。
    此值的格式為以逗號分隔的主機名稱
    及（或）數字 IP 位址清單。特殊項目 `*`
    代表所有可用的 IP 介面。項目
    `0.0.0.0` 允許監聽所有 IPv4 位址，
    `::` 則允許監聽所有 IPv6 位址。
    若此清單為空，伺服器將完全不監聽任何 IP 介面，
    此時只能使用 Unix 網域通訊端連線至伺服器。
    若清單不為空，只要伺服器能夠監聽至少一個 TCP/IP
    位址，伺服器就會啟動。對於任何無法開啟的
    TCP/IP 位址，都會發出警告。
    預設值為 localhost，
    這僅允許本機 TCP/IP「loopback」連線。

    雖然用戶端驗證（[第 20 章](../client-authentication/README.md)）能夠
    細緻地控制誰可以存取伺服器，
    `listen_addresses` 則控制哪些介面
    會接受連線嘗試，這有助於防止在不安全的
    網路介面上反覆出現的惡意連線請求。此參數只能
    在伺服器啟動時設定。
<a id="GUC-PORT"></a>

`port` (`integer`) <a id="id-1.6.6.6.2.2.2.1.3"></a> [#](#GUC-PORT)
:   伺服器監聽的 TCP 埠號；預設為 5432。請注意，
    伺服器所監聽的所有 IP 位址都使用相同的埠號。
    此參數只能在伺服器啟動時設定。
<a id="GUC-MAX-CONNECTIONS"></a>

`max_connections` (`integer`) <a id="id-1.6.6.6.2.2.3.1.3"></a> [#](#GUC-MAX-CONNECTIONS)
:   決定資料庫伺服器允許的最大並行連線數。
    預設值通常為 100 個連線，但若你的核心
    設定無法支援（由 initdb 期間判斷），
    則可能較少。此參數只能在伺服器啟動時
    設定。

    PostgreSQL 會直接根據
    `max_connections` 的值調整某些資源的大小。
    提高此值會導致這些資源（包括共享記憶體）的
    配置量增加。

    在執行 standby 伺服器時，你必須將此參數設為與
    primary 伺服器相同或更高的值，否則
    standby 伺服器中將不允許執行查詢。
<a id="GUC-RESERVED-CONNECTIONS"></a>

`reserved_connections` (`integer`) <a id="id-1.6.6.6.2.2.4.1.3"></a> [#](#GUC-RESERVED-CONNECTIONS)
:   決定為具備
    [pg_use_reserved_connections](../user-manag/predefined-roles.md#PREDEFINED-ROLE-PG-USE-RESERVED-CONNECTIONS)
    角色權限的角色所連線保留的連線「插槽」數量。
    每當可用連線插槽的數量大於
    [superuser_reserved_connections](runtime-config-connection.md#GUC-SUPERUSER-RESERVED-CONNECTIONS)，
    但小於或等於 `superuser_reserved_connections`
    與 `reserved_connections` 兩者總和時，
    新連線只會接受超級使用者，以及具備
    `pg_use_reserved_connections` 權限的角色。若可用連線
    插槽數量已等於或小於
    `superuser_reserved_connections`，新連線就只會
    接受超級使用者。

    預設值為零個連線。此值必須小於
    `max_connections` 減去
    `superuser_reserved_connections`。此參數只能
    在伺服器啟動時設定。
<a id="GUC-SUPERUSER-RESERVED-CONNECTIONS"></a>

`superuser_reserved_connections` (`integer`) <a id="id-1.6.6.6.2.2.5.1.3"></a> [#](#GUC-SUPERUSER-RESERVED-CONNECTIONS)
:   決定為 PostgreSQL 超級使用者所連線
    保留的連線「插槽」數量。同一時間
    最多只能有 [max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS)
    個連線處於作用中狀態。每當作用中並行連線的
    數量達到 `max_connections` 減去
    `superuser_reserved_connections` 時，新
    連線就只會接受超級使用者。由此參數保留的連線插槽，
    是設計用於在
    [reserved_connections](runtime-config-connection.md#GUC-RESERVED-CONNECTIONS) 保留的插槽
    耗盡後，作為緊急情況使用的最後保留額度。

    預設值為三個連線。此值必須小於
    `max_connections` 減去
    `reserved_connections`。
    此參數只能在伺服器啟動時設定。
<a id="GUC-UNIX-SOCKET-DIRECTORIES"></a>

`unix_socket_directories` (`string`) <a id="id-1.6.6.6.2.2.6.1.3"></a> [#](#GUC-UNIX-SOCKET-DIRECTORIES)
:   指定伺服器要監聽來自用戶端應用程式連線的
    Unix 網域通訊端所在目錄。
    可以透過以逗號分隔列出多個目錄，來建立多個通訊端。
    項目之間的空白字元會被忽略；如果目錄名稱中
    需要包含空白字元或逗號，請以雙引號括住該名稱。
    若此值為空，
    則代表不監聽任何 Unix 網域通訊端，此時
    只能使用 TCP/IP 通訊端連線至伺服器。

    以 `@` 開頭的值代表應建立一個
    位於抽象命名空間（abstract namespace）中的 Unix 網域通訊端
    （目前僅支援 Linux）。在這種情況下，此值
    並非指定「目錄」，而是一個前綴，實際的通訊端
    名稱會以與檔案系統命名空間相同的方式，根據
    此前綴計算得出。雖然由於這不是檔案系統位置，
    抽象通訊端名稱前綴可以自由選擇，但慣例上
    仍會使用類似檔案系統路徑的值，例如
    `@/tmp`。

    預設值通常為
    `/tmp`，但可以在建置時變更。
    在 Windows 上，預設值為空，代表預設不會
    建立任何 Unix 網域通訊端。
    此參數只能在伺服器啟動時設定。

    除了通訊端檔案本身（命名為
    `.s.PGSQL.nnnn`，其中
    *`nnnn`* 為伺服器的埠號）之外，還會在
    每一個 `unix_socket_directories` 目錄中，
    建立一個名為 `.s.PGSQL.nnnn.lock`
    的一般檔案。
    這兩個檔案都不應該手動移除。
    對於位於抽象命名空間中的通訊端，則不會建立鎖定檔案。
<a id="GUC-UNIX-SOCKET-GROUP"></a>

`unix_socket_group` (`string`) <a id="id-1.6.6.6.2.2.7.1.3"></a> [#](#GUC-UNIX-SOCKET-GROUP)
:   設定 Unix 網域通訊端的擁有群組。（通訊端的
    擁有使用者永遠是啟動伺服器的使用者。）搭配
    `unix_socket_permissions` 參數，
    此設定可以作為 Unix 網域連線的額外存取控制機制。
    根據預設，此值為空字串，代表使用
    伺服器使用者的預設群組。此參數只能在
    伺服器啟動時設定。

    此參數在 Windows 上不受支援。任何設定
    都會被忽略。此外，位於抽象命名空間中的通訊端沒有檔案擁有者，
    因此在這種情況下，此設定同樣會被忽略。
<a id="GUC-UNIX-SOCKET-PERMISSIONS"></a>

`unix_socket_permissions` (`integer`) <a id="id-1.6.6.6.2.2.8.1.3"></a> [#](#GUC-UNIX-SOCKET-PERMISSIONS)
:   設定 Unix 網域通訊端的存取權限。Unix 網域
    通訊端使用一般的 Unix 檔案系統權限集合。
    此參數的值應為一個數字模式，
    格式與
    `chmod` 及 `umask`
    系統呼叫所接受的格式相同。（若要使用慣用的八進位格式，
    該數字必須以 `0`（零）開頭。）

    預設權限為 `0777`，代表
    任何人皆可連線。合理的替代方案有
    `0770`（僅擁有者與群組，另請參閱
    `unix_socket_group`）與 `0700`
    （僅擁有者）。（請注意，對於 Unix 網域通訊端而言，
    只有寫入權限有意義，因此設定或撤銷讀取或
    執行權限並沒有意義。）

    此存取控制機制與
    [第 20 章](../client-authentication/README.md)所述的機制彼此獨立。

    此參數只能在伺服器啟動時設定。

    在某些會完全忽略通訊端權限的系統上（特別是
    Solaris 10 以後的 Solaris），此參數並無意義。在這類系統上，
    可以透過將 `unix_socket_directories` 指向一個
    搜尋權限僅限於預期對象的目錄，達到類似的效果。

    位於抽象命名空間中的通訊端沒有檔案權限，因此在這種情況下，
    此設定同樣會被忽略。
<a id="GUC-BONJOUR"></a>

`bonjour` (`boolean`) <a id="id-1.6.6.6.2.2.9.1.3"></a> [#](#GUC-BONJOUR)
:   啟用透過 Bonjour 廣告
    伺服器的存在。預設值為關閉。
    此參數只能在伺服器啟動時設定。
<a id="GUC-BONJOUR-NAME"></a>

`bonjour_name` (`string`) <a id="id-1.6.6.6.2.2.10.1.3"></a> [#](#GUC-BONJOUR-NAME)
:   指定 Bonjour 服務
    名稱。若此參數設為空字串 `''`（此為預設值），
    則會使用電腦名稱。若伺服器並非以
    Bonjour 支援編譯而成，
    則此參數會被忽略。
    此參數只能在伺服器啟動時設定。

<a id="RUNTIME-CONFIG-TCP-SETTINGS"></a>

### 19.3.2. TCP 設定 [#](#RUNTIME-CONFIG-TCP-SETTINGS)

<a id="GUC-TCP-KEEPALIVES-IDLE"></a>

`tcp_keepalives_idle` (`integer`) <a id="id-1.6.6.6.3.2.1.1.3"></a> [#](#GUC-TCP-KEEPALIVES-IDLE)
:   指定在沒有網路活動多久之後，作業系統應該
    向用戶端傳送 TCP keepalive 訊息。
    若此值指定時未帶單位，則以秒為單位。
    值為 0（預設值）代表使用作業系統的預設值。
    在 Windows 上，將此值設為 0 會使此參數變成 2 小時，
    因為 Windows 沒有提供讀取系統預設值的方式。
    此參數僅在支援 `TCP_KEEPIDLE` 或等效通訊端選項的
    系統上受支援，以及在 Windows 上；
    在其他系統上，此值必須為零。
    在透過 Unix 網域通訊端連線的工作階段中，此參數會
    被忽略，且讀取值永遠為零。
<a id="GUC-TCP-KEEPALIVES-INTERVAL"></a>

`tcp_keepalives_interval` (`integer`) <a id="id-1.6.6.6.3.2.2.1.3"></a> [#](#GUC-TCP-KEEPALIVES-INTERVAL)
:   指定用戶端未確認的 TCP keepalive 訊息
    在多久之後應該重新傳送。
    若此值指定時未帶單位，則以秒為單位。
    值為 0（預設值）代表使用作業系統的預設值。
    在 Windows 上，將此值設為 0 會使此參數變成 1 秒，
    因為 Windows 沒有提供讀取系統預設值的方式。
    此參數僅在支援 `TCP_KEEPINTVL` 或等效通訊端選項的
    系統上受支援，以及在 Windows 上；
    在其他系統上，此值必須為零。
    在透過 Unix 網域通訊端連線的工作階段中，此參數會
    被忽略，且讀取值永遠為零。
<a id="GUC-TCP-KEEPALIVES-COUNT"></a>

`tcp_keepalives_count` (`integer`) <a id="id-1.6.6.6.3.2.3.1.3"></a> [#](#GUC-TCP-KEEPALIVES-COUNT)
:   指定在伺服器判定與用戶端的連線已中斷之前，
    可以遺失的 TCP keepalive 訊息數量。
    值為 0（預設值）代表使用作業系統的預設值。
    此參數僅在支援 `TCP_KEEPCNT` 或等效通訊端選項的系統上
    受支援（不含 Windows）；
    在其他系統上，此值必須為零。
    在透過 Unix 網域通訊端連線的工作階段中，此參數會
    被忽略，且讀取值永遠為零。
<a id="GUC-TCP-USER-TIMEOUT"></a>

`tcp_user_timeout` (`integer`) <a id="id-1.6.6.6.3.2.4.1.3"></a> [#](#GUC-TCP-USER-TIMEOUT)
:   指定在 TCP 連線被強制關閉之前，
    已傳送但未被確認的資料可以保留多久。
    若此值指定時未帶單位，則以毫秒為單位。
    值為 0（預設值）代表使用作業系統的預設值。
    此參數僅在支援 `TCP_USER_TIMEOUT` 的系統上
    受支援（不含 Windows）；在其他系統上，此值必須為零。
    在透過 Unix 網域通訊端連線的工作階段中，此參數會
    被忽略，且讀取值永遠為零。
<a id="GUC-CLIENT-CONNECTION-CHECK-INTERVAL"></a>

`client_connection_check_interval` (`integer`) <a id="id-1.6.6.6.3.2.5.1.3"></a> [#](#GUC-CLIENT-CONNECTION-CHECK-INTERVAL)
:   設定在執行查詢期間，選擇性檢查用戶端是否仍保持連線的
    時間間隔。此檢查是透過輪詢通訊端執行，
    若核心回報連線已關閉，則可以讓執行時間過長的查詢
    更快被中止。

    此選項依賴 Linux、macOS、illumos，
    以及 BSD 家族作業系統所提供的核心事件，
    目前在其他系統上無法使用。

    若此值指定時未帶單位，則以毫秒為單位。
    預設值為 `0`，代表停用連線
    檢查。若不進行連線檢查，伺服器只會在
    下一次與通訊端互動時（例如等待、接收或傳送資料時），
    才會偵測到連線已中斷。

    若要讓核心本身在所有情境（包括網路故障）下，
    都能在已知的時間範圍內可靠地偵測到 TCP 連線遺失，
    可能也需要調整作業系統的 TCP keepalive 設定，
    或是 PostgreSQL 的
    [tcp_keepalives_idle](runtime-config-connection.md#GUC-TCP-KEEPALIVES-IDLE)、
    [tcp_keepalives_interval](runtime-config-connection.md#GUC-TCP-KEEPALIVES-INTERVAL) 與
    [tcp_keepalives_count](runtime-config-connection.md#GUC-TCP-KEEPALIVES-COUNT) 設定。

<a id="RUNTIME-CONFIG-CONNECTION-AUTHENTICATION"></a>

### 19.3.3. 驗證 [#](#RUNTIME-CONFIG-CONNECTION-AUTHENTICATION)

<a id="GUC-AUTHENTICATION-TIMEOUT"></a>

`authentication_timeout` (`integer`) <a id="id-1.6.6.6.4.2.1.1.3"></a> <a id="id-1.6.6.6.4.2.1.1.4"></a> <a id="id-1.6.6.6.4.2.1.1.5"></a> [#](#GUC-AUTHENTICATION-TIMEOUT)
:   完成用戶端驗證所允許的最長時間。若一個
    準用戶端在這段時間內未完成驗證協定，
    伺服器就會關閉該連線。這可以防止
    卡住的用戶端無限期佔用連線。
    若此值指定時未帶單位，則以秒為單位。
    預設值為一分鐘（`1m`）。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-PASSWORD-ENCRYPTION"></a>

`password_encryption` (`enum`) <a id="id-1.6.6.6.4.2.2.1.3"></a> [#](#GUC-PASSWORD-ENCRYPTION)
:   當在 [CREATE ROLE](../../reference/sql-commands/sql-createrole.md) 或
    [ALTER ROLE](../../reference/sql-commands/sql-alterrole.md) 中指定密碼時，
    此參數決定用來加密密碼的演算法。可能的值有
    `scram-sha-256`（以 SCRAM-SHA-256
    加密密碼），以及 `md5`（將密碼
    儲存為 MD5 雜湊值）。預設值為 `scram-sha-256`。

    請注意，較舊的用戶端可能缺乏對 SCRAM 驗證
    機制的支援，因此無法搭配以
    SCRAM-SHA-256 加密的密碼運作。詳情請參閱[20.5 節](../client-authentication/auth-password.md)。

    ### 警告

    對 MD5 加密密碼的支援已被棄用，未來的
    PostgreSQL 版本將移除此支援。有關遷移到
    其他密碼類型的詳情，請參閱[20.5 節](../client-authentication/auth-password.md)。
<a id="GUC-SCRAM-ITERATIONS"></a>

`scram_iterations` (`integer`) <a id="id-1.6.6.6.4.2.3.1.3"></a> [#](#GUC-SCRAM-ITERATIONS)
:   使用 SCRAM-SHA-256 加密密碼時所執行的
    運算迭代次數。預設值為 `4096`。
    較高的迭代次數，可以為已儲存的密碼提供額外的
    保護，防止暴力破解攻擊，但也會使驗證
    速度變慢。變更此值不會影響既有的
    SCRAM-SHA-256 加密密碼，因為迭代次數是在
    加密當下就固定的。若要套用變更後的值，必須
    重新設定密碼。

    ### 注意

    如果某個角色的密碼是以不同於
    `postgresql.conf` 檔案或伺服器命令列上所指定的
    `scram_iterations` 值建立的，未經驗證的使用者
    可以透過觀察伺服器對連線嘗試回應的差異，
    察覺該角色的存在。如果你認為這是個問題，
    請確保所有角色密碼都是在
    `scram_iterations` 設為
    `postgresql.conf` 檔案或伺服器命令列上所指定值的情況下
    建立的。
<a id="GUC-MD5-PASSWORD-WARNINGS"></a>

`md5_password_warnings` (`boolean`) <a id="id-1.6.6.6.4.2.4.1.3"></a> [#](#GUC-MD5-PASSWORD-WARNINGS)
:   控制在 `CREATE ROLE` 或
    `ALTER ROLE` 陳述式設定 MD5 加密密碼時，
    是否產生關於 MD5 密碼棄用的 `WARNING`。
    預設值為 `on`。
<a id="GUC-KRB-SERVER-KEYFILE"></a>

`krb_server_keyfile` (`string`) <a id="id-1.6.6.6.4.2.5.1.3"></a> [#](#GUC-KRB-SERVER-KEYFILE)
:   設定伺服器 Kerberos 金鑰檔的位置。預設值為
    `FILE:/usr/local/pgsql/etc/krb5.keytab`
    （其中目錄部分為建置時指定的
    `sysconfdir`；可以使用
    `pg_config --sysconfdir` 判斷此值）。
    若此參數設為空字串，會被忽略，並改用
    因系統而異的預設值。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。
    詳情請參閱[20.6 節](../client-authentication/gssapi-auth.md)。
<a id="GUC-KRB-CASEINS-USERS"></a>

`krb_caseins_users` (`boolean`) <a id="id-1.6.6.6.4.2.6.1.3"></a> [#](#GUC-KRB-CASEINS-USERS)
:   設定 GSSAPI 使用者名稱是否應以
    不區分大小寫的方式處理。
    預設值為 `off`（區分大小寫）。此參數只能
    在 `postgresql.conf` 檔案中或伺服器命令列上設定。
<a id="GUC-GSS-ACCEPT-DELEGATION"></a>

`gss_accept_delegation` (`boolean`) <a id="id-1.6.6.6.4.2.7.1.3"></a> [#](#GUC-GSS-ACCEPT-DELEGATION)
:   設定是否應接受來自用戶端的 GSSAPI 委派（delegation）。
    預設值為 `off`，代表來自用戶端的憑證
    將*不會*被接受。將此值改為 `on` 會讓伺服器
    接受用戶端委派給它的憑證。此參數只能
    在 `postgresql.conf` 檔案中或伺服器命令列上設定。
<a id="GUC-OAUTH-VALIDATOR-LIBRARIES"></a>

`oauth_validator_libraries` (`string`) <a id="id-1.6.6.6.4.2.8.1.3"></a> [#](#GUC-OAUTH-VALIDATOR-LIBRARIES)
:   用於驗證 OAuth 連線權杖（token）的
    程式庫。若只提供一個驗證器程式庫，
    預設將用於所有 OAuth 連線；否則，所有
    [`oauth` HBA 項目](../client-authentication/auth-oauth.md)
    都必須從此清單中明確設定一個
    `validator`。若設為空字串（預設值），
    OAuth 連線將被拒絕。此參數只能在
    `postgresql.conf` 檔案中設定。

    驗證器模組必須另外實作／取得；
    PostgreSQL 本身不隨附任何預設
    實作。有關實作 OAuth 驗證器的更多資訊，
    請參閱[第 50 章](../../server-programming/oauth-validators/README.md)。

<a id="RUNTIME-CONFIG-CONNECTION-SSL"></a>

### 19.3.4. SSL [#](#RUNTIME-CONFIG-CONNECTION-SSL)

有關設定 SSL 的更多資訊，請參閱[18.9 節](../runtime/ssl-tcp.md)。
基於歷史因素，即使 SSL 協定本身已被棄用，
用於控制以 TLS 協定進行傳輸加密的組態設定參數，
仍然命名為
`ssl`。
在此情境中，SSL 與
TLS 可互換使用。

<a id="GUC-SSL"></a>

`ssl` (`boolean`) <a id="id-1.6.6.6.5.3.1.1.3"></a> [#](#GUC-SSL)
:   啟用 SSL 連線。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    預設值為 `off`。
<a id="GUC-SSL-CA-FILE"></a>

`ssl_ca_file` (`string`) <a id="id-1.6.6.6.5.3.2.1.3"></a> [#](#GUC-SSL-CA-FILE)
:   指定包含 SSL 伺服器憑證授權機構（CA）的
    檔案名稱。
    相對路徑是相對於資料目錄。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    預設值為空，代表不載入任何 CA 檔案，
    也不會執行用戶端憑證驗證。
<a id="GUC-SSL-CERT-FILE"></a>

`ssl_cert_file` (`string`) <a id="id-1.6.6.6.5.3.3.1.3"></a> [#](#GUC-SSL-CERT-FILE)
:   指定包含 SSL 伺服器憑證的檔案名稱。
    相對路徑是相對於資料目錄。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    預設值為 `server.crt`。
<a id="GUC-SSL-CRL-FILE"></a>

`ssl_crl_file` (`string`) <a id="id-1.6.6.6.5.3.4.1.3"></a> [#](#GUC-SSL-CRL-FILE)
:   指定包含 SSL 用戶端憑證撤銷清單
    （CRL）的檔案名稱。
    相對路徑是相對於資料目錄。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    預設值為空，代表不載入任何 CRL 檔案（除非
    設定了 [ssl_crl_dir](runtime-config-connection.md#GUC-SSL-CRL-DIR)）。
<a id="GUC-SSL-CRL-DIR"></a>

`ssl_crl_dir` (`string`) <a id="id-1.6.6.6.5.3.5.1.3"></a> [#](#GUC-SSL-CRL-DIR)
:   指定包含 SSL 用戶端憑證撤銷清單（CRL）的
    目錄名稱。相對路徑是相對於
    資料目錄。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令
    列上設定。預設值為空，代表不使用任何 CRL（除非
    設定了 [ssl_crl_file](runtime-config-connection.md#GUC-SSL-CRL-FILE)）。

    此目錄需要以
    OpenSSL 命令
    `openssl rehash` 或 `c_rehash`
    準備。詳情請參閱其
    文件。

    使用此設定時，指定目錄中的 CRL 會在連線時
    依需求載入。新的 CRL 可以隨時加入目錄，
    並會立即生效。這與 [ssl_crl_file](runtime-config-connection.md#GUC-SSL-CRL-FILE)
    不同，後者會導致該檔案中的 CRL
    在伺服器啟動時或重新載入組態設定時載入。
    這兩個設定可以搭配使用。
<a id="GUC-SSL-KEY-FILE"></a>

`ssl_key_file` (`string`) <a id="id-1.6.6.6.5.3.6.1.3"></a> [#](#GUC-SSL-KEY-FILE)
:   指定包含 SSL 伺服器私密金鑰的檔案名稱。
    相對路徑是相對於資料目錄。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    預設值為 `server.key`。
<a id="GUC-SSL-TLS13-CIPHERS"></a>

`ssl_tls13_ciphers` (`string`) <a id="id-1.6.6.6.5.3.7.1.3"></a> [#](#GUC-SSL-TLS13-CIPHERS)
:   指定使用 TLS 1.3 版連線時允許的密碼套件
    （cipher suite）清單。可以使用以冒號分隔的清單
    指定多個密碼套件。若留白，將使用
    OpenSSL 中的預設密碼套件集合。

    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令
    列上設定。
<a id="GUC-SSL-CIPHERS"></a>

`ssl_ciphers` (`string`) <a id="id-1.6.6.6.5.3.8.1.3"></a> [#](#GUC-SSL-CIPHERS)
:   指定使用 TLS 1.2 版以下連線時允許的 SSL
    密碼清單，TLS 1.3 版連線請參閱
    [ssl_tls13_ciphers](runtime-config-connection.md#GUC-SSL-TLS13-CIPHERS)。有關此設定的語法
    與支援值清單，請參閱 OpenSSL 套件中的
    ciphers
    手冊頁。預設值
    為 `HIGH:MEDIUM:+3DES:!aNULL`。除非你有
    特定的安全性需求，否則預設值通常是合理的選擇。

    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令
    列上設定。

    預設值的說明：

    <a id="GUC-SSL-CIPHERS-HIGH"></a>

    `HIGH` [#](#GUC-SSL-CIPHERS-HIGH)
    :   使用 `HIGH` 群組密碼（例如
        AES、Camellia、3DES）的密碼套件
    <a id="GUC-SSL-CIPHERS-MEDIUM"></a>

    `MEDIUM` [#](#GUC-SSL-CIPHERS-MEDIUM)
    :   使用 `MEDIUM` 群組密碼（例如 RC4、SEED）
        的密碼套件
    <a id="GUC-SSL-CIPHERS-PLUS-3DES"></a>

    `+3DES` [#](#GUC-SSL-CIPHERS-PLUS-3DES)
    :   OpenSSL 對 `HIGH` 的預設排序
        有問題，因為它將 3DES 排在
        AES128 之前。這是錯誤的，因為 3DES 提供的
        安全性低於 AES128，而且速度也慢得多。
        `+3DES` 會將其重新排序到所有其他
        `HIGH` 與 `MEDIUM` 密碼之後。
    <a id="GUC-SSL-CIPHERS-NOT-ANULL"></a>

    `!aNULL` [#](#GUC-SSL-CIPHERS-NOT-ANULL)
    :   停用不進行驗證的匿名密碼套件。這類
        密碼套件容易受到中間人（MITM）攻擊，
        因此不應使用。

    可用密碼套件的詳細內容，會因
    OpenSSL 版本而異。可以使用命令
    `openssl ciphers -v 'HIGH:MEDIUM:+3DES:!aNULL'`
    查看目前所安裝
    OpenSSL 版本的實際詳細內容。請注意，
    此清單會在執行期間根據伺服器金鑰類型進行篩選。
<a id="GUC-SSL-PREFER-SERVER-CIPHERS"></a>

`ssl_prefer_server_ciphers` (`boolean`) <a id="id-1.6.6.6.5.3.9.1.3"></a> [#](#GUC-SSL-PREFER-SERVER-CIPHERS)
:   指定是否應使用伺服器的 SSL 密碼偏好順序，
    而非用戶端的偏好順序。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    預設值為 `on`。

    9.4 之前的 PostgreSQL 版本沒有
    此設定，永遠使用用戶端的偏好順序。此設定
    主要是為了與那些版本向後相容。使用
    伺服器的偏好順序通常比較好，因為伺服器
    更有可能被妥善設定。
<a id="GUC-SSL-GROUPS"></a>

`ssl_groups` (`string`) <a id="id-1.6.6.6.5.3.10.1.3"></a> [#](#GUC-SSL-GROUPS)
:   指定用於 TLS 金鑰交換的具名群組。
    所有連線的用戶端都必須支援此群組。
    可以使用以冒號分隔的清單指定多個群組。
    此值不需要與伺服器憑證所使用的金鑰類型相符。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。
    預設值為 `X25519:prime256v1`。

    最常見群組的
    OpenSSL 名稱為：
    `prime256v1`（NIST P-256）、
    `secp384r1`（NIST P-384）、
    `secp521r1`（NIST P-521）。
    可以使用命令
    `openssl ecparam -list_curves` 顯示不完整的可用群組清單。
    不過並非所有群組都能搭配 TLS 使用，
    也省略了許多受支援的群組名稱與別名。

    在 18.0 之前的 PostgreSQL 版本中，
    此設定名為 `ssl_ecdh_curve`，且只接受
    單一值。
<a id="GUC-SSL-MIN-PROTOCOL-VERSION"></a>

`ssl_min_protocol_version` (`enum`) <a id="id-1.6.6.6.5.3.11.1.3"></a> [#](#GUC-SSL-MIN-PROTOCOL-VERSION)
:   設定要使用的最低 SSL/TLS 協定版本。目前
    合法的值有：`TLSv1`、`TLSv1.1`、
    `TLSv1.2`、`TLSv1.3`。較舊
    版本的 OpenSSL 程式庫不支援
    所有值；若選擇不支援的設定，將會引發錯誤。
    TLS 1.0 之前的協定版本，也就是 SSL 2 版與
    3 版，永遠處於停用狀態。

    預設值為 `TLSv1.2`，在撰寫本文當下
    符合業界最佳實務。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-SSL-MAX-PROTOCOL-VERSION"></a>

`ssl_max_protocol_version` (`enum`) <a id="id-1.6.6.6.5.3.12.1.3"></a> [#](#GUC-SSL-MAX-PROTOCOL-VERSION)
:   設定要使用的最高 SSL/TLS 協定版本。合法值
    與 [ssl_min_protocol_version](runtime-config-connection.md#GUC-SSL-MIN-PROTOCOL-VERSION) 相同，
    另外還可以設為空字串，代表允許任何協定版本。
    預設為允許任何版本。設定最高協定版本
    主要用於測試，或是在某些元件無法搭配較新
    協定正常運作時使用。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-SSL-DH-PARAMS-FILE"></a>

`ssl_dh_params_file` (`string`) <a id="id-1.6.6.6.5.3.13.1.3"></a> [#](#GUC-SSL-DH-PARAMS-FILE)
:   指定包含 Diffie-Hellman 參數的檔案名稱，
    用於所謂的暫時性 DH（ephemeral DH）系列 SSL 密碼。預設值為
    空，此時會使用編譯時內建的預設 DH 參數。使用
    自訂 DH 參數，可以在攻擊者成功破解眾所周知的
    內建 DH 參數時，降低曝險程度。你可以使用命令
    `openssl dhparam -out dhparams.pem 2048`
    建立自己的 DH 參數檔案。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-SSL-PASSPHRASE-COMMAND"></a>

`ssl_passphrase_command` (`string`) <a id="id-1.6.6.6.5.3.14.1.3"></a> [#](#GUC-SSL-PASSPHRASE-COMMAND)
:   設定當需要取得用於解密 SSL 檔案（例如私密金鑰）的
    密碼短語（passphrase）時，要呼叫的外部命令。
    根據預設，此參數為空，代表使用內建的
    提示機制。

    此命令必須將密碼短語輸出到標準輸出，並以
    代碼 0 結束。在參數值中，`%p` 會被
    替換為提示字串。（若要輸出字面上的
    `%`，請寫成 `%%`。）請注意，提示
    字串很可能包含空白字元，因此請務必妥善加上引號。
    若輸出結尾有換行字元，會被移除一個。

    此命令實際上不必真的向使用者提示輸入
    密碼短語，可以從檔案讀取、從金鑰圈（keychain）
    機制取得，或以類似方式取得。至於所選機制
    是否具備足夠的安全性，則由使用者自行負責確保。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-SSL-PASSPHRASE-COMMAND-SUPPORTS-RELOAD"></a>

`ssl_passphrase_command_supports_reload` (`boolean`) <a id="id-1.6.6.6.5.3.15.1.3"></a> [#](#GUC-SSL-PASSPHRASE-COMMAND-SUPPORTS-RELOAD)
:   此參數決定當金鑰檔案需要密碼短語時，
    是否也會在重新載入組態設定期間呼叫由
    `ssl_passphrase_command` 設定的密碼短語命令。
    若此參數為 `off`（預設值），則
    `ssl_passphrase_command` 在重新載入期間將被
    忽略，若需要密碼短語，SSL 組態設定將不會
    重新載入。此設定適用於需要 TTY 進行提示的
    命令，因為伺服器執行時 TTY 可能不可用。
    若密碼短語是例如從檔案取得的，將此參數設為 on
    可能較為合適。

    在 Windows 上執行時，此參數必須設為
    `on`，因為該平台不同的程序模型，
    會使所有連線都執行組態設定重新載入。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-connection.html)（原文版本：18.6；核對日期：2026-09-24）
