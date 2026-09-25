<a id="MANAGE-AG-CREATEDB"></a>

## 22.2. 建立資料庫 [#](#MANAGE-AG-CREATEDB)

<a id="id-1.6.9.5.2"></a>

若要建立資料庫，PostgreSQL
伺服器必須已啟動並執行中（請參閱[第 18.3 節](../runtime/server-start.md)）。

資料庫是以 SQL 指令
[CREATE DATABASE](../../reference/sql-commands/sql-createdatabase.md)
建立的：

```

CREATE DATABASE name;
```

其中 *`name`* 依循 SQL 識別字的一般規則。
目前的角色會自動成為新資料庫的擁有者。稍後移除該資料庫
（同時也會移除其中所有物件，即使物件擁有者不同）
是資料庫擁有者的權限。

建立資料庫是一項受限制的操作。關於如何授予此權限，
請參閱[第 21.2 節](../user-manag/role-attributes.md)。

由於執行 `CREATE DATABASE` 指令時，
你需要先連線到資料庫伺服器，因此問題來了：
在任何一個站台上，*第一個*資料庫要如何建立？
第一個資料庫一律是在初始化資料儲存區時，
由 `initdb` 指令所建立。
（請參閱[第 18.2 節](../runtime/creating-cluster.md)。）
這個資料庫叫做
`postgres`。<a id="id-1.6.9.5.6.6"></a>因此，
要建立第一個「一般」資料庫，你可以先連線到
`postgres`。

在資料庫叢集初始化期間，還會建立另外兩個資料庫，
`template1`<a id="id-1.6.9.5.7.2"></a>
及
`template0`,<a id="id-1.6.9.5.7.4"></a>
每當叢集中建立一個新資料庫時，
基本上就是複製一份 `template1`。
這表示你在 `template1` 中所做的任何變更，
都會傳播到之後建立的所有資料庫。正因如此，
除非你希望變更傳播到每一個新建立的資料庫，
否則請避免在 `template1` 中建立物件。
`template0` 的用途，是作為
`template1` 原始內容的純淨副本。當你需要建立一個
不含任何站台自訂內容的資料庫時，
可以複製它而非 `template1`。
更多細節請參閱[第 22.3 節](manage-ag-templatedbs.md)。

為方便起見，有一個你可以從命令列（shell）
執行的程式可用來建立新資料庫，也就是
`createdb`。<a id="id-1.6.9.5.8.2"></a>

```

createdb dbname
```

`createdb` 並沒有任何魔法。它會連線到
`postgres` 資料庫，並發出
`CREATE DATABASE` 指令，
與前面所述的做法完全相同。
[createdb](../../reference/reference-client/app-createdb.md)
參考頁面包含了詳細的呼叫方式。請注意，
不帶任何引數的 `createdb` 會建立一個
以目前使用者名稱命名的資料庫。

### 注意

[第 20 章](../client-authentication/README.md)包含了
如何限制誰可以連線到指定資料庫的相關資訊。

有時候你會想要為別人建立資料庫，並讓對方
成為新資料庫的擁有者，以便他們自行
組態設定與管理該資料庫。要做到這一點，可使用以下其中一個指令：

```

CREATE DATABASE dbname OWNER rolename;
```

在 SQL 環境中執行，或者：

```

createdb -O rolename dbname
```

在命令列（shell）中執行。
只有超級使用者才能為別人（也就是為你不是其成員的角色）
建立資料庫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/manage-ag-createdb.html)（原文版本：18.6；核對日期：2026-09-25）
