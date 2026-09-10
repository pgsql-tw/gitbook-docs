## 20.12. 憑證驗證 [#](#AUTH-CERT)

<a id="id-1.6.7.19.2"></a>

此驗證方法使用 SSL 用戶端憑證執行驗證，因此僅適用於 SSL 連線；SSL 設定指示請參閱
[第 18.9.2 節](../runtime/ssl-tcp.md#SSL-OPENSSL-CONFIG)。使用此驗證方法時，伺服器會要求
用戶端提供有效且受信任的憑證，且不會向用戶端提示輸入密碼。憑證的 `cn`（Common Name）
屬性會與所要求的資料庫使用者名稱比較；若兩者相符，便允許登入。可使用使用者名稱對應，
使 `cn` 與資料庫使用者名稱不同。

SSL 憑證驗證支援下列設定選項：

`map`
:   允許在系統與資料庫使用者名稱之間建立對應。詳細資訊請參閱
    [第 20.2 節](auth-username-maps.md)。

將 `clientcert` 選項與 `cert` 驗證併用是多餘的，因為 `cert` 驗證實際上等同於
設定 `clientcert=verify-full` 的 `trust` 驗證。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-cert.html)（原文版本：18.6；核對日期：2026-09-10）
