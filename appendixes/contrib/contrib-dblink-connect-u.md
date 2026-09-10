<a id="id-1.11.7.21.8.1"></a>

## dblink_connect_u

dblink_connect_u — 以不安全的方式開啟至遠端資料庫的持續連線

## 語法

```

dblink_connect_u(text connstr) returns text
dblink_connect_u(text connname, text connstr) returns text
```

<a id="id-1.11.7.21.8.5"></a>

## 說明

`dblink_connect_u()` 與 `dblink_connect()` 相同，但它允許非超級使用者使用任何驗證方法連線。

若遠端伺服器選取不涉及密碼的驗證方法，就可能發生身分冒充與後續權限提升，因為工作階段看似源自執行本機 PostgreSQL 伺服器的使用者。即使遠端伺服器要求密碼，也可能從伺服器環境供應密碼，例如屬於伺服器使用者的 `~/.pgpass` 檔案。這不僅有身分冒充風險，也可能將密碼暴露給不可信任的遠端伺服器。因此，`dblink_connect_u()` 初始安裝時會撤銷 `PUBLIC` 的所有權限，讓它除了超級使用者外無法被呼叫。某些情況下，將 `dblink_connect_u()` 的 `EXECUTE` 權限授與被視為可信任的特定使用者可能合適，但應謹慎執行。同時建議伺服器使用者的任何 `~/.pgpass` 檔案*不要*包含指定萬用字元主機名稱的任何記錄。

進一步詳細資訊請參閱 `dblink_connect()`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-connect-u.html)
