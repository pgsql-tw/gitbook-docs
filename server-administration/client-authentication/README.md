## 第 20 章 用戶端認證

**目錄**

[20.1. `pg_hba.conf` 檔案](auth-pg-hba-conf.md)

[20.2. 使用者名稱對應](auth-username-maps.md)

[20.3. 認證方法](auth-methods.md)

[20.4. Trust 認證](auth-trust.md)

[20.5. 密碼認證](auth-password.md)

[20.6. GSSAPI 認證](gssapi-auth.md)

[20.7. SSPI 認證](sspi-auth.md)

[20.8. Ident 認證](auth-ident.md)

[20.9. Peer 認證](auth-peer.md)

[20.10. LDAP 認證](auth-ldap.md)

[20.11. RADIUS 認證](auth-radius.md)

[20.12. 憑證認證](auth-cert.md)

[20.13. PAM 認證](auth-pam.md)

[20.14. BSD 認證](auth-bsd.md)

[20.15. OAuth 授權／認證](auth-oauth.md)

[20.16. 認證問題](client-authentication-problems.md)

<a id="id-1.6.7.2"></a>

當用戶端應用程式連線到資料庫伺服器時，它會指定想要以哪一個
PostgreSQL 資料庫使用者名稱連線，這與在 Unix 電腦上以特定使用者身分登入的方式大致相同。在 SQL 環境中，作用中的資料庫
使用者名稱決定了對資料庫物件的存取權限——詳見
[第 21 章](../user-manag/README.md)。因此，限制哪些資料庫使用者可以連線是非常重要的。

### 注意

如[第 21 章](../user-manag/README.md)所述，
PostgreSQL 實際上是以「角色」的形式來進行權限
管理。在本章中，我們一律使用*資料庫使用者*一詞來表示「具有
`LOGIN` 權限的角色」。

*認證*是指資料庫伺服器用來確認用戶端身分的過程，並藉此判斷用戶端應用程式（或執行該用戶端應用程式的使用者）是否被允許以其所請求的資料庫使用者名稱連線。

PostgreSQL 提供了多種不同的
用戶端認證方法。可以根據（用戶端的）主機位址、資料庫及使用者，選擇用來驗證特定用戶端連線的方法。

PostgreSQL 資料庫使用者名稱在邏輯上與執行伺服器的作業系統使用者名稱是分開的。如果某個伺服器的所有使用者在該伺服器的機器上也都有帳號，那麼將資料庫使用者名稱設定為與其作業系統使用者名稱相符是合理的做法。然而，接受遠端連線的伺服器
可能有許多資料庫使用者並沒有本機
作業系統帳號，在這種情況下，資料庫使用者名稱與作業系統使用者名稱之間不需要有任何關聯。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/client-authentication.html)（原文版本：18.6；核對日期：2026-09-28）
