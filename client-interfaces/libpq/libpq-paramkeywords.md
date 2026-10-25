<a id="LIBPQ-PARAMKEYWORDS"></a>

## 32.1.2. 參數關鍵字 [#](#libpq-paramkeywords) <a href="#libpq-paramkeywords" id="libpq-paramkeywords"></a>

目前可辨識的參數關鍵字如下：

<a id="LIBPQ-CONNECT-HOST"></a>

### `host` [#](#libpq-connect-host) <a href="#libpq-connect-host" id="libpq-connect-host"></a>

要連線的主機名稱。<a id="id-1.7.3.8.4.2.1.1.2.1.1"></a>如果主機名稱看起來像絕對路徑名稱，它代表使用 Unix 網域通訊而非 TCP/IP 通訊；其值為存放通訊端檔案的目錄名稱。（在 Unix 上，絕對路徑名稱以斜線開頭。在 Windows 上，以磁碟機代號開頭的路徑也會被辨識。）如果主機名稱以 `@` 開頭，它會被視為抽象命名空間中的 Unix 網域通訊端（目前在 Linux 與 Windows 上支援）。未指定 `host` 或其為空時，預設行為是連線到 `/tmp`（或建置 PostgreSQL 時所指定的任何通訊端目錄）中的 Unix 網域通訊端<a id="id-1.7.3.8.4.2.1.1.2.1.4"></a>。在 Windows 上，預設是連線到 `localhost`。

