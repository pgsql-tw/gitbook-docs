<a id="PROTOCOL-REPLICATION"></a>

## 54.4. 串流複寫協定 [#](#protocol-replication) <a href="#protocol-replication" id="protocol-replication"></a>

要啟動串流複寫，前端會在啟動訊息中送出 `replication` 參數。布林值 `true`（或 `on`、`yes`、`1`）會告訴後端進入實體複寫 walsender 模式，在此模式下可以發出下面所列的一小組複寫命令，而不是 SQL 陳述式。

以 `database` 作為 `replication` 參數的值，會指示後端進入邏輯複寫 walsender 模式，並連線到 `dbname` 參數所指定的資料庫。在邏輯複寫 walsender 模式下，可以發出下面所列的複寫命令以及一般的 SQL 命令。

無論是實體複寫或邏輯複寫 walsender 模式，都只能使用簡單查詢協定。

為了測試複寫命令，你可以透過 psql 或任何其他使用 libpq 的工具，以包含 `replication` 選項的連線字串建立複寫連線，例如：

```

psql "dbname=postgres replication=database" -c "IDENTIFY_SYSTEM;"
```

不過，使用 [pg_receivewal](../../reference/reference-client/app-pgreceivewal.md)（用於實體複寫）或 [pg_recvlogical](../../reference/reference-client/app-pgrecvlogical.md)（用於邏輯複寫）通常會更有用。

啟用 [log_replication_commands](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-REPLICATION-COMMANDS) 時，複寫命令會記錄在伺服器日誌中。

複寫模式下接受的命令有：

<a id="PROTOCOL-REPLICATION-IDENTIFY-SYSTEM"></a>

