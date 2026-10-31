<a id="GLOSSARY"></a>
## 附錄 M. 詞彙表

以下列出各個術語，以及它們在 PostgreSQL 與一般關聯式資料庫系統脈絡中的意義。

<a id="GLOSSARY-ACID"></a>

### ACID [#](#glossary-acid) <a href="#glossary-acid" id="glossary-acid"></a>


[*原子性*](README.md#glossary-atomicity)、
[*一致性*](README.md#glossary-consistency)、
[*隔離性*](README.md#glossary-isolation)與
[*持久性*](README.md#glossary-durability)。
資料庫交易的這組特性，旨在確保並行運作時，甚至在發生錯誤、電源故障等情況下，資料仍然有效。
<a id="GLOSSARY-AGGREGATE"></a>

### 彙總函式（常式）（Aggregate function） [#](#glossary-aggregate) <a href="#glossary-aggregate" id="glossary-aggregate"></a>


一種[*函式*](README.md#glossary-function)，
它會將多個輸入值結合起來（*彙總*），例如計數、平均或加總，
產生單一的輸出值。

更多資訊請參閱
[第 9.21 節](../../the-sql-language/functions/functions-aggregate.md)。

另請參閱[視窗函式（常式）](README.md#glossary-window-function)。
<a id="GLOSSARY-AM"></a>

### 存取方法（Access Method） [#](#glossary-am) <a href="#glossary-am" id="glossary-am"></a>


PostgreSQL 用來存取資料表與索引中資料的介面。
這層抽象使得新增對新型資料儲存方式的支援成為可能。

更多資訊請參閱[第 62 章](../../internals/tableam/README.md)與
[第 63 章](../../internals/indexam/README.md)。

### 分析函式（Analytic function）


請參閱[視窗函式（常式）](README.md#glossary-window-function)。
<a id="GLOSSARY-ANALYZE"></a>

### 分析（操作）（Analyze） [#](#glossary-analyze) <a href="#glossary-analyze" id="glossary-analyze"></a>


從[*資料表*](README.md#glossary-table)
及其他[*關聯*](README.md#glossary-relation)的資料中收集統計資訊的動作，
用以協助[*查詢規劃器*](README.md#glossary-planner)
決定如何執行
[*查詢*](README.md#glossary-query)。

（不要將此術語與 [EXPLAIN](../../reference/sql-commands/sql-explain.md) 命令的
`ANALYZE` 選項混淆。）

更多資訊請參閱
[ANALYZE](../../reference/sql-commands/sql-analyze.md)。
<a id="GLOSSARY-AIO"></a>

### 非同步 I/O（Asynchronous I/O，AIO）<a id="id-1.11.14.3.6.3"></a> [#](#glossary-aio) <a href="#glossary-aio" id="glossary-aio"></a>


非同步 I/O（AIO）指的是以非阻塞方式（非同步地）執行 I/O，
相對於同步 I/O 會在整個 I/O 期間阻塞。

使用 AIO 時，啟動 I/O 操作與等待該操作的結果是分開的，
因此可以同時發起多個 I/O 操作，
也可以在進行 I/O 的同時執行 CPU 密集的操作。
提高並行程度的代價是複雜度隨之增加。

另請參閱[輸入／輸出](README.md#glossary-io)。
<a id="GLOSSARY-ATOMIC"></a>

### 原子的（Atomic） [#](#glossary-atomic) <a href="#glossary-atomic" id="glossary-atomic"></a>


就[*資料項*](README.md#glossary-datum)而言：
指其值無法再拆分為更小的組成部分。

就[*資料庫交易*](README.md#glossary-transaction)而言：
請參閱[*原子性*](README.md#glossary-atomicity)。
<a id="GLOSSARY-ATOMICITY"></a>

### 原子性（Atomicity） [#](#glossary-atomicity) <a href="#glossary-atomicity" id="glossary-atomicity"></a>


[*交易*](README.md#glossary-transaction)的一種特性：
其所有操作要嘛作為單一單位全部完成，要嘛全都不完成。
此外，若在交易執行期間發生系統故障，
復原之後不會看到任何部分完成的結果。
這是 ACID 特性之一。
<a id="GLOSSARY-ATTRIBUTE"></a>

### 屬性（Attribute） [#](#glossary-attribute) <a href="#glossary-attribute" id="glossary-attribute"></a>


位於[*元組*](README.md#glossary-tuple)之中、具有特定名稱與資料型別的元素。
<a id="GLOSSARY-AUTOVACUUM"></a>

### 自動清理（程序）（Autovacuum） [#](#glossary-autovacuum) <a href="#glossary-autovacuum" id="glossary-autovacuum"></a>


一組定期執行
[*清理*](README.md#glossary-vacuum)
與[*分析*](README.md#glossary-analyze)操作的背景程序。
負責協調工作、且一直存在（除非停用自動清理）的那個
[*輔助程序*](README.md#glossary-auxiliary-proc)
稱為*自動清理啟動器*（autovacuum launcher），
而實際執行這些工作的程序稱為
*自動清理工作程序*（autovacuum workers）。

更多資訊請參閱
[第 24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)。
<a id="GLOSSARY-AUXILIARY-PROC"></a>

### 輔助程序（Auxiliary process） [#](#glossary-auxiliary-proc) <a href="#glossary-auxiliary-proc" id="glossary-auxiliary-proc"></a>


[*執行個體*](README.md#glossary-instance)內的一種程序，
負責該執行個體的某項特定背景工作。
輔助程序包括
[*自動清理啟動器*](README.md#glossary-autovacuum)
（但不包括自動清理工作程序）、
[*背景寫入程序*](README.md#glossary-background-writer)、
[*檢查點程序*](README.md#glossary-checkpointer)、
[*日誌收集器*](README.md#glossary-logger)、
[*啟動程序*](README.md#glossary-startup-process)、
[*WAL 歸檔程序*](README.md#glossary-wal-archiver)、
[*WAL 接收程序*](README.md#glossary-wal-receiver)
（但不包括 [*WAL 傳送程序*](README.md#glossary-wal-sender)）、
[*WAL 摘要程序*](README.md#glossary-wal-summarizer)，
以及 [*WAL 寫入程序*](README.md#glossary-wal-writer)。
<a id="GLOSSARY-BACKEND"></a>

### 後端（程序）（Backend） [#](#glossary-backend) <a href="#glossary-backend" id="glossary-backend"></a>


[*執行個體*](README.md#glossary-instance)中的程序，
它代表某個[*用戶端工作階段*](README.md#glossary-session)運作，
並處理該工作階段的請求。

（不要將此術語與相似的術語
[*背景工作程序*](README.md#glossary-background-worker)或
[*背景寫入程序*](README.md#glossary-background-writer)混淆。）
<a id="GLOSSARY-BACKGROUND-WORKER"></a>

### 背景工作程序（Background worker） [#](#glossary-background-worker) <a href="#glossary-background-worker" id="glossary-background-worker"></a>


[*執行個體*](README.md#glossary-instance)內的程序，
負責執行系統或使用者所提供的程式碼。
它是 PostgreSQL 多項功能的基礎架構，例如
[*邏輯複寫*](README.md#glossary-replication)
與[*平行查詢*](README.md#glossary-parallel-query)。
此外，[*擴充功能*](README.md#glossary-extension)也可以加入
自訂的背景工作程序。

更多資訊請參閱
[第 46 章](../../server-programming/bgworker/README.md)。
<a id="GLOSSARY-BACKGROUND-WRITER"></a>

### 背景寫入程序（Background writer） [#](#glossary-background-writer) <a href="#glossary-background-writer" id="glossary-background-writer"></a>


一種[*輔助程序*](README.md#glossary-auxiliary-proc)，
負責將[*共享記憶體*](README.md#glossary-shared-memory)中的髒
[*資料頁*](README.md#glossary-data-page)寫入
檔案系統。它會定期喚醒，但每次只工作一小段時間，
藉此將成本高昂的 I/O 活動分散到不同時間，
避免產生較大的 I/O 尖峰而阻擋其他程序。

更多資訊請參閱
[第 19.4.4 節](../../server-administration/runtime-config/runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER)。
<a id="GLOSSARY-BASEBACKUP"></a>

### 基礎備份（Base Backup） [#](#glossary-basebackup) <a href="#glossary-basebackup" id="glossary-basebackup"></a>


所有[*資料庫叢集*](README.md#glossary-db-cluster)
檔案的二進位複本。它由 [pg_basebackup](../../reference/reference-client/app-pgbasebackup.md) 工具產生。
搭配 WAL 檔案，它可以作為復原、日誌傳送（log shipping）或串流複寫的起點。
<a id="GLOSSARY-BLOAT"></a>

### 膨脹（Bloat） [#](#glossary-bloat) <a href="#glossary-bloat" id="glossary-bloat"></a>


資料頁中不包含目前資料列版本的空間，
例如未使用（可用）的空間或過時的資料列版本。
<a id="GLOSSARY-BOOTSTRAP-SUPERUSER"></a>

### 啟動用超級使用者（Bootstrap superuser） [#](#glossary-bootstrap-superuser) <a href="#glossary-bootstrap-superuser" id="glossary-bootstrap-superuser"></a>


在[*資料庫叢集*](README.md#glossary-db-cluster)中
第一個被初始化的[*使用者*](README.md#glossary-user)。

此使用者擁有每個資料庫中的所有系統目錄資料表。它也是所有已授予權限的
源頭角色。由於這些原因，此角色不可被刪除。

此角色同時也具有一般
[*資料庫超級使用者*](README.md#glossary-database-superuser)的行為，
而且其超級使用者身分無法被移除。
<a id="GLOSSARY-BUFFER-ACCESS-STRATEGY"></a>

### 緩衝區存取策略（Buffer Access Strategy） [#](#glossary-buffer-access-strategy) <a href="#glossary-buffer-access-strategy" id="glossary-buffer-access-strategy"></a>


有些操作會存取大量的
[*頁面*](README.md#glossary-data-page)。
*緩衝區存取策略*（Buffer Access Strategy）有助於防止這些
操作從[*共享緩衝區*](README.md#glossary-shared-memory)
逐出過多的頁面。

緩衝區存取策略會建立對有限數量
[*共享緩衝區*](README.md#glossary-shared-memory)的參照，
並循環重複使用它們。當操作需要新的頁面時，會從策略環中的緩衝區
選出一個犧牲緩衝區，這可能需要將該頁面的髒資料，
以及可能還有尚未刷寫的
[*WAL*](README.md#glossary-wal)，刷寫到永久儲存裝置。

緩衝區存取策略用於各種操作，例如
大型資料表的循序掃描、`VACUUM`、
`COPY`、`CREATE TABLE AS SELECT`、
`ALTER TABLE`、`CREATE DATABASE`、
`CREATE INDEX` 與 `CLUSTER`。
<a id="GLOSSARY-CAST"></a>

### 型別轉換（Cast） [#](#glossary-cast) <a href="#glossary-cast" id="glossary-cast"></a>


將一個[*資料項*](README.md#glossary-datum)
從其目前的資料型別轉換為另一種資料型別。

更多資訊請參閱
[CREATE CAST](../../reference/sql-commands/sql-createcast.md)。
<a id="GLOSSARY-CATALOG"></a>

### 目錄（Catalog） [#](#glossary-catalog) <a href="#glossary-catalog" id="glossary-catalog"></a>


SQL 標準使用此術語來表示在
PostgreSQL 術語中稱為
[*資料庫*](README.md#glossary-database)的東西。

（不要將此術語與
[*系統目錄*](README.md#glossary-system-catalog)混淆。）

更多資訊請參閱
[第 22.1 節](../../server-administration/managing-databases/manage-ag-overview.md)。
<a id="GLOSSARY-CHECK-CONSTRAINT"></a>

### 檢查限制條件（Check constraint） [#](#glossary-check-constraint) <a href="#glossary-check-constraint" id="glossary-check-constraint"></a>


定義在[*關聯*](README.md#glossary-relation)上的一種
[*限制條件*](README.md#glossary-constraint)，
用來限制一個或多個
[*屬性*](README.md#glossary-attribute)中允許的值。
檢查限制條件可以參照該關聯中同一資料列的任何屬性，
但不能參照同一關聯的其他資料列，也不能參照其他關聯。

更多資訊請參閱
[第 5.5 節](../../the-sql-language/ddl/ddl-constraints.md)。
<a id="GLOSSARY-CHECKPOINT"></a>

### 檢查點（Checkpoint） [#](#glossary-checkpoint) <a href="#glossary-checkpoint" id="glossary-checkpoint"></a>


[*WAL*](README.md#glossary-wal) 序列中的一個點，
在該點可以保證，堆積與索引資料檔已經以該檢查點之前
在[*共享記憶體*](README.md#glossary-shared-memory)中
修改過的所有資訊完成更新；
系統會寫入一筆*檢查點記錄*（checkpoint record）並刷寫到 WAL，
以標示該點。

檢查點也指為了達到上述定義的檢查點而執行所有必要動作的行為。
此過程會在符合預先定義的條件時啟動，
例如經過了指定的時間，或已寫入一定數量的記錄；
也可以由使用者以 `CHECKPOINT` 命令觸發。

更多資訊請參閱
[第 28.5 節](../../server-administration/wal/wal-configuration.md)。
<a id="GLOSSARY-CHECKPOINTER"></a>

### 檢查點程序（Checkpointer） [#](#glossary-checkpointer) <a href="#glossary-checkpointer" id="glossary-checkpointer"></a>


一種[*輔助程序*](README.md#glossary-auxiliary-proc)，
負責執行
[*檢查點*](README.md#glossary-checkpoint)。

### 類別（舊稱）（Class）


請參閱[關聯](README.md#glossary-relation)。
<a id="GLOSSARY-CLIENT"></a>

### 用戶端（程序）（Client） [#](#glossary-client) <a href="#glossary-client" id="glossary-client"></a>


任何（可能位於遠端的）程序，它透過
[*連線*](README.md#glossary-connection)到
[*執行個體*](README.md#glossary-instance)
來建立[*工作階段*](README.md#glossary-session)，
以便與[*資料庫*](README.md#glossary-database)互動。
<a id="GLOSSARY-CLUSTER-OWNER"></a>

### 叢集擁有者（Cluster owner） [#](#glossary-cluster-owner) <a href="#glossary-cluster-owner" id="glossary-cluster-owner"></a>


擁有[*資料目錄*](README.md#glossary-data-directory)、
並以其身分執行 `postgres` 程序的作業系統使用者。
在建立新的
[*資料庫叢集*](README.md#glossary-db-cluster)之前，
此使用者必須已經存在。

在有 `root` 使用者的作業系統上，
該使用者不得作為叢集擁有者。
<a id="GLOSSARY-COLUMN"></a>

### 欄位（Column） [#](#glossary-column) <a href="#glossary-column" id="glossary-column"></a>


位於[*資料表*](README.md#glossary-table)或
[*檢視表*](README.md#glossary-view)中的
[*屬性*](README.md#glossary-attribute)。
<a id="GLOSSARY-COMMIT"></a>

### 提交（Commit） [#](#glossary-commit) <a href="#glossary-commit" id="glossary-commit"></a>


在[*資料庫*](README.md#glossary-database)中完成一筆
[*交易*](README.md#glossary-transaction)的動作，
它使該交易對其他交易可見，並確保其
[*持久性*](README.md#glossary-durability)。

更多資訊請參閱
[COMMIT](../../reference/sql-commands/sql-commit.md)。
<a id="GLOSSARY-CONCURRENCY"></a>

### 並行（Concurrency） [#](#glossary-concurrency) <a href="#glossary-concurrency" id="glossary-concurrency"></a>


多個彼此獨立的操作在
[*資料庫*](README.md#glossary-database)中同時進行的概念。
在 PostgreSQL 中，並行是由
[*多版本並行控制*](README.md#glossary-mvcc)
機制來控制的。
<a id="GLOSSARY-CONNECTION"></a>

### 連線（Connection） [#](#glossary-connection) <a href="#glossary-connection" id="glossary-connection"></a>


用戶端程序與
[*後端*](README.md#glossary-backend)程序之間已建立的通訊管道，
通常經由網路，用以支撐一個
[*工作階段*](README.md#glossary-session)。此術語
有時也作為工作階段的同義詞使用。

更多資訊請參閱
[第 19.3 節](../../server-administration/runtime-config/runtime-config-connection.md)。
<a id="GLOSSARY-CONSISTENCY"></a>

### 一致性（Consistency） [#](#glossary-consistency) <a href="#glossary-consistency" id="glossary-consistency"></a>


[*資料庫*](README.md#glossary-database)
中的資料永遠符合
[*完整性限制條件*](README.md#glossary-constraint)的特性。
交易在提交之前，可能被允許暫時違反某些限制條件，
但如果到提交時這些違反仍未解決，
該交易就會自動被
[*回復*](README.md#glossary-rollback)。
這是 ACID 特性之一。
<a id="GLOSSARY-CONSTRAINT"></a>

### 限制條件（Constraint） [#](#glossary-constraint) <a href="#glossary-constraint" id="glossary-constraint"></a>


對[*資料表*](README.md#glossary-table)中，
或[*網域*](README.md#glossary-domain)的屬性中
所允許之資料值的限制。

更多資訊請參閱
[第 5.5 節](../../the-sql-language/ddl/ddl-constraints.md)。
<a id="GLOSSARY-CUMULATIVE-STATISTICS"></a>

### 累計統計系統（Cumulative Statistics System） [#](#glossary-cumulative-statistics) <a href="#glossary-cumulative-statistics" id="glossary-cumulative-statistics"></a>


一個系統，若已啟用，會累計關於
[*執行個體*](README.md#glossary-instance)
活動的統計資訊。

更多資訊請參閱
[第 27.2 節](../../server-administration/monitoring/monitoring-stats.md)。

### 資料區（Data area）


請參閱[資料目錄](README.md#glossary-data-directory)。
<a id="GLOSSARY-DATABASE"></a>

### 資料庫（Database） [#](#glossary-database) <a href="#glossary-database" id="glossary-database"></a>


具名的
[*區域 SQL 物件*](README.md#glossary-sql-object)集合。

更多資訊請參閱
[第 22.1 節](../../server-administration/managing-databases/manage-ag-overview.md)。
<a id="GLOSSARY-DB-CLUSTER"></a>

### 資料庫叢集（Database cluster） [#](#glossary-db-cluster) <a href="#glossary-db-cluster" id="glossary-db-cluster"></a>


由多個資料庫與全域 SQL 物件，
以及它們共同的靜態與動態中繼資料所構成的集合。
有時也稱為
*叢集*（cluster）。
資料庫叢集是使用
[initdb](../../reference/reference-server/app-initdb.md) 程式建立的。

在 PostgreSQL 中，
*叢集*一詞有時也用來指稱執行個體。
（不要將此術語與 SQL 命令 `CLUSTER` 混淆。）

另請參閱[*叢集擁有者*](README.md#glossary-cluster-owner)，
即叢集在作業系統層面的擁有者，
以及[*啟動用超級使用者*](README.md#glossary-bootstrap-superuser)，
即叢集在 PostgreSQL 中的擁有者。

### 資料庫伺服器（Database server）


請參閱[執行個體](README.md#glossary-instance)。
<a id="GLOSSARY-DATABASE-SUPERUSER"></a>

### 資料庫超級使用者（Database superuser） [#](#glossary-database-superuser) <a href="#glossary-database-superuser" id="glossary-database-superuser"></a>


具有*超級使用者身分*的角色
（請參閱[第 21.2 節](../../server-administration/user-manag/role-attributes.md)）。

常簡稱為*超級使用者*。
<a id="GLOSSARY-DATA-DIRECTORY"></a>

### 資料目錄（Data directory） [#](#glossary-data-directory) <a href="#glossary-data-directory" id="glossary-data-directory"></a>


[*伺服器*](README.md#glossary-server)檔案系統上的基礎目錄，
其中包含與某個
[*資料庫叢集*](README.md#glossary-db-cluster)
相關的所有資料檔與子目錄
（但[*資料表空間*](README.md#glossary-tablespace)除外，
[*WAL*](README.md#glossary-wal) 也可選擇性地除外）。
通常使用環境變數 `PGDATA` 來
指稱資料目錄。

一個[*叢集*](README.md#glossary-db-cluster)的儲存
空間由資料目錄加上任何額外的資料表空間組成。

更多資訊請參閱
[第 66.1 節](../../internals/storage/storage-file-layout.md)。
<a id="GLOSSARY-DATA-PAGE"></a>

### 資料頁（Data page） [#](#glossary-data-page) <a href="#glossary-data-page" id="glossary-data-page"></a>


用來儲存關聯資料的基本結構。
所有頁面的大小都相同。
資料頁通常儲存在磁碟上，各自位於某個特定檔案中，
並且可以被讀入[*共享緩衝區*](README.md#glossary-shared-memory)，
在那裡它們可以被修改，而成為
*髒*（dirty）頁面。寫入磁碟之後，
它們就會變回乾淨的。新頁面最初只存在於記憶體中，
在寫入之前也是髒的。
<a id="GLOSSARY-DATUM"></a>

### 資料項（Datum） [#](#glossary-datum) <a href="#glossary-datum" id="glossary-datum"></a>


某個 SQL 資料型別的一個值的內部表示形式。
<a id="GLOSSARY-DELETE"></a>

### 刪除（Delete） [#](#glossary-delete) <a href="#glossary-delete" id="glossary-delete"></a>


從指定的
[*資料表*](README.md#glossary-table)
或[*關聯*](README.md#glossary-relation)中移除
[*資料列*](README.md#glossary-tuple)的 SQL 命令。

更多資訊請參閱
[DELETE](../../reference/sql-commands/sql-delete.md)。
<a id="GLOSSARY-DOMAIN"></a>

### 網域（Domain） [#](#glossary-domain) <a href="#glossary-domain" id="glossary-domain"></a>


以另一個底層資料型別為基礎的使用者自訂資料型別。
它的行為與底層型別相同，只是可能會限制
允許的值的集合。

更多資訊請參閱[第 8.18 節](../../the-sql-language/datatype/domains.md)。
<a id="GLOSSARY-DURABILITY"></a>

### 持久性（Durability） [#](#glossary-durability) <a href="#glossary-durability" id="glossary-durability"></a>


一種保證：一旦
[*交易*](README.md#glossary-transaction)
已[*提交*](README.md#glossary-commit)，
即使之後發生系統故障或當機，其變更仍會保留。
這是 ACID 特性之一。

### 紀元（Epoch）


請參閱[交易 ID](README.md#glossary-xid)。
<a id="GLOSSARY-EXTENSION"></a>

### 擴充功能（Extension） [#](#glossary-extension) <a href="#glossary-extension" id="glossary-extension"></a>


可以安裝在
[*執行個體*](README.md#glossary-instance)上、
用以取得額外功能的附加軟體套件。

更多資訊請參閱
[第 36.17 節](../../server-programming/extend/extend-extensions.md)。
<a id="GLOSSARY-FILE-SEGMENT"></a>

### 檔案區段（File segment） [#](#glossary-file-segment) <a href="#glossary-file-segment" id="glossary-file-segment"></a>


儲存某個[*關聯*](README.md#glossary-relation)
資料的實體檔案。
檔案區段的大小受一個設定值限制
（通常為 1 GB），
因此若關聯超過該大小，就會被分割成多個區段。

更多資訊請參閱
[第 66.1 節](../../internals/storage/storage-file-layout.md)。

（不要將此術語與相似的術語
[*WAL 區段*](README.md#glossary-wal-file)混淆。）
<a id="GLOSSARY-FOREIGN-DATA-WRAPPER"></a>

### 外部資料包裝器（Foreign data wrapper） [#](#glossary-foreign-data-wrapper) <a href="#glossary-foreign-data-wrapper" id="glossary-foreign-data-wrapper"></a>


一種表示資料的方式，讓不在本地
[*資料庫*](README.md#glossary-database)中的資料，看起來就像位於本地的
[*資料表*](README.md#glossary-table)中一樣。透過外部資料包裝器，
可以定義[*外部伺服器*](README.md#glossary-foreign-server)與
[*外部資料表*](README.md#glossary-foreign-table)。

更多資訊請參閱
[CREATE FOREIGN DATA WRAPPER](../../reference/sql-commands/sql-createforeigndatawrapper.md)。
<a id="GLOSSARY-FOREIGN-KEY"></a>

### 外鍵（Foreign key） [#](#glossary-foreign-key) <a href="#glossary-foreign-key" id="glossary-foreign-key"></a>


定義在[*資料表*](README.md#glossary-table)中
一個或多個[*欄位*](README.md#glossary-column)上的一種
[*限制條件*](README.md#glossary-constraint)，
它要求這些[*欄位*](README.md#glossary-column)中的值
在另一個（或少數情況下為同一個）
[*資料表*](README.md#glossary-table)中
識別出零筆或一筆[*資料列*](README.md#glossary-tuple)。
<a id="GLOSSARY-FOREIGN-SERVER"></a>

### 外部伺服器（Foreign server） [#](#glossary-foreign-server) <a href="#glossary-foreign-server" id="glossary-foreign-server"></a>


具名的
[*外部資料表*](README.md#glossary-foreign-table)集合，
這些外部資料表都使用同一個
[*外部資料包裝器*](README.md#glossary-foreign-data-wrapper)，
並具有其他共同的設定值。

更多資訊請參閱
[CREATE SERVER](../../reference/sql-commands/sql-createserver.md)。
<a id="GLOSSARY-FOREIGN-TABLE"></a>

### 外部資料表（關聯）（Foreign table） [#](#glossary-foreign-table) <a href="#glossary-foreign-table" id="glossary-foreign-table"></a>


一種[*關聯*](README.md#glossary-relation)，它看起來和一般的
[*資料表*](README.md#glossary-table)一樣具有
[*資料列*](README.md#glossary-tuple)與
[*欄位*](README.md#glossary-column)，但會將
資料請求透過其
[*外部資料包裝器*](README.md#glossary-foreign-data-wrapper)轉送出去，
而外部資料包裝器會傳回依照
[*外部資料表*](README.md#glossary-foreign-table)定義
所組織的[*結果集*](README.md#glossary-result-set)。

更多資訊請參閱
[CREATE FOREIGN TABLE](../../reference/sql-commands/sql-createforeigntable.md)。
<a id="GLOSSARY-FORK"></a>

### 分支（Fork） [#](#glossary-fork) <a href="#glossary-fork" id="glossary-fork"></a>


儲存一個關聯所用的各組分段檔案集，每一組即為一個分支。
*主分支*（main fork）是實際資料所在之處。
另外還有兩個存放中繼資料的次要分支：
[*可用空間對應表*](README.md#glossary-fsm)
與[*可見性對應表*](README.md#glossary-vm)。
[*無日誌關聯*](README.md#glossary-unlogged)
另外還有一個*初始化分支*（init fork）。
<a id="GLOSSARY-FSM"></a>

### 可用空間對應表（分支）（Free space map） [#](#glossary-fsm) <a href="#glossary-fsm" id="glossary-fsm"></a>


一種儲存結構，保存資料表主分支中每個資料頁的中繼資料。
每個頁面的可用空間對應表項目，記錄該頁可供未來元組使用的
可用空間大小，其結構設計使得能夠有效率地搜尋
可容納指定大小新元組的可用空間。

更多資訊請參閱
[第 66.3 節](../../internals/storage/storage-fsm.md)。
<a id="GLOSSARY-FUNCTION"></a>

### 函式（常式）（Function） [#](#glossary-function) <a href="#glossary-function" id="glossary-function"></a>


一種常式，接收零個或多個引數、傳回零個或多個
輸出值，並且限制只能在一個交易內執行。
函式是作為查詢的一部分被呼叫的，例如透過
`SELECT`。
某些函式可以傳回
[*集合*](README.md#glossary-result-set)；這類函式
稱為*集合回傳函式*（set-returning functions）。

函式也可以供
[*觸發程序*](README.md#glossary-trigger)呼叫。

更多資訊請參閱
[CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md)。

### GMT


請參閱[UTC](README.md#glossary-utc)。
<a id="GLOSSARY-GRANT"></a>

### 授予（Grant） [#](#glossary-grant) <a href="#glossary-grant" id="glossary-grant"></a>


一個 SQL 命令，用來允許
[*使用者*](README.md#glossary-user)或
[*角色*](README.md#glossary-role)存取
[*資料庫*](README.md#glossary-database)中的特定物件。

更多資訊請參閱
[GRANT](../../reference/sql-commands/sql-grant.md)。
<a id="GLOSSARY-HEAP"></a>

### 堆積（Heap） [#](#glossary-heap) <a href="#glossary-heap" id="glossary-heap"></a>


包含某個[*關聯*](README.md#glossary-relation)之
[*資料列*](README.md#glossary-tuple)屬性的值
（也就是資料本身）。
堆積實作於該關聯[*主分支*](README.md#glossary-fork)中的
一個或多個[*檔案區段*](README.md#glossary-file-segment)之內。
<a id="GLOSSARY-HOST"></a>

### 主機（Host） [#](#glossary-host) <a href="#glossary-host" id="glossary-host"></a>


透過網路與其他電腦通訊的電腦。
此術語有時作為
[*伺服器*](README.md#glossary-server)的同義詞使用。
它也用來指稱執行
[*用戶端程序*](README.md#glossary-client)的電腦。
<a id="GLOSSARY-INDEX"></a>

### 索引（關聯）（Index） [#](#glossary-index) <a href="#glossary-index" id="glossary-index"></a>


一種[*關聯*](README.md#glossary-relation)，其中包含
從[*資料表*](README.md#glossary-table)
或[*具體化檢視表*](README.md#glossary-materialized-view)衍生的資料。
其內部結構支援對原始資料的快速檢索與存取。

更多資訊請參閱
[CREATE INDEX](../../reference/sql-commands/sql-createindex.md)。
<a id="GLOSSARY-INCREMENTAL-BACKUP"></a>

### 增量備份（Incremental backup） [#](#glossary-incremental-backup) <a href="#glossary-incremental-backup" id="glossary-incremental-backup"></a>


一種特殊的[*基礎備份*](README.md#glossary-basebackup)，
對某些檔案而言，它可能只包含自前一次備份以來被修改過的頁面，
而不是每個檔案的完整內容。和基礎備份一樣，
它由 [pg_basebackup](../../reference/reference-client/app-pgbasebackup.md) 工具產生。

要還原增量備份，需使用 [pg_combinebackup](../../reference/reference-client/app-pgcombinebackup.md) 工具，
它會將增量備份與一份基礎備份合併。
之後，復原過程可以使用
[*WAL*](README.md#glossary-wal) 使
[*資料庫叢集*](README.md#glossary-db-cluster)達到
一致的狀態。

更多資訊請參閱[第 25.3.3 節](../../server-administration/backup/continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP)。
<a id="GLOSSARY-IO"></a>

### 輸入／輸出（Input/Output，I/O） [#](#glossary-io) <a href="#glossary-io" id="glossary-io"></a>


輸入／輸出（I/O）描述程式與周邊裝置之間的通訊。
在資料庫系統的脈絡中，I/O 通常（但不限於）
指與儲存裝置或網路的互動。

另請參閱[非同步 I/O](README.md#glossary-aio)。
<a id="GLOSSARY-INSERT"></a>

### 插入（Insert） [#](#glossary-insert) <a href="#glossary-insert" id="glossary-insert"></a>


用來將新資料加入
[*資料表*](README.md#glossary-table)的 SQL 命令。

更多資訊請參閱
[INSERT](../../reference/sql-commands/sql-insert.md)。
<a id="GLOSSARY-INSTANCE"></a>

### 執行個體（Instance） [#](#glossary-instance) <a href="#glossary-instance" id="glossary-instance"></a>


一群使用共同的共享記憶體區域彼此通訊的
[*後端*](README.md#glossary-backend)與
[*輔助程序*](README.md#glossary-auxiliary-proc)。由一個
[*postmaster 程序*](README.md#glossary-postmaster)
管理該執行個體；一個執行個體恰好管理一個
[*資料庫叢集*](README.md#glossary-db-cluster)
及其所有資料庫。只要 TCP 連接埠不衝突，
同一台[*伺服器*](README.md#glossary-server)上
就可以執行多個執行個體。

執行個體負責處理 DBMS 的所有關鍵功能：
對檔案與共享記憶體的讀寫存取、
確保 ACID 特性、
與[*用戶端程序*](README.md#glossary-client)之間的
[*連線*](README.md#glossary-connection)、
權限驗證、當機復原、複寫等等。
<a id="GLOSSARY-ISOLATION"></a>

### 隔離性（Isolation） [#](#glossary-isolation) <a href="#glossary-isolation" id="glossary-isolation"></a>


一筆交易的效果在其提交之前，對
[*並行交易*](README.md#glossary-concurrency)
不可見的特性。
這是 ACID 特性之一。

更多資訊請參閱[第 13.2 節](../../the-sql-language/mvcc/transaction-iso.md)。
<a id="GLOSSARY-JOIN"></a>

### 連接（Join） [#](#glossary-join) <a href="#glossary-join" id="glossary-join"></a>


用於[*查詢*](README.md#glossary-query)中的一種操作與 SQL 關鍵字，
用來結合來自多個
[*關聯*](README.md#glossary-relation)的資料。
<a id="GLOSSARY-KEY"></a>

### 鍵（Key） [#](#glossary-key) <a href="#glossary-key" id="glossary-key"></a>


一種藉由
[*資料表*](README.md#glossary-table)或
其他[*關聯*](README.md#glossary-relation)中
一個或多個[*屬性*](README.md#glossary-attribute)
所含的值，來識別該關聯中某筆
[*資料列*](README.md#glossary-tuple)的方式。
<a id="GLOSSARY-LOCK"></a>

### 鎖定（Lock） [#](#glossary-lock) <a href="#glossary-lock" id="glossary-lock"></a>


一種機制，讓程序能夠限制或阻止對某項資源的同時存取。
<a id="GLOSSARY-LOG-FILE"></a>

### 日誌檔（Log file） [#](#glossary-log-file) <a href="#glossary-log-file" id="glossary-log-file"></a>


日誌檔包含關於各種事件、供人閱讀的文字行。
例如登入失敗、長時間執行的查詢等等。

更多資訊請參閱
[第 24.3 節](../../server-administration/maintenance/logfile-maintenance.md)。
<a id="GLOSSARY-LOGGED"></a>

### 有日誌（Logged） [#](#glossary-logged) <a href="#glossary-logged" id="glossary-logged"></a>


如果對某個[*資料表*](README.md#glossary-table)的變更會送入
[*WAL*](README.md#glossary-wal)，
該資料表就被視為[*有日誌*](README.md#glossary-logged)的。預設情況下，所有一般
資料表都是有日誌的。資料表可以在
建立時或透過 `ALTER TABLE` 命令指定為
[*無日誌*](README.md#glossary-unlogged)。
<a id="GLOSSARY-LOGGER"></a>

### 日誌收集器（程序）（Logger） [#](#glossary-logger) <a href="#glossary-logger" id="glossary-logger"></a>


一種[*輔助程序*](README.md#glossary-auxiliary-proc)，
若已啟用，它會將資料庫事件的相關資訊寫入目前的
[*日誌檔*](README.md#glossary-log-file)。
當達到某些與時間或
資料量相關的條件時，就會建立新的日誌檔。
也稱為 *syslogger*。

更多資訊請參閱
[第 19.8 節](../../server-administration/runtime-config/runtime-config-logging.md)。
<a id="GLOSSARY-LOGICAL-REPLICATION-CLUSTER"></a>

### 邏輯複寫叢集（Logical replication cluster） [#](#glossary-logical-replication-cluster) <a href="#glossary-logical-replication-cluster" id="glossary-logical-replication-cluster"></a>


由發佈者執行個體與訂閱者執行個體組成的集合，
其中發佈者執行個體將變更複寫到訂閱者執行個體。
<a id="GLOSSARY-LOG-RECORD"></a>

### 日誌記錄（Log record） [#](#glossary-log-record) <a href="#glossary-log-record" id="glossary-log-record"></a>


[*WAL 記錄*](README.md#glossary-wal-record)的舊稱。
<a id="GLOSSARY-LOG-SEQUENCE-NUMBER"></a>

### 日誌序號（Log sequence number，LSN） [#](#glossary-log-sequence-number) <a href="#glossary-log-sequence-number" id="glossary-log-sequence-number"></a>


在[*WAL*](README.md#glossary-wal) 中的位元組偏移量，
隨著每一筆新的[*WAL 記錄*](README.md#glossary-wal-record)單調遞增。

更多資訊請參閱 [`pg_lsn`](../../the-sql-language/datatype/datatype-pg-lsn.md) 與[第 28.6 節](../../server-administration/wal/wal-internals.md)。

### LSN


請參閱[日誌序號](README.md#glossary-log-sequence-number)。

### 主控伺服器（Master）


請參閱[主要伺服器](README.md#glossary-primary-server)。
<a id="GLOSSARY-MATERIALIZED"></a>

### 具體化（Materialized） [#](#glossary-materialized) <a href="#glossary-materialized" id="glossary-materialized"></a>


某些資訊已預先計算並儲存起來供日後使用，
而不是在需要時即時計算的特性。

此術語用於
[*具體化檢視表*](README.md#glossary-materialized-view)，
意思是從該檢視表的查詢所衍生出的資料，會與資料來源分開、
儲存在磁碟上。

此術語也用於某些多步驟查詢，意思是
執行某個步驟所產生的資料會儲存在記憶體中
（也可能溢寫到磁碟），以便另一個步驟可以多次讀取。
<a id="GLOSSARY-MATERIALIZED-VIEW"></a>

### 具體化檢視表（關聯）（Materialized view） [#](#glossary-materialized-view) <a href="#glossary-materialized-view" id="glossary-materialized-view"></a>


一種[*關聯*](README.md#glossary-relation)，
它由 `SELECT` 陳述式定義
（就像[*檢視表*](README.md#glossary-view)一樣），
但以與[*資料表*](README.md#glossary-table)
相同的方式儲存資料。它不能
透過 `INSERT`、`UPDATE`、
`DELETE` 或 `MERGE` 操作來修改。

更多資訊請參閱
[CREATE MATERIALIZED VIEW](../../reference/sql-commands/sql-creatematerializedview.md)。
<a id="GLOSSARY-MERGE"></a>

### 合併（Merge） [#](#glossary-merge) <a href="#glossary-merge" id="glossary-merge"></a>


一個 SQL 命令，使用來源
[*關聯*](README.md#glossary-relation)的資料，
有條件地在指定的[*資料表*](README.md#glossary-table)中新增、修改
或移除[*資料列*](README.md#glossary-tuple)。

更多資訊請參閱
[MERGE](../../reference/sql-commands/sql-merge.md)。
<a id="GLOSSARY-MVCC"></a>

### 多版本並行控制（Multi-version concurrency control，MVCC） [#](#glossary-mvcc) <a href="#glossary-mvcc" id="glossary-mvcc"></a>


一種機制，設計用來讓多個
[*交易*](README.md#glossary-transaction)
能夠讀寫相同的資料列，而不會因某個程序而導致其他
程序停頓。
在 PostgreSQL 中，MVCC 的實作方式是
在[*元組*](README.md#glossary-tuple)被修改時
建立其複本（*版本*）；在能看見舊版本的交易結束之後，
就需要移除這些舊版本。
<a id="GLOSSARY-NULL"></a>

### 空值（Null） [#](#glossary-null) <a href="#glossary-null" id="glossary-null"></a>


一種表示「不存在」的概念，是關聯式
資料庫理論的核心原則之一。它代表沒有確定的值。

### 最佳化器（Optimizer）


請參閱[查詢規劃器](README.md#glossary-planner)。
<a id="GLOSSARY-PARALLEL-QUERY"></a>

### 平行查詢（Parallel query） [#](#glossary-parallel-query) <a href="#glossary-parallel-query" id="glossary-parallel-query"></a>


一種能力：將[*查詢*](README.md#glossary-query)執行的各部分分開處理，
以便在具有多顆 CPU 的伺服器上利用平行程序。
<a id="GLOSSARY-PARTITION"></a>

### 分割區（Partition） [#](#glossary-partition) <a href="#glossary-partition" id="glossary-partition"></a>


一個較大集合中，數個互斥（彼此不重疊）的子集合之一。

就[*分割資料表*](README.md#glossary-partitioned-table)而言：
各自包含分割資料表一部分資料的資料表之一，
而該分割資料表稱為*父資料表*（parent）。
分割區本身就是一個資料表，因此也可以直接查詢；
同時，分割區有時也可以是分割資料表，
因而可以建立階層結構。

就[*查詢*](README.md#glossary-query)中的
[*視窗函式*](README.md#glossary-window-function)而言，
分割區是使用者定義的準則，用來識別
[*查詢結果集*](README.md#glossary-result-set)中
哪些相鄰的[*資料列*](README.md#glossary-tuple)
可以被該函式納入考量。
<a id="GLOSSARY-PARTITIONED-TABLE"></a>

### 分割資料表（關聯）（Partitioned table） [#](#glossary-partitioned-table) <a href="#glossary-partitioned-table" id="glossary-partitioned-table"></a>


一種[*關聯*](README.md#glossary-relation)，
在語意上與[*資料表*](README.md#glossary-table)相同，
但其儲存空間分散在數個
[*分割區*](README.md#glossary-partition)中。
<a id="GLOSSARY-POSTMASTER"></a>

### Postmaster（程序） [#](#glossary-postmaster) <a href="#glossary-postmaster" id="glossary-postmaster"></a>


[*執行個體*](README.md#glossary-instance)的第一個程序。
它會啟動並管理
[*輔助程序*](README.md#glossary-auxiliary-proc)，
並且視需要建立[*後端程序*](README.md#glossary-backend)。

更多資訊請參閱
[第 18.3 節](../../server-administration/runtime/server-start.md)。
<a id="GLOSSARY-PRIMARY-KEY"></a>

### 主鍵（Primary key） [#](#glossary-primary-key) <a href="#glossary-primary-key" id="glossary-primary-key"></a>


[*唯一限制條件*](README.md#glossary-unique-constraint)的一種特例，
定義在[*資料表*](README.md#glossary-table)或其他
[*關聯*](README.md#glossary-relation)上，
它還保證[*主鍵*](README.md#glossary-primary-key)中的所有
[*屬性*](README.md#glossary-attribute)
都沒有[*空*](README.md#glossary-null)值。
顧名思義，每個資料表只能有一個
主鍵，不過可以有多個同樣不含可為空值屬性的
唯一限制條件。
<a id="GLOSSARY-PRIMARY-SERVER"></a>

### 主要伺服器（Primary） [#](#glossary-primary-server) <a href="#glossary-primary-server" id="glossary-primary-server"></a>


當兩個或更多個[*資料庫*](README.md#glossary-database)
透過[*複寫*](README.md#glossary-replication)連結時，
被視為權威資訊來源的那台[*伺服器*](README.md#glossary-server)
稱為*主要伺服器*（primary），
也稱為*主控伺服器*（master）。
<a id="GLOSSARY-PROCEDURE"></a>

### 程序（常式）（Procedure） [#](#glossary-procedure) <a href="#glossary-procedure" id="glossary-procedure"></a>


一種常式。
其獨特之處在於不傳回值，
而且允許執行交易相關的陳述式，例如
`COMMIT` 與 `ROLLBACK`。
程序是透過 `CALL` 命令呼叫的。

更多資訊請參閱
[CREATE PROCEDURE](../../reference/sql-commands/sql-createprocedure.md)。

譯註：「不傳回值」是相對於函式的概括說法。PostgreSQL 18 的程序仍可透過 OUT 或 INOUT 參數輸出值，CALL 會傳回一筆包含這些輸出參數的結果列（請參閱 CALL 命令的說明）。
<a id="GLOSSARY-QUERY"></a>

### 查詢（Query） [#](#glossary-query) <a href="#glossary-query" id="glossary-query"></a>


由用戶端傳送給[*後端*](README.md#glossary-backend)的請求，
通常是為了傳回結果或修改資料庫中的資料。
<a id="GLOSSARY-PLANNER"></a>

### 查詢規劃器（Query planner） [#](#glossary-planner) <a href="#glossary-planner" id="glossary-planner"></a>


PostgreSQL 中專門負責
決定（*規劃*）執行[*查詢*](README.md#glossary-query)
最有效率方式的部分。
也稱為*查詢最佳化器*（query optimizer）、
*最佳化器*（optimizer），或簡稱*規劃器*（planner）。

### 記錄（Record）


請參閱[元組](README.md#glossary-tuple)。

### 回收再利用（Recycling）


請參閱[WAL 檔案](README.md#glossary-wal-file)。
<a id="GLOSSARY-REFERENTIAL-INTEGRITY"></a>

### 參照完整性（Referential integrity） [#](#glossary-referential-integrity) <a href="#glossary-referential-integrity" id="glossary-referential-integrity"></a>


一種藉由[*外鍵*](README.md#glossary-foreign-key)
限制某個[*關聯*](README.md#glossary-relation)中資料的方式，
使其在另一個
[*關聯*](README.md#glossary-relation)中必須有相符的資料。
<a id="GLOSSARY-RELATION"></a>

### 關聯（Relation） [#](#glossary-relation) <a href="#glossary-relation" id="glossary-relation"></a>


[*資料庫*](README.md#glossary-database)中
所有具有名稱、以及依特定順序定義之
[*屬性*](README.md#glossary-attribute)清單的物件之通稱。
[*資料表*](README.md#glossary-table)、
[*序列*](README.md#glossary-sequence)、
[*檢視表*](README.md#glossary-view)、
[*外部資料表*](README.md#glossary-foreign-table)、
[*具體化檢視表*](README.md#glossary-materialized-view)、
複合型別與
[*索引*](README.md#glossary-index)都是關聯。

更廣泛地說，關聯是元組的集合；例如，
查詢的結果也是一個關聯。

在 PostgreSQL 中，
*類別*（Class）是
*關聯*的舊式同義詞。
<a id="GLOSSARY-REPLICA"></a>

### 複本（伺服器）（Replica） [#](#glossary-replica) <a href="#glossary-replica" id="glossary-replica"></a>


與[*主要*](README.md#glossary-primary-server)資料庫
配對的[*資料庫*](README.md#glossary-database)，
它維護主要資料庫部分或全部資料的複本。
這麼做的首要原因，是為了讓該資料能被更廣泛地存取，
以及在[*主要伺服器*](README.md#glossary-primary-server)
無法使用時維持資料的可用性。
<a id="GLOSSARY-REPLICATION"></a>

### 複寫（Replication） [#](#glossary-replication) <a href="#glossary-replication" id="glossary-replication"></a>


將一台[*伺服器*](README.md#glossary-server)上的資料
重現到另一台稱為[*複本*](README.md#glossary-replica)的伺服器上的動作。
其形式可以是*實體複寫*（physical replication），
也就是將一台伺服器上所有的檔案變更逐字複製；
或是*邏輯複寫*（logical replication），也就是將資料變更中定義好的子集，
以較高層級的表示形式傳遞。
<a id="GLOSSARY-RESTARTPOINT"></a>

### 重新啟動點（Restartpoint） [#](#glossary-restartpoint) <a href="#glossary-restartpoint" id="glossary-restartpoint"></a>


在[*複本*](README.md#glossary-replica)上執行的一種
[*檢查點*](README.md#glossary-checkpoint)變體。

更多資訊請參閱[第 28.5 節](../../server-administration/wal/wal-configuration.md)。
<a id="GLOSSARY-RESULT-SET"></a>

### 結果集（Result set） [#](#glossary-result-set) <a href="#glossary-result-set" id="glossary-result-set"></a>


SQL 命令完成時，從[*後端程序*](README.md#glossary-backend)
傳送給[*用戶端*](README.md#glossary-client)的
[*關聯*](README.md#glossary-relation)；該命令通常是
`SELECT`，但若指定了
`RETURNING` 子句，也可以是
`INSERT`、`UPDATE`、
`DELETE` 或 `MERGE` 命令。

結果集是一個關聯，這意味著一個查詢可以用於
另一個查詢的定義中，成為
*子查詢*（subquery）。
<a id="GLOSSARY-REVOKE"></a>

### 撤銷（Revoke） [#](#glossary-revoke) <a href="#glossary-revoke" id="glossary-revoke"></a>


一個命令，用來阻止一份具名的
[*角色*](README.md#glossary-role)清單存取一組具名的
[*資料庫*](README.md#glossary-database)物件。

更多資訊請參閱
[REVOKE](../../reference/sql-commands/sql-revoke.md)。
<a id="GLOSSARY-ROLE"></a>

### 角色（Role） [#](#glossary-role) <a href="#glossary-role" id="glossary-role"></a>


對[*執行個體*](README.md#glossary-database)的存取權限集合
（原文此處的連結文字寫作 instance，但連結目標是「資料庫」詞條）。
角色本身就是一種可以授予其他角色的權限。
當多個[*使用者*](README.md#glossary-user)需要
相同的權限時，通常為了方便或確保完整性而這麼做。

更多資訊請參閱
[CREATE ROLE](../../reference/sql-commands/sql-createrole.md)。
<a id="GLOSSARY-ROLLBACK"></a>

### 回復（Rollback） [#](#glossary-rollback) <a href="#glossary-rollback" id="glossary-rollback"></a>


一個命令，用來撤銷自
[*交易*](README.md#glossary-transaction)開始以來所執行的所有操作。

更多資訊請參閱
[ROLLBACK](../../reference/sql-commands/sql-rollback.md)。
<a id="GLOSSARY-ROUTINE"></a>

### 常式（Routine） [#](#glossary-routine) <a href="#glossary-routine" id="glossary-routine"></a>


儲存在資料庫系統中、可以被呼叫執行的一組已定義指令。
常式可以用多種程式語言撰寫。
常式可以是
[*函式*](README.md#glossary-function)
（包括集合回傳函式與
[*觸發程序函式*](README.md#glossary-trigger)）、
[*彙總函式*](README.md#glossary-aggregate)，
以及[*程序*](README.md#glossary-procedure)。

許多常式已在 PostgreSQL 本身中定義，
但也可以加入使用者自訂的常式。

### 資料列（Row）


請參閱[元組](README.md#glossary-tuple)。
<a id="GLOSSARY-SAVEPOINT"></a>

### 儲存點（Savepoint） [#](#glossary-savepoint) <a href="#glossary-savepoint" id="glossary-savepoint"></a>


在[*交易*](README.md#glossary-transaction)的步驟序列中的一個特殊標記。
在此時間點之後的資料修改，
可以還原到儲存點當時的狀態。

更多資訊請參閱
[SAVEPOINT](../../reference/sql-commands/sql-savepoint.md)。
<a id="GLOSSARY-SCHEMA"></a>

### 綱要（Schema） [#](#glossary-schema) <a href="#glossary-schema" id="glossary-schema"></a>


綱要是
[*SQL 物件*](README.md#glossary-sql-object)的命名空間，
這些 SQL 物件全都位於同一個
[*資料庫*](README.md#glossary-database)中。
每個 SQL 物件必須恰好位於一個綱要中（譯註：此句過度概括，只適用於隸屬綱要的物件；如下文「SQL 物件」詞條所述，擴充功能、資料型別轉換、外部資料包裝器等區域物件並不位於任何綱要中）。

所有系統定義的 SQL 物件都位於綱要 `pg_catalog` 中。（譯註：原文此處為過度概括；系統也會在 information_schema 綱要中提供依 SQL 標準定義的檢視表，因此並非所有系統提供的 SQL 物件都位於 pg_catalog 中。）

更廣泛地說，*綱要*（schema）一詞用來指稱
某個[*資料庫*](README.md#glossary-database)或
其子集的所有資料描述（[*資料表*](README.md#glossary-table)定義、
[*限制條件*](README.md#glossary-constraint)、註解等等）。

更多資訊請參閱
[第 5.10 節](../../the-sql-language/ddl/ddl-schemas.md)。

### 區段（Segment）


請參閱[檔案區段](README.md#glossary-file-segment)。
<a id="GLOSSARY-SELECT"></a>

### 選取（Select） [#](#glossary-select) <a href="#glossary-select" id="glossary-select"></a>


用來向[*資料庫*](README.md#glossary-database)
請求資料的 SQL 命令。
一般而言，`SELECT` 命令預期不會以任何方式修改
[*資料庫*](README.md#glossary-database)，
但在查詢中呼叫的[*函式*](README.md#glossary-function)
有可能產生確實會修改資料的副作用。

更多資訊請參閱
[SELECT](../../reference/sql-commands/sql-select.md)。
<a id="GLOSSARY-SEQUENCE"></a>

### 序列（關聯）（Sequence） [#](#glossary-sequence) <a href="#glossary-sequence" id="glossary-sequence"></a>


一種用來產生值的關聯。
所產生的值通常是循序且不重複的數字。
它們常用來產生代理
[*主鍵*](README.md#glossary-primary-key)
值。
<a id="GLOSSARY-SERVER"></a>

### 伺服器（Server） [#](#glossary-server) <a href="#glossary-server" id="glossary-server"></a>


執行 PostgreSQL
[*執行個體*](README.md#glossary-instance)的電腦。
*伺服器*一詞可以指實體硬體、
容器或*虛擬機器*。

此術語有時也用來指稱執行個體或主機。
<a id="GLOSSARY-SESSION"></a>

### 工作階段（Session） [#](#glossary-session) <a href="#glossary-session" id="glossary-session"></a>


一種讓用戶端與後端能夠互動、
透過[*連線*](README.md#glossary-connection)進行通訊的狀態。
<a id="GLOSSARY-SHARED-MEMORY"></a>

### 共享記憶體（Shared memory） [#](#glossary-shared-memory) <a href="#glossary-shared-memory" id="glossary-shared-memory"></a>


由[*執行個體*](README.md#glossary-instance)
共同的程序所使用的 RAM。
它映射[*資料庫*](README.md#glossary-database)
檔案的部分內容，為
[*WAL 記錄*](README.md#glossary-wal-record)提供暫存區域，
並儲存其他共用資訊。
請注意，共享記憶體屬於整個執行個體，而不屬於單一
資料庫。

共享記憶體中最大的部分稱為*共享緩衝區*（shared buffers），
用來映射資料檔的部分內容，並以頁面為單位組織。
頁面被修改後，在寫回檔案系統之前，
都稱為髒頁面。

更多資訊請參閱
[第 19.4.1 節](../../server-administration/runtime-config/runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY)。
<a id="GLOSSARY-SQL-OBJECT"></a>

### SQL 物件（SQL object） [#](#glossary-sql-object) <a href="#glossary-sql-object" id="glossary-sql-object"></a>


任何可以用 `CREATE`
命令建立的物件。大多數物件專屬於某一個資料庫，通常
稱為*區域物件*（local objects）。

大多數區域物件位於其所屬資料庫中的某個特定
[*綱要*](README.md#glossary-schema)內，
例如[*關聯*](README.md#glossary-relation)（所有類型）、
[*常式*](README.md#glossary-function)（所有類型）、
資料型別等等。
在同一個綱要中，同一類型的這類物件，其名稱強制必須唯一（譯註：常式是例外，函式與程序可以多載，只要輸入引數的型別不同，同一個綱要中就可以有同名的常式；請參閱 CREATE FUNCTION）。

也有不位於綱要中的區域物件；例如
[*擴充功能*](README.md#glossary-extension)、
[*資料型別轉換*](README.md#glossary-cast)與
[*外部資料包裝器*](README.md#glossary-foreign-data-wrapper)。
同一類型的這類物件，其名稱在資料庫內強制必須唯一。

其他物件類型，例如
[*角色*](README.md#glossary-role)、
[*資料表空間*](README.md#glossary-tablespace)、
複寫來源、邏輯複寫的訂閱，以及
資料庫本身，都不是區域 SQL 物件，因為它們
完全存在於任何特定資料庫之外；
它們稱為*全域物件*（global objects）。

譯註：上述說法對邏輯複寫的訂閱並不精確。訂閱的資訊雖然存放在叢集共用的 pg_subscription 目錄中，但每個訂閱都隸屬於某個資料庫，名稱只須在所屬資料庫內唯一（請參閱 CREATE SUBSCRIPTION）。複寫來源則確實是叢集層級物件。
這類物件的名稱在整個資料庫叢集中強制必須唯一。

更多資訊請參閱
[第 22.1 節](../../server-administration/managing-databases/manage-ag-overview.md)。
<a id="GLOSSARY-SQL-STANDARD"></a>

### SQL 標準（SQL standard） [#](#glossary-sql-standard) <a href="#glossary-sql-standard" id="glossary-sql-standard"></a>


定義 SQL 語言的一系列文件。

### 待命伺服器（Standby）


請參閱[複本（伺服器）](README.md#glossary-replica)。
<a id="GLOSSARY-STARTUP-PROCESS"></a>

### 啟動程序（Startup process） [#](#glossary-startup-process) <a href="#glossary-startup-process" id="glossary-startup-process"></a>


一種[*輔助程序*](README.md#glossary-auxiliary-proc)，
在當機復原期間以及在
[*實體複本*](README.md#glossary-replication)中重播 WAL。

（這個名稱是沿襲歷史而來：啟動程序是在
複寫功能實作之前就命名的；這個名稱指的是它在
當機後伺服器啟動時所負責的工作。）
<a id="GLOSSARY-SUPERUSER"></a>

### 超級使用者（Superuser） [#](#glossary-superuser) <a href="#glossary-superuser" id="glossary-superuser"></a>


在本手冊中，它是
[*資料庫超級使用者*](README.md#glossary-database-superuser)的同義詞。
<a id="GLOSSARY-SYSTEM-CATALOG"></a>

### 系統目錄（System catalog） [#](#glossary-system-catalog) <a href="#glossary-system-catalog" id="glossary-system-catalog"></a>


一組[*資料表*](README.md#glossary-table)，
描述該執行個體中所有
[*SQL 物件*](README.md#glossary-sql-object)
的結構。
系統目錄位於綱要 `pg_catalog` 中。
這些資料表以內部表示形式存放資料，
通常不被認為適合供使用者查看；
有一些對使用者更友善的[*檢視表*](README.md#glossary-view)，
同樣位於綱要 `pg_catalog` 中，可以更方便地存取
其中部分資訊；另外，綱要 `information_schema` 中
還有其他資料表與檢視表
（請參閱[第 35 章](../../client-interfaces/information-schema/README.md)），依照
[*SQL 標準*](README.md#glossary-sql-standard)的規定，
提供部分相同的資訊以及額外的資訊。

更多資訊請參閱
[第 5.10 節](../../the-sql-language/ddl/ddl-schemas.md)。
<a id="GLOSSARY-TABLE"></a>

### 資料表（Table） [#](#glossary-table) <a href="#glossary-table" id="glossary-table"></a>


具有共同資料結構的[*元組*](README.md#glossary-tuple)集合
（相同數量的
[*屬性*](README.md#glossary-attribute)、相同的
順序，且每個位置具有相同的名稱與型別）。
資料表是 PostgreSQL 中最常見的
[*關聯*](README.md#glossary-relation)形式。

更多資訊請參閱
[CREATE TABLE](../../reference/sql-commands/sql-createtable.md)。
<a id="GLOSSARY-TABLESPACE"></a>

### 資料表空間（Tablespace） [#](#glossary-tablespace) <a href="#glossary-tablespace" id="glossary-tablespace"></a>


伺服器檔案系統上的一個具名位置。
所有除了在[*系統目錄*](README.md#glossary-system-catalog)中的定義之外
還需要儲存空間的[*SQL 物件*](README.md#glossary-sql-object)，
都必須屬於單一資料表空間。
最初，資料庫叢集只包含一個可用的資料表空間，
作為所有 SQL 物件的預設資料表空間，稱為 `pg_default`（譯註：此說法不夠精確。初始化時其實會建立兩個資料表空間：pg_default 是 template1 與 template0 資料庫的預設資料表空間，因此除非 CREATE DATABASE 另行指定，它也是其他資料庫的預設；另一個 pg_global 則用於叢集共用的系統目錄。請參閱第 22.6 節）。

更多資訊請參閱
[第 22.6 節](../../server-administration/managing-databases/manage-ag-tablespaces.md)。
<a id="GLOSSARY-TEMPORARY-TABLE"></a>

### 暫存資料表（Temporary table） [#](#glossary-temporary-table) <a href="#glossary-temporary-table" id="glossary-temporary-table"></a>


存在期間為一個
[*工作階段*](README.md#glossary-session)或一筆
[*交易*](README.md#glossary-transaction)之生命週期的
[*資料表*](README.md#glossary-table)，
具體是哪一種於建立時指定。
其中的資料對其他工作階段不可見，也不會
[*記錄到日誌*](README.md#glossary-logged)。
暫存資料表常用來存放多步驟操作的中間資料。

更多資訊請參閱
[CREATE TABLE](../../reference/sql-commands/sql-createtable.md)。
<a id="GLOSSARY-TOAST"></a>

### TOAST [#](#glossary-toast) <a href="#glossary-toast" id="glossary-toast"></a>


一種機制，將資料表資料列中較大的屬性切分後，
儲存在稱為 *TOAST 資料表*（TOAST table）的次要資料表中。
每個具有大型屬性的關聯都有自己的 TOAST 資料表。

更多資訊請參閱
[第 66.2 節](../../internals/storage/storage-toast.md)。
<a id="GLOSSARY-TRANSACTION"></a>

### 交易（Transaction） [#](#glossary-transaction) <a href="#glossary-transaction" id="glossary-transaction"></a>


一組必須如同單一
[*原子*](README.md#glossary-atomic)命令般運作的命令：它們作為單一單位
全部成功或全部失敗，而且在交易完成之前，其效果對
其他[*工作階段*](README.md#glossary-session)不可見；
依隔離等級不同，甚至可能在更晚之後才可見。

更多資訊請參閱
[第 13.2 節](../../the-sql-language/mvcc/transaction-iso.md)。
<a id="GLOSSARY-XID"></a>

### 交易 ID（Transaction ID） [#](#glossary-xid) <a href="#glossary-xid" id="glossary-xid"></a>


每筆交易在第一次造成資料庫修改時所取得的
數值型、唯一、依序指派的識別碼。
常縮寫為 *xid*。
儲存在磁碟上時，xid 只有 32 位元寬，因此
只能產生大約四十億個寫入交易 ID；
為了讓系統能執行超過這個數量，
會使用同樣是 32 位元寬的*紀元*（epoch）。
當計數器達到最大 xid 值時，它會從
`3` 重新開始（小於該值的值保留供特殊用途：0 為無效交易 ID、1 為初始建置交易 ID、2 為凍結交易 ID），而
紀元值會加一。
在某些情境下，紀元與 xid 值會被
合起來視為單一的 64 位元值；更多細節請參閱[第 67.1 節](../../internals/transactions/transaction-id.md)。

更多資訊請參閱
[第 8.19 節](../../the-sql-language/datatype/datatype-oid.md)。
<a id="GLOSSARY-TPS"></a>

### 每秒交易數（Transactions per second，TPS） [#](#glossary-tps) <a href="#glossary-tps" id="glossary-tps"></a>


每秒執行的平均交易數，
以一次量測執行期間所有作用中工作階段的總和計算。
這被用來作為衡量
執行個體效能特性的指標。
<a id="GLOSSARY-TRIGGER"></a>

### 觸發程序（Trigger） [#](#glossary-trigger) <a href="#glossary-trigger" id="glossary-trigger"></a>


一種[*函式*](README.md#glossary-function)，可以
定義為每當某項操作（`INSERT`、
`UPDATE`、`DELETE`、
`TRUNCATE`）套用到
[*關聯*](README.md#glossary-relation)時執行。
觸發程序會在與呼叫它的陳述式相同的
[*交易*](README.md#glossary-transaction)中執行，
而如果該函式失敗，呼叫它的陳述式也會失敗。

更多資訊請參閱
[CREATE TRIGGER](../../reference/sql-commands/sql-createtrigger.md)。
<a id="GLOSSARY-TUPLE"></a>

### 元組（Tuple） [#](#glossary-tuple) <a href="#glossary-tuple" id="glossary-tuple"></a>


依固定順序排列的[*屬性*](README.md#glossary-attribute)集合。
該順序可以由包含此元組的
[*資料表*](README.md#glossary-table)
（或其他[*關聯*](README.md#glossary-relation)）定義，
此時元組通常稱為
*資料列*（row）。它也可以由結果集的結構定義，
此時它有時稱為*記錄*（record）。
<a id="GLOSSARY-UNIQUE-CONSTRAINT"></a>

### 唯一限制條件（Unique constraint） [#](#glossary-unique-constraint) <a href="#glossary-unique-constraint" id="glossary-unique-constraint"></a>


定義在[*關聯*](README.md#glossary-relation)上的一種
[*限制條件*](README.md#glossary-constraint)，
它限制一個欄位或欄位組合中允許的值，
使每個值或值的組合在該關聯中只能出現一次——
也就是說，該關聯中沒有其他資料列包含與之相等的值。

由於[*空值*](README.md#glossary-null)
彼此不被視為相等，因此允許存在多筆含有空值的資料列，
而不會違反唯一限制條件。

譯註：這是預設的 NULLS DISTINCT 行為。若以 NULLS NOT DISTINCT 定義唯一限制條件，比較時會把空值視為彼此相等：只有當兩筆資料列在限制條件涵蓋的每個欄位上都相等（空值視為與空值相等）時才會違反限制。因此單一欄位時只能有一筆空值；但對欄位組合而言，(NULL, 1) 與 (NULL, 2) 這類其他欄位不同的組合仍可並存（請參閱第 5.5.3 節）。
<a id="GLOSSARY-UNLOGGED"></a>

### 無日誌（Unlogged） [#](#glossary-unlogged) <a href="#glossary-unlogged" id="glossary-unlogged"></a>


某些[*關聯*](README.md#glossary-relation)的一種特性：
對它們的變更不會反映在
[*WAL*](README.md#glossary-wal) 中。
這會使這些關聯無法進行複寫與當機復原。

無日誌資料表的主要用途，是存放
必須在程序之間共享的暫時性工作資料。

[*暫存資料表*](README.md#glossary-temporary-table)
一律是無日誌的。
<a id="GLOSSARY-UPDATE"></a>

### 更新（Update） [#](#glossary-update) <a href="#glossary-update" id="glossary-update"></a>


一個 SQL 命令，用來修改指定
[*資料表*](README.md#glossary-table)中可能已經存在的
[*資料列*](README.md#glossary-tuple)。
它不能建立或移除資料列。

更多資訊請參閱
[UPDATE](../../reference/sql-commands/sql-update.md)。
<a id="GLOSSARY-USER"></a>

### 使用者（User） [#](#glossary-user) <a href="#glossary-user" id="glossary-user"></a>


具有*登入權限*的[*角色*](README.md#glossary-role)
（請參閱[第 21.2 節](../../server-administration/user-manag/role-attributes.md)）。
<a id="GLOSSARY-USER-MAPPING"></a>

### 使用者對應（User mapping） [#](#glossary-user-mapping) <a href="#glossary-user-mapping" id="glossary-user-mapping"></a>


將本地[*資料庫*](README.md#glossary-database)中的登入憑證，
轉換為由[*外部資料包裝器*](README.md#glossary-foreign-data-wrapper)
所定義之遠端資料系統中的憑證。

更多資訊請參閱
[CREATE USER MAPPING](../../reference/sql-commands/sql-createusermapping.md)。
<a id="GLOSSARY-UTC"></a>

### UTC [#](#glossary-utc) <a href="#glossary-utc" id="glossary-utc"></a>


協調世界時（原文此處寫作 Universal Coordinated Time，正確的英文全名是 Coordinated Universal Time），是主要的全球時間基準，
大約等於經度零度子午線上通行的時間。
常被稱為 GMT（Greenwich Mean Time，格林威治標準時間），但這種說法並不精確。
<a id="GLOSSARY-VACUUM"></a>

### 清理（Vacuum） [#](#glossary-vacuum) <a href="#glossary-vacuum" id="glossary-vacuum"></a>


從資料表或具體化檢視表中移除過時的
[*元組版本*](README.md#glossary-tuple)，
以及 PostgreSQL 的
[*MVCC*](README.md#glossary-mvcc) 實作所需的其他密切相關處理的過程。
這可以透過
`VACUUM` 命令啟動，也可以經由
[*自動清理*](README.md#glossary-autovacuum)程序自動處理。

更多資訊請參閱
[第 24.1 節](../../server-administration/maintenance/routine-vacuuming.md)。
<a id="GLOSSARY-VIEW"></a>

### 檢視表（View） [#](#glossary-view) <a href="#glossary-view" id="glossary-view"></a>


一種由
`SELECT` 陳述式定義、但本身沒有儲存空間的[*關聯*](README.md#glossary-relation)。
每當查詢參照某個檢視表時，該檢視表的定義
就會被代入查詢中，就像使用者是以子查詢的形式
輸入它，而不是輸入檢視表的名稱一樣。

更多資訊請參閱
[CREATE VIEW](../../reference/sql-commands/sql-createview.md)。
<a id="GLOSSARY-VM"></a>

### 可見性對應表（分支）（Visibility map） [#](#glossary-vm) <a href="#glossary-vm" id="glossary-vm"></a>


一種儲存結構，保存資料表主分支中每個資料頁的中繼資料。
每個頁面的可見性對應表項目儲存兩個位元：第一個
（`all-visible`）表示該頁面中的所有元組
對所有交易都可見。第二個
（`all-frozen`）表示該頁面中的所有元組
都已標記為凍結。

### WAL


請參閱[預寫式日誌](README.md#glossary-wal)。
<a id="GLOSSARY-WAL-ARCHIVER"></a>

### WAL 歸檔程序（WAL archiver） [#](#glossary-wal-archiver) <a href="#glossary-wal-archiver" id="glossary-wal-archiver"></a>


一種[*輔助程序*](README.md#glossary-auxiliary-proc)，
若已啟用，它會保存
[*WAL 檔案*](README.md#glossary-wal-file)的複本，
用以建立備份或讓
[*複本*](README.md#glossary-replica)保持在最新狀態。

更多資訊請參閱
[第 25.3 節](../../server-administration/backup/continuous-archiving.md)。
<a id="GLOSSARY-WAL-FILE"></a>

### WAL 檔案（WAL file） [#](#glossary-wal-file) <a href="#glossary-wal-file" id="glossary-wal-file"></a>


也稱為 *WAL 區段*（WAL segment）或
*WAL 區段檔*（WAL segment file）。
為[*WAL*](README.md#glossary-wal) 提供儲存空間、
依序編號的各個檔案。
這些檔案的大小都相同，且為預先定義的大小，
並依序寫入；多個同時進行的工作階段中發生的變更，
會依發生順序交錯寫入其中。
如果系統當機，這些檔案會依序讀取，
並重播其中的每一項變更，使系統恢復到當機前的狀態。

在[*檢查點*](README.md#glossary-checkpoint)
將某個 WAL 檔案中的所有變更寫入對應的資料檔之後，
該 WAL 檔案就可以被釋放。
釋放檔案的方式可以是將它刪除，或是更改它的
名稱以便日後再使用，後者稱為
*回收再利用*（recycling）。

更多資訊請參閱
[第 28.6 節](../../server-administration/wal/wal-internals.md)。
<a id="GLOSSARY-WAL-RECORD"></a>

### WAL 記錄（WAL record） [#](#glossary-wal-record) <a href="#glossary-wal-record" id="glossary-wal-record"></a>


對單一資料變更的低階描述。
它包含足夠的資訊，使得在系統故障
導致該變更遺失時，能夠重新執行（*重播*）該資料變更。
WAL 記錄使用不可列印的二進位格式。

更多資訊請參閱
[第 28.6 節](../../server-administration/wal/wal-internals.md)。
<a id="GLOSSARY-WAL-RECEIVER"></a>

### WAL 接收程序（WAL receiver） [#](#glossary-wal-receiver) <a href="#glossary-wal-receiver" id="glossary-wal-receiver"></a>


在[*複本*](README.md#glossary-replica)上執行的一種
[*輔助程序*](README.md#glossary-auxiliary-proc)，
負責從[*主要伺服器*](README.md#glossary-primary-server)
接收 WAL，供
[*啟動程序*](README.md#glossary-startup-process)重播。

更多資訊請參閱
[第 26.2 節](../../server-administration/high-availability/warm-standby.md)。

### WAL 區段（WAL segment）


請參閱[WAL 檔案](README.md#glossary-wal-file)。
<a id="GLOSSARY-WAL-SENDER"></a>

### WAL 傳送程序（WAL sender） [#](#glossary-wal-sender) <a href="#glossary-wal-sender" id="glossary-wal-sender"></a>


一種特殊的[*後端程序*](README.md#glossary-backend)，
透過網路串流傳送 WAL。接收端可以是
[*複本*](README.md#glossary-replica)中的
[*WAL 接收程序*](README.md#glossary-wal-receiver)、
[pg_receivewal](../../reference/reference-client/app-pgreceivewal.md)，或任何其他
使用複寫協定溝通的用戶端程式。
<a id="GLOSSARY-WAL-SUMMARIZER"></a>

### WAL 摘要程序（WAL summarizer） [#](#glossary-wal-summarizer) <a href="#glossary-wal-summarizer" id="glossary-wal-summarizer"></a>


一種[*輔助程序*](README.md#glossary-auxiliary-proc)，
負責為[*增量備份*](README.md#glossary-incremental-backup)
彙整 WAL 資料的摘要。

更多資訊請參閱[第 19.5.7 節](../../server-administration/runtime-config/runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION)。
<a id="GLOSSARY-WAL-WRITER"></a>

### WAL 寫入程序（WAL writer） [#](#glossary-wal-writer) <a href="#glossary-wal-writer" id="glossary-wal-writer"></a>


一種[*輔助程序*](README.md#glossary-auxiliary-proc)，
負責將[*共享記憶體*](README.md#glossary-shared-memory)中的
[*WAL 記錄*](README.md#glossary-wal-record)寫入
[*WAL 檔案*](README.md#glossary-wal-file)。

更多資訊請參閱
[第 19.5 節](../../server-administration/runtime-config/runtime-config-wal.md)。
<a id="GLOSSARY-WINDOW-FUNCTION"></a>

### 視窗函式（常式）（Window function） [#](#glossary-window-function) <a href="#glossary-window-function" id="glossary-window-function"></a>


用於[*查詢*](README.md#glossary-query)中的一種
[*函式*](README.md#glossary-function)，
它套用於該查詢[*結果集*](README.md#glossary-result-set)的某個
[*分割區*](README.md#glossary-partition)；
函式的結果是根據同一分割區或框架中
[*資料列*](README.md#glossary-tuple)的值而得。

所有[*彙總函式*](README.md#glossary-aggregate)
都可以作為視窗函式使用，但視窗函式也可以
用來做到其他事，例如為分割區中的每一資料列給定排名。
也稱為*分析函式*（analytic functions）。

譯註：此處「所有彙總函式」只適用於一般彙總函式；有序集合（ordered-set）與假設集合（hypothetical-set）彙總函式不能作為視窗函式使用（請參閱第 9.22 節）。

更多資訊請參閱
[第 3.5 節](../../tutorial/tutorial-advanced/tutorial-window.md)。
<a id="GLOSSARY-WAL"></a>

### 預寫式日誌（Write-ahead log） [#](#glossary-wal) <a href="#glossary-wal" id="glossary-wal"></a>


隨著使用者與系統所觸發的操作進行，
記錄[*資料庫叢集*](README.md#glossary-db-cluster)中各項變更的日誌。
它由許多個別的
[*WAL 記錄*](README.md#glossary-wal-record)組成，
這些記錄依序寫入[*WAL 檔案*](README.md#glossary-wal-file)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/glossary.html)（原文版本：18.6；核對日期：2026-10-23）
