<a id="CLIENT-AUTHENTICATION-PROBLEMS"></a>

## 20.16. 驗證問題 [#](#CLIENT-AUTHENTICATION-PROBLEMS)

驗證失敗及相關問題，通常會透過以下這類錯誤訊息顯現出來：

```

FATAL:  no pg_hba.conf entry for host "123.123.123.123", user "andym", database "testdb"
```

如果你成功連上伺服器，但伺服器不願意與你溝通，最有可能出現的就是這種訊息。正如
訊息所示，伺服器拒絕了這個連線請求，因為它在
`pg_hba.conf` 設定檔中找不到相符的項目。

```

FATAL:  password authentication failed for user "andym"
```

像這樣的訊息表示你已經連上了伺服器，伺服器也願意與你溝通，但你必須
先通過 `pg_hba.conf` 檔案中指定的授權
方法才行。請檢查你所提供的密碼；若錯誤訊息中提到 Kerberos 或 ident
這類驗證方式，則請檢查對應的軟體設定。

```

FATAL:  user "andym" does not exist
```

找不到訊息中指出的資料庫使用者名稱。

```

FATAL:  database "testdb" does not exist
```

你嘗試連線的資料庫並不存在。請注意，如果你沒有指定資料庫名稱，預設會
使用資料庫使用者名稱作為資料庫名稱。

### 提示

伺服器記錄檔中可能包含比回報給用戶端更多的
驗證失敗相關資訊。如果你對失敗原因感到困惑，請檢查伺服器記錄檔。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/client-authentication-problems.html)（原文版本：18.6；核對日期：2026-09-25）