也接受以逗號分隔的主機名稱清單，此時會依序嘗試清單中的每個主機名稱；清單中的空項目會選用上述的預設行為。詳細資訊請參閱[第 32.1.1.3 節](libpq-connstring.md#libpq-multiple-hosts)。

<a id="LIBPQ-CONNECT-HOSTADDR"></a>

### `hostaddr` [#](#libpq-connect-hostaddr) <a href="#libpq-connect-hostaddr" id="libpq-connect-hostaddr"></a>

要連線之主機的數字 IP 位址。它應該採用標準的 IPv4 位址格式，例如 `172.28.40.9`。如果你的機器支援 IPv6，也可以使用 IPv6 位址。當此參數指定為非空字串時，一律使用 TCP/IP 通訊。如果未指定此參數，會查詢 `host` 的值以找出對應的 IP 位址；或者，如果 `host` 指定的是 IP 位址，就直接使用該值。

使用 `hostaddr` 可讓應用程式避免查詢主機名稱，這對有時間限制的應用程式可能很重要。不過，GSSAPI 或 SSPI 認證方法，以及 `verify-full` SSL 憑證驗證，都需要主機名稱。適用下列規則：

* 如果指定了 `host` 而沒有指定 `hostaddr`，就會進行主機名稱查詢。（使用 `PQconnectPoll` 時，查詢會在 `PQconnectPoll` 第一次處理此主機名稱時進行，而且可能導致 `PQconnectPoll` 阻塞相當長的時間。）
* 如果指定了 `hostaddr` 而沒有指定 `host`，`hostaddr` 的值即為伺服器的網路位址。如果認證方法需要主機名稱，連線嘗試將會失敗。
* 如果同時指定了 `host` 與 `hostaddr`，`hostaddr` 的值即為伺服器的網路位址。除非認證方法需要，否則 `host` 的值會被忽略；若認證方法需要，則它會被用作主機名稱。

請注意，如果 `host` 不是網路位址 `hostaddr` 上伺服器的名稱，認證很可能會失敗。此外，當同時指定了 `host` 與 `hostaddr` 時，會使用 `host` 在密碼檔中識別此連線（請參閱[第 32.16 節](libpq-pgpass.md)）。

也接受以逗號分隔的 `hostaddr` 值清單，此時會依序嘗試清單中的每個主機。清單中的空項目會使用對應的主機名稱；如果該主機名稱也是空的，則使用預設主機名稱。詳細資訊請參閱[第 32.1.1.3 節](libpq-connstring.md#libpq-multiple-hosts)。

如果既沒有主機名稱也沒有主機位址，libpq 會使用本機的 Unix 網域通訊端連線；在 Windows 上，則會嘗試連線到 `localhost`。

<a id="LIBPQ-CONNECT-PORT"></a>

### `port` [#](#libpq-connect-port) <a href="#libpq-connect-port" id="libpq-connect-port"></a>

伺服器主機上要連線的連接埠號碼，或 Unix 網域連線所用的通訊端檔名副檔名。<a id="id-1.7.3.8.4.2.1.3.2.1.1"></a>如果在 `host` 或 `hostaddr` 參數中提供了多個主機，此參數可以指定一個與主機清單等長、以逗號分隔的連接埠清單，也可以指定一個用於所有主機的單一連接埠號碼。空字串或以逗號分隔之清單中的空項目，代表建置 PostgreSQL 時所設定的預設連接埠號碼。

<a id="LIBPQ-CONNECT-DBNAME"></a>

### `dbname` [#](#libpq-connect-dbname) <a href="#libpq-connect-dbname" id="libpq-connect-dbname"></a>

資料庫名稱。預設與使用者名稱相同。在某些情境下，會檢查此值是否為延伸格式；這些格式的更多細節請參閱[第 32.1.1 節](libpq-connstring.md#libpq-connstring)。

<a id="LIBPQ-CONNECT-USER"></a>

### `user` [#](#libpq-connect-user) <a href="#libpq-connect-user" id="libpq-connect-user"></a>

用來連線的 PostgreSQL 使用者名稱。預設與執行應用程式之使用者的作業系統名稱相同。

<a id="LIBPQ-CONNECT-PASSWORD"></a>

### `password` [#](#libpq-connect-password) <a href="#libpq-connect-password" id="libpq-connect-password"></a>

伺服器要求密碼認證時所使用的密碼。

<a id="LIBPQ-CONNECT-PASSFILE"></a>

### `passfile` [#](#libpq-connect-passfile) <a href="#libpq-connect-passfile" id="libpq-connect-passfile"></a>

指定用來儲存密碼之檔案的名稱（請參閱[第 32.16 節](libpq-pgpass.md)）。預設為 `~/.pgpass`，在 Microsoft Windows 上則為 `%APPDATA%\postgresql\pgpass.conf`。（如果此檔案不存在，不會回報錯誤。）

<a id="LIBPQ-CONNECT-REQUIRE-AUTH"></a>

### `require_auth` [#](#libpq-connect-require-auth) <a href="#libpq-connect-require-auth" id="libpq-connect-require-auth"></a>

指定用戶端要求伺服器使用的認證方法。如果伺服器沒有使用所要求的方法來認證用戶端，或者伺服器沒有完整完成認證交握，連線就會失敗。也可以提供以逗號分隔的方法清單，伺服器必須恰好使用其中一種方法，連線才會成功。預設情況下，接受任何認證方法，而且伺服器可以完全略過認證。

方法可以加上 `!` 前綴來表示否定，此時伺服器*不得*嘗試所列的方法；接受任何其他方法，而且伺服器可以完全不認證用戶端。如果提供的是以逗號分隔的清單，伺服器不得嘗試所列否定方法中的*任何*一種。否定形式與非否定形式不可在同一個設定中混用。

最後一個特殊情況是，`none` 方法要求伺服器不得使用認證挑戰。（它也可以被否定，以要求某種形式的認證。）

可以指定下列方法：

- `password`

  伺服器必須要求明文密碼認證。

- `md5`

  伺服器必須要求 MD5 雜湊密碼認證。

  #### 警告

  MD5 加密密碼的支援已被棄用，並將在 PostgreSQL 的未來版本中移除。關於遷移到其他密碼類型的細節，請參閱[第 20.5 節](../../server-administration/client-authentication/auth-password.md)。

- `gss`

  伺服器必須透過 GSSAPI 要求 Kerberos 交握，或建立 GSS 加密通道（另請參閱 [gssencmode](libpq-paramkeywords.md#libpq-connect-gssencmode)）。

- `sspi`

  伺服器必須要求 Windows SSPI 認證。

- `scram-sha-256`

  伺服器必須與用戶端成功完成 SCRAM-SHA-256 認證交換。

- `oauth`

  伺服器必須向用戶端要求 OAuth 持有者權杖。

- `none`

  伺服器不得要求用戶端進行認證交換。（這既不禁止透過 TLS 的用戶端憑證認證，也不禁止透過其加密傳輸的 GSS 認證。）

<a id="LIBPQ-CONNECT-CHANNEL-BINDING"></a>

### `channel_binding` [#](#libpq-connect-channel-binding) <a href="#libpq-connect-channel-binding" id="libpq-connect-channel-binding"></a>

此選項控制用戶端對通道綁定的使用。設定為 `require` 表示連線必須採用通道綁定；`prefer` 表示若可用，用戶端會選擇通道綁定；`disable` 則禁止使用通道綁定。如果 PostgreSQL 編譯時有 SSL 支援，預設值為 `prefer`；否則預設值為 `disable`。

通道綁定是伺服器向用戶端認證自身的一種方法。只有在透過 SSL 連線、連到使用 `SCRAM` 認證方法的 PostgreSQL 11 或更新版本伺服器時，才支援此功能。

<a id="LIBPQ-CONNECT-CONNECT-TIMEOUT"></a>

### `connect_timeout` [#](#libpq-connect-connect-timeout) <a href="#libpq-connect-connect-timeout" id="libpq-connect-connect-timeout"></a>

連線時等待的最長時間，以秒為單位（寫成十進位整數，例如 `10`）。零、負值或未指定表示無限期等待。此逾時分別套用於每個主機名稱或 IP 位址。例如，如果你指定了兩個主機，且 `connect_timeout` 為 5，那麼每個主機在 5 秒內沒有建立連線就會逾時，因此等待連線所花的總時間最多可能達 10 秒。

<a id="LIBPQ-CONNECT-CLIENT-ENCODING"></a>

### `client_encoding` [#](#libpq-connect-client-encoding) <a href="#libpq-connect-client-encoding" id="libpq-connect-client-encoding"></a>

為此連線設定 `client_encoding` 組態參數。除了對應的伺服器選項所接受的值之外，你也可以使用 `auto`，從用戶端目前的區域設定（在 Unix 系統上為 `LC_CTYPE` 環境變數）判斷正確的編碼。

<a id="LIBPQ-CONNECT-OPTIONS"></a>

### `options` [#](#libpq-connect-options) <a href="#libpq-connect-options" id="libpq-connect-options"></a>

指定在連線開始時要傳送給伺服器的命令列選項。例如，將此設為 `-c geqo=off` 或 `--geqo=off`，會將工作階段中 `geqo` 參數的值設為 `off`。此字串中的空白會被視為命令列引數的分隔符，除非以反斜線（`\`）跳脫；要表示字面上的反斜線，請寫 `\\`。關於可用選項的詳細討論，請參閱[第 19 章](../../server-administration/runtime-config/README.md)。

<a id="LIBPQ-CONNECT-APPLICATION-NAME"></a>

### `application_name` [#](#libpq-connect-application-name) <a href="#libpq-connect-application-name" id="libpq-connect-application-name"></a>

指定 [application_name](../../server-administration/runtime-config/runtime-config-logging.md#GUC-APPLICATION-NAME) 組態參數的值。

<a id="LIBPQ-CONNECT-FALLBACK-APPLICATION-NAME"></a>

### `fallback_application_name` [#](#libpq-connect-fallback-application-name) <a href="#libpq-connect-fallback-application-name" id="libpq-connect-fallback-application-name"></a>

指定 [application_name](../../server-administration/runtime-config/runtime-config-logging.md#GUC-APPLICATION-NAME) 組態參數的備用值。如果沒有透過連線參數或 `PGAPPNAME` 環境變數為 `application_name` 提供值，就會使用此值。對於希望設定預設應用程式名稱、但允許使用者覆寫的通用工具程式而言，指定備用名稱很有用。

<a id="LIBPQ-KEEPALIVES"></a>

### `keepalives` [#](#libpq-keepalives) <a href="#libpq-keepalives" id="libpq-keepalives"></a>

控制是否使用用戶端的 TCP keepalive。預設值為 1，表示開啟；但如果不需要 keepalive，你可以將它改為 0，表示關閉。對於透過 Unix 網域通訊端建立的連線，此參數會被忽略。

<a id="LIBPQ-KEEPALIVES-IDLE"></a>

### `keepalives_idle` [#](#libpq-keepalives-idle) <a href="#libpq-keepalives-idle" id="libpq-keepalives-idle"></a>

控制閒置多少秒之後，TCP 應該向伺服器傳送 keepalive 訊息。值為零表示使用系統預設值。對於透過 Unix 網域通訊端建立的連線，或者停用了 keepalive 時，此參數會被忽略。只有在提供 `TCP_KEEPIDLE` 或同等通訊端選項的系統上，以及在 Windows 上才支援此參數；在其他系統上沒有作用。

<a id="LIBPQ-KEEPALIVES-INTERVAL"></a>

### `keepalives_interval` [#](#libpq-keepalives-interval) <a href="#libpq-keepalives-interval" id="libpq-keepalives-interval"></a>

控制未獲伺服器確認的 TCP keepalive 訊息應在多少秒之後重新傳送。值為零表示使用系統預設值。對於透過 Unix 網域通訊端建立的連線，或者停用了 keepalive 時，此參數會被忽略。只有在提供 `TCP_KEEPINTVL` 或同等通訊端選項的系統上，以及在 Windows 上才支援此參數；在其他系統上沒有作用。

<a id="LIBPQ-KEEPALIVES-COUNT"></a>

### `keepalives_count` [#](#libpq-keepalives-count) <a href="#libpq-keepalives-count" id="libpq-keepalives-count"></a>

控制在用戶端與伺服器的連線被視為中斷之前，可以遺失多少個 TCP keepalive。值為零表示使用系統預設值。對於透過 Unix 網域通訊端建立的連線，或者停用了 keepalive 時，此參數會被忽略。只有在提供 `TCP_KEEPCNT` 或同等通訊端選項的系統上才支援此參數；在其他系統上沒有作用。

<a id="LIBPQ-TCP-USER-TIMEOUT"></a>

### `tcp_user_timeout` [#](#libpq-tcp-user-timeout) <a href="#libpq-tcp-user-timeout" id="libpq-tcp-user-timeout"></a>

控制已傳送的資料在連線被強制關閉之前，可以維持未確認狀態多少毫秒。值為零表示使用系統預設值。對於透過 Unix 網域通訊端建立的連線，此參數會被忽略。只有在提供 `TCP_USER_TIMEOUT` 的系統上才支援此參數；在其他系統上沒有作用。

<a id="LIBPQ-CONNECT-REPLICATION"></a>

### `replication` [#](#libpq-connect-replication) <a href="#libpq-connect-replication" id="libpq-connect-replication"></a>

此選項決定連線是否應該使用複寫協定而非一般協定。PostgreSQL 的複寫連線以及 pg_basebackup 等工具在內部使用的就是這個協定，但第三方應用程式也可以使用它。關於複寫協定的說明，請參閱[第 54.4 節](../../internals/protocol/protocol-replication.md)。

支援下列值，不區分大小寫：

- `true`, `on`, `yes`, `1`

  連線進入實體複寫模式。

- `database`

  連線進入邏輯複寫模式，連線到 `dbname` 參數所指定的資料庫。

- `false`, `off`, `no`, `0`

  連線為一般連線，這是預設行為。

在實體或邏輯複寫模式中，只能使用簡單查詢協定。

<a id="LIBPQ-CONNECT-GSSENCMODE"></a>

### `gssencmode` [#](#libpq-connect-gssencmode) <a href="#libpq-connect-gssencmode" id="libpq-connect-gssencmode"></a>

此選項決定是否要與伺服器協商安全的 GSS TCP/IP 連線，或以何種優先順序協商。共有三種模式：

- `disable`

  只嘗試未使用 GSSAPI 加密的連線

- `prefer`（預設）

  如果存在 GSSAPI 憑證（也就是在憑證快取中），先嘗試 GSSAPI 加密連線；如果失敗或沒有憑證，再嘗試未使用 GSSAPI 加密的連線。當 PostgreSQL 編譯時有 GSSAPI 支援，這是預設值。

- `require`

  只嘗試 GSSAPI 加密連線

對於 Unix 網域通訊端通訊，`gssencmode` 會被忽略。如果 PostgreSQL 編譯時沒有 GSSAPI 支援，使用 `require` 選項會導致錯誤，而 `prefer` 雖會被接受，但 libpq 實際上不會嘗試 GSSAPI 加密連線。<a id="id-1.7.3.8.4.2.1.21.2.2.7"></a>

<a id="LIBPQ-CONNECT-SSLMODE"></a>

### `sslmode` [#](#libpq-connect-sslmode) <a href="#libpq-connect-sslmode" id="libpq-connect-sslmode"></a>

此選項決定是否要與伺服器協商安全的 SSL TCP/IP 連線，或以何種優先順序協商。共有六種模式：

- `disable`

  只嘗試非 SSL 連線

- `allow`

  先嘗試非 SSL 連線；如果失敗，再嘗試 SSL 連線

- `prefer`（預設）

  先嘗試 SSL 連線；如果失敗，再嘗試非 SSL 連線

- `require`

  只嘗試 SSL 連線。如果存在根 CA 檔，就以與指定 `verify-ca` 時相同的方式驗證憑證

- `verify-ca`

  只嘗試 SSL 連線，並驗證伺服器憑證是由受信任的憑證授權單位（CA）所簽發

- `verify-full`

  只嘗試 SSL 連線，驗證伺服器憑證是由受信任的 CA 所簽發，並且所要求的伺服器主機名稱與憑證中的名稱相符

關於這些選項如何運作的詳細說明，請參閱[第 32.19 節](libpq-ssl.md)。

對於 Unix 網域通訊端通訊，`sslmode` 會被忽略。如果 PostgreSQL 編譯時沒有 SSL 支援，使用 `require`、`verify-ca` 或 `verify-full` 選項會導致錯誤，而 `allow` 與 `prefer` 選項雖會被接受，但 libpq 實際上不會嘗試 SSL 連線。<a id="id-1.7.3.8.4.2.1.22.2.2.10"></a>

請注意，如果可以使用 GSSAPI 加密，無論 `sslmode` 的值為何，都會優先使用它而非 SSL 加密。要在具有可運作之 GSSAPI 基礎架構（例如 Kerberos 伺服器）的環境中強制使用 SSL 加密，請同時將 `gssencmode` 設為 `disable`。

<a id="LIBPQ-CONNECT-REQUIRESSL"></a>

### `requiressl` [#](#libpq-connect-requiressl) <a href="#libpq-connect-requiressl" id="libpq-connect-requiressl"></a>

此選項已被棄用，請改用 `sslmode` 設定。

如果設為 1，就要求與伺服器建立 SSL 連線（這等同於 `sslmode` `require`）。此時如果伺服器不接受 SSL 連線，libpq 會拒絕連線。如果設為 0（預設），libpq 會與伺服器協商連線類型（等同於 `sslmode` `prefer`）。只有在 PostgreSQL 編譯時有 SSL 支援的情況下，才能使用此選項。

<a id="LIBPQ-CONNECT-SSLNEGOTIATION"></a>

### `sslnegotiation` [#](#libpq-connect-sslnegotiation) <a href="#libpq-connect-sslnegotiation" id="libpq-connect-sslnegotiation"></a>

如果使用 SSL，此選項控制如何與伺服器協商 SSL 加密。在預設的 `postgres` 模式中，用戶端會先詢問伺服器是否支援 SSL。在 `direct` 模式中，用戶端會在建立 TCP/IP 連線後直接開始標準的 SSL 交握。傳統的 PostgreSQL 協定協商對於各種伺服器設定最具彈性。如果已知伺服器支援直接 SSL 連線，後者可以少一次往返，降低連線延遲，也允許使用與協定無關的 SSL 網路工具。直接 SSL 選項是在 PostgreSQL 第 17 版引入的。

- `postgres`

  執行 PostgreSQL 協定協商。如果未提供此選項，這是預設值。

- `direct`

  在建立 TCP/IP 連線後直接開始 SSL 交握。只有在 `sslmode=require` 或更高等級時才允許這麼做，因為較弱的設定可能在伺服器不支援直接 SSL 交握時，導致非預期地退回明文認證。

<a id="LIBPQ-CONNECT-SSLCOMPRESSION"></a>

### `sslcompression` [#](#libpq-connect-sslcompression) <a href="#libpq-connect-sslcompression" id="libpq-connect-sslcompression"></a>

如果設為 1，透過 SSL 連線傳送的資料會被壓縮。如果設為 0，則停用壓縮。預設值為 0。如果建立的是沒有 SSL 的連線，此參數會被忽略。

SSL 壓縮如今被認為不安全，已不再建議使用。OpenSSL 1.1.0 預設停用壓縮，許多作業系統發行版在更早的版本中也停用了壓縮，因此如果伺服器不接受壓縮，將此參數設為開啟不會有任何效果。PostgreSQL 14 已在後端完全停用壓縮。

如果安全性不是首要考量，在網路是瓶頸的情況下，壓縮可以提升傳輸量。如果 CPU 效能是限制因素，停用壓縮可以改善回應時間與傳輸量。

<a id="LIBPQ-CONNECT-SSLCERT"></a>

### `sslcert` [#](#libpq-connect-sslcert) <a href="#libpq-connect-sslcert" id="libpq-connect-sslcert"></a>

此參數指定用戶端 SSL 憑證的檔案名稱，取代預設的 `~/.postgresql/postgresql.crt`。如果沒有建立 SSL 連線，此參數會被忽略。

<a id="LIBPQ-CONNECT-SSLKEY"></a>

### `sslkey` [#](#libpq-connect-sslkey) <a href="#libpq-connect-sslkey" id="libpq-connect-sslkey"></a>

此參數指定用戶端憑證所用之私密金鑰的位置。它可以指定一個檔案名稱，用來取代預設的 `~/.postgresql/postgresql.key`；也可以指定從外部「引擎」取得的金鑰（引擎是 OpenSSL 的可載入模組）。外部引擎的指定應由以冒號分隔的引擎名稱與引擎特定的金鑰識別碼組成。如果沒有建立 SSL 連線，此參數會被忽略。

<a id="LIBPQ-CONNECT-SSLKEYLOGFILE"></a>

### `sslkeylogfile` [#](#libpq-connect-sslkeylogfile) <a href="#libpq-connect-sslkeylogfile" id="libpq-connect-sslkeylogfile"></a>

此參數指定 libpq 記錄此 SSL 上下文中所用金鑰的位置。這對於使用 Wireshark 等網路檢測工具對 PostgreSQL 協定互動或用戶端連線進行除錯很有用。如果沒有建立 SSL 連線，或者使用的是 LibreSSL（LibreSSL 不支援金鑰記錄），此參數會被忽略。金鑰會以 NSS 格式記錄。

#### 警告

金鑰記錄會在金鑰記錄檔（keylog file）中暴露可能敏感的資訊。金鑰記錄檔應該與 [sslkey](libpq-paramkeywords.md#libpq-connect-sslkey) 檔案一樣謹慎處理。

<a id="LIBPQ-CONNECT-SSLPASSWORD"></a>

### `sslpassword` [#](#libpq-connect-sslpassword) <a href="#libpq-connect-sslpassword" id="libpq-connect-sslpassword"></a>

此參數指定 `sslkey` 中所指定之私密金鑰的密碼，讓用戶端憑證的私鑰即使在無法實際以互動方式輸入通關密語時，也能以加密形式儲存在磁碟上。

以任何非空值指定此參數，都會抑制 OpenSSL 在加密的用戶端憑證金鑰提供給 libpq 時預設會發出的 `Enter PEM pass phrase:` 提示。

如果金鑰沒有加密，此參數會被忽略。此參數對由 OpenSSL 引擎指定的金鑰沒有作用，除非該引擎使用 OpenSSL 的密碼回呼機制來進行提示。

此選項沒有對應的環境變數，也沒有在 `.pgpass` 中查詢它的機制。它可以用在服務檔的連線定義中。用途較複雜的使用者應該考慮使用 OpenSSL 引擎，以及 PKCS#11 或 USB 加密卸載裝置等工具。

<a id="LIBPQ-CONNECT-SSLCERTMODE"></a>

### `sslcertmode` [#](#libpq-connect-sslcertmode) <a href="#libpq-connect-sslcertmode" id="libpq-connect-sslcertmode"></a>

此選項決定是否可以將用戶端憑證傳送給伺服器，以及伺服器是否必須要求憑證。共有三種模式：

- `disable`

  即使有可用的用戶端憑證（位於預設位置或透過 [sslcert](libpq-paramkeywords.md#libpq-connect-sslcert) 提供），也絕不傳送。

- `allow`（預設）

  如果伺服器要求憑證，而且用戶端有憑證可傳送，就可以傳送憑證。

- `require`

  伺服器*必須*要求憑證。如果用戶端沒有傳送憑證，而伺服器仍成功認證了用戶端，連線就會失敗。

#### 注意

`sslcertmode=require` 並不會增加任何額外的安全性，因為無法保證伺服器會正確驗證憑證；無論 PostgreSQL 伺服器是否驗證用戶端的 TLS 憑證，通常都會向用戶端要求憑證。在為較複雜的 TLS 設定進行疑難排解時，此選項可能有用。

<a id="LIBPQ-CONNECT-SSLROOTCERT"></a>

### `sslrootcert` [#](#libpq-connect-sslrootcert) <a href="#libpq-connect-sslrootcert" id="libpq-connect-sslrootcert"></a>

此參數指定包含 SSL 憑證授權單位（CA）憑證的檔案名稱。如果該檔案存在，會驗證伺服器的憑證是否由這些授權單位之一所簽署。預設值為 `~/.postgresql/root.crt`。

也可以改為指定特殊值 `system`，此時會載入 SSL 實作所提供的受信任 CA 根憑證。這些根憑證的確切位置因 SSL 實作與平台而異。特別是對 OpenSSL 而言，這些位置還可以再由 `SSL_CERT_DIR` 與 `SSL_CERT_FILE` 環境變數修改。

#### 注意

使用 `sslrootcert=system` 時，預設的 `sslmode` 會改為 `verify-full`，而任何較弱的設定都會導致錯誤。在大多數情況下，任何人都能輕易地為自己所控制的主機名稱取得受系統信任的憑證，使得 `verify-ca` 及所有更弱的模式毫無用處。

特殊的 `system` 值會優先於同名的本機憑證檔。如果因為某些原因你遇到這種情況，請改用其他路徑，例如 `sslrootcert=./system`。

<a id="LIBPQ-CONNECT-SSLCRL"></a>

### `sslcrl` [#](#libpq-connect-sslcrl) <a href="#libpq-connect-sslcrl" id="libpq-connect-sslcrl"></a>

此參數指定 SSL 伺服器憑證撤銷清單（CRL）的檔案名稱。在嘗試認證伺服器憑證時，會拒絕此檔案（若存在）中所列的憑證。如果 [sslcrl](libpq-paramkeywords.md#libpq-connect-sslcrl) 與 [sslcrldir](libpq-paramkeywords.md#libpq-connect-sslcrldir) 都沒有設定，此設定會被視為 `~/.postgresql/root.crl`。

<a id="LIBPQ-CONNECT-SSLCRLDIR"></a>

### `sslcrldir` [#](#libpq-connect-sslcrldir) <a href="#libpq-connect-sslcrldir" id="libpq-connect-sslcrldir"></a>

此參數指定 SSL 伺服器憑證撤銷清單（CRL）的目錄名稱。在嘗試認證伺服器憑證時，會拒絕此目錄（若存在）中各檔案所列的憑證。

此目錄需要以 OpenSSL 命令 `openssl rehash` 或 `c_rehash` 準備。詳細資訊請參閱其文件。

`sslcrl` 與 `sslcrldir` 可以同時指定。

<a id="LIBPQ-CONNECT-SSLSNI"></a>

### `sslsni`<a id="id-1.7.3.8.4.2.1.34.1.2"></a> [#](#libpq-connect-sslsni) <a href="#libpq-connect-sslsni" id="libpq-connect-sslsni"></a>

如果設為 1（預設），libpq 會在啟用 SSL 的連線上設定 TLS 擴充「伺服器名稱指示」（Server Name Indication，SNI）。將此參數設為 0 即可關閉此功能。

支援 SSL 的代理伺服器可以利用伺服器名稱指示來路由連線，而不必解密 SSL 串流。（請注意，除非代理伺服器能夠識別 PostgreSQL 協定交握，否則這需要將 `sslnegotiation` 設為 `direct`。）不過，SNI 會讓目的主機名稱以明文出現在網路流量中，因此在某些情況下可能並不理想。

<a id="LIBPQ-CONNECT-REQUIREPEER"></a>

### `requirepeer` [#](#libpq-connect-requirepeer) <a href="#libpq-connect-requirepeer" id="libpq-connect-requirepeer"></a>

此參數指定伺服器的作業系統使用者名稱，例如 `requirepeer=postgres`。建立 Unix 網域通訊端連線時，如果設定了此參數，用戶端會在連線開始時檢查伺服器程序是否以指定的使用者名稱執行；如果不是，連線會因錯誤而中止。此參數可用來提供伺服器認證，類似於 TCP/IP 連線上以 SSL 憑證所提供的認證。（請注意，如果 Unix 網域通訊端位於 `/tmp` 或其他可被公眾寫入的位置，任何使用者都可以啟動一個在該處監聽的伺服器。請使用此參數確保你所連線的是由受信任使用者執行的伺服器。）只有在已實作 `peer` 認證方法的平台上才支援此選項；請參閱[第 20.9 節](../../server-administration/client-authentication/auth-peer.md)。

<a id="LIBPQ-CONNECT-SSL-MIN-PROTOCOL-VERSION"></a>

### `ssl_min_protocol_version` [#](#libpq-connect-ssl-min-protocol-version) <a href="#libpq-connect-ssl-min-protocol-version" id="libpq-connect-ssl-min-protocol-version"></a>

此參數指定連線所允許的最低 SSL/TLS 協定版本。有效值為 `TLSv1`、`TLSv1.1`、`TLSv1.2` 與 `TLSv1.3`。所支援的協定取決於所使用的 OpenSSL 版本，較舊的版本不支援最新的協定版本。如果未指定，預設值為 `TLSv1.2`，這符合撰寫本文時的業界最佳實務。

<a id="LIBPQ-CONNECT-SSL-MAX-PROTOCOL-VERSION"></a>

### `ssl_max_protocol_version` [#](#libpq-connect-ssl-max-protocol-version) <a href="#libpq-connect-ssl-max-protocol-version" id="libpq-connect-ssl-max-protocol-version"></a>

此參數指定連線所允許的最高 SSL/TLS 協定版本。有效值為 `TLSv1`、`TLSv1.1`、`TLSv1.2` 與 `TLSv1.3`。所支援的協定取決於所使用的 OpenSSL 版本，較舊的版本不支援最新的協定版本。如果未設定，此參數會被忽略，連線將使用後端所定義的上限（如果有設定的話）。設定最高協定版本主要用於測試，或某些元件在使用較新的協定時有問題的情況。

<a id="LIBPQ-CONNECT-MIN-PROTOCOL-VERSION"></a>

### `min_protocol_version` [#](#libpq-connect-min-protocol-version) <a href="#libpq-connect-min-protocol-version" id="libpq-connect-min-protocol-version"></a>

指定連線所允許的最低協定版本。預設允許 libpq 所支援的任何 PostgreSQL 協定版本，目前也就是 `3.0`。如果伺服器連這個協定版本都不支援，連線將會被關閉。

目前支援的值為 `3.0`、`3.2` 與 `latest`。`latest` 值等同於所使用之 libpq 版本所支援的最新協定版本，目前為 `3.2`。

<a id="LIBPQ-CONNECT-MAX-PROTOCOL-VERSION"></a>

### `max_protocol_version` [#](#libpq-connect-max-protocol-version) <a href="#libpq-connect-max-protocol-version" id="libpq-connect-max-protocol-version"></a>

指定要向伺服器請求的協定版本。預設使用 PostgreSQL 協定的 `3.0` 版，除非連線字串指定了依賴更高協定版本的功能，此時會使用 libpq 所支援的最新版本。如果伺服器不支援用戶端所請求的協定版本，連線會自動降級為伺服器所支援的較低次要協定版本。連線嘗試完成後，你可以使用 [`PQfullProtocolVersion`](libpq-status.md#libpq-pqfullprotocolversion) 找出實際協商出的確切協定版本。

目前支援的值為 `3.0`、`3.2` 與 `latest`。`latest` 值等同於所使用之 libpq 版本所支援的最新協定版本，目前為 `3.2`。

<a id="LIBPQ-CONNECT-KRBSRVNAME"></a>

### `krbsrvname` [#](#libpq-connect-krbsrvname) <a href="#libpq-connect-krbsrvname" id="libpq-connect-krbsrvname"></a>

以 GSSAPI 進行認證時所使用的 Kerberos 服務名稱。它必須與伺服器設定中所指定的服務名稱相符，Kerberos 認證才能成功。（另請參閱[第 20.6 節](../../server-administration/client-authentication/gssapi-auth.md)。）預設值通常是 `postgres`，但可以在建置 PostgreSQL 時透過 configure 的 `--with-krb-srvnam` 選項變更。在大多數環境中，此參數從來不需要變更。某些 Kerberos 實作可能需要不同的服務名稱，例如 Microsoft Active Directory 要求服務名稱為大寫（`POSTGRES`）。

<a id="LIBPQ-CONNECT-GSSLIB"></a>

### `gsslib` [#](#libpq-connect-gsslib) <a href="#libpq-connect-gsslib" id="libpq-connect-gsslib"></a>

用於 GSSAPI 認證的 GSS 函式庫。目前除了同時包含 GSSAPI 與 SSPI 支援的 Windows 建置版本之外，此參數都會被忽略。在該情況下，將此參數設為 `gssapi`，可讓 libpq 使用 GSSAPI 函式庫進行認證，而不是使用預設的 SSPI。

<a id="LIBPQ-CONNECT-GSSDELEGATION"></a>

### `gssdelegation` [#](#libpq-connect-gssdelegation) <a href="#libpq-connect-gssdelegation" id="libpq-connect-gssdelegation"></a>

將 GSS 憑證轉送（委派）給伺服器。預設值為 `0`，表示不會將憑證轉送給伺服器。將此設為 `1`，可在可能時轉送憑證。

<a id="LIBPQ-CONNECT-SCRAM-CLIENT-KEY"></a>

### `scram_client_key` [#](#libpq-connect-scram-client-key) <a href="#libpq-connect-scram-client-key" id="libpq-connect-scram-client-key"></a>

以 base64 編碼的 SCRAM 用戶端金鑰。外部資料包裝器或類似的中介軟體可以用它來啟用 SCRAM 直通（pass-through）認證。其中一種實作請參閱[第 F.38.1.10 節](../../appendixes/contrib/postgres-fdw.md#POSTGRES-FDW-OPTIONS-CONNECTION-MANAGEMENT)。它並非供使用者或用戶端應用程式直接指定。

<a id="LIBPQ-CONNECT-SCRAM-SERVER-KEY"></a>

### `scram_server_key` [#](#libpq-connect-scram-server-key) <a href="#libpq-connect-scram-server-key" id="libpq-connect-scram-server-key"></a>

以 base64 編碼的 SCRAM 伺服器金鑰。外部資料包裝器或類似的中介軟體可以用它來啟用 SCRAM 直通（pass-through）認證。其中一種實作請參閱[第 F.38.1.10 節](../../appendixes/contrib/postgres-fdw.md#POSTGRES-FDW-OPTIONS-CONNECTION-MANAGEMENT)。它並非供使用者或用戶端應用程式直接指定。

<a id="LIBPQ-CONNECT-SERVICE"></a>

### `service` [#](#libpq-connect-service) <a href="#libpq-connect-service" id="libpq-connect-service"></a>

用於取得額外參數的服務名稱。它指定 `pg_service.conf` 中保存額外連線參數的服務名稱。這讓應用程式只需指定服務名稱，連線參數便可集中維護。請參閱[第 32.17 節](libpq-pgservice.md)。

<a id="LIBPQ-CONNECT-TARGET-SESSION-ATTRS"></a>

### `target_session_attrs` [#](#libpq-connect-target-session-attrs) <a href="#libpq-connect-target-session-attrs" id="libpq-connect-target-session-attrs"></a>

此選項決定工作階段是否必須具備某些屬性才可被接受。它通常與多個主機名稱搭配使用，以便在數個主機中選出第一個可接受的候選。共有六種模式：

- `any`（預設）

  任何成功的連線都可接受

- `read-write`

  工作階段預設必須接受讀寫交易（也就是說，伺服器不得處於熱待命模式，而且 `default_transaction_read_only` 參數必須為 `off`）

- `read-only`

  工作階段預設不得接受讀寫交易（與前者相反）

- `primary`

  伺服器不得處於熱待命模式

- `standby`

  伺服器必須處於熱待命模式

- `prefer-standby`

  先嘗試尋找待命伺服器，但如果所列的主機都不是待命伺服器，就以 `any` 模式再試一次

<a id="LIBPQ-CONNECT-LOAD-BALANCE-HOSTS"></a>

### `load_balance_hosts` [#](#libpq-connect-load-balance-hosts) <a href="#libpq-connect-load-balance-hosts" id="libpq-connect-load-balance-hosts"></a>

控制用戶端嘗試連線到可用主機與位址的順序。一旦某次連線嘗試成功，就不會再嘗試其他主機與位址。此參數通常與多個主機名稱，或會傳回多個 IP 的 DNS 紀錄搭配使用。此參數可以與 [target_session_attrs](libpq-paramkeywords.md#libpq-connect-target-session-attrs) 搭配使用，例如只在待命伺服器之間進行負載平衡。成功連線後，在傳回之連線上的後續查詢都會送到同一台伺服器。目前有兩種模式：

- `disable`（預設）

  不在主機之間進行負載平衡。主機會依提供的順序嘗試，位址則依從 DNS 或 hosts 檔案收到的順序嘗試。

- `random`

  主機與位址會以隨機順序嘗試。此值主要適用於同時開啟多個連線的情況，這些連線可能來自不同的機器。如此一來，連線便可在多台 PostgreSQL 伺服器之間進行負載平衡。

  雖然隨機負載平衡由於其隨機的本質，幾乎永遠不會產生完全均勻的分布，但在統計上會相當接近。這裡有一個重要的面向：此演算法使用兩層隨機選擇。首先，主機會以隨機順序解析。其次，在解析下一個主機之前，會以隨機順序嘗試目前主機的所有已解析位址。在某些情況下，這種行為可能會大幅扭曲每個節點所獲得的連線數量，例如某些主機解析出的位址比其他主機多的時候。但也可以刻意利用這種偏差，例如在主機字串中多次提供較大型伺服器的主機名稱，以增加它所獲得的連線數量。

  使用此值時，建議同時為 [connect_timeout](libpq-paramkeywords.md#libpq-connect-connect-timeout) 設定一個合理的值。如此一來，如果用於負載平衡的某個節點沒有回應，就會嘗試新的節點。

<a id="LIBPQ-CONNECT-OAUTH-ISSUER"></a>

### `oauth_issuer` [#](#libpq-connect-oauth-issuer) <a href="#libpq-connect-oauth-issuer" id="libpq-connect-oauth-issuer"></a>

伺服器為此連線要求 OAuth 權杖時，所要聯繫之受信任核發者的 HTTPS URL。此參數對所有 OAuth 連線都是必要的；它應該與[伺服器 HBA 設定](../../server-administration/client-authentication/auth-oauth.md)中的 `issuer` 設定完全相符。

在標準認證交握的過程中，libpq 會向伺服器索取一份*發現文件（discovery document）：*也就是提供一組 OAuth 設定參數的 URL。伺服器必須提供一個直接由 `oauth_issuer` 的各組成部分建構而成的 URL，而且此值必須與發現文件本身所宣告的核發者識別碼完全相符，否則連線將會失敗。這是為了防範針對 OAuth 用戶端的一類[「混淆攻擊」（mix-up attacks）](https://mailarchive.ietf.org/arch/msg/oauth/JIVxFBGsJBVtm7ljwJhPUm3Fr-w/)所必需的。

你也可以將 `oauth_issuer` 明確設為用於 OAuth 發現的 `/.well-known/` URI。在這種情況下，如果伺服器要求不同的 URL，連線將會失敗，但[自訂 OAuth 流程](libpq-oauth.md#libpq-oauth-authdata-hooks)也許能透過使用先前快取的權杖來加快標準交握。（在這種情況下，建議也設定 [oauth_scope](libpq-paramkeywords.md#libpq-connect-oauth-scope)，因為用戶端將沒有機會向伺服器詢問正確的範圍設定，而權杖的預設範圍可能不足以建立連線。）libpq 目前支援下列眾所周知的端點：

* `/.well-known/openid-configuration`
* `/.well-known/oauth-authorization-server`

#### 警告

在 OAuth 連線交握期間，核發者擁有很高的權限。根據經驗法則，如果你不信任某個 URL 的營運者處理對你伺服器的存取，或直接冒充你，那麼該 URL 就不應被信任為 `oauth_issuer`。

<a id="LIBPQ-CONNECT-OAUTH-CLIENT-ID"></a>

### `oauth_client_id` [#](#libpq-connect-oauth-client-id) <a href="#libpq-connect-oauth-client-id" id="libpq-connect-oauth-client-id"></a>

由授權伺服器所核發的 OAuth 2.0 用戶端識別碼。如果 PostgreSQL 伺服器為此連線[要求 OAuth 權杖](../../server-administration/client-authentication/auth-oauth.md)（而且沒有安裝[自訂 OAuth 掛鉤](libpq-oauth.md#libpq-oauth-authdata-hooks)來提供權杖），就必須設定此參數；否則連線將會失敗。

<a id="LIBPQ-CONNECT-OAUTH-CLIENT-SECRET"></a>

### `oauth_client_secret` [#](#libpq-connect-oauth-client-secret) <a href="#libpq-connect-oauth-client-secret" id="libpq-connect-oauth-client-secret"></a>

聯繫 OAuth 授權伺服器時所使用的用戶端密碼（如果有的話）。此參數是否為必要，由 OAuth 提供者決定；「公開」（public）用戶端通常不使用祕密（secret），而「機密」（confidential）用戶端通常會使用。

<a id="LIBPQ-CONNECT-OAUTH-SCOPE"></a>

### `oauth_scope` [#](#libpq-connect-oauth-scope) <a href="#libpq-connect-oauth-scope" id="libpq-connect-oauth-scope"></a>

傳送給授權伺服器之存取請求的範圍，以 OAuth 範圍識別碼組成、以空白分隔的清單（可能為空）來指定。此參數是選用的，供進階用途使用。

通常用戶端會從 PostgreSQL 伺服器取得適當的範圍設定。如果使用了此參數，伺服器所要求的範圍清單將被忽略。這可以防止較不受信任的伺服器向終端使用者要求不適當的存取範圍。不過，如果用戶端的範圍設定沒有包含伺服器所需的範圍，伺服器很可能會拒絕所核發的權杖，連線也將會失敗。

空範圍清單的意義取決於提供者。OAuth 授權伺服器可以選擇核發具有「預設範圍」（無論那恰好是什麼）的權杖，也可能完全拒絕該權杖請求。

[返回 32.1. 資料庫連線控制函式](libpq-connect.md#libpq-connect)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-connect.html)（原文版本：18.6；核對日期：2026-10-18）
