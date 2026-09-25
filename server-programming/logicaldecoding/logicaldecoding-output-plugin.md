<a id="LOGICALDECODING-OUTPUT-PLUGIN"></a>
## 47.6. 邏輯解碼輸出外掛程式 [#](#LOGICALDECODING-OUTPUT-PLUGIN)

[47.6.1. 初始化函式](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-INIT)

[47.6.2. 能力](logicaldecoding-output-plugin.md#LOGICALDECODING-CAPABILITIES)

[47.6.3. 輸出模式](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-MODE)

[47.6.4. 輸出外掛程式回呼](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-CALLBACKS)

[47.6.5. 產生輸出用的函式](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT)

在 PostgreSQL 原始碼樹的
[`contrib/test_decoding`](../../appendixes/contrib/test-decoding.md)
子目錄中，可以找到輸出外掛程式的範例。

<a id="LOGICALDECODING-OUTPUT-INIT"></a>

### 47.6.1. 初始化函式 [#](#LOGICALDECODING-OUTPUT-INIT)

<a id="id-1.8.14.12.3.2"></a>

輸出外掛程式是透過動態載入一個以該輸出外掛程式名稱
作為程式庫基底名稱的共享程式庫來載入的。系統會使用一般的
程式庫搜尋路徑來尋找該程式庫。為了提供所需的輸出
外掛程式回呼，並表明該程式庫實際上就是一個輸出
外掛程式，它需要提供一個名為
`_PG_output_plugin_init` 的函式。這個函式會被傳入一個
結構，需要以個別動作的回呼函式指標
填入這個結構。

```

typedef struct OutputPluginCallbacks
{
    LogicalDecodeStartupCB startup_cb;
    LogicalDecodeBeginCB begin_cb;
    LogicalDecodeChangeCB change_cb;
    LogicalDecodeTruncateCB truncate_cb;
    LogicalDecodeCommitCB commit_cb;
    LogicalDecodeMessageCB message_cb;
    LogicalDecodeFilterByOriginCB filter_by_origin_cb;
    LogicalDecodeShutdownCB shutdown_cb;
    LogicalDecodeFilterPrepareCB filter_prepare_cb;
    LogicalDecodeBeginPrepareCB begin_prepare_cb;
    LogicalDecodePrepareCB prepare_cb;
    LogicalDecodeCommitPreparedCB commit_prepared_cb;
    LogicalDecodeRollbackPreparedCB rollback_prepared_cb;
    LogicalDecodeStreamStartCB stream_start_cb;
    LogicalDecodeStreamStopCB stream_stop_cb;
    LogicalDecodeStreamAbortCB stream_abort_cb;
    LogicalDecodeStreamPrepareCB stream_prepare_cb;
    LogicalDecodeStreamCommitCB stream_commit_cb;
    LogicalDecodeStreamChangeCB stream_change_cb;
    LogicalDecodeStreamMessageCB stream_message_cb;
    LogicalDecodeStreamTruncateCB stream_truncate_cb;
} OutputPluginCallbacks;

typedef void (*LogicalOutputPluginInit) (struct OutputPluginCallbacks *cb);
```

`begin_cb`、`change_cb`
與 `commit_cb` 這三個回呼是必要的，
而 `startup_cb`、`truncate_cb`、
`message_cb`、`filter_by_origin_cb`
與 `shutdown_cb` 則是選用的。
若未設定 `truncate_cb`，但需要解碼
`TRUNCATE`，則該動作會被忽略。

輸出外掛程式也可以定義函式，以支援大型
進行中交易的串流傳輸。`stream_start_cb`、
`stream_stop_cb`、`stream_abort_cb`、
`stream_commit_cb` 與 `stream_change_cb`
是必要的，而 `stream_message_cb` 與
`stream_truncate_cb` 則是選用的。若該輸出
外掛程式也支援兩階段提交，則同時也需要
`stream_prepare_cb`。

輸出外掛程式也可以定義函式，以支援兩階段提交，
讓動作能在 `PREPARE TRANSACTION` 時被解碼。
`begin_prepare_cb`、`prepare_cb`、
`commit_prepared_cb` 與 `rollback_prepared_cb`
這些回呼是必要的，而 `filter_prepare_cb` 則是選用的。
若該輸出外掛程式也支援大型進行中交易的串流傳輸，
則同時也需要 `stream_prepare_cb`。

<a id="LOGICALDECODING-CAPABILITIES"></a>

### 47.6.2. 能力 [#](#LOGICALDECODING-CAPABILITIES)

為了解碼、格式化並輸出變更，輸出外掛程式可以使用
後端大部分的一般基礎架構，包括呼叫輸出函式。只要
存取的關係，是由 `initdb` 在
`pg_catalog` 綱要中建立的，
或是使用以下方式標記為使用者提供的目錄資料表，
就允許對關係進行唯讀存取：

```

ALTER TABLE user_catalog_table SET (user_catalog_table = true);
CREATE TABLE another_catalog_table(data text) WITH (user_catalog_table = true);
```

請注意，輸出外掛程式中對使用者目錄資料表，或一般系統
目錄資料表的存取，都必須僅透過 `systable_*`
掃描 API 來進行。透過 `heap_*` 掃描 API 存取，
會導致錯誤。此外，任何會導致交易 ID 指派的
動作都是被禁止的。這其中包括對資料表寫入、
執行 DDL 變更，以及呼叫 `pg_current_xact_id()`。

<a id="LOGICALDECODING-OUTPUT-MODE"></a>

### 47.6.3. 輸出模式 [#](#LOGICALDECODING-OUTPUT-MODE)

輸出外掛程式回呼，可以以幾乎任意的
格式，將資料傳遞給消費端。對於某些使用情境而言，例如
透過 SQL 檢視變更，以能夠容納任意資料的資料型別
（例如 `bytea`）傳回資料，會比較麻煩。若輸出外掛程式
只輸出以伺服器編碼表示的文字資料，
它可以在[啟動
回呼](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-STARTUP)中，將
`OutputPluginOptions.output_type` 設定為
`OUTPUT_PLUGIN_TEXTUAL_OUTPUT`，而非
`OUTPUT_PLUGIN_BINARY_OUTPUT`，來宣告這一點。
在這種情況下，所有的資料都必須以伺服器編碼表示，
以便 `text` 資料值能夠容納它。這一點在
啟用了斷言（assertion）的建置版本中會被檢查。

<a id="LOGICALDECODING-OUTPUT-PLUGIN-CALLBACKS"></a>

### 47.6.4. 輸出外掛程式回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-CALLBACKS)

輸出外掛程式會透過它需要提供的
各種回呼，得知正在發生的變更。

並行的交易，會依照提交順序解碼，且只有屬於
特定交易的變更，才會在該交易的
`begin` 與 `commit`
回呼之間被解碼。明確或隱含被回復的
交易，永遠不會被解碼。成功的儲存點
（savepoint），會依照它們在該交易中執行的順序，
併入包含它們的交易中。使用
`PREPARE TRANSACTION` 為兩階段提交而準備的交易，
若提供了解碼它所需的輸出外掛程式回呼，
同樣也會被解碼。目前正在被解碼的已準備交易，
有可能會透過
`ROLLBACK PREPARED` 指令被並行中止。在這種情況下，
該交易的邏輯解碼也會一併被中止。一旦偵測到中止，
並呼叫了 `prepare_cb` 回呼，
這類交易的所有變更就會被跳過。因此，即使發生
並行中止，也會提供足夠的資訊給輸出外掛程式，
讓它能在解碼到 `ROLLBACK PREPARED` 時，
正確地處理它。

### 注意

只有已安全刷寫（flush）至磁碟的交易，才會
被解碼。這可能導致在
`synchronous_commit` 設為
`off` 時，緊接在後的
`pg_logical_slot_get_changes()` 呼叫中，
`COMMIT` 不會立即被解碼。

<a id="LOGICALDECODING-OUTPUT-PLUGIN-STARTUP"></a>

#### 47.6.4.1. 啟動回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-STARTUP)

選用的 `startup_cb` 回呼，會在
複寫插槽被建立，或被要求串流傳輸變更時被呼叫，
與目前有多少變更已準備好可以輸出無關。

```

typedef void (*LogicalDecodeStartupCB) (struct LogicalDecodingContext *ctx,
                                        OutputPluginOptions *options,
                                        bool is_init);
```

當複寫插槽正在被建立時，`is_init`
參數會是 true，否則為 false。
*`options`* 指向一個選項的結構，
輸出外掛程式可以設定這個結構：

```

typedef struct OutputPluginOptions
{
    OutputPluginOutputType output_type;
    bool        receive_rewrites;
} OutputPluginOptions;
```

`output_type` 必須設定為
`OUTPUT_PLUGIN_TEXTUAL_OUTPUT`
或 `OUTPUT_PLUGIN_BINARY_OUTPUT` 其中之一。另請參閱
[47.6.3 節](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-MODE)。
若 `receive_rewrites` 為 true，則系統
也會針對某些 DDL 操作期間，由堆積重寫（heap rewrite）所產生的變更，
呼叫輸出外掛程式。這對於處理 DDL
複寫的外掛程式而言頗為重要，但它們需要特殊處理。

啟動回呼應該驗證
`ctx->output_plugin_options` 中所存在的選項。若輸出外掛程式
需要保有狀態，可以
使用 `ctx->output_plugin_private` 來儲存它。

<a id="LOGICALDECODING-OUTPUT-PLUGIN-SHUTDOWN"></a>

#### 47.6.4.2. 關閉回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-SHUTDOWN)

選用的 `shutdown_cb` 回呼，會在
先前活躍的複寫插槽不再被使用時呼叫，
可用於釋放輸出外掛程式私有的資源。此插槽
不一定會被刪除，只是串流傳輸被停止而已。

```

typedef void (*LogicalDecodeShutdownCB) (struct LogicalDecodingContext *ctx);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-BEGIN"></a>

#### 47.6.4.3. 交易開始回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-BEGIN)

必要的 `begin_cb` 回呼，會在
一個已提交交易的開始被解碼時呼叫。已中止的交易，
以及它們的內容，永遠不會被解碼。

```

typedef void (*LogicalDecodeBeginCB) (struct LogicalDecodingContext *ctx,
                                      ReorderBufferTXN *txn);
```

*`txn`* 參數包含該交易的中繼資訊，
例如它被提交時的時間戳記，以及
它的 XID。

<a id="LOGICALDECODING-OUTPUT-PLUGIN-COMMIT"></a>

#### 47.6.4.4. 交易結束回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-COMMIT)

必要的 `commit_cb` 回呼，會在
交易提交被解碼時呼叫。若有任何列被修改，
則所有已修改列的 `change_cb` 回呼，
都會在此之前被呼叫。

```

typedef void (*LogicalDecodeCommitCB) (struct LogicalDecodingContext *ctx,
                                       ReorderBufferTXN *txn,
                                       XLogRecPtr commit_lsn);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-CHANGE"></a>

#### 47.6.4.5. 變更回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-CHANGE)

必要的 `change_cb` 回呼，會針對交易內
每一筆個別的列修改被呼叫，無論它是
`INSERT`、`UPDATE`
還是 `DELETE`。即使原始指令一次修改了
多筆列，該回呼仍然會針對每一列個別呼叫。
`change_cb` 回呼可以存取系統或
使用者目錄資料表，以協助輸出該列
修改的詳細內容。在解碼已準備（但尚未
提交）的交易，或解碼未提交交易的過程中，
這個變更回呼也有可能因為這個交易本身
同時被回復，而發生錯誤。在這種情況下，
這個已中止交易的邏輯解碼，會被優雅地停止。

```

typedef void (*LogicalDecodeChangeCB) (struct LogicalDecodingContext *ctx,
                                       ReorderBufferTXN *txn,
                                       Relation relation,
                                       ReorderBufferChange *change);
```

*`ctx`* 與 *`txn`* 參數，
其內容與 `begin_cb`
及 `commit_cb` 回呼相同，但另外還會傳入
一個關係描述子 *`relation`*，指向該列
所屬的關係，以及一個描述該列修改的結構
*`change`*。

### 注意

只有未記錄（unlogged，
請參閱[`UNLOGGED`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-UNLOGGED)）
且非暫存（temporary，
請參閱[`TEMPORARY` 或 `TEMP`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-TEMPORARY)）
的使用者自訂資料表中的變更，才能使用
邏輯解碼來擷取。

<a id="LOGICALDECODING-OUTPUT-PLUGIN-TRUNCATE"></a>

#### 47.6.4.6. TRUNCATE 回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-TRUNCATE)

選用的 `truncate_cb` 回呼，會針對
`TRUNCATE` 指令被呼叫。

```

typedef void (*LogicalDecodeTruncateCB) (struct LogicalDecodingContext *ctx,
                                         ReorderBufferTXN *txn,
                                         int nrelations,
                                         Relation relations[],
                                         ReorderBufferChange *change);
```

這些參數與 `change_cb`
回呼類似。不過，因為透過外部鍵連結的
資料表上的 `TRUNCATE` 動作，需要一起執行，
這個回呼接收的是一個關係的陣列，而不是只有單一一個。
詳情請參閱 [TRUNCATE](../../reference/sql-commands/sql-truncate.md) 陳述式的說明。

<a id="LOGICALDECODING-OUTPUT-PLUGIN-FILTER-ORIGIN"></a>

#### 47.6.4.7. 來源篩選回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-FILTER-ORIGIN)

選用的 `filter_by_origin_cb` 回呼，
是用來判斷從 *`origin_id`* 重播的資料，
輸出外掛程式是否感興趣。

```

typedef bool (*LogicalDecodeFilterByOriginCB) (struct LogicalDecodingContext *ctx,
                                               RepOriginId origin_id);
```

*`ctx`* 參數的內容，
與其他回呼相同。除了來源之外，沒有其他可用的
資訊。若要表示來自傳入節點的變更並不相關，
請傳回 true，使它們被篩選掉；否則傳回 false。
對於已被篩選掉的交易與變更，
其他回呼都不會被呼叫。

在實作串接式（cascading）或多方向複寫解決方案時，
這一點相當有用。依來源篩選，可以避免在
這類架構中，將相同的變更來回複寫。雖然
交易與變更本身也帶有關於來源的
資訊，但透過這個回呼進行篩選，
明顯更有效率。

<a id="LOGICALDECODING-OUTPUT-PLUGIN-MESSAGE"></a>

#### 47.6.4.8. 通用訊息回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-MESSAGE)

選用的 `message_cb` 回呼，會在
一則邏輯解碼訊息被解碼時呼叫。

```

typedef void (*LogicalDecodeMessageCB) (struct LogicalDecodingContext *ctx,
                                        ReorderBufferTXN *txn,
                                        XLogRecPtr message_lsn,
                                        bool transactional,
                                        const char *prefix,
                                        Size message_size,
                                        const char *message);
```

*`txn`* 參數包含該交易的中繼資訊，
例如它被提交時的時間戳記，以及它的
XID。不過請注意，當該訊息是非交易性的，
且在記錄該訊息的交易中，XID 尚未被指派時，
它可以是 NULL。*`lsn`*（即上方回呼簽章中的 message_lsn 參數）是
該訊息在 WAL 中的位置。*`transactional`*
表示該訊息是否以交易性方式傳送。與變更
回呼類似，在解碼已準備（但尚未提交）的
交易，或解碼未提交交易的過程中，這個訊息
回呼也有可能因為這個交易本身同時被回滾，
而發生錯誤。在這種情況下，這個已中止交易
的邏輯解碼，會被優雅地停止。
*`prefix`* 是一個任意的、以 null 結尾的前綴，
可用於辨識目前這個外掛程式所感興趣的訊息。
最後，*`message`* 參數，則保存了
大小為 *`message_size`* 的實際訊息。

務必格外小心，確保輸出外掛程式認為感興趣的前綴
是唯一的。使用擴充功能或輸出外掛程式本身的
名稱，通常是不錯的選擇。

<a id="LOGICALDECODING-OUTPUT-PLUGIN-FILTER-PREPARE"></a>

#### 47.6.4.9. 準備篩選回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-FILTER-PREPARE)

選用的 `filter_prepare_cb` 回呼，
是用來判斷目前這個兩階段提交交易的一部分資料，
應該在目前的 prepare 階段解碼，還是稍後
在 `COMMIT PREPARED` 時，
當作一般的單階段交易來解碼。若要表示
應該跳過解碼，請傳回 `true`；
否則傳回 `false`。若未定義該回呼，
則會假設為 `false`（也就是不進行篩選，
所有使用兩階段提交的交易，同樣會以兩個階段解碼）。

```

typedef bool (*LogicalDecodeFilterPrepareCB) (struct LogicalDecodingContext *ctx,
                                              TransactionId xid,
                                              const char *gid);
```

*`ctx`* 參數的內容，與其他
回呼相同。參數 *`xid`*
與 *`gid`*，提供了兩種不同的方式來識別
該交易。之後的 `COMMIT PREPARED` 或
`ROLLBACK PREPARED`，會同時帶有這兩個識別碼，
讓輸出外掛程式可以選擇要使用哪一個。

該回呼在解碼一筆交易的過程中，可能會被呼叫多次，
且對於同一對
*`xid`* 與 *`gid`*，
每次呼叫時都必須提供相同的靜態答案。

<a id="LOGICALDECODING-OUTPUT-PLUGIN-BEGIN-PREPARE"></a>

#### 47.6.4.10. 交易開始準備回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-BEGIN-PREPARE)

必要的 `begin_prepare_cb` 回呼，會在
一個已準備交易的開始被解碼時呼叫。這個回呼中，
可以使用作為
*`txn`* 參數一部分的 *`gid`*
欄位，來檢查該外掛程式是否已經收到過這個
`PREPARE`，在這種情況下，它可以選擇
擲回錯誤，或跳過該交易剩餘的變更。

```

typedef void (*LogicalDecodeBeginPrepareCB) (struct LogicalDecodingContext *ctx,
                                             ReorderBufferTXN *txn);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-PREPARE"></a>

#### 47.6.4.11. 交易準備回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-PREPARE)

必要的 `prepare_cb` 回呼，會在
一個為兩階段提交而準備的交易被解碼時呼叫。
若有任何列被修改，則所有已修改資料列的
`change_cb` 回呼，都會在此之前被呼叫。這個回呼中，
可以使用作為 *`txn`* 參數一部分的
*`gid`* 欄位。

```

typedef void (*LogicalDecodePrepareCB) (struct LogicalDecodingContext *ctx,
                                        ReorderBufferTXN *txn,
                                        XLogRecPtr prepare_lsn);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-COMMIT-PREPARED"></a>

#### 47.6.4.12. 已準備交易的提交回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-COMMIT-PREPARED)

必要的 `commit_prepared_cb` 回呼，會在
一個交易的 `COMMIT PREPARED` 被解碼時呼叫。
這個回呼中，可以使用作為 *`txn`* 參數
一部分的 *`gid`* 欄位。

```

typedef void (*LogicalDecodeCommitPreparedCB) (struct LogicalDecodingContext *ctx,
                                               ReorderBufferTXN *txn,
                                               XLogRecPtr commit_lsn);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-ROLLBACK-PREPARED"></a>

#### 47.6.4.13. 已準備交易回滾回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-ROLLBACK-PREPARED)

必要的 `rollback_prepared_cb` 回呼，會在
一個交易的 `ROLLBACK PREPARED` 被解碼時
呼叫。這個回呼中，可以使用作為 *`txn`*
參數一部分的 *`gid`* 欄位。參數
*`prepare_end_lsn`* 與
*`prepare_time`*，可用來檢查該外掛程式
是否已收到這個 `PREPARE TRANSACTION`，
若是，就可以套用該回滾，否則，就可以跳過該
回滾。單憑 *`gid`* 並不足夠，
因為下游節點有可能有一個識別碼相同的已準備交易。

```

typedef void (*LogicalDecodeRollbackPreparedCB) (struct LogicalDecodingContext *ctx,
                                                 ReorderBufferTXN *txn,
                                                 XLogRecPtr prepare_end_lsn,
                                                 TimestampTz prepare_time);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-STREAM-START"></a>

#### 47.6.4.14. 串流開始回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-START)

必要的 `stream_start_cb` 回呼，會在
從一個進行中的交易開啟一個串流變更區塊時呼叫。

```

typedef void (*LogicalDecodeStreamStartCB) (struct LogicalDecodingContext *ctx,
                                            ReorderBufferTXN *txn);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-STREAM-STOP"></a>

#### 47.6.4.15. 串流停止回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-STOP)

必要的 `stream_stop_cb` 回呼，會在
關閉一個進行中交易的串流變更區塊時呼叫。

```

typedef void (*LogicalDecodeStreamStopCB) (struct LogicalDecodingContext *ctx,
                                           ReorderBufferTXN *txn);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-STREAM-ABORT"></a>

#### 47.6.4.16. 串流中止回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-ABORT)

必要的 `stream_abort_cb` 回呼，會被呼叫，
以中止先前已串流傳輸的交易。

```

typedef void (*LogicalDecodeStreamAbortCB) (struct LogicalDecodingContext *ctx,
                                            ReorderBufferTXN *txn,
                                            XLogRecPtr abort_lsn);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-STREAM-PREPARE"></a>

#### 47.6.4.17. 串流準備回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-PREPARE)

`stream_prepare_cb` 回呼會被呼叫，
以作為兩階段提交的一部分，準備先前已串流傳輸的交易。
當輸出外掛程式同時支援大型進行中交易的串流傳輸，
以及兩階段提交時，就需要這個回呼。

```

typedef void (*LogicalDecodeStreamPrepareCB) (struct LogicalDecodingContext *ctx,
                                              ReorderBufferTXN *txn,
                                              XLogRecPtr prepare_lsn);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-STREAM-COMMIT"></a>

#### 47.6.4.18. 串流提交回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-COMMIT)

必要的 `stream_commit_cb` 回呼，會被呼叫，
以提交先前已串流傳輸的交易。

```

typedef void (*LogicalDecodeStreamCommitCB) (struct LogicalDecodingContext *ctx,
                                             ReorderBufferTXN *txn,
                                             XLogRecPtr commit_lsn);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-STREAM-CHANGE"></a>

#### 47.6.4.19. 串流變更回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-CHANGE)

必要的 `stream_change_cb` 回呼，會在
傳送一個串流變更區塊（由 `stream_start_cb`
與 `stream_stop_cb` 呼叫所界定）中的變更時呼叫。
由於該交易有可能在之後的某個時間點中止，
而我們不會為已中止的交易解碼變更，因此
實際的變更內容並不會被顯示。

```

typedef void (*LogicalDecodeStreamChangeCB) (struct LogicalDecodingContext *ctx,
                                             ReorderBufferTXN *txn,
                                             Relation relation,
                                             ReorderBufferChange *change);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-STREAM-MESSAGE"></a>

#### 47.6.4.20. 串流訊息回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-MESSAGE)

選用的 `stream_message_cb` 回呼，會在
傳送一個串流變更區塊（由 `stream_start_cb`
與 `stream_stop_cb` 呼叫所界定）中的通用訊息時呼叫。
由於該交易有可能在之後的某個時間點中止，
而我們不會為已中止的交易解碼變更，因此
交易性訊息的內容並不會被顯示。

```

typedef void (*LogicalDecodeStreamMessageCB) (struct LogicalDecodingContext *ctx,
                                              ReorderBufferTXN *txn,
                                              XLogRecPtr message_lsn,
                                              bool transactional,
                                              const char *prefix,
                                              Size message_size,
                                              const char *message);
```

<a id="LOGICALDECODING-OUTPUT-PLUGIN-STREAM-TRUNCATE"></a>

#### 47.6.4.21. 串流 TRUNCATE 回呼 [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-TRUNCATE)

選用的 `stream_truncate_cb` 回呼，會針對
一個串流變更區塊（由 `stream_start_cb`
與 `stream_stop_cb` 呼叫所界定）中的
`TRUNCATE` 指令呼叫。

```

typedef void (*LogicalDecodeStreamTruncateCB) (struct LogicalDecodingContext *ctx,
                                               ReorderBufferTXN *txn,
                                               int nrelations,
                                               Relation relations[],
                                               ReorderBufferChange *change);
```

這些參數與 `stream_change_cb`
回呼類似。不過，因為透過外部鍵連結的
資料表上的 `TRUNCATE` 動作，需要一起執行，
這個回呼接收的是一個關係的陣列，而不是只有單一一個。
詳情請參閱 [TRUNCATE](../../reference/sql-commands/sql-truncate.md) 陳述式的說明。

<a id="LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT"></a>

### 47.6.5. 產生輸出用的函式 [#](#LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT)

若要真正產生輸出，輸出外掛程式可以在
`begin_cb`、`commit_cb`
或 `change_cb` 回呼內，將資料寫入
`ctx->out` 中的 `StringInfo` 輸出緩衝區。在寫入輸出
緩衝區之前，必須呼叫 `OutputPluginPrepareWrite(ctx, last_write)`，
而在寫入該緩衝區完成後，必須呼叫
`OutputPluginWrite(ctx, last_write)`
來執行寫入。*`last_write`*
表示這次特定的寫入，是否為該回呼的最後一次寫入。

以下範例展示了如何將資料輸出給
輸出外掛程式的消費端：

```

OutputPluginPrepareWrite(ctx, true);
appendStringInfo(ctx->out, "BEGIN %u", txn->xid);
OutputPluginWrite(ctx, true);
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-output-plugin.html)（原文版本：18.6；核對日期：2026-09-25）
