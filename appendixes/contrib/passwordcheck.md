<a id="PASSWORDCHECK"></a>

## F.24. passwordcheck — 驗證密碼強度 [#](#PASSWORDCHECK)

[F.24.1. 設定參數](passwordcheck.md#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

<a id="id-1.11.7.34.2"></a>

`passwordcheck` 模組會在使用者透過
[CREATE ROLE](../../reference/sql-commands/sql-createrole.md) 或
[ALTER ROLE](../../reference/sql-commands/sql-alterrole.md) 設定密碼時檢查其密碼。
如果密碼被判定為過於脆弱，系統會拒絕該密碼，並使該指令以錯誤終止。

若要啟用此模組，請將 `'$libdir/passwordcheck'` 新增至
`postgresql.conf` 中的 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES)，然後重新啟動伺服器。

你可以修改原始碼，讓此模組符合你的需求。舉例來說，你可以使用
[CrackLib](https://github.com/cracklib/cracklib) 檢查密碼；只需取消 `Makefile` 中兩行內容的註解，然後重新建置模組即可。（基於授權因素，我們無法預設納入 CrackLib。）
未使用 CrackLib 時，模組會強制套用數項簡單的密碼強度規則；你可以視需要修改或擴充這些規則。

### 注意

為防止未加密的密碼透過網路傳送、寫入伺服器日誌，或以其他方式遭資料庫管理員竊取，PostgreSQL 允許使用者提供預先加密的密碼。許多用戶端程式會使用此功能，並在將密碼傳送至伺服器之前加密密碼。

這會限制 `passwordcheck` 模組的實用性，因為在這種情況下，它只能嘗試猜測密碼。因此，如果你的安全性需求很高，不建議使用 `passwordcheck`。
使用 GSSAPI 等外部驗證方法（請參閱[第 20 章](../../server-administration/client-authentication/README.md)）比依賴資料庫中的密碼更安全。

或者，你可以修改 `passwordcheck`，使其拒絕預先加密的密碼；但強制使用者以明文設定密碼也有其自身的安全風險。

<a id="PASSWORDCHECK-CONFIGURATION-PARAMETERS"></a>

### F.24.1. 設定參數 [#](#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

`passwordcheck.min_password_length` (`integer`) <a id="id-1.11.7.34.7.2.1.1.3"></a>
:   可接受的最小密碼長度，以位元組為單位。預設值為 8。只有
    超級使用者可以變更此設定。

    ### 註

    如果使用者提供預先加密的密碼，此參數不會產生任何作用。

一般會在 `postgresql.conf` 中設定此參數，但超級使用者可以在自己的工作階段中即時變更它。典型的用法如下：

```

# postgresql.conf
passwordcheck.min_password_length = 12
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/passwordcheck.html)
