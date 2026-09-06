## F.2. `auth_delay` — 驗證失敗時暫停 [#](#AUTH-DELAY)

[F.2.1. 設定參數](auth-delay.md#AUTH-DELAY-CONFIGURATION-PARAMETERS)

[F.2.2. 作者](auth-delay.md#AUTH-DELAY-AUTHOR)

<a id="id-1.11.7.12.2"></a>

`auth_delay` 會讓伺服器在回報驗證失敗前短暫暫停，使針對資料庫密碼的暴力破解攻擊較為困難。請注意，它無法防止阻斷服務攻擊，甚至可能使情況惡化，因為等待回報驗證失敗的程序仍會占用連線槽。

此模組必須透過 `postgresql.conf` 中的 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) 載入，才能運作。

<a id="AUTH-DELAY-CONFIGURATION-PARAMETERS"></a>

### F.2.1. 設定參數 [#](#AUTH-DELAY-CONFIGURATION-PARAMETERS)

`auth_delay.milliseconds` (`integer`) <a id="id-1.11.7.12.5.2.1.1.3"></a>
:   回報驗證失敗前等待的毫秒數。預設值為 0。

這些參數必須在 `postgresql.conf` 中設定。典型的使用方式如下：

```

# postgresql.conf
shared_preload_libraries = 'auth_delay'

auth_delay.milliseconds = '500'
```

<a id="AUTH-DELAY-AUTHOR"></a>

### F.2.2. 作者 [#](#AUTH-DELAY-AUTHOR)

KaiGai Kohei `<kaigai@ak.jp.nec.com>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-delay.html)（原文版本：18.6；核對日期：2026-09-06）
