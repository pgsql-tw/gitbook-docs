<a id="MANAGE-AG-TEMPLATEDBS"></a>

## 22.3. 範本資料庫 [#](#MANAGE-AG-TEMPLATEDBS)

`CREATE DATABASE` 實際上是透過複製既有資料庫來運作的。
依預設，它會複製名為
`template1` 的標準系統資料庫。<a id="id-1.6.9.6.2.3"></a>因此該資料庫就是用來建立新資料庫的
「範本（template）」。如果你在 `template1` 中新增物件，
這些物件就會被複製到之後所建立的使用者資料庫中。這樣的
行為讓你能對資料庫中標準物件集合進行站台在地化（site-local）的修改。
舉例來說，如果你在 `template1` 中安裝了程序語言 PL/Perl，
那麼使用者資料庫在建立時就會自動具備該語言，
不需要額外採取任何動作。

不過，`CREATE DATABASE` 並不會複製附加在來源資料庫上的資料庫層級
`GRANT` 權限。新資料庫會具有預設的資料庫層級權限。

還有第二個標準系統資料庫，名為
`template0`。<a id="id-1.6.9.6.4.2"></a>該資料庫所包含的資料，
與 `template1` 最初的內容相同，
也就是說，只包含你所使用的
PostgreSQL 版本預先定義的標準物件。`template0`
在資料庫叢集初始化之後，就絕對不應該被更改。透過指示
`CREATE DATABASE` 複製 `template0` 而非
`template1`，你可以建立一個「純淨（pristine）」的使用者
資料庫（也就是其中不存在使用者自訂物件，且系統
物件也未被更動的資料庫），其中不含
`template1` 中任何站台在地化新增的內容。這在還原
`pg_dump` 傾印檔時特別方便：傾印指令稿應該還原到一個
純淨的資料庫中，以確保能重新建立出被傾印資料庫的正確內容，
而不會與後來可能
被加入 `template1` 的物件發生衝突。

另一個常見的複製 `template0` 而非
`template1` 的原因是：複製 `template0` 時
可以指定新的編碼與語系設定，而複製
`template1` 則必須沿用其本身的設定。
這是因為 `template1` 可能包含編碼相關
或語系相關的資料，而 `template0` 則確定不含這類資料。

若要透過複製 `template0` 來建立資料庫，可使用：

```

CREATE DATABASE dbname TEMPLATE template0;
```

在 SQL 環境中執行，或：

```

createdb -T template0 dbname
```

在殼層（shell）中執行。

你可以建立額外的範本資料庫，事實上，只要在
`CREATE DATABASE` 中指定其名稱作為範本，就能複製
叢集中的任何資料庫。不過，重要的是要了解，這（目前）並不打算作為
通用的「`COPY DATABASE`」機制。
其主要限制是：在複製來源資料庫的過程中，不能有其他工作階段
連線到該資料庫。若 `CREATE
DATABASE` 開始執行時已存在其他連線，就會執行失敗；
在複製作業進行期間，系統也會阻止新的
連線連往來源資料庫。

`pg_database`<a id="id-1.6.9.6.8.2"></a> 中有兩個對每個
資料庫都很有用的旗標：`datistemplate` 與
`datallowconn` 這兩個欄位。`datistemplate`
可以被設定，用來表示某個資料庫是要作為
`CREATE DATABASE` 的範本使用。若設定了這個旗標，該資料庫可以被任何具有 `CREATEDB` 權限的使用者複製；若未設定，
則只有超級使用者與該資料庫的擁有者可以複製它。
若 `datallowconn` 為 false，則不允許對該資料庫建立新連線
（但既有的工作階段並不會僅因為將此旗標設為 false 就被終止）。`template0`
資料庫通常會被標記為 `datallowconn = false`，以防止其被修改。
`template0` 與 `template1`
都應該始終標記為 `datistemplate = true`。

### 注意

除了 `template1` 是 `CREATE DATABASE` 在未特別指定來源資料庫時
預設使用的名稱這項事實之外，`template1` 與 `template0`
本身並沒有任何特殊地位。
舉例來說，你可以刪除 `template1`，再從
`template0` 重新建立它，而不會有任何不良後果。這種
作法在你不小心於 `template1` 中新增了一堆雜物時，
可能會是明智的選擇。（若要刪除 `template1`，
必須先讓 `pg_database.datistemplate = false`。）

資料庫叢集初始化時，也會建立
`postgres` 資料庫。這個資料庫的用途是作為使用者與應用程式連線的
預設資料庫。它只是 `template1` 的一份複本，
若有需要，可以將其刪除並重新建立。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/manage-ag-templatedbs.html)（原文版本：18.6；核對日期：2026-09-25）
