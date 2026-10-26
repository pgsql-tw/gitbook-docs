<a id="WARM-STANDBY"></a>

## 26.2. 日誌傳送待命伺服器 [#](#warm-standby) <a href="#warm-standby" id="warm-standby"></a>

[26.2.1. 規劃](warm-standby.md#standby-planning)

[26.2.2. 待命伺服器的運作](warm-standby.md#standby-server-operation)

[26.2.3. 為待命伺服器準備主要伺服器](warm-standby.md#preparing-primary-for-standby)

[26.2.4. 設定待命伺服器](warm-standby.md#standby-server-setup)

[26.2.5. 串流複寫](warm-standby.md#streaming-replication)

[26.2.6. 複寫插槽](warm-standby.md#streaming-replication-slots)

[26.2.7. 串接複寫](warm-standby.md#cascading-replication)

[26.2.8. 同步複寫](warm-standby.md#synchronous-replication)

[26.2.9. 待命伺服器上的持續歸檔](warm-standby.md#continuous-archiving-in-standby)

持續歸檔可用來建立*高可用性*（high
availability，HA）的叢集組態：由一台或多台
*待命伺服器*（standby server）隨時準備好在
主要伺服器故障時接手運作。這項功能一般稱為
*暖備援*（warm standby）或*日誌傳送*（log shipping）。

主要伺服器與待命伺服器共同運作來提供這項功能，
不過這些伺服器之間只是鬆散耦合。主要伺服器以
持續歸檔模式運作，而每台待命伺服器則以持續復原模式運作，
讀取來自主要伺服器的 WAL 檔案。啟用這項功能
不需要對資料庫中的資料表做任何變更，
因此相較於其他某些複寫解決方案，它的管理負擔較低。
這種組態對主要伺服器的效能影響也相對較低。

將 WAL 紀錄直接從一台資料庫伺服器搬移到另一台，
通常稱為日誌傳送。PostgreSQL
實作的是以檔案為基礎的日誌傳送，一次傳輸一個檔案
（WAL 區段）的 WAL 紀錄。WAL 檔案（16MB）可以
輕鬆且低成本地傳送到任何距離之外，無論是
相鄰的系統、同一地點的另一個系統，或是
地球另一端的另一個系統。這種技術所需的頻寬
會隨主要伺服器的交易速率而變化。
以紀錄為基礎的日誌傳送粒度更細，會透過網路連線
以增量方式串流傳送 WAL 變更（請參閱[第 26.2.5 節](warm-standby.md#streaming-replication)）。

應該注意的是，日誌傳送是非同步的，也就是說，WAL
紀錄是在交易提交之後才傳送的。因此，若主要伺服器
發生災難性故障，就會存在一段可能遺失資料的時間窗口；
尚未傳送的交易將會遺失。在以檔案為基礎的日誌傳送中，
資料遺失窗口的大小可以透過
`archive_timeout` 參數來限制，此參數最低可以設定到
只有幾秒鐘。然而，這麼低的設定
會大幅增加傳送檔案所需的頻寬。
串流複寫（請參閱[第 26.2.5 節](warm-standby.md#streaming-replication)）
則可以讓資料遺失窗口小得多。

復原效能足夠好，因此待命伺服器在被啟用後，
通常只需片刻就能完全可用。
因此，這稱為能提供高可用性的
暖備援組態。從歸檔的基礎備份還原伺服器
並向前復原（rollforward），會花上長得多的時間，因此該技術只能
作為災難復原的解決方案，而無法提供高可用性。
待命伺服器也可以用於唯讀查詢，在這種情況下，
它稱為*熱備援*（hot standby）伺服器。更多資訊請參閱
[第 26.4 節](hot-standby.md)。

<a id="id-1.6.13.16.7"></a><a id="id-1.6.13.16.8"></a><a id="id-1.6.13.16.9"></a><a id="id-1.6.13.16.10"></a><a id="id-1.6.13.16.11"></a><a id="id-1.6.13.16.12"></a><a id="STANDBY-PLANNING"></a>

### 26.2.1. 規劃 [#](#standby-planning) <a href="#standby-planning" id="standby-planning"></a>

通常明智的做法是讓主要伺服器與待命伺服器
盡可能相似，至少從資料庫伺服器的角度來看是如此。
特別是，與資料表空間相關聯的路徑名稱
會原封不動地傳遞過去，因此若使用了資料表空間功能，
主要伺服器與待命伺服器都必須使用相同的資料表空間掛載路徑。
請記住，如果在主要伺服器上執行
[CREATE TABLESPACE](../../reference/sql-commands/sql-createtablespace.md)，
則它所需的任何新掛載點，都必須在該命令執行之前，
先在主要伺服器與所有待命伺服器上建立好。硬體不需要完全相同，
但經驗顯示，在應用程式與系統的整個生命週期中，
維護兩個相同的系統要比維護兩個不同的系統來得容易。
無論如何，硬體架構都必須相同——例如，
從 32 位元系統傳送到 64 位元系統是行不通的。

一般而言，在執行不同 PostgreSQL 主要版本
的伺服器之間進行日誌傳送是不可能的。
PostgreSQL 全球開發團隊（PostgreSQL Global
Development Group）的政策是不在次要版本升級時
變更磁碟格式，因此在主要伺服器與待命伺服器上
執行不同的次要版本，很可能可以順利運作。
然而，這並未提供正式支援，建議你盡可能讓
主要伺服器與待命伺服器維持在相同的版本。
更新到新的次要版本時，最安全的做法是
先更新待命伺服器——新的次要版本能夠讀取
先前次要版本的 WAL 檔案的可能性，比反過來的情況更高。

<a id="STANDBY-SERVER-OPERATION"></a>

### 26.2.2. 待命伺服器的運作 [#](#standby-server-operation) <a href="#standby-server-operation" id="standby-server-operation"></a>

如果伺服器啟動時，資料目錄中存在
<a id="FILE-STANDBY-SIGNAL"></a>
`standby.signal`
<a id="id-1.6.13.16.14.2.3"></a>
檔案，伺服器就會進入待命模式。

在待命模式下，伺服器會持續套用從主要伺服器
接收到的 WAL。待命伺服器可以從 WAL 歸檔
（請參閱 [restore_command](../runtime-config/runtime-config-wal.md#GUC-RESTORE-COMMAND)）讀取 WAL，或透過 TCP 連線
直接從主要伺服器讀取（串流複寫）。待命伺服器
也會嘗試還原在待命叢集的
`pg_wal` 目錄中找到的任何 WAL。這通常發生在伺服器
重新啟動之後，待命伺服器會再次重放重新啟動之前
從主要伺服器串流過來的 WAL；不過你也可以隨時手動將檔案複製到
`pg_wal`，讓它們被重放。

啟動時，待命伺服器首先會呼叫 `restore_command`，
還原歸檔位置中所有可用的 WAL。一旦
到達那裡可用 WAL 的結尾，且 `restore_command`
失敗，它就會嘗試還原 `pg_wal` 目錄中任何可用的 WAL。
如果這也失敗，而且已設定串流複寫，
待命伺服器就會嘗試連線到主要伺服器，並從
在歸檔或 `pg_wal` 中找到的最後一筆有效紀錄開始串流 WAL。如果這失敗了，
或者沒有設定串流複寫，又或者連線之後中斷了，
待命伺服器就會回到步驟 1，再次嘗試從歸檔
還原檔案。這種從歸檔、`pg_wal`
以及透過串流複寫重試的迴圈會一直持續，直到伺服器
被停止或被提升為止。

當執行 `pg_ctl promote`，或
呼叫 `pg_promote()` 時，伺服器就會離開待命模式，
切換為正常運作。在失效切換之前，
歸檔或 `pg_wal` 中任何可立即取得的 WAL
都會被還原，但不會嘗試連線到主要伺服器。

<a id="PREPARING-PRIMARY-FOR-STANDBY"></a>

### 26.2.3. 為待命伺服器準備主要伺服器 [#](#preparing-primary-for-standby) <a href="#preparing-primary-for-standby" id="preparing-primary-for-standby"></a>

在主要伺服器上設定持續歸檔，將 WAL 歸檔到
待命伺服器可存取的歸檔目錄，如
[第 25.3 節](../backup/continuous-archiving.md)所述。即使主要伺服器停機，
歸檔位置也應該可以從待命伺服器存取，也就是說，它應該
位於待命伺服器本身或另一台受信任的伺服器上，而不是
位於主要伺服器上。

如果你想使用串流複寫，請在主要伺服器上設定驗證，
允許來自待命伺服器的複寫連線；
也就是建立一個角色，並在
`pg_hba.conf` 中提供一個或多個適當的項目，其資料庫欄位設為
`replication`。另外，也請確認在主要伺服器的設定檔中，
`max_wal_senders` 設為足夠大的值。
如果會使用複寫插槽，
也請確認 `max_replication_slots` 設得足夠高。

依照[第 25.3.2 節](../backup/continuous-archiving.md#backup-base-backup)所述製作基礎備份，
用來初始建立（bootstrap）待命伺服器。

<a id="STANDBY-SERVER-SETUP"></a>

### 26.2.4. 設定待命伺服器 [#](#standby-server-setup) <a href="#standby-server-setup" id="standby-server-setup"></a>

若要設定待命伺服器，請還原從主要伺服器取得的基礎備份
（請參閱[第 25.3.5 節](../backup/continuous-archiving.md#backup-pitr-recovery)）。在待命伺服器的叢集資料
目錄中建立一個
[`standby.signal`](warm-standby.md#FILE-STANDBY-SIGNAL)<a id="id-1.6.13.16.16.2.3"></a>
檔案。將 [restore_command](../runtime-config/runtime-config-wal.md#GUC-RESTORE-COMMAND) 設為一個從 WAL 歸檔
複製檔案的簡單命令。如果你打算為了高可用性
而設置多台待命伺服器，請確認 `recovery_target_timeline` 設為
`latest`（預設值），讓待命伺服器跟隨
失效切換到另一台待命伺服器時所發生的時間軸變更。

<a id="STANDBY-SERVER-SETUP-NOTE"></a>

### 注意

如果檔案不存在，[restore_command](../runtime-config/runtime-config-wal.md#GUC-RESTORE-COMMAND) 應該立即返回；
必要時，伺服器會再次重試該命令。

如果你想使用串流複寫，請在
[primary_conninfo](../runtime-config/runtime-config-replication.md#GUC-PRIMARY-CONNINFO) 中填入 libpq 連線字串，包括
主機名稱（或 IP 位址），以及連線到主要伺服器所需的
任何其他細節。如果主要伺服器需要密碼進行
驗證，該密碼也需要指定在
[primary_conninfo](../runtime-config/runtime-config-replication.md#GUC-PRIMARY-CONNINFO) 中。

如果你是為了高可用性而設定待命伺服器，
請像主要伺服器一樣設定 WAL 歸檔、連線與驗證，
因為待命伺服器在失效切換之後會作為主要伺服器運作。

如果你使用 WAL 歸檔，可以使用 [archive_cleanup_command](../runtime-config/runtime-config-wal.md#GUC-ARCHIVE-CLEANUP-COMMAND) 參數
移除待命伺服器不再需要的檔案，藉此將歸檔的大小降到最低。
pg_archivecleanup 工具程式是專門設計來
在典型的單一待命伺服器組態中搭配 `archive_cleanup_command` 使用的，
請參閱 [pg_archivecleanup](../../reference/reference-server/pgarchivecleanup.md)。
不過請注意，如果你將歸檔用於備份用途，即使
待命伺服器已不再需要某些檔案，你仍需要保留
至少從最新一次基礎備份進行復原所需的檔案。

以下是一個簡單的組態範例：

```

primary_conninfo = 'host=192.168.1.50 port=5432 user=foo password=foopass options=''-c wal_sender_timeout=5000'''
restore_command = 'cp /path/to/archive/%f %p'
archive_cleanup_command = 'pg_archivecleanup /path/to/archive %r'
```

你可以擁有任意數量的待命伺服器，但如果你使用串流
複寫，請確認在主要伺服器上將 `max_wal_senders` 設得夠高，
以允許它們同時連線。

<a id="STREAMING-REPLICATION"></a>

### 26.2.5. 串流複寫 [#](#streaming-replication) <a href="#streaming-replication" id="streaming-replication"></a>

<a id="id-1.6.13.16.17.2"></a>

串流複寫可以讓待命伺服器保持比以檔案為基礎的日誌傳送
更即時的狀態。待命伺服器會連線到
主要伺服器，主要伺服器會在 WAL 紀錄產生時就將其串流傳送給待命伺服器，
而不必等待 WAL 檔案被填滿。

串流複寫預設是非同步的
（請參閱[第 26.2.8 節](warm-standby.md#synchronous-replication)），在這種情況下，從
主要伺服器提交交易到變更在待命伺服器上變得可見之間，
會有一小段延遲。不過這段延遲
比以檔案為基礎的日誌傳送小得多，假設待命伺服器的效能
足以跟上負載，通常小於一秒。使用
串流複寫時，不需要 `archive_timeout` 來
縮小資料遺失窗口。

如果你使用串流複寫，但沒有搭配以檔案為基礎的持續
歸檔，伺服器可能會在待命伺服器收到舊的 WAL 區段之前
就將其回收。如果發生這種情況，就需要從新的基礎備份
重新初始化待命伺服器。你可以透過將
`wal_keep_size` 設為足夠大的值，以確保
WAL 區段不會過早被回收，或是為待命伺服器設定複寫
插槽，來避免這種情況。如果你設置了待命伺服器可以存取的 WAL 歸檔，
就不需要這些解決方案，因為只要歸檔保留了足夠的區段，
待命伺服器隨時都可以使用歸檔來追上進度。

若要使用串流複寫，請依照[第 26.2 節](warm-standby.md)所述，設置一台以檔案為基礎的
日誌傳送待命伺服器。將以檔案為基礎的日誌傳送待命伺服器
轉換為串流複寫待命伺服器的步驟，
是將 `primary_conninfo` 設定
指向主要伺服器。在主要伺服器上設定
[listen_addresses](../runtime-config/runtime-config-connection.md#GUC-LISTEN-ADDRESSES) 與驗證選項
（請參閱 `pg_hba.conf`），讓待命伺服器
可以連線到主要伺服器上的 `replication` 虛擬資料庫
（請參閱[第 26.2.5.1 節](warm-standby.md#STREAMING-REPLICATION-AUTHENTICATION)）。

在支援 keepalive socket 選項的系統上，設定
[tcp_keepalives_idle](../runtime-config/runtime-config-connection.md#GUC-TCP-KEEPALIVES-IDLE)、
[tcp_keepalives_interval](../runtime-config/runtime-config-connection.md#GUC-TCP-KEEPALIVES-INTERVAL) 與
[tcp_keepalives_count](../runtime-config/runtime-config-connection.md#GUC-TCP-KEEPALIVES-COUNT)，有助於主要伺服器及時
察覺中斷的連線。

設定來自待命伺服器的最大並行連線數
（詳情請參閱 [max_wal_senders](../runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS)）。

當待命伺服器啟動且 `primary_conninfo` 設定
正確時，待命伺服器會在重放歸檔中所有可用的
WAL 檔案之後連線到主要伺服器。如果連線成功
建立，你會在待命伺服器上看到一個 `walreceiver`，並在
主要伺服器上看到一個對應的 `walsender` 程序。

<a id="STREAMING-REPLICATION-AUTHENTICATION"></a>

#### 26.2.5.1. 驗證 [#](#STREAMING-REPLICATION-AUTHENTICATION)

設定複寫的存取權限，讓只有受信任的使用者
可以讀取 WAL 串流，是非常重要的，因為
很容易從中擷取出具特權的資訊。待命伺服器必須
以具有 `REPLICATION` 權限的帳號或超級使用者身分
向主要伺服器進行驗證。
建議為複寫建立一個專用的使用者帳號，具有
`REPLICATION` 與 `LOGIN`
權限。雖然 `REPLICATION`
權限賦予非常高的權限，但它不允許該使用者
修改主要系統上的任何資料，而
`SUPERUSER` 權限則允許。

複寫的用戶端驗證，是由
`pg_hba.conf` 中在 *`database`* 欄位指定 `replication`
的紀錄所控制。例如，如果待命伺服器執行於
主機 IP `192.168.1.100`，且複寫用的帳號名稱
是 `foo`，管理員可以在主要伺服器的
`pg_hba.conf` 檔案中加入以下這一行：

```

# Allow the user "foo" from host 192.168.1.100 to connect to the primary
# as a replication standby if the user's password is correctly supplied.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    replication     foo             192.168.1.100/32        scram-sha-256
```

主要伺服器的主機名稱與連接埠號碼、連線使用者名稱
以及密碼，都指定在 [primary_conninfo](../runtime-config/runtime-config-replication.md#GUC-PRIMARY-CONNINFO) 中。
密碼也可以設定在待命伺服器上的 `~/.pgpass` 檔案中
（在 *`database`*
欄位指定 `replication`）。
例如，如果主要伺服器執行於主機 IP `192.168.1.50`、
連接埠 `5432`，複寫用的帳號名稱是
`foo`，且密碼是 `foopass`，管理員
可以在待命伺服器的 `postgresql.conf` 檔案中
加入以下這一行：

```

# The standby connects to the primary that is running on host 192.168.1.50
# and port 5432 as the user "foo" whose password is "foopass".
primary_conninfo = 'host=192.168.1.50 port=5432 user=foo password=foopass'
```

<a id="STREAMING-REPLICATION-MONITORING"></a>

#### 26.2.5.2. 監控 [#](#STREAMING-REPLICATION-MONITORING)

串流複寫的一個重要健康指標，是已在主要伺服器上產生、
但尚未在待命伺服器上套用的 WAL 紀錄量。
你可以比較主要伺服器上目前的 WAL 寫入
位置，以及待命伺服器所接收到的最後一個 WAL 位置，來計算這段延遲（嚴格來說，這樣算出的是待命伺服器尚未接收的 WAL 量，也就是接收延遲；若要計算尚未套用的量，應改與待命伺服器的重放位置 pg_last_wal_replay_lsn 比較——原文此處將兩者混為一談）。
這些位置可以分別在主要伺服器上使用
`pg_current_wal_lsn`，以及在待命伺服器上使用
`pg_last_wal_receive_lsn` 來取得
（詳情請參閱[表 9.97](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-BACKUP-TABLE) 與
[表 9.98](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-RECOVERY-INFO-TABLE)）。
待命伺服器上最後的 WAL 接收位置，也會顯示在
WAL 接收程序的程序狀態中，可以使用
`ps` 命令顯示（詳情請參閱[第 27.1 節](../monitoring/monitoring-ps.md)）。

你可以透過
[`pg_stat_replication`](../monitoring/monitoring-stats.md#monitoring-pg-stat-replication-view) 檢視表取得 WAL 傳送程序的清單。
`pg_current_wal_lsn` 與該檢視表的 `sent_lsn` 欄位之間的差異很大時，
可能表示主要伺服器的負載很重；而
`sent_lsn` 與待命伺服器上的
`pg_last_wal_receive_lsn` 之間的差異，則可能表示
網路延遲，或是待命伺服器的負載很重。

在熱備援伺服器上，可以透過
[`pg_stat_wal_receiver`](../monitoring/monitoring-stats.md#monitoring-pg-stat-wal-receiver-view) 檢視表取得 WAL 接收程序的狀態。
`pg_last_wal_replay_lsn` 與該
檢視表的 `flushed_lsn` 之間的差異很大時，表示接收 WAL
的速度比重放它的速度還快。

<a id="STREAMING-REPLICATION-SLOTS"></a>

### 26.2.6. 複寫插槽 [#](#streaming-replication-slots) <a href="#streaming-replication-slots" id="streaming-replication-slots"></a>

<a id="id-1.6.13.16.18.2"></a>

複寫插槽提供一種自動化的方式，用來確保
主要伺服器在所有待命伺服器都收到 WAL 區段之前，
不會移除這些區段；並確保即使
待命伺服器已中斷連線，主要伺服器也不會移除可能導致
[復原衝突](hot-standby.md#hot-standby-conflict)的資料列。

若不使用複寫插槽，也可以改用 [wal_keep_size](../runtime-config/runtime-config-replication.md#GUC-WAL-KEEP-SIZE)，
或是使用
[archive_command](../runtime-config/runtime-config-wal.md#GUC-ARCHIVE-COMMAND) 或 [archive_library](../runtime-config/runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) 將區段儲存到歸檔中，
來防止舊的 WAL 區段被移除。
這些方法的缺點是，它們
常常會保留比所需更多的 WAL 區段，
而複寫插槽只會保留已知需要的區段數量。

同樣地，單獨使用 [hot_standby_feedback](../runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK) 而
不同時使用複寫插槽，可以防止相關的資料列
被 vacuum 移除，但在待命伺服器未連線的任何時段內，
都無法提供保護。

<a id="STREAMING-REPLICATION-SLOTS-CAUTION"></a>

### 小心

請留意，複寫插槽可能會使伺服器保留
大量 WAL 區段，以致於填滿配置給
`pg_wal` 的空間。
可以使用 [max_slot_wal_keep_size](../runtime-config/runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE) 來限制
複寫插槽所保留之 WAL 檔案的大小。

<a id="STREAMING-REPLICATION-SLOTS-MANIPULATION"></a>

#### 26.2.6.1. 查詢與操作複寫插槽 [#](#STREAMING-REPLICATION-SLOTS-MANIPULATION)

每個複寫插槽都有一個名稱，名稱可以包含小寫字母、
數字與底線字元。

現有的複寫插槽及其狀態可以在
[`pg_replication_slots`](../../internals/views/view-pg-replication-slots.md)
檢視表中查看。

插槽可以透過串流複寫
協定（請參閱[第 54.4 節](../../internals/protocol/protocol-replication.md)）或 SQL
函式（請參閱[第 9.28.6 節](../../the-sql-language/functions/functions-admin.md#functions-replication)）來建立與移除。

<a id="STREAMING-REPLICATION-SLOTS-CONFIG"></a>

#### 26.2.6.2. 組態範例 [#](#STREAMING-REPLICATION-SLOTS-CONFIG)

你可以像這樣建立複寫插槽：

```

postgres=# SELECT * FROM pg_create_physical_replication_slot('node_a_slot');
  slot_name  | lsn
-------------+-----
 node_a_slot |

postgres=# SELECT slot_name, slot_type, active FROM pg_replication_slots;
  slot_name  | slot_type | active
-------------+-----------+--------
 node_a_slot | physical  | f
(1 row)
```

若要設定待命伺服器使用此插槽，應在待命伺服器上
設定 `primary_slot_name`。以下是一個簡單的範例：

```

primary_conninfo = 'host=192.168.1.50 port=5432 user=foo password=foopass'
primary_slot_name = 'node_a_slot'
```

<a id="CASCADING-REPLICATION"></a>

### 26.2.7. 串接複寫 [#](#cascading-replication) <a href="#cascading-replication" id="cascading-replication"></a>

<a id="id-1.6.13.16.19.2"></a>

串接複寫功能可以讓待命伺服器接受複寫
連線，並將 WAL 紀錄串流傳送給其他待命伺服器，扮演中繼的角色。
這可以用來減少直接連線到主要伺服器的連線數，
也可以將跨站點的頻寬負擔降到最低。

同時作為接收端與傳送端的待命伺服器，稱為串接
待命伺服器（cascading standby）。較直接連線到主要伺服器的待命伺服器，稱為
上游伺服器，而距離較遠的那些待命伺服器則是下游
伺服器。串接複寫不會限制下游伺服器的數量
或排列方式，不過每台待命伺服器都只會連線到
一台上游伺服器，而這條鏈最終會連結到單一一台主要伺服器。

串接待命伺服器傳送的，不僅是從
主要伺服器接收到的 WAL 紀錄，還包括從歸檔還原的 WAL 紀錄。因此，即使某個上游連線中的複寫
連線被終止，只要還有新的 WAL 紀錄可用，
串流複寫就會繼續向下游進行。

串接複寫目前是非同步的。同步複寫
（請參閱[第 26.2.8 節](warm-standby.md#synchronous-replication)）的設定目前對
串接複寫沒有作用。

無論串接的排列方式為何，熱備援回饋（hot standby feedback）都會向上游傳遞。

如果上游待命伺服器被提升為新的主要伺服器，而
`recovery_target_timeline` 設為 `'latest'`（預設值），
下游伺服器就會繼續從新的主要伺服器串流。

若要使用串接複寫，請設置串接待命伺服器，使其可以
接受複寫連線（也就是設定
[max_wal_senders](../runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS) 與 [hot_standby](../runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY)，
並設定
[以主機為基礎的驗證](../client-authentication/auth-pg-hba-conf.md)）。
你也需要在下游待命伺服器中設定 `primary_conninfo`，
使其指向串接待命伺服器。

<a id="SYNCHRONOUS-REPLICATION"></a>

### 26.2.8. 同步複寫 [#](#synchronous-replication) <a href="#synchronous-replication" id="synchronous-replication"></a>

<a id="id-1.6.13.16.20.2"></a>

PostgreSQL 的串流複寫預設是非同步的。
如果主要伺服器
當機，某些已提交的交易可能尚未
複寫到待命伺服器，進而造成資料遺失。資料遺失
的量與失效切換當下的複寫延遲成正比。

同步複寫提供了確認某個交易所做的所有變更
都已傳輸到一台或多台同步待命伺服器的能力。
這擴充了交易提交所提供的標準持久性層級。
這種保護層級在電腦科學理論中稱為
2-safe 複寫；當 `synchronous_commit` 設為
`remote_write` 時，則稱為 group-1-safe
（group-safe 與 1-safe）。

要求同步複寫時，寫入交易的每次提交
都會等待，直到收到確認，
表示該提交已寫入主要伺服器與待命伺服器兩者
磁碟上的預寫日誌（write-ahead log）為止。資料遺失的唯一可能，
是主要伺服器與待命伺服器同時發生
當機。這可以提供高得多的持久性層級，但前提是
系統管理員對這兩台伺服器的放置位置與管理
都很謹慎。等待確認會增加使用者對於
伺服器當機時變更不會遺失的信心，但
也必然會增加提出請求之交易的回應時間。
最短的等待時間是主要伺服器與待命伺服器之間的往返時間。

唯讀交易與交易回滾不需要等待
待命伺服器的回覆。子交易的提交不會等待
待命伺服器的回應，只有最上層的提交才會等待。長時間
執行的動作（例如資料載入或建立索引）在
最終的提交訊息之前都不會等待。所有兩階段提交的動作
都需要等待提交，包括準備（prepare）與提交兩者。

同步待命伺服器可以是實體複寫待命伺服器，或是邏輯
複寫訂閱者。它也可以是任何其他知道如何傳送適當
回饋訊息的實體或邏輯 WAL
複寫串流消費者。除了內建的實體與邏輯複寫
系統之外，這也包括特殊程式，例如
`pg_receivewal` 與 `pg_recvlogical`，
以及某些第三方複寫系統與自訂程式。
關於同步複寫支援的詳細資訊，請查看各自的文件。

<a id="SYNCHRONOUS-REPLICATION-CONFIG"></a>

#### 26.2.8.1. 基本組態 [#](#SYNCHRONOUS-REPLICATION-CONFIG)

一旦設定好串流複寫，設定同步
複寫只需要再多一個組態步驟：
必須將 [synchronous_standby_names](../runtime-config/runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES) 設為
非空值。`synchronous_commit` 也必須設為
`on`，但由於這是預設值，通常不需要
變更。（請參閱[第 19.5.1 節](../runtime-config/runtime-config-wal.md#runtime-config-wal-settings)與
[第 19.6.2 節](../runtime-config/runtime-config-replication.md#runtime-config-replication-primary)。）
這個組態會讓每次提交都等待
待命伺服器確認已將提交紀錄寫入持久性
儲存裝置。
`synchronous_commit` 可以由個別
使用者設定，因此可以在設定檔中、針對特定
使用者或資料庫設定，或由應用程式動態設定，
以便逐筆交易控制持久性保證。

提交紀錄寫入主要伺服器的磁碟之後，
該 WAL 紀錄接著會被傳送到待命伺服器。每當一批新的 WAL 資料
寫入磁碟時，待命伺服器就會傳送回覆訊息，除非
待命伺服器上的 `wal_receiver_status_interval` 設為零。
在 `synchronous_commit` 設為
`remote_apply` 的情況下，待命伺服器會在提交紀錄
被重放、使交易變得可見時傳送回覆訊息。
如果根據主要伺服器上 `synchronous_standby_names` 的設定，
該待命伺服器被選為同步待命伺服器，則該待命伺服器的回覆
訊息會與其他同步待命伺服器的回覆訊息一起納入考量，
以決定何時釋放正在等待
提交紀錄已被接收之確認的交易。這些參數
讓管理員可以指定哪些待命伺服器應該作為
同步待命伺服器。請注意，同步
複寫的組態主要是在主要伺服器上進行。具名的待命伺服器必須直接
連線到主要伺服器；主要伺服器對於使用串接複寫的下游
待命伺服器一無所知。

將 `synchronous_commit` 設為 `remote_write`，會
讓每次提交都等待待命伺服器確認已收到
提交紀錄，並已將其寫出到它自己的作業系統，但不會
等待資料在待命伺服器上刷寫到磁碟。這個
設定提供的持久性保證比 `on`
弱：待命伺服器在作業系統
當機時可能會遺失資料，但 PostgreSQL 當機時則不會。
不過，這在實務上是很有用的設定，
因為它可以縮短交易的回應時間。
只有在主要伺服器與待命伺服器都當機，且
主要伺服器的資料庫同時損毀時，才可能發生資料遺失。

將 `synchronous_commit` 設為 `remote_apply`，會
讓每次提交都等待，直到目前的同步待命伺服器回報
它們已重放該交易、使其對使用者
查詢可見為止。在簡單的情況下，這可以實現具有因果
一致性（causal consistency）的負載平衡。

如果要求快速關閉（fast shutdown），使用者就會停止等待。不過，
與使用非同步複寫時一樣，伺服器在所有待處理的 WAL 紀錄
都傳輸到目前已連線的待命伺服器之前，
不會完全關閉。

<a id="SYNCHRONOUS-REPLICATION-MULTIPLE-STANDBYS"></a>

#### 26.2.8.2. 多台同步待命伺服器 [#](#SYNCHRONOUS-REPLICATION-MULTIPLE-STANDBYS)

同步複寫支援一台或多台同步待命伺服器；
交易會等待，直到所有被視為
同步的待命伺服器都確認收到其資料為止。交易必須等待其回覆的
同步待命伺服器數量，是在
`synchronous_standby_names` 中指定的。此參數也會指定
待命伺服器名稱清單，以及從所列伺服器中選擇同步待命伺服器的方法（`FIRST` 與
`ANY`）。

方法 `FIRST` 指定以優先順序為基礎的同步
複寫，並讓交易提交等待，直到其 WAL 紀錄
複寫到依優先順序選出的指定數量同步待命伺服器為止。
名稱在清單中出現得較前面的待命伺服器
會獲得較高的優先順序，並被視為同步待命伺服器。清單中
出現在較後面的其他待命伺服器，則代表潛在的同步
待命伺服器。如果目前的任何一台同步待命伺服器因
任何原因中斷連線，它會立即被
優先順序次高的待命伺服器取代。

以優先順序為基礎的多台同步待命伺服器，其
`synchronous_standby_names` 範例如下：

```

synchronous_standby_names = 'FIRST 2 (s1, s2, s3)'
```

在這個範例中，如果有四台待命伺服器 `s1`、`s2`、
`s3` 與 `s4` 正在執行，兩台待命伺服器
`s1` 與 `s2` 會被選為同步待命伺服器，
因為它們的名稱出現在待命伺服器名稱清單的前面。
`s3` 是潛在的同步待命伺服器，當 `s1` 或
`s2` 其中之一失效時，它會接手
同步待命伺服器的角色。`s4` 是非同步待命伺服器，因為
它的名稱不在清單中。

方法 `ANY` 指定以法定數量（quorum）為基礎的同步
複寫，並讓交易提交等待，直到其 WAL 紀錄
複寫到清單中*至少*指定數量的
同步待命伺服器為止。

以法定數量為基礎的多台同步待命伺服器，其
`synchronous_standby_names` 範例如下：

```

synchronous_standby_names = 'ANY 2 (s1, s2, s3)'
```

在這個範例中，如果有四台待命伺服器 `s1`、`s2`、
`s3` 與 `s4` 正在執行，交易提交將會
等待 `s1`、
`s2` 與 `s3` 之中至少任意兩台待命伺服器的回覆。`s4` 是非同步
待命伺服器，因為它的名稱不在清單中。

待命伺服器的同步狀態可以使用
`pg_stat_replication` 檢視表查看。

<a id="SYNCHRONOUS-REPLICATION-PERFORMANCE"></a>

#### 26.2.8.3. 效能規劃 [#](#SYNCHRONOUS-REPLICATION-PERFORMANCE)

同步複寫通常需要仔細規劃與放置
待命伺服器，以確保應用程式的效能可以接受。等待
並不會耗用系統資源，但交易鎖定會持續
被持有，直到傳輸獲得確認為止。因此，不謹慎地使用
同步複寫，會因為回應時間增加與競爭加劇，
而降低資料庫應用程式的效能。

PostgreSQL 允許應用程式開發者
指定透過複寫所需的持久性層級。這可以
針對整個系統指定，也可以針對
特定使用者或連線，甚至個別交易來指定。

例如，某個應用程式的工作負載可能由以下組成：
10% 的變更是重要的客戶詳細資料，而
90% 的變更是較不重要的資料，即使遺失，企業也比較
容易承受，例如使用者之間的聊天訊息。

透過在應用程式層級（在主要伺服器上）指定同步複寫選項，
我們就可以為最重要的變更提供同步複寫，
而不會拖慢整體工作負載的大部分。
應用程式層級的選項是一項重要且實用的工具，可以讓
高效能應用程式享有同步複寫的好處。

你應該考慮到，網路頻寬必須高於
WAL 資料的產生速率。

<a id="SYNCHRONOUS-REPLICATION-HA"></a>

#### 26.2.8.4. 高可用性規劃 [#](#SYNCHRONOUS-REPLICATION-HA)

`synchronous_standby_names` 指定在
`synchronous_commit` 設為 `on`、
`remote_apply` 或 `remote_write` 時所進行的交易提交，
要等待其回應之同步待命伺服器的數量與
名稱。如果任何一台同步待命伺服器當機，
這類交易提交可能永遠無法完成。

高可用性的最佳解決方案，是確保你保有與要求數量
一樣多的同步待命伺服器。這可以透過使用
`synchronous_standby_names` 指定多台
潛在的同步待命伺服器來達成。

在以優先順序為基礎的同步複寫中，名稱
在清單中出現得較前面的待命伺服器會被用作同步待命伺服器。
列在它們之後的待命伺服器，會在目前的某一台同步待命伺服器
失效時，接手同步待命伺服器的角色。

在以法定數量為基礎的同步複寫中，清單中出現的
所有待命伺服器都會被用作同步待命伺服器的候選者。
即使其中一台失效，其他待命伺服器仍會繼續擔任
同步待命伺服器候選者的角色。

當待命伺服器第一次連接到主要伺服器時，它還不會被正確地
同步。這稱為 `catchup` 模式。一旦
待命伺服器與主要伺服器之間的延遲第一次降到零，
我們就會進入即時的 `streaming` 狀態。
在待命伺服器剛建立之後，追趕期間可能會很長。
如果待命伺服器被關閉，追趕期間
會隨著待命伺服器停機的時間長度而增加。
待命伺服器只有在
到達 `streaming` 狀態之後，才能成為同步待命伺服器。
這個狀態可以使用
`pg_stat_replication` 檢視表查看。

如果主要伺服器在提交正在等待確認時重新啟動，那些
正在等待的交易會在主要
資料庫復原之後被標記為完全提交。
沒有任何方法可以確定在主要伺服器當機時，所有待命伺服器都已收到所有
待處理的 WAL 資料。某些
交易可能在待命伺服器上不會顯示為已提交，即使
它們在主要伺服器上顯示為已提交。我們提供的保證是：
在確知 WAL 資料已被所有同步待命伺服器
安全接收之前，應用程式不會收到
交易成功提交的明確確認。

如果你確實無法保有與要求數量一樣多的同步待命伺服器，
那麼你應該在 `synchronous_standby_names` 中
減少交易提交必須等待其回應的同步待命伺服器數量
（或停用它），並
在主要伺服器上重新載入設定檔。

如果主要伺服器與其餘的待命伺服器隔離，你應該
失效切換到那些其餘待命伺服器之中最佳的候選者。

如果你需要在交易正在等待時重新建立待命伺服器，
請確認函式 `pg_backup_start()`
與 `pg_backup_stop()` 是在
`synchronous_commit` = `off` 的工作階段中執行，否則那些
請求將會永遠等待待命伺服器出現。

<a id="CONTINUOUS-ARCHIVING-IN-STANDBY"></a>

### 26.2.9. 待命伺服器上的持續歸檔 [#](#continuous-archiving-in-standby) <a href="#continuous-archiving-in-standby" id="continuous-archiving-in-standby"></a>

<a id="id-1.6.13.16.21.2"></a>

在待命伺服器上使用持續 WAL 歸檔時，有兩種
不同的情境：WAL 歸檔可以由主要伺服器
與待命伺服器共用，或者待命伺服器可以擁有自己的 WAL 歸檔。當
待命伺服器擁有自己的 WAL 歸檔時，請將 `archive_mode`
設為 `always`，待命伺服器就會針對它收到的每一個 WAL 區段
呼叫歸檔命令，無論該區段是透過從歸檔還原
或是透過串流複寫取得。共用歸檔也可以
用類似的方式處理，但 `archive_command` 或 `archive_library` 必須
檢查要歸檔的檔案是否已經存在，以及現有檔案
的內容是否完全相同。這需要在
`archive_command` 或 `archive_library` 中更加小心，因為它必須
注意不要以不同的內容覆寫現有檔案，
但在完全相同的檔案被歸檔兩次時要回傳成功。而且
如果兩台伺服器試圖同時歸檔同一個檔案，
這一切都必須在沒有競爭條件（race condition）的情況下完成。

如果 `archive_mode` 設為 `on`，
歸檔程序在復原或待命模式期間不會啟用。如果待命
伺服器被提升，它會在提升之後開始歸檔，但
不會歸檔任何不是由它自己產生的 WAL 或時間軸歷史
檔案。若要在歸檔中取得完整的
WAL 檔案序列，你必須確保所有 WAL 在
到達待命伺服器之前都已歸檔。對於以檔案為基礎的日誌傳送而言，
這本來就成立，因為待命伺服器只能還原
在歸檔中找到的檔案；但如果啟用了串流複寫，就不是如此。
當伺服器不在復原模式時，
`on` 與 `always` 模式之間沒有任何差異。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/warm-standby.html)（原文版本：18.6；核對日期：2026-10-10）
