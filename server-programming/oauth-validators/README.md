## 第 50 章 OAuth 驗證器模組

**目錄**

[50.1. 安全地設計驗證器模組](oauth-validator-design.md)
:   [50.1.1. 驗證器的職責](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-RESPONSIBILITIES)

    [50.1.2. 一般撰碼準則](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-GUIDELINES)

    [50.1.3. 授權使用者（使用者對應委派）](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-USERMAP-DELEGATION)

[50.2. 初始化函式](oauth-validator-init.md)

[50.3. OAuth 驗證器回呼函式](oauth-validator-callbacks.md)
:   [50.3.1. 啟動回呼](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-STARTUP)

    [50.3.2. 驗證回呼](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-VALIDATE)

    [50.3.3. 關閉回呼](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-SHUTDOWN)

<a id="id-1.8.17.2"></a>

PostgreSQL 提供了一套基礎架構，可用來建立自訂模組，對 OAuth 持有者權杖執行伺服器端驗證。由於 OAuth 的實作方式差異極大，而持有者權杖的驗證方式又高度依賴於發行方，因此伺服器本身無法自行檢查權杖；驗證器模組提供了伺服器與所使用之 OAuth 提供者之間的整合層。

OAuth 驗證器模組至少必須包含一個初始化函式（見[第 50.2 節](oauth-validator-init.md)），以及執行驗證所需的回呼函式（見[第 50.3.2 節](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-VALIDATE)）。

### 警告

由於行為異常的驗證器可能讓未經授權的使用者進入資料庫，因此正確的實作方式對伺服器的安全至關重要。設計考量請參閱[第 50.1 節](oauth-validator-design.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/oauth-validators.html)（原文版本：18.6；核對日期：2026-09-15）
