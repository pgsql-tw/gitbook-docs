<a id="WAL-CONFIGURATION"></a>

## 28.5. WAL 組態設定 [#](#WAL-CONFIGURATION)

有數個與 WAL 相關的組態參數，會影響資料庫效能。
本節將說明這些參數的用途。關於設定伺服器組態參數的
一般資訊，請參閱[第 19 章](../runtime-config/README.md)。

*檢查點*（checkpoint）<a id="id-1.6.15.7.3.2"></a>
是交易序列中的某些時間點，在這些時間點上，可以保證堆積（heap）
與索引資料檔案，都已經套用了該檢查點之前寫入的所有資訊。
在檢查點時刻，所有髒（dirty）資料頁面都會排清至磁碟，
並將一筆特殊的檢查點紀錄寫入 WAL 檔案。
（相關的變更紀錄，先前就已經排清至 WAL 檔案中。）
一旦發生當機，當機復原程序會查看最新的檢查點紀錄，
以判斷應從 WAL 中的哪個位置（稱為 redo 紀錄）開始執行
REDO 操作。在該位置之前對資料檔案所做的任何變更，
都能保證已經寫入磁碟。因此，在某次檢查點之後，
早於包含 redo 紀錄之區段的 WAL 區段，就不再需要，
可以回收利用或移除。（若正在進行 WAL 歸檔，
則 WAL 區段必須先歸檔，才能回收利用或移除。）

檢查點要求將所有髒資料頁面排清至磁碟，這可能造成
相當大的 I/O 負載。因此，檢查點活動會受到節流控管，
讓 I/O 從檢查點開始時啟動，並在下一次檢查點應該開始之前完成；
這能將檢查點期間的效能衰退降到最低。

