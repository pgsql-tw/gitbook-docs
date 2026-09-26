<a id="HOT-STANDBY"></a>

## 26.4. 熱備援 [#](#HOT-STANDBY)

[26.4.1. 使用者總覽](hot-standby.md#HOT-STANDBY-USERS)

[26.4.2. 處理查詢衝突](hot-standby.md#HOT-STANDBY-CONFLICT)

[26.4.3. 管理員總覽](hot-standby.md#HOT-STANDBY-ADMIN)

[26.4.4. 熱備援參數參考](hot-standby.md#HOT-STANDBY-PARAMETERS)

[26.4.5. 注意事項](hot-standby.md#HOT-STANDBY-CAVEATS)

<a id="id-1.6.13.18.2"></a>

「熱備援」（Hot Standby）一詞，用來描述伺服器在進行封存復原
（archive recovery）或處於待命模式時，仍能連線並執行唯讀查詢的能力。
這項能力不論是對複寫用途，或是要以高度精確度將備份還原到指定狀態，
都相當有用。熱備援一詞，也指伺服器能夠在使用者持續執行查詢及／或
保持連線開啟的同時，從復原狀態過渡到正常運作狀態的能力。

在熱備援模式下執行查詢，與一般查詢操作十分類似，
不過仍存在若干使用面與管理面上的差異，詳述如下。

<a id="HOT-STANDBY-USERS"></a>

### 26.4.1. 使用者總覽 [#](#HOT-STANDBY-USERS)

當待命伺服器上的
[hot_standby](../runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY)
參數設為 true 時，一旦復原程序已將系統帶入一致狀態、
且已準備好進行熱備援，它就會開始接受連線。
所有這類連線都是嚴格唯讀的；即使是暫存資料表也無法寫入。

由於待命伺服器上的資料需要一些時間才能從主要伺服器送達，
主要伺服器與待命伺服器之間會存在可測得的延遲。因此，
幾乎同時在主要伺服器與待命伺服器上執行相同的查詢，
可能會得到不同的結果。我們稱待命伺服器上的資料與主要伺服器
之間是*最終一致*（eventually consistent）的。一旦某筆交易的
提交記錄在待命伺服器上被重播（replay），該筆交易所做的變更，
就會對待命伺服器上之後建立的任何 snapshot 可見。
Snapshot 的建立時機可能是在每個查詢開始時，或是在每個交易開始時，
視目前的交易隔離等級而定。詳情請參閱
[第 13.2 節](../../the-sql-language/mvcc/transaction-iso.md)。

在熱備援期間所啟動的交易，可以發出以下指令：

* 查詢存取：`SELECT`、`COPY TO`
* 游標指令：`DECLARE`、`FETCH`、`CLOSE`
* 設定：`SHOW`、`SET`、`RESET`
* 交易管理指令：

  * `BEGIN`、`END`、`ABORT`、`START TRANSACTION`
  * `SAVEPOINT`、`RELEASE`、`ROLLBACK TO SAVEPOINT`
  * `EXCEPTION` 區塊及其他內部子交易
* `LOCK TABLE`，但僅限於明確指定以下其中一種模式時：
  `ACCESS SHARE`、`ROW SHARE` 或 `ROW EXCLUSIVE`。
* 執行計畫與資源：`PREPARE`、`EXECUTE`、
  `DEALLOCATE`、`DISCARD`
* 外掛程式與擴充套件：`LOAD`
* `UNLISTEN`

在熱備援期間所啟動的交易，永遠不會被指派交易 ID，
也無法寫入系統的 write-ahead log。
因此，以下操作會產生錯誤訊息：

* 資料操作語言（DML）：`INSERT`、
  `UPDATE`、`DELETE`、
  `MERGE`、`COPY FROM`、
  `TRUNCATE`。
  請注意，在復原期間並不允許任何會導致觸發程序執行的操作。
  這項限制即使對暫存資料表也同樣適用，因為在不指派交易 ID
  的情況下無法讀取或寫入資料表的資料列，而目前在熱備援環境中
  無法指派交易 ID。
* 資料定義語言（DDL）：`CREATE`、
  `DROP`、`ALTER`、`COMMENT`。
  這項限制即使對暫存資料表也同樣適用，因為執行這些操作
  將需要更新系統目錄資料表。
* `SELECT ... FOR SHARE | UPDATE`，因為在不更新底層資料檔案的
  情況下，無法取得資料列鎖。
* 會產生 DML 指令的 `SELECT` 陳述式規則（rule）。
* 明確要求高於 `ROW EXCLUSIVE MODE` 模式的 `LOCK`。
* 未指定模式、以簡短預設形式使用的 `LOCK`，因為它會要求
  `ACCESS EXCLUSIVE MODE`。
* 明確設定為非唯讀狀態的交易管理指令：

  * `BEGIN READ WRITE`、
    `START TRANSACTION READ WRITE`
  * `SET TRANSACTION READ WRITE`、
    `SET SESSION CHARACTERISTICS AS TRANSACTION READ WRITE`
  * `SET transaction_read_only = off`
* 兩階段提交指令：`PREPARE TRANSACTION`、
  `COMMIT PREPARED`、`ROLLBACK PREPARED`，
  因為即使是唯讀交易，也需要在準備階段（兩階段提交的第一階段）
  寫入 WAL。
* 序列更新：`nextval()`、`setval()`
* `LISTEN`、`NOTIFY`

在正常運作下，「唯讀」交易是可以使用
`LISTEN` 及 `NOTIFY` 的，因此熱備援工作階段
所受到的限制，比一般唯讀工作階段稍微嚴格一些。未來版本中，
這些限制中的部分，有可能會放寬。

在熱備援期間，`transaction_read_only` 參數永遠為 true，
且無法變更。但只要沒有嘗試修改資料庫，熱備援期間的連線，
運作方式就會與其他一般資料庫連線非常相似。如果發生失效切換
或計畫性切換，資料庫就會切換為正常處理模式。在伺服器切換
模式期間，工作階段會保持連線。一旦熱備援結束，就可以開始
讀寫交易（即使該工作階段是在熱備援期間開始的也一樣）。

使用者可以透過發出 `SHOW in_hot_standby`，
來判斷自己的工作階段目前是否正處於熱備援狀態。
（在 14 版之前的伺服器中，並不存在 `in_hot_standby`
參數；針對較舊的伺服器，可行的替代方法是
`SHOW transaction_read_only`。）此外，還有一組函式
（[表 9.98](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-RECOVERY-INFO-TABLE)）
可讓使用者取得待命伺服器的相關資訊。這些函式可讓你撰寫
能夠得知資料庫目前狀態的程式。它們可以用來監控復原的進度，
或用來讓你撰寫複雜的程式，將資料庫還原到特定狀態。

<a id="HOT-STANDBY-CONFLICT"></a>

### 26.4.2. 處理查詢衝突 [#](#HOT-STANDBY-CONFLICT)

主要伺服器與待命伺服器在許多方面都屬於鬆散連接的關係。
主要伺服器上的操作，會對待命伺服器產生影響。因此，
兩者之間有可能出現負面互動或衝突。最容易理解的衝突是效能問題：
如果主要伺服器上正在進行大量資料載入，就會在待命伺服器上
產生類似的 WAL 記錄串流，導致待命伺服器上的查詢，
可能會與之爭奪系統資源，例如 I/O。

熱備援還可能發生其他類型的衝突。這些衝突屬於*硬衝突*
（hard conflicts），意思是查詢可能需要被取消，在某些情況下，
甚至需要中斷工作階段的連線，才能解決衝突。系統提供了
使用者幾種方式來處理這些衝突。衝突情況包括：

* 主要伺服器上取得的 Access Exclusive 鎖——包含明確的
  `LOCK` 指令，以及各種 DDL 操作——
  與待命查詢中的資料表存取發生衝突。
* 在主要伺服器上卸除（drop）一個資料表空間，
  與待命查詢中，將該資料表空間用於暫存工作檔案的情況發生衝突。
* 在主要伺服器上卸除一個資料庫，與待命伺服器上連線至
  該資料庫的工作階段發生衝突。
* 套用來自 WAL 的 vacuum 清理記錄，與其 snapshot
  仍能「看見」待移除資料列的待命交易發生衝突。
* 套用來自 WAL 的 vacuum 清理記錄，與正在待命伺服器上
  存取目標頁面的查詢發生衝突，不論待移除的資料是否可見。

在主要伺服器上，這些情況只會導致等待；使用者可以選擇
取消其中任一方的衝突操作。然而，在待命伺服器上則沒有選擇餘地：
該 WAL 記錄的操作已經在主要伺服器上發生，因此待命伺服器
不能不套用它。此外，讓 WAL 套用無限期等待，往往也相當不理想，
因為待命伺服器的狀態會與主要伺服器的差距越拉越大。因此，
系統提供了一種機制，可以強制取消與即將套用的 WAL 記錄
發生衝突的待命查詢。

這類問題情境的一個範例，是主要伺服器上的管理員，
對一個目前正在待命伺服器上被查詢的資料表執行
`DROP TABLE`。顯然，如果 `DROP TABLE`
在待命伺服器上被套用，待命查詢就無法繼續執行。
如果這種情況發生在主要伺服器上，`DROP TABLE` 會
等待，直到另一個查詢完成為止。但當 `DROP TABLE`
是在主要伺服器上執行時，主要伺服器並不知道待命伺服器上
正在執行哪些查詢，因此它不會為任何這類待命查詢而等待。
WAL 變更記錄會在待命查詢仍在執行的期間傳送到待命伺服器，
因而造成衝突。待命伺服器必須延遲套用這些 WAL 記錄
（以及之後所有的記錄），否則就得取消發生衝突的查詢，
以便讓 `DROP TABLE` 得以套用。

當發生衝突的查詢執行時間很短時，通常會希望透過稍微延遲
WAL 套用，讓它得以完成；但長時間延遲 WAL 套用，
通常並不理想。因此，取消機制設有
[max_standby_archive_delay](../runtime-config/runtime-config-replication.md#GUC-MAX-STANDBY-ARCHIVE-DELAY)
及
[max_standby_streaming_delay](../runtime-config/runtime-config-replication.md#GUC-MAX-STANDBY-STREAMING-DELAY)
兩個參數，用來定義 WAL 套用所允許的最大延遲。一旦套用任何
新收到的 WAL 資料，所花費的時間超過相對應的延遲設定，
發生衝突的查詢就會被取消。之所以有兩個參數，
是為了讓你可以針對從封存中讀取 WAL 資料的情況
（也就是從基礎備份進行初次復原，或是讓落後甚多的
待命伺服器「追上進度」），以及透過串流複寫讀取 WAL 資料的情況，
分別指定不同的延遲值。

若待命伺服器主要是為了高可用性而存在，最好將延遲參數設得
相對短一些，這樣伺服器才不會因為待命查詢所造成的延遲，
而大幅落後主要伺服器。然而，如果待命伺服器的用途是
執行長時間執行的查詢，那麼較高、甚至是無限的延遲值，
可能會比較合適。不過請留意，如果延遲套用 WAL 記錄，
長時間執行的查詢可能會導致待命伺服器上的其他工作階段，
無法看到主要伺服器上最近的變更。

一旦超過 `max_standby_archive_delay` 或
`max_standby_streaming_delay` 所指定的延遲，
發生衝突的查詢就會被取消。這通常只會導致一個取消錯誤，
不過在重播 `DROP DATABASE` 的情況下，整個
發生衝突的工作階段都會被終止。此外，如果衝突牽涉到
由閒置交易所持有的鎖，發生衝突的工作階段也會被終止
（這項行為未來可能會有所變動）。

被取消的查詢可以立即重試（當然，需要先開始一個新交易）。
由於查詢取消與否，取決於正在重播之 WAL 記錄的性質，
被取消的查詢如果再次執行，很可能會成功。

請記住，延遲參數所比較的，是自待命伺服器收到 WAL 資料
以來所經過的時間。因此，待命伺服器上任何一個查詢
所獲得的寬限期，絕不會超過延遲參數所設定的值，
如果待命伺服器已經因為等待先前的查詢完成、
或是因為無法跟上沉重的更新負載而落後，
寬限期甚至可能會明顯更短。

待命查詢與 WAL 重播之間最常見的衝突原因，是「過早清理」
（early cleanup）。在正常情況下，當沒有任何交易需要看到
舊版本資料列，以確保依照 MVCC 規則呈現正確的可見性時，
PostgreSQL 會允許清理這些舊版本資料列。然而，
這項規則只能套用於在主要伺服器上執行的交易。因此，
主要伺服器上的清理作業，有可能會移除仍然對待命伺服器上
某個交易可見的資料列版本。

資料列版本清理並非造成待命查詢衝突的唯一可能原因。
所有僅索引掃描（index-only scan，包括在待命伺服器上執行的那些），
都必須使用與可見性對照表（visibility map）「一致」的 MVCC
snapshot。因此，只要 `VACUUM`
[將某個頁面在可見性對照表中標記為全可見](../maintenance/routine-vacuuming.md#VACUUM-FOR-VISIBILITY-MAP)，
而該頁面包含一個或多個*不*對所有待命查詢可見的資料列，
就必然會產生衝突。因此，即使是對一個沒有任何已更新或已刪除、
需要清理之資料列的資料表執行 `VACUUM`，
也有可能導致衝突。

使用者應該清楚了解：在主要伺服器上被定期且大量更新的資料表，
會很快導致待命伺服器上執行時間較長的查詢被取消。在這種情況下，
為 `max_standby_archive_delay` 或
`max_standby_streaming_delay`
設定一個有限值，可以視為類似設定 `statement_timeout`。

如果發現待命查詢被取消的次數無法接受，還是有補救方式可用。
第一個選項，是設定 `hot_standby_feedback` 參數，
這可以避免 `VACUUM` 移除近期才變成死亡（dead）的
資料列，因此清理衝突就不會發生。如果你這麼做，
應該注意，這會延遲主要伺服器上死亡資料列的清理，
可能導致不理想的資料表膨脹。不過，這種清理狀況，
不會比讓待命查詢直接在主要伺服器上執行時更糟，
而你仍然能享有將執行負載分擔到待命伺服器上的好處。
如果待命伺服器頻繁連線與斷線，你可能會想要做一些調整，
以因應 `hot_standby_feedback` 回饋未被提供的期間。
舉例來說，可以考慮提高 `max_standby_archive_delay`，
這樣在斷線期間，查詢就不會因為 WAL 封存檔中的衝突
而被迅速取消。你也應該考慮提高
`max_standby_streaming_delay`，
以避免在重新連線後，因新到達的串流 WAL 項目
而導致查詢被迅速取消。

查詢取消的次數及其原因，可以透過待命伺服器上的
`pg_stat_database_conflicts` 系統檢視表查看。
`pg_stat_database` 系統檢視表
也包含摘要資訊。

使用者可以控制當 WAL 重播因衝突而等待超過
`deadlock_timeout` 時，是否要產生一則日誌訊息。
這是由
[log_recovery_conflict_waits](../runtime-config/runtime-config-logging.md#GUC-LOG-RECOVERY-CONFLICT-WAITS)
參數控制的。

<a id="HOT-STANDBY-ADMIN"></a>

### 26.4.3. 管理員總覽 [#](#HOT-STANDBY-ADMIN)

如果 `postgresql.conf` 中的 `hot_standby`
為 `on`（此為預設值），且存在一個
[`standby.signal`](warm-standby.md#FILE-STANDBY-SIGNAL)<a id="id-1.6.13.18.7.2.5"></a>
檔案，伺服器就會以熱備援模式運作。不過，熱備援連線
可能需要一段時間才會被允許，因為伺服器在完成足夠的復原、
達到可供查詢執行的一致狀態之前，並不會接受連線。
在此期間，嘗試連線的用戶端會收到錯誤訊息而被拒絕。
若要確認伺服器是否已啟動完成，可以讓應用程式反覆嘗試連線，
或是在伺服器日誌中尋找以下訊息：

```

LOG:  entering standby mode

... then some time later ...

LOG:  consistent recovery state reached
LOG:  database system is ready to accept read-only connections
```

一致性資訊會在主要伺服器上，每次執行檢查點時記錄一次。
如果所讀取的 WAL，是在主要伺服器上 `wal_level`
未設為 `replica` 或 `logical` 的期間所寫入的，
就無法啟用熱備援。即使已經達到一致狀態，如果同時符合
以下兩個條件，復原 snapshot 仍可能尚未準備好進行熱備援，
因而延遲接受唯讀連線。若要啟用熱備援，主要伺服器上，
擁有超過 64 個子交易的長時間執行寫入交易必須先結束。

* 某個寫入交易擁有超過 64 個子交易
* 存在執行時間非常長的寫入交易

如果你執行的是以檔案為基礎的日誌傳送（「warm standby」），
你可能需要等到下一個 WAL 檔案送達為止，
這個等待時間，可能長達主要伺服器上 `archive_timeout`
的設定值。

部分參數的設定，決定了用於追蹤交易 ID、鎖，
以及已準備交易（prepared transaction）的共享記憶體大小。
為確保待命伺服器在復原期間不會耗盡共享記憶體，
這些共享記憶體結構在待命伺服器上，不得小於主要伺服器上的設定。
舉例來說，如果主要伺服器曾使用過已準備交易，
但待命伺服器並未配置任何用於追蹤已準備交易的共享記憶體，
那麼在待命伺服器的組態設定變更之前，復原就無法繼續進行。
受影響的參數如下：

* `max_connections`
* `max_prepared_transactions`
* `max_locks_per_transaction`
* `max_wal_senders`
* `max_worker_processes`

確保這不會成為問題的最簡單方式，就是將待命伺服器上
這些參數的設定值，設為等於或大於主要伺服器上的設定值。
因此，如果你想要調高這些數值，應該先在所有待命伺服器上調整，
再套用到主要伺服器。反之，如果你想要調低這些數值，
應該先在主要伺服器上調整，再套用到所有待命伺服器。
請記住，當某個待命伺服器被提升之後，它就會成為後續
待命伺服器所需參數設定的新基準。因此，為避免在計畫性切換
或失效切換期間發生這類問題，建議讓所有待命伺服器上的
這些設定保持一致。

WAL 會追蹤主要伺服器上這些參數的變更。如果熱備援
伺服器在處理 WAL 時，發現主要伺服器上目前的值高於
自己的值，就會記錄一則警告訊息，並暫停復原，例如：

```

WARNING:  hot standby is not possible because of insufficient parameter settings
DETAIL:  max_connections = 80 is a lower setting than on the primary server, where its value was 100.
LOG:  recovery has paused
DETAIL:  If recovery is unpaused, the server will shut down.
HINT:  You can then restart the server after making the necessary configuration changes.
```

此時，必須先更新待命伺服器上的設定，並重新啟動該實例，
復原才能繼續進行。如果該待命伺服器並非熱備援伺服器，
那麼在遇到不相容的參數變更時，它會立即關閉而不會暫停，
因為此時繼續維持運作已沒有意義。

管理員為
[max_standby_archive_delay](../runtime-config/runtime-config-replication.md#GUC-MAX-STANDBY-ARCHIVE-DELAY)
及
[max_standby_streaming_delay](../runtime-config/runtime-config-replication.md#GUC-MAX-STANDBY-STREAMING-DELAY)
選擇適當的設定值十分重要。最佳選擇會因業務優先順序而異。
舉例來說，如果伺服器的主要任務是作為高可用性伺服器，
你會希望設定較低的延遲值，甚至可能設為零，不過這是相當
激進的設定。如果待命伺服器的任務，是作為決策支援查詢的
額外伺服器，那麼將最大延遲值設為許多小時、甚至是 -1
（表示永遠等待查詢完成），可能也是可以接受的。

主要伺服器上寫入的交易狀態「hint bits」並不會被記錄到 WAL 中，
因此待命伺服器上的資料，很可能會在待命伺服器上重新寫入
這些提示位元。因此，即使所有使用者都只有唯讀權限，
待命伺服器仍然會執行磁碟寫入；不過資料值本身並不會有任何變動。
使用者仍然會寫入大型排序暫存檔，並重新產生 relcache 資訊檔，
因此在熱備援模式下，資料庫並沒有任何部分是真正唯讀的。
另請注意，即使交易在本機是唯讀的，使用 dblink 模組
對遠端資料庫進行的寫入，以及使用 PL 函式在資料庫外部
進行的其他操作，仍然是可行的。

在復原模式期間，不接受以下類型的管理指令：

* 資料定義語言（DDL）：例如 `CREATE INDEX`
* 權限與擁有權：`GRANT`、`REVOKE`、
  `REASSIGN`
* 維護指令：`ANALYZE`、`VACUUM`、
  `CLUSTER`、`REINDEX`

同樣要注意的是，這些指令中有一些，實際上在主要伺服器的
「唯讀」模式交易期間是被允許的。

因此，你無法建立僅存在於待命伺服器上的額外索引，
也無法建立僅存在於待命伺服器上的統計資訊。如果需要這些
管理指令，應該在主要伺服器上執行，這些變更最終會傳播到
待命伺服器。

`pg_cancel_backend()`
與 `pg_terminate_backend()` 可以對使用者後端程序作用，
但無法對執行復原的啟動程序作用。
`pg_stat_activity` 不會將正在復原中的交易顯示為
使用中（active）。因此，在復原期間，
`pg_prepared_xacts` 永遠是空的。如果你想要
解決處於不確定狀態的已準備交易，請在主要伺服器上檢視
`pg_prepared_xacts`，並在該處發出指令解決這些交易，
或是在復原結束後再解決。

`pg_locks` 會如常顯示後端程序所持有的鎖。
`pg_locks` 也會顯示由啟動程序所管理的一個虛擬交易，
該交易擁有復原過程中所重播之交易所持有的所有
`AccessExclusiveLocks`。請注意，啟動程序
在對資料庫進行變更時並不會取得鎖，因此除了
`AccessExclusiveLocks` 之外的鎖，
並不會顯示在啟動程序（Startup process）的
`pg_locks` 中；這些鎖只是被假定為存在。

Nagios 的 check_pgsql 外掛可以正常運作，
因為它所檢查的簡單資訊確實存在。
check_postgres 監控指令碼也可以正常運作，
不過部分回報的數值，可能會產生不同或令人困惑的結果。
舉例來說，由於待命伺服器上不會執行 vacuum，
最後一次 vacuum 的時間就不會被維護更新。
在主要伺服器上執行的 vacuum，其變更仍然會送到待命伺服器。

WAL 檔案控制指令在復原期間無法運作，
例如 `pg_backup_start`、`pg_switch_wal` 等。

動態可載入模組可以正常運作，包括
`pg_stat_statements`。

在復原期間，advisory lock 可以正常運作，
包括死結偵測。請注意，advisory lock 永遠不會被記錄到
WAL 中，因此不論是在主要伺服器或待命伺服器上，
advisory lock 都不可能與 WAL 重播發生衝突。
在主要伺服器上取得 advisory lock，也不會在待命伺服器上
觸發類似的 advisory lock。Advisory lock 只與
取得該鎖的伺服器有關。

以觸發程序為基礎的複寫系統，例如 Slony、
Londiste 及 Bucardo，完全無法在待命伺服器上執行，
不過只要變更沒有被送到待命伺服器上套用，它們仍然可以
在主要伺服器上順利運作。WAL 重播並非以觸發程序為基礎，
因此你無法從待命伺服器將資料轉送到任何需要額外資料庫寫入、
或依賴使用觸發程序的系統。

無法指派新的 OID，不過部分 UUID 產生器，
只要不需要將新狀態寫入資料庫，仍然可以正常運作。

目前，在唯讀交易期間不允許建立暫存資料表，
因此在某些情況下，既有的指令碼可能無法正確執行。
這項限制未來版本可能會放寬。這既是 SQL 標準相容性議題，
也是技術性議題。

`DROP TABLESPACE` 只有在該資料表空間為空的情況下，
才能成功執行。部分待命伺服器上的使用者，
可能正透過自己的 `temp_tablespaces` 參數，
使用中該資料表空間。如果該資料表空間中存在暫存檔案，
所有使用中的查詢都會被取消，以確保暫存檔案能夠被移除，
如此該資料表空間才能被移除，WAL 重播也才能繼續進行。

在主要伺服器上執行 `DROP DATABASE` 或
`ALTER DATABASE ... SET TABLESPACE`，
會產生一筆 WAL 項目，導致待命伺服器上所有連線至
該資料庫的使用者被強制中斷連線。不論
`max_standby_streaming_delay` 的設定為何，
這項動作都會立即發生。請注意，
`ALTER DATABASE ... RENAME` 並不會中斷使用者連線，
在大多數情況下不會被察覺，不過在某些情況下，
如果程式在某種程度上依賴資料庫名稱，則可能導致程式混亂。

在正常（非復原）模式下，如果你對一個具有登入能力的角色
發出 `DROP USER` 或 `DROP ROLE`，
而該使用者仍處於連線狀態，那麼已連線的使用者不會受到任何影響——
他們會保持連線。不過該使用者將無法重新連線。這項行為
在復原期間也同樣適用，因此在主要伺服器上執行 `DROP USER`，
並不會中斷該使用者在待命伺服器上的連線。

累計統計系統在復原期間是啟用的。所有掃描、讀取、區塊、
索引使用情況等，都會在待命伺服器上正常被記錄。
不過，WAL 重播並不會遞增與關聯（relation）及資料庫相關
的計數器。也就是說，重播並不會遞增
`pg_stat_all_tables` 中的欄位（例如 `n_tup_ins`），
啟動程序所執行的讀取或寫入，也不會被追蹤到
`pg_statio_` 檢視表中，相關聯的
`pg_stat_database` 欄位也不會被遞增。

Autovacuum 在復原期間並未啟用。它會在復原結束時正常啟動。

檢查點程序與背景寫入程序在復原期間都是啟用的。
檢查點程序會執行重新啟動點（restartpoint，
類似主要伺服器上的檢查點），而背景寫入程序則會執行
一般的區塊清理活動，這可能包括更新儲存在待命伺服器上的
hint bit 資訊。`CHECKPOINT` 指令在復原期間
是被接受的，不過它執行的是重新啟動點，而非新的檢查點。

<a id="HOT-STANDBY-PARAMETERS"></a>

### 26.4.4. 熱備援參數參考 [#](#HOT-STANDBY-PARAMETERS)

上面在[第 26.4.2 節](hot-standby.md#HOT-STANDBY-CONFLICT)
及[第 26.4.3 節](hot-standby.md#HOT-STANDBY-ADMIN)中，
已經提到過各種參數。

在主要伺服器上，可以使用
[wal_level](../runtime-config/runtime-config-wal.md#GUC-WAL-LEVEL)
參數。
[max_standby_archive_delay](../runtime-config/runtime-config-replication.md#GUC-MAX-STANDBY-ARCHIVE-DELAY)
及
[max_standby_streaming_delay](../runtime-config/runtime-config-replication.md#GUC-MAX-STANDBY-STREAMING-DELAY)，
如果設定在主要伺服器上，則不會有任何效果。

在待命伺服器上，可以使用
[hot_standby](../runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY)、
[max_standby_archive_delay](../runtime-config/runtime-config-replication.md#GUC-MAX-STANDBY-ARCHIVE-DELAY)
及
[max_standby_streaming_delay](../runtime-config/runtime-config-replication.md#GUC-MAX-STANDBY-STREAMING-DELAY)
這些參數。

<a id="HOT-STANDBY-CAVEATS"></a>

### 26.4.5. 注意事項 [#](#HOT-STANDBY-CAVEATS)

熱備援存在幾項限制。這些限制未來版本有可能、
也很可能會被修正：

* 在建立 snapshot 之前，必須完整掌握所有執行中交易的資訊。
  使用大量子交易（目前超過 64 個）的交易，
  會延遲唯讀連線的開始，直到執行時間最長的寫入交易完成為止。
  如果發生這種情況，伺服器日誌中會送出說明訊息。
* 待命查詢的有效起始點，是在主要伺服器每次執行檢查點時產生的。
  如果待命伺服器在主要伺服器處於關閉狀態時被關閉，
  在主要伺服器啟動、於 WAL 日誌中產生更多起始點之前，
  可能就無法重新進入熱備援狀態。在最常見會發生這種情況的場景下，
  這其實並不是問題。一般來說，如果主要伺服器已關閉且不再可用，
  那通常是因為發生了嚴重故障，無論如何都需要將待命伺服器
  轉換為新的主要伺服器來運作。而在主要伺服器是被刻意關閉的情況下，
  協調確保待命伺服器能夠順利成為新的主要伺服器，
  也是標準作業程序的一部分。
* 在復原結束時，由已準備交易所持有的 `AccessExclusiveLocks`，
  會需要兩倍於正常數量的鎖資料表項目。如果你打算執行大量
  通常會取得 `AccessExclusiveLocks` 的並行已準備交易，
  或是打算執行一個會取得許多 `AccessExclusiveLocks`
  的大型交易，建議你選擇較大的 `max_locks_per_transaction`
  值，可能需要達到主要伺服器上該參數值的兩倍之多。
  如果你將 `max_prepared_transactions` 設為 0，
  就完全不需要考慮這一點。
* 可序列化（Serializable）交易隔離等級，目前尚無法在熱備援中使用。
  （詳情請參閱
  [第 13.2.3 節](../../the-sql-language/mvcc/transaction-iso.md#XACT-SERIALIZABLE)
  及
  [第 13.4.1 節](../../the-sql-language/mvcc/applevel-consistency.md#SERIALIZABLE-CONSISTENCY)。）
  在熱備援模式下，嘗試將交易設定為可序列化隔離等級，
  將會產生錯誤。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/hot-standby.html)（原文版本：18.6；核對日期：2026-09-26）
