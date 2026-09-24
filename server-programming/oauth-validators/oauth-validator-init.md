<a id="OAUTH-VALIDATOR-INIT"></a>
## 50.2. 初始化函式 [#](#OAUTH-VALIDATOR-INIT)

<a id="id-1.8.17.7.2"></a>

OAuth 驗證器模組是從 [oauth_validator_libraries](../../server-administration/runtime-config/runtime-config-connection.md#GUC-OAUTH-VALIDATOR-LIBRARIES) 所列出的共享程式庫中動態載入的。模組會在有進行中的登入程序提出要求時，依需要載入。系統會使用一般的程式庫搜尋路徑來定位該程式庫。為了提供驗證器回呼函式，並表明該程式庫是一個 OAuth 驗證器模組，程式庫必須提供一個名為 `_PG_oauth_validator_module_init` 的函式。這個函式的回傳值必須是一個指向 `OAuthValidatorCallbacks` 結構型別的指標，其中包含一個魔術數字，以及指向該模組各個權杖驗證函式的指標。回傳的指標必須具有伺服器生命週期，通常的做法是把它定義為全域範圍中的 `static const` 變數。

```

typedef struct OAuthValidatorCallbacks
{
    uint32        magic;            /* must be set to PG_OAUTH_VALIDATOR_MAGIC */

    ValidatorStartupCB startup_cb;
    ValidatorShutdownCB shutdown_cb;
    ValidatorValidateCB validate_cb;
} OAuthValidatorCallbacks;

typedef const OAuthValidatorCallbacks *(*OAuthValidatorModuleInit) (void);
```

只有 `validate_cb` 回呼函式是必要的，其餘皆為選用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/oauth-validator-init.html)（原文版本：18.6；核對日期：2026-09-24）