伺服器的檢查點程序（checkpointer process）會每隔一段時間，
自動執行一次檢查點。每經過
[checkpoint_timeout](../runtime-config/runtime-config-wal.md#GUC-CHECKPOINT-TIMEOUT) 秒，
或當 [max_wal_size](../runtime-config/runtime-config-wal.md#GUC-MAX-WAL-SIZE) 即將被超過時，
就會開始一次檢查點，視何者先發生而定。這兩者的預設值，
分別是 5 分鐘與 1 GB。若自前一次檢查點以來，
尚未有任何 WAL 寫入，即使 `checkpoint_timeout`
已經過去，新的檢查點仍會被略過。（若正在使用 WAL 歸檔，
且您想針對檔案歸檔的頻率設定下限，以限縮潛在的資料遺失，
應該調整 [archive_timeout](../runtime-config/runtime-config-wal.md#GUC-ARCHIVE-TIMEOUT) 參數，
而不是調整檢查點相關參數。）您也可以使用 SQL 指令
`CHECKPOINT`，強制執行一次檢查點。

降低 `checkpoint_timeout` 及／或
`max_wal_size`，會讓檢查點發生得更頻繁。
這能加快當機後的復原速度，因為需要重做的工作較少。
不過，這必須與更頻繁排清髒資料頁面所增加的成本
互相權衡。若已設定 [full_page_writes](../runtime-config/runtime-config-wal.md#GUC-FULL-PAGE-WRITES)
（此為預設值），還有另一項因素需要考量。為確保資料頁面的
一致性，每次檢查點之後，資料頁面第一次被修改時，
都會將該頁面的完整內容記錄下來。在這種情況下，
較小的檢查點間隔，會增加寫入 WAL 的資料量，
部分抵銷了縮短間隔原本想達到的目的，
並且無論如何都會造成更多磁碟 I/O。

檢查點相當昂貴，原因有二：首先，它們需要將目前所有的髒緩衝區
寫出；其次，如上所述，它們會導致後續產生額外的 WAL 流量。
因此，明智的做法是，將檢查點相關參數設定得夠高，
讓檢查點不至於發生得太頻繁。您可以設定
[checkpoint_warning](../runtime-config/runtime-config-wal.md#GUC-CHECKPOINT-WARNING) 參數，
作為檢查點參數是否合理的簡易檢查方式。若檢查點發生的間隔，
比 `checkpoint_warning` 秒還要短，
伺服器日誌就會輸出一則訊息，建議增加
`max_wal_size`。偶爾出現這樣的訊息，
不必過度緊張，但若經常出現，就應該調高檢查點控制參數。
若您尚未將 `max_wal_size` 設定得夠高，
諸如大型 `COPY` 傳輸之類的批次操作，
可能會導致出現多次這類警告。

為避免大量頁面寫入瞬間湧入而淹沒 I/O 系統，
檢查點期間髒緩衝區的寫入，會分散在一段時間內進行。
該段時間由 [checkpoint_completion_target](../runtime-config/runtime-config-wal.md#GUC-CHECKPOINT-COMPLETION-TARGET)
控制，其值以檢查點間隔（由 `checkpoint_timeout` 設定）
的比例形式表示。系統會調整 I/O 速率，讓檢查點
在經過 `checkpoint_timeout` 秒數的指定比例後，
或在超過 `max_wal_size` 之前完成，視何者先發生而定。
以預設值 0.9 而言，可以預期 PostgreSQL
會在下一次排定的檢查點開始前不久，完成每一次檢查點
（大約在前一次檢查點所耗費時間的 90% 左右）。這會盡可能地
分散 I/O，讓檢查點的 I/O 負載，在整個檢查點間隔內
保持一致。這麼做的缺點是，延長檢查點會影響復原時間，
因為需要保留更多 WAL 區段，以供復原時可能使用。
若使用者擔心復原所需的時間，可能會想要降低
`checkpoint_timeout`，讓檢查點發生得更頻繁，
但仍將 I/O 分散在整個檢查點間隔內。或者，
也可以降低 `checkpoint_completion_target`，
但這會導致 I/O 密集的時段（檢查點期間）與 I/O 較少的時段
（檢查點完成後、下一次排定的檢查點開始前）交替出現，
因此並不建議這麼做。雖然 `checkpoint_completion_target`
理論上可以設定到高達 1.0，但通常建議不要將它設定得
高於 0.9（此為預設值），因為檢查點除了寫入髒緩衝區之外，
還包含其他一些活動。設定為 1.0，相當有可能導致檢查點
無法準時完成，進而因所需 WAL 區段數量的非預期變動，
而造成效能損失。

在 Linux 與 POSIX 平台上，
[checkpoint_flush_after](../runtime-config/runtime-config-wal.md#GUC-CHECKPOINT-FLUSH-AFTER)
讓您可以強制在寫入可設定的位元組數之後，
將檢查點所寫入的作業系統頁面排清至磁碟。否則，
這些頁面可能會被保留在作業系統的頁面快取中，
導致在檢查點結束時發出 `fsync` 時發生停滯。
這項設定通常有助於降低交易延遲，但也可能對效能
造成不利影響，特別是對於大於
[shared_buffers](../runtime-config/runtime-config-resource.md#GUC-SHARED-BUFFERS)、
但小於作業系統頁面快取的工作負載而言。

`pg_wal` 目錄中 WAL 區段檔案的數量，
取決於 `min_wal_size`、`max_wal_size`，
以及先前檢查點週期中所產生的 WAL 量。當舊的 WAL
區段檔案不再需要時，就會被移除或回收利用（也就是重新命名，
成為編號序列中未來要使用的區段）。若因 WAL 輸出速率
短期出現高峰，導致超過 `max_wal_size`，
就會移除不需要的區段檔案，直到系統回到此限制之下為止。
在此限制之下，系統會回收利用足夠數量的 WAL 檔案，
以涵蓋到下一次檢查點為止的預估需求，其餘的則會移除。
此預估值是根據先前檢查點週期中所使用 WAL 檔案數量的
移動平均值計算而得。若實際使用量超過預估值，
該移動平均值會立即提高，因此在某種程度上，
它會因應尖峰使用量，而非平均使用量。
`min_wal_size` 為將回收利用、供未來使用的
WAL 檔案數量，設下一個下限；即使系統處於閒置狀態，
且 WAL 使用量預估值顯示幾乎不需要 WAL，
仍會持續回收利用這麼多數量的 WAL，供未來使用。

與 `max_wal_size` 無關的是，系統一律會保留
最近 [wal_keep_size](../runtime-config/runtime-config-replication.md#GUC-WAL-KEEP-SIZE)
百萬位元組（megabytes）的 WAL 檔案，再加上額外一個 WAL 檔案。
此外，若使用了 WAL 歸檔，舊的區段在歸檔完成之前，
不能被移除或回收利用。若 WAL 歸檔的速度，
跟不上 WAL 產生的速度，或者 `archive_command`
或 `archive_library` 一再失敗，
舊的 WAL 檔案就會持續累積在 `pg_wal` 中，
直到問題解決為止。使用複寫插槽（replication slot）
但速度緩慢或失敗的待命伺服器，也會造成相同的效果
（請參閱[26.2.6 節](../high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS)）。
同樣地，若啟用了 [WAL 摘要功能](../runtime-config/runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION)，
舊的區段會被保留，直到完成摘要為止。

在歸檔復原或待命模式下，伺服器會定期執行
*重新啟動點*（restartpoint）<a id="id-1.6.15.7.12.2"></a>，
這與正常運作時的檢查點類似：伺服器會強制將其所有狀態
寫入磁碟，更新 `pg_control` 檔案，
標示已處理過的 WAL 資料不需要再次掃描，
接著回收利用 `pg_wal` 目錄中任何舊的
WAL 區段檔案。重新啟動點的執行頻率，
不能高於主要伺服器上檢查點的頻率，因為重新啟動點
只能在檢查點紀錄處執行。重新啟動點可以依排程執行，
也可以依外部請求執行。
[`pg_stat_checkpointer`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW)
檢視表中的 `restartpoints_timed` 計數器，
會計算前者的次數，而 `restartpoints_req`
則會計算後者的次數。
當到達某筆檢查點紀錄時，若自上一次實際執行的重新啟動點
以來，已經過至少
[checkpoint_timeout](../runtime-config/runtime-config-wal.md#GUC-CHECKPOINT-TIMEOUT) 秒，
或先前嘗試執行重新啟動點失敗，就會依排程觸發
重新啟動點。在後者的情況下，
下一次重新啟動點會排定在 15 秒後執行。
依請求觸發重新啟動點的原因，與觸發檢查點的原因類似，
但主要是因為 WAL 大小即將超過
[max_wal_size](../runtime-config/runtime-config-wal.md#GUC-MAX-WAL-SIZE)。
然而，由於執行重新啟動點的時機受到限制，
在復原期間，`max_wal_size` 經常會被超過，
超出的量最多可達一個檢查點週期所產生的 WAL 量。
（無論如何，`max_wal_size` 從來就不是硬性限制，
因此您應該始終保留充裕的餘裕，以避免磁碟空間耗盡。）
[`pg_stat_checkpointer`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW)
檢視表中的 `restartpoints_done` 計數器，
會計算實際真正執行過的重新啟動點次數。

在某些情況下，當主要伺服器上的 WAL 大小快速增加時，
例如在執行大量 `INSERT` 期間，
待命伺服器上的 `restartpoints_req` 計數器，
可能會呈現尖峰式的成長。這是因為，由於 WAL 消耗量增加
而請求建立新的重新啟動點，卻因為自上一次重新啟動點以來的
安全檢查點紀錄，尚未在待命伺服器上重播完成，
而無法執行。這是正常的行為，不會導致系統資源消耗增加。
在與重新啟動點相關的計數器中，只有
`restartpoints_done` 計數器，
才表示確實耗用了值得注意的系統資源。

有兩個常用的內部 WAL 函式：
`XLogInsertRecord` 與 `XLogFlush`。
`XLogInsertRecord` 用於將一筆新的紀錄，
放入共享記憶體中的 WAL 緩衝區。若沒有空間可容納新紀錄，
`XLogInsertRecord` 就必須寫出（移至核心快取）
一些已填滿的 WAL 緩衝區。這並不理想，因為
`XLogInsertRecord` 在每一次資料庫底層修改
（例如資料列的插入）時都會被使用，而此時系統
正持有受影響資料頁面的排他鎖定，因此該操作必須
盡可能地快速。更糟的是，寫出 WAL 緩衝區，
也可能迫使系統建立新的 WAL 區段，
這會耗費更多時間。正常情況下，WAL 緩衝區
應該由 `XLogFlush` 請求寫出並排清，
這類請求大多在交易確認時發出，以確保交易紀錄
已排清至永久儲存體。在 WAL 輸出量很高的系統上，
`XLogFlush` 請求的發生頻率，
可能不足以避免 `XLogInsertRecord`
必須自行執行寫出動作。在這類系統上，
應該透過修改 [wal_buffers](../runtime-config/runtime-config-wal.md#GUC-WAL-BUFFERS)
參數，增加 WAL 緩衝區的數量。當
[full_page_writes](../runtime-config/runtime-config-wal.md#GUC-FULL-PAGE-WRITES) 已設定，
且系統非常忙碌時，將 `wal_buffers`
設定得更高，有助於平順化每次檢查點結束後
緊接而來那段時間的回應時間。

[commit_delay](../runtime-config/runtime-config-wal.md#GUC-COMMIT-DELAY) 參數，
定義了群組確認（group commit）領導者程序，
在 `XLogFlush` 中取得鎖定之後，
會睡眠多少微秒，而在這段期間，群組確認的跟隨者，
則會在領導者之後排隊等候。這段延遲讓其他伺服器
程序，能夠將自己的確認紀錄，加入 WAL 緩衝區，
使它們全都能在領導者最終執行的同步操作中一併排清。
若未啟用 [fsync](../runtime-config/runtime-config-wal.md#GUC-FSYNC)，
或目前處於作用中交易狀態的其他工作階段，
少於 [commit_siblings](../runtime-config/runtime-config-wal.md#GUC-COMMIT-SIBLINGS) 個，
就不會發生睡眠；這是為了避免在其他工作階段不太可能
即將確認交易時仍進行睡眠。請注意，在某些平台上，
睡眠請求的解析度為十毫秒，因此
`commit_delay` 設定在 1 到 10000 微秒
之間的任何非零值，效果都會相同。另請注意，
在某些平台上，睡眠操作實際耗費的時間，
可能會略長於參數所要求的時間。

由於 `commit_delay` 的目的，是讓每次排清操作的成本，
能夠分攤給同時確認的多筆交易（其代價可能是增加交易延遲），
因此必須先量化該成本，才能明智地選擇此設定值。
該成本越高，`commit_delay` 在提升交易輸出量方面
預期就越有效，但這種效果有其上限。
[pg_test_fsync](../../reference/reference-server/pgtestfsync.md) 程式，
可用來量測單次 WAL 排清操作所需的平均時間（以微秒為單位）。
將該程式回報「單次 8kB 寫入操作後執行排清」所需平均時間的一半，
設定為 `commit_delay` 的值，通常是最有效的設定，
因此建議以此值，作為針對特定工作負載進行最佳化時的起始點。
雖然調校 `commit_delay`，在 WAL 儲存於高延遲
的旋轉式磁碟上時特別有用，但即使儲存媒體的同步時間非常快，
例如固態硬碟，或具電池備援寫入快取的 RAID 陣列，
其效益仍可能相當顯著；但這一點絕對應該針對具代表性的
工作負載進行測試。在這類情況下，應使用較高的
`commit_siblings` 值，而較小的
`commit_siblings` 值，則通常在延遲較高的媒體上
有所幫助。請注意，`commit_delay` 設定得過高，
確實有可能導致交易延遲大幅增加，進而使整體交易輸出量下降。

當 `commit_delay` 設定為零（預設值）時，
仍有可能出現某種形式的群組確認，但每個群組，
將只由那些在前一次排清操作（若有的話）進行期間，
到達需要排清自身確認紀錄之時間點的工作階段所組成。
在用戶端數量較多時，往往會出現「跳板效應」（gangway effect），
因此即使 `commit_delay` 為零，
群組確認的效果依然顯著，也因此明確設定
`commit_delay`，所能帶來的幫助往往較小。
設定 `commit_delay` 只有在下列兩種情況下才有幫助：
(1) 存在一些同時確認的交易，且 (2) 輸出量在某種程度上
受到確認速率的限制；但在旋轉延遲較高的情況下，
即使只有兩個用戶端（也就是一個正在確認的用戶端，
加上一筆同層交易），這項設定仍能有效提升交易輸出量。

[wal_sync_method](../runtime-config/runtime-config-wal.md#GUC-WAL-SYNC-METHOD) 參數，
決定 PostgreSQL 要求核心將 WAL 更新
強制寫出至磁碟的方式。就可靠性而言，所有選項應該都相同，
唯一的例外是 `fsync_writethrough`，
它有時能強制排清磁碟快取，即使其他選項無法做到這一點。
不過，哪一個選項最快，相當取決於平台。
您可以使用 [pg_test_fsync](../../reference/reference-server/pgtestfsync.md)
程式，測試不同選項的速度。請注意，
若 `fsync` 已被關閉，此參數就無關緊要。

啟用 [wal_debug](../runtime-config/runtime-config-developer.md#GUC-WAL-DEBUG) 組態參數
（前提是編譯 PostgreSQL 時已加入對此功能的支援），
會使每一次 `XLogInsertRecord` 與 `XLogFlush`
的 WAL 呼叫，都被記錄到伺服器日誌中。
此選項未來可能會被更通用的機制取代。

有兩個將 WAL 資料寫入磁碟的內部函式：
`XLogWrite` 與 `issue_xlog_fsync`。
啟用 [track_wal_io_timing](../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING) 時，
`XLogWrite` 寫入與 `issue_xlog_fsync`
同步 WAL 資料至磁碟所耗費的總時間，
會分別以 `write_time` 與 `fsync_time`，
計入 [pg_stat_io](../monitoring/monitoring-stats.md#PG-STAT-IO-VIEW)
中 `object` 為 `wal` 的項目。
`XLogWrite` 通常由 `XLogInsertRecord`
（當 WAL 緩衝區中沒有空間容納新紀錄時）、
`XLogFlush` 以及 WAL 寫入器呼叫，
用於將 WAL 緩衝區寫入磁碟，並呼叫
`issue_xlog_fsync`。
`issue_xlog_fsync` 通常由 `XLogWrite` 呼叫，
用於將 WAL 檔案同步至磁碟。
若 `wal_sync_method` 為 `open_datasync`
或 `open_sync`，`XLogWrite` 中的寫入操作，
即可保證已寫入的 WAL 資料同步至磁碟，
此時 `issue_xlog_fsync` 不會執行任何動作。
若 `wal_sync_method` 為 `fdatasync`、
`fsync` 或 `fsync_writethrough` 其中之一，
寫入操作只會將 WAL 緩衝區移至核心快取，
`issue_xlog_fsync` 才會將它們同步至磁碟。
無論 `track_wal_io_timing` 的設定為何，
`XLogWrite` 寫入以及 `issue_xlog_fsync`
同步 WAL 資料至磁碟的次數，也會分別以
`writes` 與 `fsyncs`，
計入 `pg_stat_io` 中 `object`
為 `wal` 的項目。

[recovery_prefetch](../runtime-config/runtime-config-wal.md#GUC-RECOVERY-PREFETCH) 參數，
可用於指示核心，及早開始讀取即將需要、
但目前尚未存在於 PostgreSQL 緩衝區集區中的磁碟區塊，
藉此縮短復原期間的 I/O 等待時間。
[maintenance_io_concurrency](../runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY)
與 [wal_decode_buffer_size](../runtime-config/runtime-config-wal.md#GUC-WAL-DECODE-BUFFER-SIZE)
這兩項設定，分別限制了預先讀取的並行程度與距離。
此參數預設值為 `try`，這會在支援發出
預讀建議（read-ahead advice）的系統上，啟用此功能。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/wal-configuration.html)（原文版本：18.6；核對日期：2026-09-22）