- `IDENTIFY_SYSTEM` <a id="id-1.10.6.9.7.1.1.1.2"></a> [#](#PROTOCOL-REPLICATION-IDENTIFY-SYSTEM)


  要求伺服器表明自己的身分。伺服器會回覆一個只有一筆資料列的結果集，其中包含四個欄位：

  - `systemid` (`text`)

    識別該叢集的唯一系統識別碼。可用來確認用於初始化待命伺服器的基礎備份是否來自同一個叢集。

  - `timeline` (`int8`)

    目前的時間軸 ID。也可用來確認待命伺服器與主要伺服器是否一致。

  - `xlogpos` (`text`)

    目前的 WAL 刷寫（flush）位置。可用來取得預寫日誌中一個已知、可以開始串流的位置。

  - `dbname` (`text`)

    所連線的資料庫，或為 null。

<a id="PROTOCOL-REPLICATION-SHOW"></a>

- `SHOW` *`name`* <a id="id-1.10.6.9.7.1.2.1.3"></a> [#](#PROTOCOL-REPLICATION-SHOW)


  要求伺服器送出某個執行期參數目前的設定值。這類似於 SQL 命令 [SHOW](../../reference/sql-commands/sql-show.md)。

  - *`name`*

    執行期參數的名稱。可用的參數記載於[第 19 章](../../server-administration/runtime-config/README.md)。

<a id="PROTOCOL-REPLICATION-TIMELINE-HISTORY"></a>

- `TIMELINE_HISTORY` *`tli`* <a id="id-1.10.6.9.7.1.3.1.3"></a> [#](#PROTOCOL-REPLICATION-TIMELINE-HISTORY)


  要求伺服器送出時間軸 *`tli`* 的時間軸歷史檔案。伺服器會回覆一個只有一筆資料列的結果集，其中包含兩個欄位。雖然這些欄位標示為 `text`，但它們實際上傳回的是未經任何編碼轉換的原始位元組：

  - `filename` (`text`)

    時間軸歷史檔案的檔名，例如 `00000002.history`。

  - `content` (`text`)

    時間軸歷史檔案的內容。

<a id="PROTOCOL-REPLICATION-CREATE-REPLICATION-SLOT"></a>

- `CREATE_REPLICATION_SLOT` *`slot_name`* [ `TEMPORARY` ] { `PHYSICAL` | `LOGICAL` *`output_plugin`* } [ ( *`option`* [, ...] ) ] <a id="id-1.10.6.9.7.1.4.1.8"></a> [#](#PROTOCOL-REPLICATION-CREATE-REPLICATION-SLOT)


  建立實體或邏輯複寫插槽。關於複寫插槽的更多資訊，請參閱[第 26.2.6 節](../../server-administration/high-availability/warm-standby.md#streaming-replication-slots)。

  - *`slot_name`*

    要建立的插槽名稱。必須是有效的複寫插槽名稱（請參閱[第 26.2.6.1 節](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS-MANIPULATION)）。

  - *`output_plugin`*

    用於邏輯解碼的輸出外掛名稱（請參閱[第 47.6 節](../../server-programming/logicaldecoding/logicaldecoding-output-plugin.md)）。

  - `TEMPORARY`

    指定此複寫插槽為暫時插槽。暫時插槽不會儲存到磁碟，並會在發生錯誤或工作階段結束時自動刪除。

  支援下列選項：

  - `TWO_PHASE [ boolean ]`

    若為 true，此邏輯複寫插槽支援兩階段提交的解碼。使用此選項時，與兩階段提交相關的命令，例如 `PREPARE TRANSACTION`、`COMMIT PREPARED` 與 `ROLLBACK PREPARED`，會被解碼並傳送。交易會在 `PREPARE TRANSACTION` 時被解碼並傳送。預設值為 false。

  - `RESERVE_WAL [ boolean ]`

    若為 true，此實體複寫插槽會立即保留 WAL。否則，只有在串流複寫用戶端連線時才會保留 WAL。預設值為 false。

  - `SNAPSHOT { 'export' | 'use' | 'nothing' }`

    決定如何處理在邏輯插槽初始化期間建立的快照。`'export'` 是預設值，會匯出快照供其他工作階段使用。此選項不能在交易內使用。`'use'` 會將快照用於執行該命令的目前交易。此選項必須在交易中使用，而且 `CREATE_REPLICATION_SLOT` 必須是該交易中執行的第一個命令。最後，`'nothing'` 只會照常將快照用於邏輯解碼，但不會對它做任何其他事。

  - `FAILOVER [ boolean ]`

    若為 true，此插槽會啟用同步到待命伺服器的功能，使邏輯複寫在容錯移轉（failover）之後能夠繼續進行。預設值為 false。

  伺服器會以一個只有一筆資料列的結果集回應此命令，其中包含下列欄位：

  - `slot_name` (`text`)

    新建立之複寫插槽的名稱。

  - `consistent_point` (`text`)

    插槽達到一致狀態時的 WAL 位置。這是在此複寫插槽上可以開始串流的最早位置。

  - `snapshot_name` (`text`)

    此命令所匯出之快照的識別碼。在此連線上執行新的命令或關閉複寫連線之前，該快照都有效。如果建立的插槽是實體插槽，則為 null。

  - `output_plugin` (`text`)

    新建立之複寫插槽所使用的輸出外掛名稱。如果建立的插槽是實體插槽，則為 null。

<a id="PROTOCOL-REPLICATION-CREATE-REPLICATION-SLOT-LEGACY"></a>

- `CREATE_REPLICATION_SLOT` *`slot_name`* [ `TEMPORARY` ] { `PHYSICAL` [ `RESERVE_WAL` ] | `LOGICAL` *`output_plugin`* [ `EXPORT_SNAPSHOT` | `NOEXPORT_SNAPSHOT` | `USE_SNAPSHOT` | `TWO_PHASE` ] } [#](#PROTOCOL-REPLICATION-CREATE-REPLICATION-SLOT-LEGACY)


  為了與較舊的版本相容，`CREATE_REPLICATION_SLOT` 命令的這種替代語法仍受支援。

<a id="PROTOCOL-REPLICATION-ALTER-REPLICATION-SLOT"></a>

- `ALTER_REPLICATION_SLOT` *`slot_name`* ( *`option`* [, ...] ) <a id="id-1.10.6.9.7.1.6.1.4"></a> [#](#PROTOCOL-REPLICATION-ALTER-REPLICATION-SLOT)


  變更複寫插槽的定義。關於複寫插槽的更多資訊，請參閱[第 26.2.6 節](../../server-administration/high-availability/warm-standby.md#streaming-replication-slots)。此命令目前只支援邏輯複寫插槽。

  - *`slot_name`*

    要變更的插槽名稱。必須是有效的複寫插槽名稱（請參閱[第 26.2.6.1 節](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS-MANIPULATION)）。

  支援下列選項：

  - `TWO_PHASE [ boolean ]`

    若為 true，此邏輯複寫插槽支援兩階段提交的解碼。使用此選項時，與兩階段提交相關的命令，例如 `PREPARE TRANSACTION`、`COMMIT PREPARED` 與 `ROLLBACK PREPARED`，會被解碼並傳送。交易會在 `PREPARE TRANSACTION` 時被解碼並傳送。

  - `FAILOVER [ boolean ]`

    若為 true，此插槽會啟用同步到待命伺服器的功能，使邏輯複寫在容錯移轉之後能夠繼續進行。

<a id="PROTOCOL-REPLICATION-READ-REPLICATION-SLOT"></a>

- `READ_REPLICATION_SLOT` *`slot_name`* <a id="id-1.10.6.9.7.1.7.1.3"></a> [#](#PROTOCOL-REPLICATION-READ-REPLICATION-SLOT)


  讀取與某個複寫插槽相關聯的一些資訊。如果該複寫插槽不存在，會傳回一筆各值皆為 `NULL` 的資料列（tuple）。此命令目前只支援實體複寫插槽。

  伺服器會以一個只有一筆資料列的結果集回應此命令，其中包含下列欄位：

  - `slot_type` (`text`)

    複寫插槽的類型，為 `physical` 或 `NULL`。

  - `restart_lsn` (`text`)

    複寫插槽的 `restart_lsn`。

  - `restart_tli` (`int8`)

    依照目前的時間軸歷史，與 `restart_lsn` 相關聯的時間軸 ID。

<a id="PROTOCOL-REPLICATION-START-REPLICATION"></a>

- `START_REPLICATION` [ `SLOT` *`slot_name`* ] [ `PHYSICAL` ] *`XXX/XXX`* [ `TIMELINE` *`tli`* ] <a id="id-1.10.6.9.7.1.8.1.8"></a> [#](#PROTOCOL-REPLICATION-START-REPLICATION)


  指示伺服器開始串流 WAL，從 WAL 位置 *`XXX/XXX`* 開始。如果指定了 `TIMELINE` 選項，串流會從時間軸 *`tli`* 開始；否則會選擇伺服器目前的時間軸。伺服器可能會回覆錯誤，例如所要求的 WAL 區段已經被回收再利用的時候。成功時，伺服器會回應 CopyBothResponse 訊息，然後開始向前端串流 WAL。

  如果透過 *`slot_name`* 提供了插槽名稱，該插槽會隨著複寫的進展而更新，讓伺服器知道待命伺服器仍然需要哪些 WAL 區段，以及（若 `hot_standby_feedback` 為開啟）仍然需要哪些交易。

  如果用戶端要求的時間軸不是最新的，但屬於伺服器歷史的一部分，伺服器會串流該時間軸上從所要求的起點開始、直到伺服器切換到另一個時間軸那一點為止的所有 WAL。如果用戶端要求恰好從某個舊時間軸的結尾開始串流，伺服器會完全略過 COPY 模式。

  在串流完某個非最新時間軸上的所有 WAL 之後，伺服器會以退出 COPY 模式來結束串流。當用戶端也以退出 COPY 模式來確認這一點時，伺服器會送出一個包含一筆資料列、兩個欄位的結果集，指出此伺服器歷史中的下一個時間軸。第一個欄位是下一個時間軸的 ID（型別 `int8`），第二個欄位是發生切換的 WAL 位置（型別 `text`）。通常，切換位置就是已串流之 WAL 的結尾，但在一些極端情況下，伺服器可能會送出一些它在被提升（promote）為主要伺服器之前自己尚未重播過的舊時間軸 WAL。最後，伺服器會送出兩則 CommandComplete 訊息（一則結束 CopyData，另一則結束 `START_REPLICATION` 本身），並準備好接受新的命令。

  WAL 資料以一系列 CopyData 訊息送出；詳情請參閱[第 54.6 節](protocol-message-types.md)與[第 54.7 節](protocol-message-formats.md)。（這允許其他資訊穿插其中；特別是，伺服器在開始串流之後若遇到失敗，可以送出 ErrorResponse 訊息。）從伺服器送往用戶端的每則 CopyData 訊息，其酬載都包含下列其中一種格式的訊息：

  <a id="PROTOCOL-REPLICATION-XLOGDATA"></a>

  - XLogData (B) [#](#PROTOCOL-REPLICATION-XLOGDATA)
    - Byte1('w')

      將此訊息識別為 WAL 資料。

    - Int64

      此訊息中 WAL 資料的起點。

    - Int64

      伺服器上目前的 WAL 結尾。

    - Int64

      傳送當下伺服器的系統時鐘，以自 2000-01-01 午夜起算的微秒數表示。

    - Byte*`n`*

      WAL 資料串流的一個片段。

      單一 WAL 記錄絕不會被拆分到兩則 XLogData 訊息中。當一筆 WAL 記錄跨越 WAL 頁面邊界，因而已經使用接續記錄（continuation record）拆分時，它可以在頁面邊界處被拆分。換句話說，第一筆主要 WAL 記錄與它的接續記錄可以在不同的 XLogData 訊息中送出。
  <a id="PROTOCOL-REPLICATION-PRIMARY-KEEPALIVE-MESSAGE"></a>

  - 主要伺服器保活訊息（Primary keepalive message）(B) [#](#PROTOCOL-REPLICATION-PRIMARY-KEEPALIVE-MESSAGE)
    - Byte1('k')

      將此訊息識別為傳送端的保活（keepalive）訊息。

    - Int64

      伺服器上目前的 WAL 結尾。

    - Int64

      傳送當下伺服器的系統時鐘，以自 2000-01-01 午夜起算的微秒數表示。

    - Byte1

      1 表示用戶端應該盡快回覆此訊息，以避免因逾時而斷線。否則為 0。

  接收端程序可以隨時使用下列其中一種訊息格式（同樣放在 CopyData 訊息的酬載中）回覆傳送端：

  <a id="PROTOCOL-REPLICATION-STANDBY-STATUS-UPDATE"></a>

  - 待命伺服器狀態更新（Standby status update）(F) [#](#PROTOCOL-REPLICATION-STANDBY-STATUS-UPDATE)
    - Byte1('r')

      將此訊息識別為接收端狀態更新。

    - Int64

      待命伺服器上已接收並寫入磁碟的最後一個 WAL 位元組的位置 + 1。

    - Int64

      待命伺服器上已刷寫（flush）至磁碟的最後一個 WAL 位元組的位置 + 1。

    - Int64

      待命伺服器上已套用的最後一個 WAL 位元組的位置 + 1。

    - Int64

      傳送當下用戶端的系統時鐘，以自 2000-01-01 午夜起算的微秒數表示。

    - Byte1

      若為 1，表示用戶端要求伺服器立即回覆此訊息。這可用來對伺服器進行 ping，以測試連線是否仍然正常。
  <a id="PROTOCOL-REPLICATION-HOT-STANDBY-FEEDBACK-MESSAGE"></a>

  - 熱待命回饋訊息（Hot standby feedback message）(F) [#](#PROTOCOL-REPLICATION-HOT-STANDBY-FEEDBACK-MESSAGE)
    - Byte1('h')

      將此訊息識別為熱待命（hot standby）回饋訊息。

    - Int64

      傳送當下用戶端的系統時鐘，以自 2000-01-01 午夜起算的微秒數表示。

    - Int32

      待命伺服器目前的全域 `xmin`，不包括來自任何複寫插槽的 `catalog_xmin`。如果此值與接下來的 `catalog_xmin` 皆為 0，這會被視為一項通知，表示此連線上將不再送出熱待命回饋。之後的非零訊息可以重新啟動回饋機制。

    - Int32

      待命伺服器上全域 `xmin` xid 的 epoch。

    - Int32

      待命伺服器上任何複寫插槽中最低的 `catalog_xmin`。如果待命伺服器上不存在 `catalog_xmin`，或者熱待命回饋正在停用，則設為 0。

    - Int32

      待命伺服器上 `catalog_xmin` xid 的 epoch。

<a id="PROTOCOL-REPLICATION-START-REPLICATION-SLOT-LOGICAL"></a>

- `START_REPLICATION` `SLOT` *`slot_name`* `LOGICAL` *`XXX/XXX`* [ ( *`option_name`* [ *`option_value`* ] [, ...] ) ] [#](#PROTOCOL-REPLICATION-START-REPLICATION-SLOT-LOGICAL)


  指示伺服器開始為邏輯複寫串流 WAL，起點為 WAL 位置 *`XXX/XXX`* 或插槽的 `confirmed_flush_lsn`（請參閱[第 53.20 節](../views/view-pg-replication-slots.md)）兩者中較大的一個。這種行為讓用戶端在沒有資料要處理時，更容易避免更新其本機的 LSN 狀態。不過，從與所要求不同的 LSN 開始，可能無法捕捉到某些類型的用戶端錯誤；因此用戶端可能會希望在發出 `START_REPLICATION` 之前，先檢查 `confirmed_flush_lsn` 是否符合其預期。

  伺服器可能會回覆錯誤，例如插槽不存在的時候。成功時，伺服器會回應 CopyBothResponse 訊息，然後開始向前端串流 WAL。

  CopyBothResponse 訊息內的訊息，與 `START_REPLICATION ... PHYSICAL` 所記載的格式相同，包括兩則 CommandComplete 訊息。

  與所選插槽相關聯的輸出外掛會用來處理要串流的輸出。

  - `SLOT` *`slot_name`*

    要從中串流變更的插槽名稱。此參數為必要，且必須對應到一個以 `LOGICAL` 模式透過 `CREATE_REPLICATION_SLOT` 建立的現有邏輯複寫插槽。

  - *`XXX/XXX`*

    開始串流的 WAL 位置。

  - *`option_name`*

    傳給插槽之邏輯解碼輸出外掛的選項名稱。標準（`pgoutput`）外掛所接受的選項，請參閱[第 54.5 節](protocol-logical-replication.md)。

  - *`option_value`*

    與指定選項相關聯的選用值，形式為字串常數。

<a id="PROTOCOL-REPLICATION-DROP-REPLICATION-SLOT"></a>

- `DROP_REPLICATION_SLOT` *`slot_name`* [ `WAIT` ] <a id="id-1.10.6.9.7.1.10.1.4"></a> [#](#PROTOCOL-REPLICATION-DROP-REPLICATION-SLOT)


  刪除複寫插槽，並釋放任何已保留的伺服器端資源。

  - *`slot_name`*

    要刪除的插槽名稱。

  - `WAIT`

    如果插槽正在使用中，此選項會讓命令等待它變成非使用中，而不是採取引發錯誤的預設行為。

<a id="PROTOCOL-REPLICATION-UPLOAD-MANIFEST"></a>

- `UPLOAD_MANIFEST` <a id="id-1.10.6.9.7.1.11.1.2"></a> [#](#PROTOCOL-REPLICATION-UPLOAD-MANIFEST)


  上傳備份清單（backup manifest），為進行增量備份做準備。

<a id="PROTOCOL-REPLICATION-BASE-BACKUP"></a>

- `BASE_BACKUP` [ ( *`option`* [, ...] ) ] <a id="id-1.10.6.9.7.1.12.1.3"></a> [#](#PROTOCOL-REPLICATION-BASE-BACKUP)


  指示伺服器開始串流基礎備份。系統會在備份開始之前自動進入備份模式，並在備份完成時退出備份模式。接受下列選項：

  - `LABEL` *`'label'`*

    設定備份的標籤。如果未指定，會使用備份標籤 `base backup`。標籤的引號規則與開啟 [standard_conforming_strings](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS) 時的標準 SQL 字串相同。

  - `TARGET` *`'target'`*

    告訴伺服器要把備份送到哪裡。如果目標是 `client`（這是預設值），備份資料會送到用戶端。如果是 `server`，備份資料會寫入伺服器上由 `TARGET_DETAIL` 選項所指定的路徑名稱。如果是 `blackhole`，備份資料不會送到任何地方，只會直接被捨棄。

    `server` 目標需要超級使用者權限，或已被授予 `pg_write_server_files` 角色。

  - `TARGET_DETAIL` *`'detail'`*

    提供關於備份目標的額外資訊。

    目前，只有在備份目標為 `server` 時才能使用此選項。它指定備份應寫入的伺服器目錄。

  - `PROGRESS [ boolean ]`

    若設為 true，則要求產生進度報告所需的資訊。這會在每個資料表空間的標頭中送回一個大約的大小，可用來計算串流已經進行了多少。這是在傳輸開始之前先列舉所有檔案的大小一次來計算的，因此可能會對效能造成負面影響。特別是，第一筆資料開始串流之前可能需要較長的時間。由於資料庫檔案在備份期間可能會變動，此大小只是大約值，在估算時間與實際送出檔案之間，可能會變大也可能會變小。預設值為 false。

  - `CHECKPOINT { 'fast' | 'spread' }`

    設定在基礎備份開始時所要執行的檢查點類型。預設值為 `spread`。

  - `WAL [ boolean ]`

    若設為 true，則在備份中包含必要的 WAL 區段。這會在基礎目錄 tar 檔的 `pg_wal` 目錄中，包含備份開始與停止之間的所有檔案。預設值為 false。

  - `WAIT [ boolean ]`

    若設為 true，備份會等到最後一個所需的 WAL 區段已經封存為止；若未啟用 WAL 封存，則發出警告。若為 false，備份既不會等待，也不會發出警告，而由用戶端負責確保所需的日誌可用。預設值為 true。

  - `COMPRESSION` *`'method'`*

    指示伺服器使用指定的方法壓縮備份。目前支援的方法有 `gzip`、`lz4` 與 `zstd`。

  - `COMPRESSION_DETAIL` *`detail`*

    為所選的壓縮方法指定詳細設定。此選項只應該與 `COMPRESSION` 選項一起使用。如果值為整數，它指定的是壓縮等級。否則，它應該是以逗號分隔的項目清單，每個項目的形式為 *`keyword`* 或 *`keyword=value`*。目前支援的關鍵字有 `level`、`long` 與 `workers`。

    `level` 關鍵字設定壓縮等級。對 `gzip` 而言，壓縮等級應該是介於 `1` 到 `9` 之間的整數（預設為 `Z_DEFAULT_COMPRESSION`，即 `-1`）；對 `lz4` 而言，是介於 1 到 12 之間的整數（預設為 `0`，表示快速壓縮模式）；對 `zstd` 而言，則是介於 `ZSTD_minCLevel()`（通常為 `-131072`）與 `ZSTD_maxCLevel()`（通常為 `22`）之間的整數（預設為 `ZSTD_CLEVEL_DEFAULT`，即 `3`）。

    `long` 關鍵字會啟用長距離比對模式，以較高的記憶體使用量為代價，換取更好的壓縮率。只有 `zstd` 支援長距離模式。

    `workers` 關鍵字設定平行壓縮應使用的執行緒數量。只有 `zstd` 支援平行壓縮。

  - `MAX_RATE` *`rate`*

    限制（節流）每單位時間從伺服器傳輸到用戶端的最大資料量。預期的單位是每秒 KB。如果指定了此選項，其值必須等於零，或者落在 32 kB 到 1 GB 的範圍內（含兩端）。如果傳入零或未指定此選項，則不對傳輸施加任何限制。

  - `TABLESPACE_MAP [ boolean ]`

    若為 true，則將目錄 `pg_tblspc` 中現有符號連結的相關資訊，納入名為 `tablespace_map` 的檔案中。資料表空間對應檔包含目錄 `pg_tblspc/` 中現有的每個符號連結名稱，以及該符號連結的完整路徑。預設值為 false。

  - `VERIFY_CHECKSUMS [ boolean ]`

    若為 true，且已啟用檢查碼，則在基礎備份期間驗證檢查碼。若為 false，則略過此步驟。預設值為 true。

  - `MANIFEST` *`manifest_option`*

    當以 `yes` 或 `force-encode` 的值指定此選項時，會建立備份清單並隨備份一起送出。備份清單是備份中所有檔案的清單，但不包括可能被納入的任何 WAL 檔案。它也會儲存每個檔案的大小、最後修改時間，以及選擇性的檢查碼。`force-encode` 值會強制所有檔名都以十六進位編碼；否則，只有名稱為非 UTF8 八位元組序列的檔案才會進行這種編碼。`force-encode` 主要用於測試目的，以確保讀取備份清單的用戶端能夠處理這種情況。為了與先前的版本相容，預設值為 `MANIFEST 'no'`。

  - `MANIFEST_CHECKSUMS` *`checksum_algorithm`*

    指定應套用到備份清單中每個檔案的檢查碼演算法。目前可用的演算法有 `NONE`、`CRC32C`、`SHA224`、`SHA256`、`SHA384` 與 `SHA512`。預設值為 `CRC32C`。

  - `INCREMENTAL`

    要求進行增量備份。在以此選項執行基礎備份之前，必須先執行 `UPLOAD_MANIFEST` 命令。

  備份開始時，伺服器會先送出兩個一般結果集，接著是一個或多個 CopyOutResponse 結果。

  第一個一般結果集包含備份的起始位置，為一筆具有兩個欄位的資料列。第一個欄位包含以 XLogRecPtr 格式表示的起始位置，第二個欄位包含對應的時間軸 ID。

  第二個一般結果集針對每個資料表空間各有一筆資料列。此資料列中的欄位有：

  - `spcoid` (`oid`)

    資料表空間的 OID；如果是基礎目錄，則為 null。

  - `spclocation` (`text`)

    資料表空間目錄的完整路徑；如果是基礎目錄，則為 null。

  - `size` (`int8`)

    如果有要求進度報告，則為資料表空間的大約大小，以 KB（1024 位元組）為單位；否則為 null。

  在第二個一般結果集之後，會送出一個 CopyOutResponse。每則 CopyData 訊息的酬載都會包含下列其中一種格式的訊息：

  - 新封存檔（new archive）(B)
    - Byte1('n')

      將此訊息識別為表示新封存檔的開始。主資料目錄會有一個封存檔，每個額外的資料表空間也各有一個；每個封存檔都使用 tar 格式（遵循 POSIX 1003.1-2008 標準中所規定的「ustar interchange format」）。

    - String

      此封存檔的檔名。

    - String

      對主資料目錄而言，為空字串。對其他資料表空間而言，則為建立此封存檔所來源之目錄的完整路徑。

  - 備份清單（manifest）(B)
    - Byte1('m')

      將此訊息識別為表示備份清單的開始。

  - 封存檔或備份清單資料（archive or manifest data）(B)
    - Byte1('d')

      將此訊息識別為包含封存檔或備份清單資料。

    - Byte*`n`*

      資料位元組。

  - 進度報告（progress report）(B)
    - Byte1('p')

      將此訊息識別為進度報告。

    - Int64

      目前資料表空間中已處理完成的位元組數。

  在 CopyOutResponse（或所有這類回應）送出之後，會送出最後一個一般結果集，其中包含備份的 WAL 結束位置，格式與起始位置相同。

  資料目錄與每個資料表空間的 tar 封存檔，會包含這些目錄中的所有檔案，無論它們是 PostgreSQL 的檔案，還是加入同一目錄的其他檔案。唯一被排除的檔案有：

  * `postmaster.pid`
  * `postmaster.opts`
  * `pg_internal.init`（存在於多個目錄中）
  * PostgreSQL 伺服器運作期間建立的各種暫存檔案與目錄，例如任何以 `pgsql_tmp` 開頭的檔案或目錄，以及暫時關聯。
  * 無日誌（unlogged）關聯，但不包括在復原時重新建立（空的）無日誌關聯所需的初始化分支（init fork）。
  * `pg_wal`，包括其子目錄。如果執行備份時包含 WAL 檔案，則會納入一個合成版本的 `pg_wal`，但它只會包含備份正常運作所需的檔案，而不包含其餘內容。
  * `pg_dynshmem`、`pg_notify`、`pg_replslot`、`pg_serial`、`pg_snapshots`、`pg_stat_tmp` 與 `pg_subtrans` 會以空目錄的形式複製（即使它們是符號連結）。
  * 一般檔案與目錄以外的檔案，例如符號連結（上面列出的目錄除外）以及特殊裝置檔案與作業系統檔案，都會被略過。（`pg_tblspc` 中的符號連結會被保留。）

  如果伺服器上的底層檔案系統支援，會設定擁有者、群組與檔案模式。

在上述所有命令中，指定 `boolean` 型別的參數時，可以省略 *`value`* 部分，這等同於指定 `TRUE`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/protocol-replication.html)（原文版本：18.6；核對日期：2026-10-17）
