<a id="TUTORIAL-CREATEDB"></a>

## 1.3. 建立資料庫 [#](#TUTORIAL-CREATEDB)

<a id="id-1.4.3.4.2"></a><a id="id-1.4.3.4.3"></a>

要確認你能否存取資料庫伺服器，第一個測試是嘗試建立一個資料庫。一個執行中的 PostgreSQL 伺服器可以管理許多個資料庫。通常每個專案或每位使用者會使用各自獨立的資料庫。

你的環境管理員可能已經為你建立了一個資料庫。若是如此，你可以省略這個步驟，直接跳到下一節。

要從命令列建立新的資料庫（本例命名為 `mydb`），請使用下列指令：

```

$ createdb mydb
```

如果執行後沒有任何回應，表示這個步驟已成功，你可以略過本節其餘內容。

如果你看到類似下列的訊息：

```

createdb: command not found
```

表示 PostgreSQL 沒有正確安裝：可能根本沒有安裝，或是你的 shell 搜尋路徑沒有包含它。請改用絕對路徑執行這個指令：

```

$ /usr/local/pgsql/bin/createdb mydb
```

你所在環境的路徑可能不同。請聯絡你的環境管理員，或查閱安裝說明來修正這個問題。

也可能出現下列回應：

```

createdb: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: No such file or directory
        Is the server running locally and accepting connections on that socket?
```

這表示伺服器沒有啟動，或是伺服器沒有在 `createdb` 預期連線的位置監聽。同樣地，請查閱安裝說明或洽詢管理員。

也可能出現下列回應：

```

createdb: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: FATAL:  role "joe" does not exist
```

其中會顯示你自己的登入名稱。如果管理員還沒有為你建立 PostgreSQL 使用者帳號，就會發生這種情況。（PostgreSQL 使用者帳號與作業系統使用者帳號是分開的。）如果你就是管理員，請參閱[第 21 章](../../server-administration/user-manag/README.md)瞭解如何建立帳號。你必須切換成安裝 PostgreSQL 時所用的作業系統使用者（通常是 `postgres`），才能建立第一個使用者帳號。也有可能你被指派的 PostgreSQL 使用者名稱與你的作業系統使用者名稱不同；此時你需要使用 `-U` 選項，或設定環境變數 `PGUSER`，來指定你的 PostgreSQL 使用者名稱。

如果你有使用者帳號，但該帳號沒有建立資料庫所需的權限，你會看到下列訊息：

```

createdb: error: database creation failed: ERROR:  permission denied to create database
```

並不是每位使用者都有權建立新的資料庫。如果 PostgreSQL 拒絕讓你建立資料庫，就需要由環境管理員授予你建立資料庫的權限；遇到這種情況請洽詢你的環境管理員。如果你是自行安裝 PostgreSQL，那麼在本教學中，請以啟動伺服器時所用的使用者帳號登入。
[<a id="id-1.4.3.4.10.4"></a>[1]](#ftn.id-1.4.3.4.10.4)

你也可以建立其他名稱的資料庫。PostgreSQL 允許你在同一個環境中建立任意數量的資料庫。資料庫名稱的第一個字元必須是字母，長度上限為 63 個位元組。一個方便的做法是建立與你目前使用者名稱同名的資料庫。許多工具會預設使用這個資料庫名稱，因此可以省下一些輸入。要建立這個資料庫，只需輸入：

```

$ createdb
```

如果你不想再使用某個資料庫，可以將它移除。舉例來說，如果你是資料庫 `mydb` 的擁有者（建立者），可以用下列指令刪除它：

```

$ dropdb mydb
```

（這個指令不會以使用者帳號名稱作為預設的資料庫名稱，你一定要指定資料庫名稱。）這個動作會實際移除與該資料庫相關的所有檔案，而且無法復原，因此執行前務必審慎考慮。

關於 `createdb` 與 `dropdb` 的更多資訊，請分別參閱 [createdb](../../reference/reference-client/app-createdb.md) 與 [dropdb](../../reference/reference-client/app-dropdb.md)。

<br>

---

<a id="ftn.id-1.4.3.4.10.4"></a>

[[1]](#id-1.4.3.4.10.4) 
這樣做之所以可行，原因如下：PostgreSQL 使用者名稱與作業系統使用者帳號是分開的。連線到資料庫時，你可以選擇要以哪個 PostgreSQL 使用者名稱連線；如果沒有指定，預設會使用與你目前作業系統帳號相同的名稱。而且一定會有一個 PostgreSQL 使用者帳號，名稱與啟動伺服器的作業系統使用者相同，該使用者也一定擁有建立資料庫的權限。除了以該使用者登入之外，你也可以在各處都指定 `-U` 選項，選擇要以哪個 PostgreSQL 使用者名稱連線。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-createdb.html)（原文版本：18.6；核對日期：2026-09-11）
