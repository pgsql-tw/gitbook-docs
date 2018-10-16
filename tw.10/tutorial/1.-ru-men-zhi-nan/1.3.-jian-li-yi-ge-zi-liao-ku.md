# 1.3. 建立一個資料庫

第一個測試確認你是否能夠存取一個資料庫服務，就是嘗試去建立一個資料庫。一個執行中的 PostgreSQL 服務可以管理許多個資料庫。一般來說，每一個專案或使用者會分開使用不同的資料庫。

你的系統管理員也可能已經為你建立了一個資料庫，如果是這樣的話，那你可以略過本節說明，直接進入到下一節的內容。

要建立一個新的資料庫，在本例中取名叫「mydb」，你可以使用以下的命令：

```text
$ createdb mydb
```

如果在這個步驟沒有產生任何回應，那就是成功了。你可以跳過本節剩餘的部份。

但你如果看到如下的訊息：

```text
createdb: command not found
```

這個訊息代表 PostgreSQL 並沒有被正確的安裝。不是它沒有被安裝好，那就是你的命令路徑設定並未包含這個指令。  
嘗試使用下列這個包含絕對路徑的指令看看：

```text
$ /usr/local/pgsql/bin/createdb mydb
```

命令路徑在你的系統可能會有些不同。洽詢你的系統管理員，或著檢查安裝步驟以修正這個情況。

另一種回應可能是如此：

```text
createdb: could not connect to database postgres: could not connect to server: No such file or directory
        Is the server running locally and accepting
        connections on Unix domain socket "/tmp/.s.PGSQL.5432"?
```

這代表了資料庫服務尚未啓動，或者它並不存在於createdb預設連線的位置。同樣地，檢查安裝的步驟或洽詢系統管理者。

而另一種回應也可能是：

```text
createdb: could not connect to database postgres: FATAL:  role "joe" does not exist
```

這裡指出你用來連線的使用者名稱。這種情況可能會發生在你的資料庫管理員並未建立屬於你的資料庫。（PostgreSQL 的使用者帳戶是獨立於作業系統的使用者帳戶的）如果你是資料庫管理員，請參閱[第 21 章](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/iii-server-administration/database-roles.md)，進行建立資料庫帳戶。你必須是 PostgreSQL 初始安裝的管理者（通常是 postgres），以建立第一個一般資料庫使用者的帳戶。這個情況也可能發生在，你被發配的 PostgreSQL 使用者名稱有別於你的作業系統使用者名稱，如果是這樣的話，那你需要在指令上使用 -U 選項，或者設定 PGUSER 環境變數，以指定你的 PostgreSQL 使用者名稱。

如果你有一個資料庫帳戶，但你並沒有建立資料庫的權限，你將會看到下列訊息：

```text
createdb: database creation failed: ERROR:  permission denied to create database
```

並非每一個使用者都被授權可以建立一個新的資料庫。如果 PostgreSQL 拒絕你建立資料庫，那麼系統管理者就需要賦予你建立資料庫的權限。洽詢你的系統管理者，如果是這種情況的話。如果你是自行安裝 PostgreSQL，那麼你應該以你啓動資料庫服務的使用者登入作業系統，再嘗試這個操作。

你也可以建立資料庫，但使用其他的名稱。PostgreSQL 允許在資料庫系統中建立無限制數量的資料庫。資料庫名稱必須是以英文字母為開頭，總長度限制為 63 位元組。一個簡便的方式是，建立一個與你使用者名稱同名的資料庫。許多工具會預設假定資料庫名稱和你同名，所以這可以省略一些文字的輸入。要建立這樣的資料庫，只要簡單地輸入：

```text
$ createdb
```

如果你不再使用你的資料庫，你可以移除它。舉例來說，你是 mydb 這個資料庫的擁有者（建立者），你可以使用下列指令來消毁它：

```text
$ dropdb mydb
```

（對這個指令來說，資料庫名稱並不會預設使用你的使用者同名資料庫。你必須明確地指定名稱）這個動作會完全地移除所有和這個資料庫相關的檔案，並且沒有回復的可能，所以要進行這個動作的話，請一定要考慮清楚。

更多有關於 createdb 和 dropdb 的說明，請參閱 [createdb](../../reference/client-applications/createdb.md) 和 [dropdb ](../../reference/client-applications/dropdb.md)的相關章節。

