<a id="OAUTH-VALIDATOR-CALLBACKS"></a>
## 50.3. OAuth 驗證器回呼函式 [#](#OAUTH-VALIDATOR-CALLBACKS)

[50.3.1. 啟動回呼](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-STARTUP)

[50.3.2. 驗證回呼](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-VALIDATE)

[50.3.3. 關閉回呼](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-SHUTDOWN)

OAuth 驗證器模組透過定義一組回呼函式來實作其功能。伺服器會依需要呼叫這些回呼函式，以處理來自使用者的驗證請求。

<a id="OAUTH-VALIDATOR-CALLBACK-STARTUP"></a>

### 50.3.1. 啟動回呼 [#](#OAUTH-VALIDATOR-CALLBACK-STARTUP)

`startup_cb` 回呼函式會在載入模組後立即執行。此回呼函式可用來設定本地狀態，並視需要執行額外的初始化。若驗證器模組有狀態需要保存，可使用 `state->private_data` 來儲存。

```

typedef void (*ValidatorStartupCB) (ValidatorModuleState *state);
```

<a id="OAUTH-VALIDATOR-CALLBACK-VALIDATE"></a>

### 50.3.2. 驗證回呼 [#](#OAUTH-VALIDATOR-CALLBACK-VALIDATE)

`validate_cb` 回呼函式會在使用者嘗試以 OAuth 進行驗證時，於 OAuth 交換過程中執行。先前呼叫中設定的任何狀態，都可以在 `state->private_data` 中取得。

```

typedef bool (*ValidatorValidateCB) (const ValidatorModuleState *state,
                                     const char *token, const char *role,
                                     ValidatorModuleResult *result);
```

*`token`* 將包含待驗證的持有者權杖。PostgreSQL 已確保該權杖在語法上格式正確，但尚未執行其他驗證。*`role`* 將包含使用者請求登入所使用的角色。此回呼函式必須在 `result` 結構中設定輸出參數，其定義如下：

```

typedef struct ValidatorModuleResult
{
    bool        authorized;
    char       *authn_id;
} ValidatorModuleResult;
```

只有當模組將 `result->authorized` 設為 `true` 時，連線才會繼續進行。若要驗證使用者身分，應將（依權杖判斷出的）已驗證使用者名稱以 palloc 配置後，回傳於 `result->authn_id` 欄位中。或者，若權杖有效但無法判斷相關聯的使用者身分，`result->authn_id` 可設為 NULL。

驗證器可回傳 `false` 以表示發生內部錯誤，此時任何結果參數都會被忽略，連線將會失敗。否則驗證器應回傳 `true`，表示它已處理該權杖並做出授權決策。

`validate_cb` 回傳後的行為，取決於實際的 HBA 設定。正常情況下，`result->authn_id` 使用者名稱必須與使用者登入所使用的角色完全相符（此行為可透過使用者對應調整）。但當依據啟用 `delegate_ident_mapping` 的 HBA 規則進行驗證時，PostgreSQL 完全不會對 `result->authn_id` 的值執行任何檢查；此時便須由驗證器自行確保該權杖具備足夠的權限，讓使用者能以所指定的 *`role`* 登入。

<a id="OAUTH-VALIDATOR-CALLBACK-SHUTDOWN"></a>

### 50.3.3. 關閉回呼 [#](#OAUTH-VALIDATOR-CALLBACK-SHUTDOWN)

`shutdown_cb` 回呼函式會在伺服器後端完成該連線的權杖驗證後執行。若驗證器模組配置了任何狀態，此回呼函式應將其釋放，以避免資源洩漏。

```

typedef void (*ValidatorShutdownCB) (ValidatorModuleState *state);
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/oauth-validator-callbacks.html)（原文版本：18.6；核對日期：2026-09-15）
