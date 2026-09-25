<a id="AUTH-TRUST"></a>

## 20.4. 信任驗證 [#](#AUTH-TRUST)

當指定 `trust` 驗證時，PostgreSQL
會假設任何能夠連線到伺服器的人，都已被授權以其所指定的任何資料庫使用者名稱
（甚至是超級使用者名稱）存取資料庫。
當然，`database` 及
`user` 欄位所設下的限制仍然適用。
此方法只能在伺服器連線已具備充分的作業系統層級保護時使用。

`trust` 驗證對於單一使用者工作站上的本機連線而言，
是適當且非常方便的做法。但在多使用者機器上，
單獨使用它通常*不*恰當。不過，
如果你利用檔案系統權限限制對伺服器 Unix 網域通訊端檔案的存取，
即使在多使用者機器上，你也有可能可以使用 `trust`。
要做到這一點，可依照[第 19.3 節](../runtime-config/runtime-config-connection.md)所述，
設定 `unix_socket_permissions`
（可能還需要 `unix_socket_group`）組態參數。
或者，你也可以設定 `unix_socket_directories`
組態參數，將通訊端檔案放在受到適當限制的目錄中。

設定檔案系統權限只對 Unix 通訊端連線有幫助。
本機 TCP/IP 連線不受檔案系統權限限制。
因此，如果你想以檔案系統權限來達成本機安全性，
請將 `pg_hba.conf` 中的
`host ... 127.0.0.1 ...` 那一行移除，
或將其改為非 `trust` 的驗證方法。

`trust` 驗證只有在你信任所有被
`pg_hba.conf` 中指定 `trust` 的那些行
允許連線到伺服器的每一台機器上的每一位使用者時，
才適合用於 TCP/IP 連線。除了來自本機（127.0.0.1）的連線之外，
將 `trust` 用於其他任何 TCP/IP 連線，很少是合理的做法。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-trust.html)（原文版本：18.6；核對日期：2026-09-25）
