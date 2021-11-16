# 19.3. 連線與認證

## 19.3.1. 連線設定

#### `listen_addresses` (`string`)

指定伺服器監聽用戶端應用程序連線的 TCP/IP 位址。該值採用逗號分隔的主機名稱或數字 IP 位址列表的形式。特殊項目「\*」對應於所有可用的 IP。項目 0.0.0.0 允許監聽所有 IPv4 位址，還有「::」允許監聽所有 IPv6 位址。如果列表為空，則伺服器根本不監聽任何 IP 接口，在這種情況下，就只能使用 Unix-domain socket 來連接它。預設值是 localhost，它只允許進行本地 TCP/IP loopback 連線。儘管用戶端身份驗證（[第 20 章](../client-authentication/)）允許對誰可以存取伺服器進行細維的控制，但 listen\_addresses 控制哪些 IP 接受連線嘗試，這有助於防止在不安全的網路接口上重複發出惡意的連線請求。此參數只能在伺服器啟動時設定。

#### `port` (`integer`)

伺服器監聽的 TCP 連接埠；預設是 5432。請注意，相同的連接埠號號用於伺服器監聽的所有 IP 地址。此參數只能在伺服器啟動時設定。

#### `max_connections` (`integer`)

決定資料庫伺服器的最大同時連線數。預設值通常為 100 個連線，但如果您的核心設定不支援它（在 initdb 期間確定），則可能會更少。該參數只能在伺服器啟動時設定。

運行備用伺服器時，必須將此參數設定為與主服務器上相同或更高的值。 否則，查詢將不被允許在備用伺服器中使用。

#### `superuser_reserved_connections` (`integer`)

決定為 PostgreSQL 超級使用者連線保留的連線「插槽」的數量。最多 max\_connections 連線可以同時活動。當活動同時連線的數量為 max\_connections 減去 superuser\_reserved\_connections 以上時，新連線將僅接受超級使用者，並且不會接受新的複寫作業連線。

預設值是三個連線。該值必須小於 max\_connections 的值。此參數只能在伺服器啟動時設定。

#### `unix_socket_directories` (`string`)

指定伺服器要監聽來自用戶端應用程序以 Unix-domain socket 連線的目錄。列出由逗號分隔的多個目錄可以建立多個 socket。項目之間的空白會被忽略；如果您需要在名稱中包含空格或逗號，請用雙引號括住目錄名稱。空值表示不監聽任何 Unix-domain socket，在這種情況下，只有 TCP/IP 協定可用於連線到服務器。預設值通常是 /tmp，但可以在編譯時變更。此參數只能在伺服器啟動時設定。

除了名為 .s.PGSQL.nnnn 的 socket 檔案本身之外，其中 nnnn 是伺服器的連接埠號號，將在每個 unix\_socket\_directories 目錄中建立一個名為 .s.PGSQL.nnnn.lock 的普通檔案。這兩個檔案都不應該手動刪除。

這個參數與 Windows 無關，它沒有 Unix-domain socket。

`unix_socket_group` (`string`)

設定 Unix-domain socket 的群組。（socket 的使用者始終是啟動伺服器的使用者。）結合參數 unix\_socket\_permissions，可以將其用作為 Unix-domain socket 的附加存取控制機制。預設情況下，這是空字符串，它使用服務器用戶的預設群組。此參數只能在伺服器啟動時設定。

這個參數與 Windows 無關，它沒有 Unix-domain socket。

`unix_socket_permissions` (`integer`)

設定 Unix-domain socket 的存取權限。Unix-domain socket 使用一般的 Unix 檔案系統權限設定。期望的參數值是以 chmod 和 umask 系統呼叫可接受的格式指定數字模式。（要使用習慣的八進制格式，數字必須以 0（零）開頭。）

預設權限是 0777，意味著任何人都可以進行連線。合理的選擇是 0770（僅使用者和其群組，另請參閱 unix\_socket\_group）和 0700（僅使用者本身）。（請注意，對於Unix-domain socket，只有寫入權限很重要，所以設定還是撤消讀取或執行權限都沒有意義。）

這種存取控制機制獨立於[第 20 章](../client-authentication/)中所描述的機制。

此參數只能在伺服器啟動時設定。

此參數在某些系統上無關緊要，特別是從 Solaris 10 開始的 Solaris，會完全忽略權限許可。在那裡，透過將 unix\_socket\_directories 指向具有僅限於所需的搜尋權限的目錄，就可以實現類似的效果。這個參數與 Windows 也是無關的，它沒有 Unix-domain socket。

`bonjour` (`boolean`)

透過 Bonjour 啟用伺服器存在的廣播。預設是關閉的。此參數只能在伺服器啟動時設定。

