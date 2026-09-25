<a id="AUTH-PASSWORD"></a>

## 20.5. 密碼驗證 [#](#AUTH-PASSWORD)

<a id="id-1.6.7.12.2"></a><a id="id-1.6.7.12.3"></a><a id="id-1.6.7.12.4"></a>

有好幾種以密碼為基礎的驗證方法。這些方法的運作方式類似，但在使用者密碼於
伺服器上的儲存方式，以及用戶端所提供的密碼如何透過連線傳送這兩點上有所不同。

`scram-sha-256`
:   `scram-sha-256` 方法會執行 SCRAM-SHA-256
    驗證，如 [RFC 7677](https://datatracker.ietf.org/doc/html/rfc7677) 所述。這
    是一種挑戰－回應（challenge-response）機制，可防止在不受信任的連線上被側錄密碼，並支援
    以一種被認為安全的加密雜湊形式，將密碼儲存在伺服器上。

    這是目前所提供的方法中最安全的一種，但較舊版的用戶端程式庫並不支援它。

`md5`
:   `md5` 方法使用一種自訂、安全性較低的挑戰－回應機制。它可以防止密碼側錄，
    並避免將密碼以明碼形式儲存在伺服器上，但若攻擊者成功從伺服器竊取密碼雜湊值，
    這個方法就無法提供任何保護。此外，如今 MD5 雜湊演算法在面對蓄意攻擊時已
    不再被視為安全。

    為了讓使用者能更容易地從 `md5` 方法轉換到較新的
    SCRAM 方法，若在 `pg_hba.conf` 中指定的方法是
    `md5`，但使用者在伺服器上的密碼是以 SCRAM 加密的
    （見下文），則系統會自動改用以 SCRAM 為基礎的驗證。

    ### 警告

    對 MD5 加密密碼的支援已經棄用，未來的 PostgreSQL 版本將會移除此支援。有關遷移到
    其他密碼類型的細節，請參閱下方的說明。

`password`
:   `password` 方法會以明碼傳送密碼，因此容易受到密碼「側錄」攻擊。
    應盡可能避免使用這個方法。不過，如果連線受到 SSL 加密保護，那麼使用
    `password` 就是安全的。（不過，若本來就打算依賴 SSL，
    採用 SSL 憑證驗證可能是更好的選擇。）

PostgreSQL 資料庫密碼與作業系統使用者密碼是分開的。每個
資料庫使用者的密碼都儲存在 `pg_authid` 系統
目錄中。密碼可以使用 SQL 指令
[CREATE ROLE](../../reference/sql-commands/sql-createrole.md) 與
[ALTER ROLE](../../reference/sql-commands/sql-alterrole.md) 來管理，
例如：**`CREATE ROLE foo WITH LOGIN PASSWORD 'secret'`**，
或是使用 psql
指令 `\password`。
若使用者尚未設定密碼，則儲存的密碼會是 null，該使用者的密碼驗證將永遠失敗。

不同的密碼式驗證方法是否可用，取決於使用者的密碼在伺服器上是以何種方式加密
（更精確地說，是雜湊）的。這是由設定密碼當下的組態
參數 [password_encryption](../runtime-config/runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION) 所控制的。若密碼是
使用 `scram-sha-256` 設定加密的，那麼它可以用於
驗證方法 `scram-sha-256`
與 `password`（不過在後者的情況下，密碼傳輸
會是明碼形式）。驗證方法規格
`md5` 會如上所述，在這種情況下自動改用
`scram-sha-256` 方法，因此也能正常運作。若密碼是使用
`md5` 設定加密的，那麼它就只能用於
`md5` 與 `password` 驗證
方法規格（同樣地，在後者的情況下密碼會以明碼傳輸）。（先前的 PostgreSQL
版本支援以明碼在伺服器上儲存密碼，現在已不再支援這種做法。）若要
檢視目前儲存的密碼雜湊值，請參閱系統
目錄 `pg_authid`。

若要將既有的安裝環境從 `md5`
升級到 `scram-sha-256`，在確認所有使用中的用戶端程式庫版本都夠新、
足以支援 SCRAM 之後，請在 `postgresql.conf` 中
設定 `password_encryption = 'scram-sha-256'`，
讓所有使用者重新設定新密碼，
並將 `pg_hba.conf` 中的驗證方法規格改為
`scram-sha-256`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-password.html)（原文版本：18.6；核對日期：2026-09-25）
