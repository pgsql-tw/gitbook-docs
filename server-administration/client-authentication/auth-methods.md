<a id="AUTH-METHODS"></a>

## 20.3. 認證方法 [#](#AUTH-METHODS)

PostgreSQL 提供多種驗證使用者的方法：

* [Trust 認證](auth-trust.md)，單純信任使用者的身分如其所宣稱。
* [密碼認證](auth-password.md)，要求使用者傳送密碼。
* [GSSAPI 認證](gssapi-auth.md)，依賴與 GSSAPI 相容的安全性函式庫。通常用於存取
  Kerberos 或 Microsoft Active Directory 伺服器等認證伺服器。
* [SSPI 認證](sspi-auth.md)，使用類似 GSSAPI 的 Windows 專屬通訊協定。
* [Ident 認證](auth-ident.md)，依賴用戶端機器上的「識別通訊協定」
  （[RFC 1413](https://datatracker.ietf.org/doc/html/rfc1413)）
  服務。（在本機 Unix-socket 連線上，這會被視為 peer 認證。）
* [Peer 認證](auth-peer.md)，依賴作業系統機制來識別本機連線另一端的程序。此方法不支援遠端連線。
* [LDAP 認證](auth-ldap.md)，依賴 LDAP 認證伺服器。
* [RADIUS 認證](auth-radius.md)，依賴 RADIUS 認證伺服器。
* [憑證認證](auth-cert.md)，要求使用 SSL 連線，並透過檢查使用者傳送的
  SSL 憑證來進行驗證。
* [PAM 認證](auth-pam.md)，依賴 PAM（可插拔認證模組）函式庫。
* [BSD 認證](auth-bsd.md)，依賴 BSD 認證框架（目前僅在 OpenBSD 上可用）。
* [OAuth 授權／認證](auth-oauth.md)，
  依賴外部的 OAuth 2.0 身分識別提供者。

Peer 認證通常適合用於本機連線，不過在某些情況下 trust 認證也已足夠。
密碼認證是遠端連線最簡單的選擇。
其他所有選項都需要某種外部安全性基礎設施
（通常是認證伺服器，或用於核發 SSL 憑證的憑證授權單位），或是與平台有關。

以下各節將更詳細地說明這些認證方法。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-methods.html)（原文版本：18.6；核對日期：2026-09-28）
