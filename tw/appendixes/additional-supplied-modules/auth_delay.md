# F.3. auth\_delay

auth\_delay 讓伺服器在回報身份驗證失敗之前會短暫暫停，從而使對資料庫密碼的暴力攻擊更加困難。請注意，它不會阻止拒絕服務攻擊，甚至可能加劇攻擊，因為在回報身份驗證失敗之前等待的程序仍然會佔用連線。

要使用這個功能，必須透過 postgresql.conf 中的 [shared\_preload\_libraries](../../server-administration/server-configuration/client-connection-defaults.md#shared_preload_libraries-string) 載入此模組。

## F.3.1. Configuration Parameters

`auth_delay.milliseconds` \(`int`\)

The number of milliseconds to wait before reporting an authentication failure. The default is 0.

These parameters must be set in `postgresql.conf`. Typical usage might be:

```text
# postgresql.conf
shared_preload_libraries = 'auth_delay'

auth_delay.milliseconds = '500'
```

## F.3.2. Author

KaiGai Kohei `<`[`kaigai@ak.jp.nec.com`](mailto:kaigai@ak.jp.nec.com)`>`

