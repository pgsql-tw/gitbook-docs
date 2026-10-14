<a id="STORAGE-FILE-LAYOUT"></a>

## 66.1. 資料庫檔案配置 [#](#STORAGE-FILE-LAYOUT)

本節從檔案與目錄的層級說明儲存格式。

傳統上，資料庫叢集所使用的設定檔與資料檔會一起存放在叢集的資料目錄中，這個目錄通常稱為 `PGDATA`（取自可用來定義它的環境變數名稱）。`PGDATA` 的常見位置是 `/var/lib/pgsql/data`。同一部機器上可以存在多個由不同伺服器執行個體所管理的叢集。

`PGDATA` 目錄包含數個子目錄與控制檔，如[表 66.1](storage-file-layout.md#PGDATA-CONTENTS-TABLE) 所示。除了這些必要項目之外，叢集設定檔 `postgresql.conf`、`pg_hba.conf` 與 `pg_ident.conf` 傳統上也存放在 `PGDATA` 中，不過也可以將它們放在其他地方。

<a id="PGDATA-CONTENTS-TABLE"></a>

**表 66.1. `PGDATA` 的內容**

<table border="1" class="table" summary="PGDATA 的內容"><colgroup><col/><col/></colgroup><thead><tr><th>
項目
</th><th>說明</th></tr></thead><tbody><tr><td><code class="filename">PG_VERSION</code></td><td>包含 <span class="productname">PostgreSQL</span> 主要版本號碼的檔案</td></tr><tr><td><code class="filename">base</code></td><td>包含各資料庫專屬子目錄的子目錄</td></tr><tr><td><code class="filename">current_logfiles</code></td><td>記錄日誌收集器目前正在寫入之日誌檔的檔案</td></tr><tr><td><code class="filename">global</code></td><td>包含整個叢集共用之資料表（例如
 <code class="structname">pg_database</code>）的子目錄</td></tr><tr><td><code class="filename">pg_commit_ts</code></td><td>包含交易提交時間戳記資料的子目錄</td></tr><tr><td><code class="filename">pg_dynshmem</code></td><td>包含動態共享記憶體子系統所使用之檔案的子目錄</td></tr><tr><td><code class="filename">pg_logical</code></td><td>包含邏輯解碼狀態資料的子目錄</td></tr><tr><td><code class="filename">pg_multixact</code></td><td>包含多重交易（multitransaction）狀態資料的子目錄（用於共享資料列鎖定）</td></tr><tr><td><code class="filename">pg_notify</code></td><td>包含 LISTEN/NOTIFY 狀態資料的子目錄</td></tr><tr><td><code class="filename">pg_replslot</code></td><td>包含複寫槽位資料的子目錄</td></tr><tr><td><code class="filename">pg_serial</code></td><td>包含已提交之可序列化交易相關資訊的子目錄</td></tr><tr><td><code class="filename">pg_snapshots</code></td><td>包含已匯出快照的子目錄</td></tr><tr><td><code class="filename">pg_stat</code></td><td>包含統計資訊子系統永久檔案的子目錄</td></tr><tr><td><code class="filename">pg_stat_tmp</code></td><td>包含統計資訊子系統暫存檔案的子目錄</td></tr><tr><td><code class="filename">pg_subtrans</code></td><td>包含子交易狀態資料的子目錄</td></tr><tr><td><code class="filename">pg_tblspc</code></td><td>包含指向資料表空間之符號連結的子目錄</td></tr><tr><td><code class="filename">pg_twophase</code></td><td>包含預備交易狀態檔的子目錄</td></tr><tr><td><code class="filename">pg_wal</code></td><td>包含 WAL（預寫式日誌，Write Ahead Log）檔案的子目錄</td></tr><tr><td><code class="filename">pg_xact</code></td><td>包含交易提交狀態資料的子目錄</td></tr><tr><td><code class="filename">postgresql.auto.conf</code></td><td>用來儲存由
<code class="command">ALTER SYSTEM</code> 所設定之組態參數的檔案</td></tr><tr><td><code class="filename">postmaster.opts</code></td><td>記錄伺服器上次啟動時所用命令列選項的檔案</td></tr><tr><td><code class="filename">postmaster.pid</code></td><td>一個鎖定檔，記錄目前 postmaster 的程序 ID（PID）、叢集資料目錄路徑、postmaster 啟動時間戳記、通訊埠號碼、Unix 網域 socket 目錄路徑（可能為空）、第一個有效的 listen_address（IP 位址或 <code class="literal">*</code>，若未在 TCP 上監聽則為空），以及共享記憶體區段 ID（伺服器關閉後此檔案就不存在）</td></tr></tbody></table>

<br>

叢集中的每個資料庫在 `PGDATA``/base` 內都有一個子目錄，以該資料庫在 `pg_database` 中的 OID 命名。這個子目錄是該資料庫檔案的預設位置；特別是，資料庫的系統目錄就存放在那裡。

請注意，以下各節說明的是內建的 `heap` [資料表存取方法](../tableam/README.md)以及內建[索引存取方法](../indexam/README.md)的行為。由於 PostgreSQL 具有可擴充的特性，其他存取方法的運作方式可能不同。

每個資料表與索引都存放在個別的檔案中。對於一般關聯，這些檔案是以資料表或索引的 *filenode*（檔案節點）編號命名，這個編號可以在 `pg_class`.`relfilenode` 中找到。但對於暫存關聯，檔名的形式為 `tBBB_FFF`，其中 *`BBB`* 是建立該檔案之後端的程序編號，*`FFF`* 則是 filenode 編號。無論哪一種情況，除了主檔案（又稱為主分支（main fork））之外，每個資料表與索引都有一個*可用空間對應表*（請參閱[第 66.3 節](storage-fsm.md)），用來儲存關聯中可用空間的資訊。可用空間對應表存放在一個以 filenode 編號加上後綴 `_fsm` 命名的檔案中。資料表還有一個*可見性對應表*，存放在後綴為 `_vm` 的分支中，用來追蹤哪些頁面已知不含死亡資料列。可見性對應表在[第 66.4 節](storage-vm.md)中有進一步說明。不記錄 WAL 的資料表（unlogged table）與索引有第三個分支，稱為初始化分支（initialization fork），存放在後綴為 `_init` 的分支中（請參閱[第 66.5 節](storage-init.md)）。

### 小心

請注意，雖然資料表的 filenode 經常與其 OID 相同，但*不一定*如此；某些操作，例如 `TRUNCATE`、`REINDEX`、`CLUSTER` 以及某些形式的 `ALTER TABLE`，可能會在保留 OID 的同時變更 filenode。請避免假設 filenode 與資料表 OID 相同。此外，對於某些系統目錄（包括 `pg_class` 本身），`pg_class`.`relfilenode` 的內容為零。這些系統目錄實際的 filenode 編號存放在較低層級的資料結構中，可以使用 `pg_relation_filenode()` 函式取得。

當資料表或索引超過 1 GB 時，會被分割成以 GB 為大小的*區段*。第一個區段的檔名與 filenode 相同；後續的區段則命名為 filenode.1、filenode.2 等。這種安排可以避免在有檔案大小限制的平台上發生問題。（實際上，1 GB 只是預設的區段大小。區段大小可以在建置 PostgreSQL 時使用設定選項 `--with-segsize` 調整。）原則上，可用空間對應表與可見性對應表的分支也可能需要多個區段，不過這在實務上不太可能發生。

若資料表中有欄位可能存放很大的項目，該資料表就會有一個相關聯的 *TOAST* 資料表，用來以資料列外（out-of-line）的方式儲存太大而無法直接保存在資料表資料列中的欄位值。`pg_class`.`reltoastrelid` 會從資料表連結到它的 TOAST 資料表（若有的話）。更多資訊請參閱[第 66.2 節](storage-toast.md)。

資料表與索引的內容會在[第 66.6 節](storage-page-layout.md)中進一步討論。

資料表空間會讓情況變得更複雜。每個使用者定義的資料表空間在 `PGDATA``/pg_tblspc` 目錄中都有一個符號連結，指向實體的資料表空間目錄（也就是該資料表空間的 `CREATE TABLESPACE` 命令中所指定的位置）。這個符號連結以該資料表空間的 OID 命名。在實體資料表空間目錄中，有一個名稱取決於 PostgreSQL 伺服器版本的子目錄，例如 `PG_9.0_201008051`。（使用這個子目錄的原因，是讓資料庫的各個後續版本可以使用相同的 `CREATE TABLESPACE` 位置值而不會衝突。）在這個版本專屬的子目錄中，每個在該資料表空間中有元素的資料庫都有一個子目錄，以該資料庫的 OID 命名。資料表與索引就依 filenode 命名規則存放在該目錄中。`pg_default` 資料表空間不是透過 `pg_tblspc` 存取，而是對應到 `PGDATA``/base`。同樣地，`pg_global` 資料表空間也不是透過 `pg_tblspc` 存取，而是對應到 `PGDATA``/global`。

`pg_relation_filepath()` 函式會顯示任何關聯的完整路徑（相對於 `PGDATA`）。它通常可以用來取代記住上述許多規則。但請記住，這個函式只會提供關聯主分支第一個區段的名稱——你可能需要附加區段編號，以及／或 `_fsm`、`_vm` 或 `_init`，才能找到與該關聯相關的所有檔案。

暫存檔（用於排序超過記憶體容量之資料等操作）會建立在 `PGDATA``/base/pgsql_tmp` 中；若為它們指定了 `pg_default` 以外的資料表空間，則會建立在該資料表空間目錄的 `pgsql_tmp` 子目錄中。暫存檔的名稱形式為 `pgsql_tmpPPP.NNN`，其中 *`PPP`* 是擁有該檔案之後端的 PID，*`NNN`* 則用來區分該後端的不同暫存檔。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage-file-layout.html)（原文版本：18.6；核對日期：2026-10-12）
