<a id="LOGICALDECODING-EXPLANATION"></a>
## 47.2. 邏輯解碼概念 [#](#LOGICALDECODING-EXPLANATION)

[47.2.1. 邏輯解碼](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-LOG-DEC)

[47.2.2. 複寫插槽](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS)

[47.2.3. 複寫插槽同步](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)

[47.2.4. 輸出外掛程式](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS)

[47.2.5. 匯出的快照](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS)

<a id="LOGICALDECODING-EXPLANATION-LOG-DEC"></a>

### 47.2.1. 邏輯解碼 [#](#LOGICALDECODING-EXPLANATION-LOG-DEC)

<a id="id-1.8.14.8.2.2"></a>

邏輯解碼是一種將資料庫資料表中所有持久性變更，擷取為一種連貫、易於理解的格式的過程，使其在無需深入了解資料庫內部狀態的情況下即可解讀。

在 PostgreSQL 中，邏輯解碼是透過將
[先寫式日誌（write-ahead log）](../../server-administration/wal/README.md)（描述儲存層級上的變更）的內容，解碼為特定應用程式所需的形式（例如資料列串流或 SQL 陳述式）來實作的。

<a id="LOGICALDECODING-REPLICATION-SLOTS"></a>

### 47.2.2. 複寫插槽 [#](#LOGICALDECODING-REPLICATION-SLOTS)

<a id="id-1.8.14.8.3.2"></a>

在邏輯複寫的語境中，插槽代表一串變更串流，可依照這些變更在來源伺服器上發生的順序，重播給用戶端。每個插槽都會從單一資料庫串流出一連串的變更。

### 注意

PostgreSQL 也有串流複寫插槽
（見[26.2.5 節](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION)），但其用法略有不同。

複寫插槽有一個識別碼，在一個 PostgreSQL 叢集中的
所有資料庫間皆為唯一。插槽的存續與使用它的連線無關，且具備當機安全性。

在正常運作下，邏輯插槽只會將每項變更傳送一次。每個插槽目前的位置只會在檢查點時被持久化，因此若發生當機，該插槽可能會回退到較早的 LSN，導致伺服器重新啟動時，近期的變更會被再次傳送。邏輯解碼用戶端有責任避免因重複處理同一則訊息而產生不良後果。用戶端或許會想記錄解碼時所看到的最後一個 LSN，並略過任何重複的資料，或者（在使用複寫協定時）要求解碼從該 LSN 開始，而不是讓伺服器自行決定起始點。複寫進度追蹤功能正是為此目的而設計，請參閱[複寫來源](../replication-origins/README.md)。

單一資料庫可以存在多個彼此獨立的插槽。每個插槽都有自己的狀態，讓不同的消費者可以從資料庫變更串流中的不同位置接收變更。對於大多數應用程式而言，每個消費者都需要一個各自獨立的插槽。

邏輯複寫插槽對於接收端的狀態一無所知。甚至可以讓多個不同的接收端，在不同時間使用同一個插槽；它們只會收到自上一個接收端停止消費之後所發生的變更。在任何時間點，都只能有一個接收端從某個插槽消費變更。

邏輯複寫插槽也可以建立在熱備援伺服器（hot standby）上。為避免
`VACUUM` 從系統目錄中移除所需的資料列，應在
備援伺服器上設定 `hot_standby_feedback`。儘管如此，若任何所需的資料列仍遭移除，該插槽就會失效。強烈建議在主要伺服器與備援伺服器之間使用實體插槽。否則，`hot_standby_feedback`
雖然仍會運作，但僅在連線存續期間有效（舉例來說，節點重新啟動便會使其失效）。如此一來，主要伺服器可能會刪除備援伺服器上的邏輯解碼所需的系統目錄資料列（因為它不知道備援伺服器上的
`catalog_xmin`）。
若主要伺服器上的 `wal_level` 被降低至低於
`logical`，備援伺服器上既有的邏輯插槽也會失效。
一旦備援伺服器在 WAL 串流中偵測到此類變更，便會立即執行此動作。
這意味著，對於（若有）落後的 walsender 而言，某些直到主要伺服器上
`wal_level` 參數變更為止的 WAL 記錄將不會被解碼。

