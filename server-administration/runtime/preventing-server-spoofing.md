<a id="PREVENTING-SERVER-SPOOFING"></a>

## 18.7. 防止伺服器被偽造（Spoofing） [#](#PREVENTING-SERVER-SPOOFING)

<a id="id-1.6.5.10.2"></a>

當伺服器正在執行時，惡意使用者無法取代正常的資料庫伺服器。
不過，當伺服器停機時，本機使用者就有可能透過啟動自己的伺服器，
來偽造正常伺服器。這個偽造伺服器，可以讀取用戶端傳送的密碼與查詢，
但由於目錄權限的保護，`PGDATA` 目錄仍然是安全的，
因此無法傳回任何資料。之所以可能發生偽造，是因為任何使用者，
都能啟動資料庫伺服器；除非特別設定，
否則用戶端無法辨識出無效的伺服器。

防止 `local` 連線遭到偽造的其中一種方法，
是使用一個 Unix 網域 socket 目錄
（[unix_socket_directories](../runtime-config/runtime-config-connection.md#GUC-UNIX-SOCKET-DIRECTORIES)），
該目錄只允許受信任的本機使用者具有寫入權限。這能防止惡意使用者，
在該目錄中建立自己的 socket 檔案。若您擔心仍有某些應用程式，
可能參照 `/tmp` 作為 socket 檔案的位置，因而容易遭到偽造，
可以在作業系統啟動期間，建立一個指向已搬移之 socket 檔案的
符號連結 `/tmp/.s.PGSQL.5432`。您也可能需要修改
`/tmp` 的清理指令碼，以防止該符號連結被移除。

針對 `local` 連線，另一個選項，是讓用戶端使用
[`requirepeer`](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNECT-REQUIREPEER)，
指定連線至該 socket 的伺服器程序必須屬於的擁有者。

若要防止 TCP 連線遭到偽造，可以使用 SSL 憑證，
並確保用戶端會檢查伺服器的憑證，或者使用 GSSAPI 加密
（若這兩者分別用於不同的連線，也可以兩者併用）。

若要以 SSL 防止偽造，伺服器必須設定為只接受
`hostssl` 連線（[20.1 節](../client-authentication/auth-pg-hba-conf.md)），
並具備 SSL 金鑰與憑證檔案（[18.9 節](ssl-tcp.md)）。
TCP 用戶端必須使用 `sslmode=verify-ca` 或
`verify-full` 進行連線，並安裝適當的根憑證檔案
（[32.19.1 節](../../client-interfaces/libpq/libpq-ssl.md#LIBQ-SSL-CERTIFICATES)）。
或者，也可以透過 `sslrootcert=system`，
使用 SSL 實作所定義的
[系統 CA 集區](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNECT-SSLROOTCERT)；
在這種情況下，為了安全起見，會強制採用
`sslmode=verify-full`，因為要取得由公開 CA
所簽署的憑證，通常相當容易。

若要防止在網路上使用
[scram-sha-256](../client-authentication/auth-password.md) 密碼驗證時
發生伺服器偽造，您應確保連線至伺服器時使用 SSL，
並搭配前一段所述的其中一種防偽造方法。此外，
libpq 中的 SCRAM 實作，無法保護整個驗證交換過程，
但使用 `channel_binding=require` 連線參數，
可以提供一種對伺服器偽造的緩解措施。使用惡意伺服器
攔截 SCRAM 交換過程的攻擊者，可以透過離線分析，
潛在地從用戶端推算出雜湊後的密碼。

若要以 GSSAPI 防止偽造，伺服器必須設定為只接受
`hostgssenc` 連線
（[20.1 節](../client-authentication/auth-pg-hba-conf.md)），
並搭配使用 `gss` 驗證方式。TCP 用戶端，
則必須使用 `gssencmode=require` 進行連線。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/preventing-server-spoofing.html)（原文版本：18.6；核對日期：2026-09-24）
