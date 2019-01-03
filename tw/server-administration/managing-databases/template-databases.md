---
description: 版本：11
---

# 22.3. 樣版資料庫

CREATE DATABASE 實際上是透過複製現有資料庫來作業的。預設情況下，它是複製名為 template1 的標準系統資料庫。因此，該資料庫是製作新資料庫的「樣板」。如果向 template1 新增物件，則會使這些物件複製到隨後建立的使用者資料庫中。此行為可以對資料庫中的標準物件集合進行本地的修改。例如，如果在 template1 中安裝程序語言 PL/Perl，它將自動在使用者資料庫中可用，而在建立這些資料庫時不需要採取任何額外操作。

有一個名為 template0 的第二個標準系統資料庫。此資料庫包含與 template1 初始內容相同的資料，即只有您的 PostgreSQL 版本預先定義的標準物件。初始化資料庫叢集後，永遠都不應變更 template0。透過指示 CREATE DATABASE 複製 template0 而不是 template1，您可以建立一個「virgin」使用者資料庫，其中不包含 template1 中的任何本地變更。這在恢復 pg\_dump 轉存時尤其方便：轉存腳本應該在原始資料庫中恢復，以確保重新建立轉存資料庫的正確內容，而不會與稍後可能增加到 template1 的物件發生衝突。

複製 template0 而不是 template1 的另一個常見原因是，在複製 template0 時可以指定新的編碼和區域設定，而 template1 的副本必須使用與其相同的設定。這是因為 template1 可能包含特定於編碼或特定於語言環境的資料，是 template0 所不知道的。

要透過複製 template0 建立資料庫，請使用：

```text
CREATE DATABASE dbname TEMPLATE template0;
```

在 SQL 環境，或：

```text
createdb -T template0 dbname
```

在命令列。

要建立其他樣模資料庫，實際上可以透過將其名稱指定為 CREATE DATABASE 的樣板來複製叢集中的任何資料庫。然而，重要的是要理解，這不能用作通用的「COPY DATABASE」操作。主要限制是在複製來源資料庫時不能將其他連線連接到來源資料庫。如果啟動時存在任何其他的連線，則 CREATE DATABASE 將會失敗；在複製操作期間，會阻止與來源資料庫的新連線。

每個資料庫的 pg\_database 中都存在兩個有用的標記：欄位 datistemplate 和 datallowconn。可以設定 datistemplate 以指示資料庫是否用作 CREATE DATABASE 的樣板。如果設定了此標記，則任何具有 CREATEDB 權限的使用者都可以複製資料庫；如果未設定，則只有超級使用者和資料庫的所有者才能複製它。如果 datallowconn 為 false，則不允許與該資料庫建立新的連線（但僅透過將標記設定為 false，不會終止現有連線）。template0 資料庫通常標記為 datallowconn = false 以防止其修改。template0 和 template1 都應該始終保持 datistemplate = true 標記。

#### 注意

除了名稱 template1 是 CREATE DATABASE 的預設來源資料庫名稱之外，template1 和 template0 沒有任何特殊狀態。例如，可以刪除 template1 並從 template0 重新建立它而不會產生任何不良影響。如果一個人在 template1 中不小心加入了一堆垃圾，那麼這個方案可能是可接受的。（要刪除 template1，必須具有 pg\_database.datistemplate = false。）

初始化資料庫叢集時也會建立 postgres 資料庫。此資料庫用作連線使用者和應用程序的預設資料庫。它只是 template1 的副本，可以在必要時刪除並重新建立。

