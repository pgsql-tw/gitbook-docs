<a id="BACKUP-DUMP"></a>

## 25.1. SQL 傾印 [#](#BACKUP-DUMP)

[25.1.1. 還原傾印內容](backup-dump.md#BACKUP-DUMP-RESTORE)

[25.1.2. 使用 pg_dumpall](backup-dump.md#BACKUP-DUMP-ALL)

[25.1.3. 處理大型資料庫](backup-dump.md#BACKUP-DUMP-LARGE)

這種傾印方式的概念，是產生一個包含 SQL 指令的檔案，
當這個檔案被送回伺服器時，會重建出與傾印當下相同狀態的資料庫。
PostgreSQL 為此提供了公用程式
[pg_dump](../../reference/reference-client/app-pgdump.md)。
這個指令的基本用法為：

```

pg_dump dbname > dumpfile
```

如你所見，pg_dump 會將結果寫到標準輸出。
我們稍後會看到這一點有何用處。上述指令會建立一個文字檔，
但 pg_dump 也可以建立其他格式的檔案，
這些格式支援平行化，並能更細緻地控制物件的還原。

pg_dump 是一個一般的 PostgreSQL
用戶端應用程式（雖然是個特別聰明的用戶端）。這代表你可以
從任何能存取資料庫的遠端主機執行這個備份程序。但請記得，
pg_dump 並不會以特殊權限運作。它必須對你想備份的
所有資料表擁有讀取權限，因此若要備份整個資料庫，
你幾乎總是需要以資料庫超級使用者的身分執行它。
（若你沒有足夠的權限備份整個資料庫，仍然可以使用
`-n schema` 或 `-t table`
等選項，備份你有權限存取的部分資料庫。）

若要指定 pg_dump 應連接的資料庫伺服器，
請使用命令列選項 `-h host` 與
`-p port`。預設主機為本機，
或是你 `PGHOST` 環境變數所指定的值。
同樣地，預設連接埠由 `PGPORT` 環境變數指定，
若未設定，則採用編譯時內建的預設值。
（方便的是，伺服器通常會有相同的編譯時預設值。）

如同其他任何 PostgreSQL 用戶端應用程式，
pg_dump 預設會以與目前作業系統使用者名稱相同的
資料庫使用者名稱進行連線。若要覆寫這個行為，
可以指定 `-U` 選項，或設定環境變數
`PGUSER`。請記得，pg_dump 的連線
同樣受一般用戶端驗證機制的約束（相關說明請參閱
[第 20 章](../client-authentication/README.md)）。

相較於稍後介紹的其他備份方法，pg_dump 的一項
重要優勢在於：pg_dump 的輸出結果，
通常可以重新載入到較新版本的 PostgreSQL 中，
而檔案層級備份與持續歸檔則都高度依附於特定的伺服器版本。
pg_dump 也是唯一在將資料庫轉移到不同機器架構時
（例如從 32 位元轉移到 64 位元伺服器）依然可行的方法。

由 pg_dump 建立的傾印檔案在內部是一致的，
也就是說，這份傾印代表的是 pg_dump 開始執行時
資料庫的一份快照。pg_dump 在運作期間不會阻擋
資料庫上的其他操作。（例外情況是那些需要以獨佔鎖運作的操作，
例如大多數形式的 `ALTER TABLE`。）

<a id="BACKUP-DUMP-RESTORE"></a>

### 25.1.1. 還原傾印內容 [#](#BACKUP-DUMP-RESTORE)

由 pg_dump 建立的文字檔案，設計上是要以
psql 程式的預設設定來讀取的。還原一份文字傾印檔的
一般指令形式為

```

psql -X dbname < dumpfile
```

其中 *`dumpfile`* 是
pg_dump 指令輸出的檔案。這個指令不會建立
資料庫 *`dbname`*，因此在執行
psql 之前，你必須先自行從 `template0`
建立這個資料庫（例如使用
`createdb -T template0 dbname`）。
為確保 psql 以其預設設定執行，
請使用 `-X`（`--no-psqlrc`）選項。
psql 支援與 pg_dump 類似的選項，
用來指定要連線的資料庫伺服器及所使用的使用者名稱。詳情請參閱
[psql](../../reference/reference-client/app-psql.md) 參考頁面。

非文字格式的傾印檔案，應該使用
[pg_restore](../../reference/reference-client/app-pgrestore.md)
公用程式來還原。

在還原一份 SQL 傾印之前，所有擁有物件，
或在被傾印資料庫中的物件上被授予權限的使用者，
都必須已經存在。若非如此，還原時將無法以原本的擁有權
及／或權限重建這些物件。（有時這正是你想要的結果，
但通常並非如此。）

依預設，psql 指令稿在遇到 SQL 錯誤後
仍會繼續執行。你可能會想以設定
`ON_ERROR_STOP` 變數的方式執行
psql，改變這項行為，讓
psql 在發生 SQL 錯誤時以結束狀態碼 3 結束：

```

psql -X --set ON_ERROR_STOP=on dbname < dumpfile
```

無論採用哪種方式，你最終得到的都只會是一個部分還原的資料庫。
另一種做法是，指定整份傾印應以單一交易的方式還原，
讓還原動作要嘛完全完成，要嘛完全回復。這種模式可以透過
在 psql 命令列選項中加入 `-1` 或
`--single-transaction` 來指定。使用這個模式時，
請注意即使是一個微小的錯誤，也可能導致一個已經跑了好幾個小時的
還原動作被回復。不過，這樣做可能仍優於在部分還原的資料庫上，
手動進行複雜的善後清理工作。

pg_dump 與 psql 讀寫管線的能力，
讓你可以將一個資料庫直接從一台伺服器傾印到另一台伺服器，例如：

```

pg_dump -h host1 dbname | psql -X -h host2 dbname
```

### 重要事項

pg_dump 產生的傾印檔案，是相對於
`template0` 而言的。這代表任何透過
`template1` 加入的語言、程序等物件，
也都會被 pg_dump 一併傾印出來。因此，
在還原時，若你使用的是自訂過的 `template1`，
就必須如上例所示，從 `template0` 建立空的資料庫。

還原備份之後，最好對每個資料庫執行一次
[`ANALYZE`](../../reference/sql-commands/sql-analyze.md)，
讓查詢最佳化工具擁有有用的統計資訊；詳情請參閱
[第 24.1.3 節](../maintenance/routine-vacuuming.md#VACUUM-FOR-STATISTICS)
與
[第 24.1.6 節](../maintenance/routine-vacuuming.md#AUTOVACUUM)。
關於如何有效率地將大量資料載入 PostgreSQL，
更多建議請參閱
[第 14.4 節](../../the-sql-language/performance-tips/populate.md)。

<a id="BACKUP-DUMP-ALL"></a>

### 25.1.2. 使用 pg_dumpall [#](#BACKUP-DUMP-ALL)

pg_dump 一次只會傾印單一資料庫，
且不會傾印關於角色或資料表空間的資訊
（因為這些是叢集層級、而非資料庫層級的資料）。
為了方便傾印整個資料庫叢集的全部內容，PostgreSQL
提供了
[pg_dumpall](../../reference/reference-client/app-pg-dumpall.md)
程式。pg_dumpall 會備份指定叢集中的
每個資料庫，同時也會保存叢集層級的資料，
例如角色與資料表空間定義。這個指令的基本用法為：

```

pg_dumpall > dumpfile
```

產生的傾印檔案可以用 psql 還原：

```

psql -X -f dumpfile postgres
```

（實際上，你可以指定任何已存在的資料庫名稱作為起點，
但若你要載入的是一個空的叢集，通常應該使用
`postgres`。）在還原 pg_dumpall
的傾印檔時，一定需要具備資料庫超級使用者的存取權限，
因為這是還原角色與資料表空間資訊所必需的。若你使用了
資料表空間，請確保傾印檔中的資料表空間路徑，
適合新安裝環境。

pg_dumpall 的運作方式，是先發出用來重建角色、
資料表空間與空資料庫的指令，接著再針對每個資料庫呼叫一次
pg_dump。這代表雖然每個資料庫本身在內部是一致的，
但不同資料庫的快照彼此並不同步。

叢集層級的資料可以單獨使用 pg_dumpall 的
`--globals-only` 選項來傾印。若你是對個別
資料庫執行 pg_dump 指令，就必須另外執行這個步驟，
才能完整備份整個叢集。

<a id="BACKUP-DUMP-LARGE"></a>

### 25.1.3. 處理大型資料庫 [#](#BACKUP-DUMP-LARGE)

有些作業系統有檔案大小上限，在建立大型 pg_dump
輸出檔案時可能會造成問題。幸運的是，pg_dump
可以寫入標準輸出，因此你可以使用標準的 Unix 工具，
來解決這個潛在的問題。以下有幾種可行的方法：

**使用壓縮傾印檔。**
你可以使用自己偏好的壓縮程式，例如 gzip：

```

pg_dump dbname | gzip > filename.gz
```

以下列方式重新載入：

```

gunzip -c filename.gz | psql dbname
```

或者：

```

cat filename.gz | gunzip | psql dbname
```

**使用 `split`。**
`split` 指令可以讓你把輸出拆成多個較小的檔案，
使其大小符合底層檔案系統可接受的限制。舉例來說，
若要拆成每份 2 GB 的區塊：

```

pg_dump dbname | split -b 2G - filename
```

以下列方式重新載入：

```

cat filename* | psql dbname
```

若使用 GNU 版本的 split，可以將它與
gzip 搭配使用：

```

pg_dump dbname | split -b 2G --filter='gzip > $FILE.gz'
```

可以使用 `zcat` 來還原。

**使用 pg_dump 的自訂傾印格式。**
若 PostgreSQL 是在已安裝 zlib
壓縮函式庫的系統上建置的，自訂傾印格式會在資料寫入輸出檔案時
一併進行壓縮。這會產生與使用 `gzip` 相近的
傾印檔大小，而且還多了一項優點：可以選擇性地還原個別資料表。
以下指令會以自訂傾印格式傾印一個資料庫：

```

pg_dump -Fc dbname > filename
```

自訂格式的傾印檔並不是給 psql 使用的指令稿，
而是必須使用 pg_restore 來還原，例如：

```

pg_restore -d dbname filename
```

詳情請參閱
[pg_dump](../../reference/reference-client/app-pgdump.md)
與
[pg_restore](../../reference/reference-client/app-pgrestore.md)
參考頁面。

對於非常大型的資料庫，你可能需要將 `split`
與另外兩種方法之一搭配使用。

**使用 pg_dump 的平行傾印功能。**
若要加快大型資料庫的傾印速度，可以使用
pg_dump 的平行模式。這會同時傾印多個資料表。
你可以透過 `-j` 參數控制平行程度。平行傾印
僅支援「目錄」封存格式。

```

pg_dump -j num -F d -f out.dir dbname
```

你可以使用 `pg_restore -j` 來平行還原一份傾印檔。
這適用於任何以「自訂」或「目錄」封存模式建立的封存檔，
無論其是否是以 `pg_dump -j` 建立的。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/backup-dump.html)（原文版本：18.6；核對日期：2026-09-28）