`bonjour_name` (`string`)

指定 Bonjour 的服務名稱。如果此參數設定為空字串''（這是預設值），則使用電腦名稱。 如果伺服器未使用 Bonjour 支援進行編譯，則此參數將被忽略。此參數只能在伺服器啟動時設定。

`tcp_keepalives_idle` (`integer`)

指定 TCP 在發送 Keepalive 訊息給用戶端之後保持連線的秒數。值為 0 時使用系統預設值。此參數僅在支援 TCP\_KEEPIDLE 或等效網路選項的系統上以及在 Windows 上受到支援；在其他系統上，它必須是零。在透過 Unix-domain socket 的連線中，該參數將被忽略並始終為零。

#### 注意

在 Windows 上，值為 0 會將此參數設定為2小時，因為 Windows 不提供讀取系統預設值的方法。

`tcp_keepalives_interval` (`integer`)

指定用戶端未回應的 TCP 保持活動訊息應重新傳輸的秒數。值為 0 時使用系統預設值。此參數僅在支援 TCP\_KEEPINTVL 或等效網路選項的系統上以及在 Windows 上受到支援；在其他系統上，它必須是零。在透過 Unix-domain socket 的連線中，此參數將被忽略並始終為零。

#### 注意

在 Windows 上，值為 0 會將此參數設定為 1 秒，因為 Windows 不提供讀取系統預設值的方法。

`tcp_keepalives_count` (`integer`)

指定在伺服器連線到用戶端之前可能已經失去的 TCP 保持連線的數量。值為 0 時使用系統預設值。此參數僅在支援 TCP\_KEEPCNT 或等效網路選項的系統上受到支持；在其他系統上，它必須是零。在透過 Unix-domain socket 的連線中，此參數將被忽略並始終為零。

#### 注意

此參數在 Windows 上不支援，並且必須為零。

## 19.3.2. 安全性與認證

#### `authentication_timeout` (`integer`)

以秒為單位設定用戶端身份驗證的最長時間。如果可能的用戶端在這段時間內還沒有完成認證協議，伺服器將會關閉連線。這可以防止掛起的用戶端無限期地佔用連線。預設值是一分鐘。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

#### `password_encryption` (`enum`)

在 [CREATE ROLE](../../reference/sql-commands/create-role.md) 或 [ALTER ROLE](../../reference/sql-commands/alter-role.md) 中指定了密碼後，此參數確定用於加密密碼的演算法。預設值為 md5，它將密碼儲存為 MD5 雜湊值（也可以使用 on，作為 md5 的別名）。將此參數設定為 scram-sha-256 將使用 SCRAM-SHA-256 來加密密碼。

請注意，較舊的用戶端程式可能會缺乏對 SCRAM 身份驗證機制的支援，因此不適用於使用 SCRAM-SHA-256 加密的密碼。有關更多詳細資訊，請參閱 [20.5 節](../client-authentication/password-authentication.md)。

`ssl` (`boolean`)

啟用 SSL 連線。使用前請先閱讀[第 18.9 節](../server-setup-and-operation/secure-tcp-ip-connections-with-ssl.md)。 此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設是關閉的。

`ssl_ca_file` (`string`)

指定包含 SSL 伺服器證書頒發機構（CA）的檔案名稱。相對路徑與資料目錄有關。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設值為空，表示未載入 CA 檔案，並且不執行用戶端證書驗證。

在以前的 PostgreSQL 版本中，該檔案的名稱被硬性指定為 root.crt。

`ssl_cert_file` (`string`)

指定包含 SSL 伺服器證書的檔案名稱。相對路徑與資料目錄有關。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設值是 server.crt。

`ssl_crl_file` (`string`)

指定包含 SSL 伺服器證書吊銷列表（CRL）的文件的名稱。相對路徑與資料目錄有關。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設值為空，表示沒有加載 CRL 檔案。

在以前的 PostgreSQL 版本中，該檔案的名稱被硬性指定為 root.crl。

`ssl_key_file` (`string`)

指定包含 SSL 伺服器私鑰的檔案名稱。相對路徑與資料目錄有關。 此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設值是 server.key。

`ssl_ciphers` (`string`)

指定允許在安全連線上使用的 SSL 密碼套件列表。有關此設定的語法和支援的列表，請參閱 OpenSSL 軟體套件中的密碼手冊文件。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設值為 HIGH:MEDIUM:+3DES:!aNULL。這個預設通常是一個合理的設定，除非您有特定的安全要求。

預設值延伸說明：

`HIGH`

使用來自 HIGH group 的密碼套件（例如：AES，Camellia，3DES）

`MEDIUM`