建立邏輯插槽需要目前所有執行中交易的相關資訊。在主要伺服器上，
可直接取得此資訊，但在備援伺服器上，此資訊則必須向
主要伺服器取得。因此，建立插槽可能需要等待主要伺服器上發生某些活動。若主要伺服器處於閒置狀態，在
備援伺服器上建立邏輯插槽可能會耗費相當長的時間。可以透過在主要伺服器上呼叫
`pg_log_standby_snapshot` 函式來加快此過程。

### 小心

複寫插槽的存續會跨越當機，且對其消費者的狀態一無所知。即使沒有任何連線在使用它們，它們仍會阻止所需資源被移除。這會消耗儲存空間，因為只要仍被某個複寫
插槽所需要，`VACUUM` 就無法移除所需的 WAL 或系統目錄中所需的資料列。在極端情況下，這可能導致資料庫為防止交易 ID 回捲而關閉（見[24.1.5 節](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)）。
因此，若某個插槽已不再需要，就應將其刪除。

<a id="LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION"></a>

### 47.2.3. 複寫插槽同步 [#](#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)

可以在建立插槽時，透過
[`pg_create_logical_replication_slot`](../../the-sql-language/functions/functions-admin.md#PG-CREATE-LOGICAL-REPLICATION-SLOT) 的
`failover` 參數，或透過
`CREATE SUBSCRIPTION` 的
[`failover`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER) 選項，
將主要伺服器上的邏輯複寫插槽同步至熱備援伺服器。
此外，還必須在備援伺服器上啟用
[`sync_replication_slots`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS)。在備援伺服器上啟用
[`sync_replication_slots`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS)
後，容錯移轉插槽便可由插槽同步工作程序定期同步。若要使同步機制運作，
主要伺服器與備援伺服器之間必須具備一個實體複寫插槽（也就是說，
應在備援伺服器上設定
[`primary_slot_name`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME)），並且
必須在備援伺服器上啟用
[`hot_standby_feedback`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK)。
此外還必須在
[`primary_conninfo`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-PRIMARY-CONNINFO)
中指定有效的 `dbname`。
強烈建議在主要伺服器的
[`synchronized_standby_slots`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS)
清單中，列出該實體複寫插槽的名稱，以避免訂閱端消費變更的速度快過熱備援伺服器。即使組態設定正確無誤，由於必須等待
[`synchronized_standby_slots`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS)
中列出的插槽，向邏輯訂閱端傳送變更時仍會有一定的延遲。
當使用了 `synchronized_standby_slots` 時，
主要伺服器在完全關閉之前，會先等待
`synchronized_standby_slots` 中所指定實體複寫插槽所對應的
備援伺服器，確認已接收到直到主要伺服器上最新
排清（flush）位置為止的 WAL。

### 注意

雖然啟用
[`sync_replication_slots`](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS) 可讓
容錯移轉插槽自動定期同步，但也可以在備援伺服器上使用
[`pg_sync_replication_slots`](../../the-sql-language/functions/functions-admin.md#PG-SYNC-REPLICATION-SLOTS) 函式手動同步。
不過，此函式主要是為了測試與除錯而設計，應謹慎使用。與自動同步不同的是，它
不具備週期性重試機制，因此更容易發生同步失敗，尤其是在初始同步情境下，此時插槽所需的 WAL 檔案
或目錄資料列，可能已在備援伺服器上被移除，或有被移除的風險。相對地，透過
`sync_replication_slots` 進行的自動同步，可提供
持續性的插槽更新，實現無縫的容錯移轉，並支援高可用性。
因此，這是建議採用的插槽同步方式。

當插槽同步依建議方式設定完成，
且已（無論是自動或透過 `pg_sync_replication_slots` 手動）完成初始同步後，
只有在滿足以下條件時，備援伺服器才能持久化該已同步的插槽：
主要伺服器上的邏輯複寫插槽，必須保留備援伺服器上仍然可用的 WAL
與系統目錄資料列。這可確保資料完整性，並讓邏輯複寫在
提升為主要伺服器之後，仍能順利延續。
若所需的 WAL 或目錄資料列已從
備援伺服器上清除，為避免資料遺失，該插槽將不會被持久化。在此類
情況下，可能會出現以下日誌訊息：

```

LOG:  could not synchronize replication slot "failover_slot"
DETAIL:  Synchronization could lead to data loss, because the remote slot needs WAL at LSN 0/3003F28 and catalog xmin 754, but the standby has LSN 0/3003F28 and catalog xmin 756.
```

若該邏輯複寫插槽正被消費者主動使用，則不需要任何
人工介入；該插槽會自動前進，
同步作業也會在下一個週期恢復。不過，若未設定任何
消費者，則建議在主要伺服器上手動使用
[`pg_logical_slot_get_changes`](../../the-sql-language/functions/functions-admin.md#PG-LOGICAL-SLOT-GET-CHANGES) 或
[`pg_logical_slot_get_binary_changes`](../../the-sql-language/functions/functions-admin.md#PG-LOGICAL-SLOT-GET-BINARY-CHANGES) 使插槽前進，
讓同步作業得以繼續進行。

容錯移轉之後能否恢復邏輯複寫，取決於容錯移轉發生當時，
[pg_replication_slots](../../internals/views/view-pg-replication-slots.md) 中備援伺服器上已同步插槽的
`synced`
值。只有在容錯移轉之前，於備援伺服器上已達到 synced 狀態為 true 的持久性插槽，
才能在容錯移轉後用於邏輯複寫。
暫時性的已同步插槽無法用於邏輯解碼，因此
這些插槽的邏輯複寫也就無法恢復。舉例來說，若某個已同步插槽因訂閱被停用，
而無法在備援伺服器上變為持久性插槽，那麼即使該訂閱後來被重新啟用，
在容錯移轉後也無法恢復。

若要從已同步的邏輯插槽，在容錯移轉後恢復邏輯複寫，必須將該訂閱的
'conninfo' 變更為指向新的主要伺服器。這可透過
[`ALTER SUBSCRIPTION ... CONNECTION`](../../reference/sql-commands/sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-CONNECTION) 完成。
建議在將備援伺服器提升為主要伺服器之前，先停用相關訂閱，
並在變更連線字串之後再重新啟用。

### 小心

在提升過程中，舊的主要伺服器有可能重新上線，若訂閱未被停用，
邏輯訂閱端可能會在提升完成後，仍持續從舊的主要伺服器接收資料，
直到連線字串被變更為止。這可能導致資料不一致的問題，
使邏輯訂閱端無法從新的主要伺服器繼續複寫。

<a id="LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS"></a>

### 47.2.4. 輸出外掛程式 [#](#LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS)

輸出外掛程式會將資料，從先寫式日誌的內部表示法，轉換為複寫插槽消費者所需要的格式。

<a id="LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS"></a>

### 47.2.5. 匯出的快照 [#](#LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS)

當使用串流複寫介面建立新的複寫插槽時
（見[CREATE_REPLICATION_SLOT](../../internals/protocol/protocol-replication.md#PROTOCOL-REPLICATION-CREATE-REPLICATION-SLOT)），
系統會匯出一份快照
（見[9.28.5 節](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)），該快照會精確顯示
資料庫在此之後、所有變更都將被納入變更串流時的狀態。此快照可用來
建立新的複本，方式是使用
[`SET TRANSACTION
SNAPSHOT`](../../reference/sql-commands/sql-set-transaction.md) 來讀取該插槽建立當下的資料庫狀態。接著可以使用此交易來傾印
資料庫在該時間點的狀態，之後便可利用該插槽的內容進行更新，而不會遺失任何變更。

不需要匯出快照的應用程式，可以使用
`SNAPSHOT 'nothing'` 選項來抑制此行為。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-explanation.html)（原文版本：18.6；核對日期：2026-09-22）
