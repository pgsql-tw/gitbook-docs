<a id="MANAGE-AG-TABLESPACES"></a>

## 22.6. 資料表空間 [#](#MANAGE-AG-TABLESPACES)

<a id="id-1.6.9.9.2"></a>

PostgreSQL 的資料表空間讓資料庫管理者可以在檔案系統中定義位置，用來存放代表資料庫物件的檔案。資料表空間建立後，之後在建立資料庫物件時就能以名稱來參照它。

透過使用資料表空間，管理者可以控制 PostgreSQL 安裝環境的磁碟配置。這至少在兩方面很有用。第一，如果初始化叢集所在的磁碟分割區或磁碟區空間用盡且無法擴充，就可以在另一個分割區上建立資料表空間，並先使用它，直到系統能夠重新配置為止。

第二，資料表空間讓管理者可以根據對資料庫物件使用模式的了解來最佳化效能。舉例來說，使用非常頻繁的索引可以放在速度非常快、可用性很高的磁碟上，例如昂貴的固態儲存裝置。同時，儲存封存資料、很少被使用或對效能要求不高的資料表，則可以存放在較便宜、速度較慢的磁碟系統上。

### 警告

資料表空間雖然位於 PostgreSQL 主要資料目錄之外，但它是資料庫叢集不可分割的一部分，*不能*被當作一組獨立的資料檔案來對待。它們依賴主要資料目錄中所包含的中繼資料，因此不能附加到不同的資料庫叢集，也不能單獨備份。同樣地，如果你遺失了某個資料表空間（檔案被刪除、磁碟故障等），資料庫叢集可能會變得無法讀取或無法啟動。將資料表空間放在像 RAM 磁碟這樣的暫存檔案系統上，會危及整個叢集的可靠性。

若要定義資料表空間，請使用 [CREATE TABLESPACE](../../reference/sql-commands/sql-createtablespace.md)
指令，舉例來說：<a id="id-1.6.9.9.7.2"></a>：

```

CREATE TABLESPACE fastspace LOCATION '/ssd1/postgresql/data';
```

這個位置必須是一個已存在的空目錄，且擁有者必須是執行 PostgreSQL 的作業系統使用者。之後在此資料表空間中建立的所有物件，都會以檔案的形式儲存在這個目錄底下。這個位置不能位於可移除式或暫時性的儲存裝置上，否則如果資料表空間遺失或消失，叢集可能會無法正常運作。

### 注意

通常在同一個邏輯檔案系統上建立多個資料表空間沒有太大意義，因為你無法控制個別檔案在邏輯檔案系統中的存放位置。不過，PostgreSQL 並不會強制限制這一點，實際上它也不會直接感知你系統上的檔案系統邊界，只會把檔案存放在你告訴它使用的目錄中。

建立資料表空間本身必須以資料庫超級使用者的身分進行，但之後你可以允許一般資料庫使用者使用它，做法是授予他們該資料表空間的 `CREATE`
權限。

資料表、索引，以及整個資料庫，都可以被指定到特定的資料表空間。要這麼做，擁有該資料表空間 `CREATE`
權限的使用者，必須將資料表空間名稱作為參數傳遞給相關指令。舉例來說，以下指令會在資料表空間 `space1` 中建立一個資料表：

```

CREATE TABLE foo(i int) TABLESPACE space1;
```

另一種方式是使用 [default_tablespace](../runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLESPACE) 參數：

```

SET default_tablespace = space1;
CREATE TABLE foo(i int);
```

當 `default_tablespace` 被設為非空字串時，它會為沒有明確指定 TABLESPACE 子句的
`CREATE TABLE` 與 `CREATE INDEX` 指令，提供一個隱含的 `TABLESPACE` 子句。

另外還有一個 [temp_tablespaces](../runtime-config/runtime-config-client.md#GUC-TEMP-TABLESPACES) 參數，用來
決定暫存資料表與索引，以及用於排序大型資料集等用途之暫存
檔案的存放位置。這個參數可以設定為一份資料表空間名稱清單，而不限於單一名稱，
讓與暫存物件相關的負載能夠分散到多個資料表空間上。每次需要建立
暫存物件時，都會從清單中隨機挑選一個成員。

與資料庫關聯的資料表空間，會用來儲存該資料庫的系統目錄。此外，
若在資料庫中建立資料表、索引與暫存檔案時未指定 `TABLESPACE`
子句，且未由 `default_tablespace` 或
`temp_tablespaces`（視情況而定）指定其他選擇，則會使用這個資料表空間作為預設值。
如果建立資料庫時沒有為其指定資料表空間，它會使用其所複製之樣板資料庫相同的資料表空間。

初始化資料庫叢集時，會自動建立兩個資料表空間。
`pg_global` 資料表空間僅用於共享系統目錄。
`pg_default` 資料表空間則是
`template1` 與 `template0` 資料庫的預設資料表空間（因此，
除非在 `CREATE
DATABASE` 中以 `TABLESPACE` 子句覆寫，否則它也會是其他資料庫的預設資料表空間）。

資料表空間建立後，只要提出請求的使用者擁有足夠的權限，就可以從任何資料庫使用它。這表示在所有使用
該資料表空間的資料庫中的所有物件都被移除之前，這個資料表空間都無法被刪除。

若要移除一個空的資料表空間，請使用 [DROP TABLESPACE](../../reference/sql-commands/sql-droptablespace.md)
指令。

若要確認目前存在的資料表空間有哪些，可以查詢
[`pg_tablespace`](../../internals/catalogs/catalog-pg-tablespace.md) 系統目錄，例如

```

SELECT spcname, spcowner::regrole, pg_tablespace_location(oid) FROM pg_tablespace;
```

你可以查詢哪些資料庫使用了哪些資料表空間；
請見 [表 9.76](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-CATALOG-TABLE)。[psql](../../reference/reference-client/app-psql.md) 程式的 `\db` 中繼指令
在列出現有資料表空間時也很有用。

`$PGDATA/pg_tblspc` 目錄中包含了符號連結，分別
指向叢集中定義的各個非內建資料表空間。
雖然不建議這麼做，但你可以透過手動重新定義這些連結來調整資料表空間的
配置。無論如何，都不要在伺服器執行期間進行這項操作。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/manage-ag-tablespaces.html)（原文版本：18.6；核對日期：2026-09-25）