使用來自 MEDIUM group 的密碼套件（例如：RC4，SEED）

`+3DES`

HIGH 的 OpenSSL 預設順序有問題，因為它的 3DES 高於 AES128。這是錯誤的，因為 3DES 比 AES128 提供較低的安全性，而且速度也更慢。+3DES 將所有其他高級和中級密碼重新排序。

`!aNULL`

停用不進行身份驗證的匿名密碼套件。這種密碼套件容易受到中間人攻擊，因此不應使用。

可用的密碼套件詳細訊息將因 OpenSSL 版本而異。使用命令 `openssl ciphers -v'HIGH:MEDIUM:+3DES:!aNULL' `來查看當下安裝的 OpenSSL 版本細節。請注意，此列表在運行時基於伺服器密鑰型別進行過濾。

`ssl_prefer_server_ciphers` (`boolean`)

指定是否使用伺服器的 SSL 密碼設定，而不是用戶端的。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設值是 true。

較舊的 PostgreSQL 版本並沒有此設定，始終使用用戶端的設定。此設定主要是為了與這些版本的相容性。使用伺服器的選項通常更好，因為伺服器更有可能做適當的配置。

`ssl_ecdh_curve` (`string`)

指定要在 ECDH 密鑰交換中使用的 curve 名稱。它需要所有連線的用戶端支援。它不需要與伺服器的 curve 鍵使用的相同。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設為 prime256v1。

最常用 curve 的 OpenSSL 名稱為：prime256v1（NIST P-256），secp384r1（NIST P-384），secp521r1（NIST P-521）。可用 curve 的完整列表可以使用 openssl ecparam -list\_curves 指令列出。但並非所有的結果都可以在 TLS 中使用。

`password_encryption` (`enum`)

當在 [CREATE ROLE](../../reference/sql-commands/create-role.md) 或 [ALTER ROLE](../../reference/sql-commands/alter-role.md) 中指定密碼時，此參數決定用於加密密碼的演算法。預設值是md5，它將密碼儲存為MD5 hash（on 也被接受，作為 md5 的別名）。將此參數設定為 scram-sha-256 時將使用 SCRAM-SHA-256 加密密碼。

