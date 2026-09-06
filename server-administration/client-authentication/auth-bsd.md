## 20.14. BSD 驗證 [#](#AUTH-BSD)

<a id="id-1.6.7.21.2"></a>

此驗證方法的運作方式與 `password` 類似，但使用 BSD Authentication 驗證密碼。BSD Authentication 只用來驗證使用者名稱與密碼的組合。因此，要使用 BSD Authentication 進行驗證，使用者的角色必須已存在於資料庫中。BSD Authentication 框架目前僅適用於 OpenBSD。

PostgreSQL 中的 BSD Authentication 使用 `auth-postgresql` 登入類型；若 `login.conf` 定義了 `postgresql` 登入類別，便使用該類別進行驗證。預設情況下，此登入類別不存在，因此 PostgreSQL 會使用預設登入類別。

### 注意

若要使用 BSD Authentication，必須先將 PostgreSQL 使用者帳號（也就是執行伺服器的作業系統使用者）加入 `auth` 群組。OpenBSD 系統預設就有 `auth` 群組。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-bsd.html)（原文版本：18.6；核對日期：2026-09-07）