請注意，較舊的用戶端可能缺少對 SCRAM 認證機制的支援，因此不適用於使用 SCRAM-SHA-256 加密的密碼。有關更多詳細訊息，請參閱[第 20.3.2 節](../client-authentication/authentication-methods.md#20-3-2-password-authentication)。

`ssl_dh_params_file` (`string`)

指定包含用於所謂的 ephemeral DH family 的 SSL 加密的 Diffie-Hellman 參數的檔案名稱。預設值為空，在這種情況下，使用預設編譯的 DH 參數。如果攻擊者設法破解眾所周知的編譯 DH 參數，則使用自行定義 DH 參數可以減少暴露的可能性。 您可以使用指令 `openssl dhparam -out dhparams.pem 2048` 建立您自己的DH參數檔案。

此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

`krb_server_keyfile` (`string`)

設定 Kerberos 伺服器密鑰檔案的位置。有關詳細訊息，請參閱[第 20.3.3 節](../client-authentication/authentication-methods.md)。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

`krb_caseins_users` (`boolean`)

設定是否應該區分大小寫地處理 GSSAPI 用戶名。預設是關閉的（區分大小寫）。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

`db_user_namespace` (`boolean`)

此參數啟用每個資料庫分別的使用者名稱。預設是關閉的。 此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

如果開啓的話，您應該將使用者建立為 username@dbname。當連線用戶端傳遞使用者名稱時，@和資料庫名稱將附加到使用者名稱中，並且該伺服器會查詢特定於資料庫的使用者名稱。請注意，當您在 SQL 環境中建立名稱包含 @ 的使用者時，您需要以引號括住使用者名稱。

啟用此參數後，您仍然可以建立普通的全域使用者。在用戶端指定使用者名稱時簡單追加 @，例如 joe@。在使用者名稱被伺服器查詢之前，@ 將被剝離。

db\_user\_namespace 會導致用戶端和伺服器的使用者名稱表示方式不同。身份驗證檢查始終使用伺服器的使用者名稱完成，因此必須為伺服器的使用者名稱配置身份驗證方法，而不是用戶端。而 md5 在用戶端和伺服器上均使用使用者名稱作為 salt，所以 md5 不能與 db\_user\_namespace 一起使用。

#### 注意

此功能是一種臨時措施，到找到完整的解決方案的時候，這個選項將被刪除。

## 19.3.3. SSL

有關設定 SSL 的更多資訊，請參閱[第 18.9 節](../server-setup-and-operation/secure-tcp-ip-connections-with-ssl.md)。

`ssl` (`boolean`)

啟用 SSL 連線。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設為 off。

`ssl_ca_file` (`string`)

Specifies the name of the file containing the SSL server certificate authority (CA). Relative paths are relative to the data directory. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is empty, meaning no CA file is loaded, and client certificate verification is not performed.

`ssl_cert_file` (`string`)

Specifies the name of the file containing the SSL server certificate. Relative paths are relative to the data directory. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `server.crt`.

(`string`)

Specifies the name of the file containing the SSL server certificate revocation list (CRL). Relative paths are relative to the data directory. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is empty, meaning no CRL file is loaded.

`ssl_key_file` (`string`)

Specifies the name of the file containing the SSL server private key. Relative paths are relative to the data directory. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `server.key`.

`ssl_ciphers` (`string`)

Specifies a list of SSL cipher suites that are allowed to be used on secure connections. See the ciphers manual page in the OpenSSL package for the syntax of this setting and a list of supported values. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default value is `HIGH:MEDIUM:+3DES:!aNULL`. The default is usually a reasonable choice unless you have specific security requirements.

Explanation of the default value:

`HIGH`

Cipher suites that use ciphers from `HIGH` group (e.g., AES, Camellia, 3DES)

`MEDIUM`

Cipher suites that use ciphers from `MEDIUM` group (e.g., RC4, SEED)

`+3DES`

The OpenSSL default order for `HIGH` is problematic because it orders 3DES higher than AES128. This is wrong because 3DES offers less security than AES128, and it is also much slower. `+3DES` reorders it after all other `HIGH` and `MEDIUM` ciphers.

`!aNULL`

Disables anonymous cipher suites that do no authentication. Such cipher suites are vulnerable to man-in-the-middle attacks and therefore should not be used.

Available cipher suite details will vary across OpenSSL versions. Use the command `openssl ciphers -v 'HIGH:MEDIUM:+3DES:!aNULL'` to see actual details for the currently installed OpenSSL version. Note that this list is filtered at run time based on the server key type

`ssl_prefer_server_ciphers` (`boolean`)

Specifies whether to use the server's SSL cipher preferences, rather than the client's. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `true`.

Older PostgreSQL versions do not have this setting and always use the client's preferences. This setting is mainly for backward compatibility with those versions. Using the server's preferences is usually better because it is more likely that the server is appropriately configured.

`ssl_ecdh_curve` (`string`)

Specifies the name of the curve to use in ECDH key exchange. It needs to be supported by all clients that connect. It does not need to be the same curve used by the server's Elliptic Curve key. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `prime256v1`.

OpenSSL names for the most common curves are: `prime256v1` (NIST P-256), `secp384r1` (NIST P-384), `secp521r1` (NIST P-521). The full list of available curves can be shown with the command `openssl ecparam -list_curves`. Not all of them are usable in TLS though.

`ssl_dh_params_file` (`string`)

Specifies the name of the file containing Diffie-Hellman parameters used for so-called ephemeral DH family of SSL ciphers. The default is empty, in which case compiled-in default DH parameters used. Using custom DH parameters reduces the exposure if an attacker manages to crack the well-known compiled-in DH parameters. You can create your own DH parameters file with the command `openssl dhparam -out dhparams.pem 2048`.

This parameter can only be set in the `postgresql.conf` file or on the server command line.

`ssl_passphrase_command` (`string`)

Sets an external command to be invoked when a passphrase for decrypting an SSL file such as a private key needs to be obtained. By default, this parameter is empty, which means the built-in prompting mechanism is used.

The command must print the passphrase to the standard output and exit with code 0. In the parameter value, `%p` is replaced by a prompt string. (Write `%%` for a literal `%`.) Note that the prompt string will probably contain whitespace, so be sure to quote adequately. A single newline is stripped from the end of the output if present.

The command does not actually have to prompt the user for a passphrase. It can read it from a file, obtain it from a keychain facility, or similar. It is up to the user to make sure the chosen mechanism is adequately secure.

This parameter can only be set in the `postgresql.conf` file or on the server command line

`ssl_passphrase_command_supports_reload` (`boolean`)

This parameter determines whether the passphrase command set by `ssl_passphrase_command` will also be called during a configuration reload if a key file needs a passphrase. If this parameter is false (the default), then `ssl_passphrase_command` will be ignored during a reload and the SSL configuration will not be reloaded if a passphrase is needed. That setting is appropriate for a command that requires a TTY for prompting, which might not be available when the server is running. Setting this parameter to true might be appropriate if the passphrase is obtained from a file, for example.

This parameter can only be set in the `postgresql.conf` file or on the server command line.
