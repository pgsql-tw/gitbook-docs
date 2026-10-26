<a id="LIBPQ-PIPELINE-MODE"></a>

## 32.5. 管線模式 [#](#libpq-pipeline-mode) <a href="#libpq-pipeline-mode" id="libpq-pipeline-mode"></a>

[32.5.1. 使用管線模式](libpq-pipeline-mode.md#libpq-pipeline-using)

[32.5.2. 與管線模式相關的函式](libpq-pipeline-mode.md#libpq-pipeline-functions)

[32.5.3. 何時使用管線模式](libpq-pipeline-mode.md#libpq-pipeline-tips)

<a id="id-1.7.3.12.2"></a><a id="id-1.7.3.12.3"></a><a id="id-1.7.3.12.4"></a>

libpq 管線模式讓應用程式
不必先讀取前一個已送出查詢的結果，就能送出下一個查詢。
利用管線模式，用戶端等待伺服器的時間會比較少，
因為多個查詢／結果可以在單一次網路往返交換中
送出／接收。

雖然管線模式能大幅提升效能，但使用管線模式撰寫
用戶端程式比較複雜，因為這牽涉到
管理待處理查詢的佇列，並找出哪個結果
對應到佇列中的哪個查詢。

管線模式通常也會在用戶端與伺服器兩端消耗較多記憶體，
不過謹慎且積極地管理送出／接收佇列可以減輕
這個問題。無論連線處於阻塞或非阻塞模式，
這一點都適用。

雖然 libpq 的管線 API 是在
PostgreSQL 14 中引入的，但它是用戶端功能，
不需要伺服器的特殊支援，可在任何
支援 v3 延伸查詢協定的伺服器上運作。詳細資訊請參閱
[第 54.2.4 節](../../internals/protocol/protocol-flow.md#protocol-flow-pipelining)。

<a id="LIBPQ-PIPELINE-USING"></a>

### 32.5.1. 使用管線模式 [#](#libpq-pipeline-using) <a href="#libpq-pipeline-using" id="libpq-pipeline-using"></a>

若要發出管線，應用程式必須將連線切換為
管線模式，
這是透過 [`PQenterPipelineMode`](libpq-pipeline-mode.md#LIBPQ-PQENTERPIPELINEMODE) 達成的。
可以使用 [`PQpipelineStatus`](libpq-pipeline-mode.md#LIBPQ-PQPIPELINESTATUS)
測試管線模式是否處於啟用狀態。
在管線模式下，只允許使用
延伸查詢協定的[非同步操作](libpq-async.md)；
不允許包含多個 SQL 命令的命令字串，
`COPY` 也不允許。
使用同步命令執行函式，
例如 `PQfn`、
`PQexec`、
`PQexecParams`、
`PQprepare`、
`PQexecPrepared`、
`PQdescribePrepared`、
`PQdescribePortal`、
`PQclosePrepared`、
`PQclosePortal`，
屬於錯誤狀況。
`PQsendQuery` 也
不允許使用，因為它使用的是簡單查詢協定。
當所有已送出之命令的結果都處理完畢，且
管線結束結果也已取用之後，應用程式可以使用
[`PQexitPipelineMode`](libpq-pipeline-mode.md#LIBPQ-PQEXITPIPELINEMODE) 回到非管線模式。

### 注意

在 libpq 中，管線模式最好搭配
[非阻塞模式](libpq-async.md#libpq-pqsetnonblocking)使用。若
在阻塞模式下使用，用戶端與伺服器之間可能會發生死結。
[<a id="id-1.7.3.12.9.3.1.3"></a>[15]](#ftn.id-1.7.3.12.9.3.1.3)

<a id="LIBPQ-PIPELINE-SENDING"></a>

#### 32.5.1.1. 發出查詢 [#](#LIBPQ-PIPELINE-SENDING)

進入管線模式之後，應用程式使用
[`PQsendQueryParams`](libpq-async.md#libpq-pqsendqueryparams)
或其預備查詢版本的同系列函式
[`PQsendQueryPrepared`](libpq-async.md#libpq-pqsendqueryprepared) 送出請求。
這些請求會在用戶端排入佇列，直到刷寫到伺服器為止；
這會在使用 [`PQpipelineSync`](libpq-pipeline-mode.md#LIBPQ-PQPIPELINESYNC)
於管線中建立同步點時發生，
或在呼叫 [`PQflush`](libpq-async.md#libpq-pqflush) 時發生。
函式 [`PQsendPrepare`](libpq-async.md#libpq-pqsendprepare)、
[`PQsendDescribePrepared`](libpq-async.md#libpq-pqsenddescribeprepared)、
[`PQsendDescribePortal`](libpq-async.md#libpq-pqsenddescribeportal)、
[`PQsendClosePrepared`](libpq-async.md#libpq-pqsendcloseprepared) 與
[`PQsendClosePortal`](libpq-async.md#libpq-pqsendcloseportal) 在管線模式下也可以運作。
結果的處理方式說明如下。

伺服器會依照用戶端送出的順序執行陳述式並傳回結果。
伺服器會立即開始執行管線中的命令，
而不會等待管線結束。
請注意，結果會在伺服器端緩衝；伺服器會在以
`PQpipelineSync` 或
`PQsendPipelineSync` 建立同步點時，或在呼叫
`PQsendFlushRequest` 時，刷寫該緩衝區。
若任何陳述式發生錯誤，伺服器會中止目前的
交易，並且在下一個同步點之前，不執行佇列中任何後續的命令；
每個這樣的命令都會產生一個 `PGRES_PIPELINE_ABORTED` 結果。
（即使管線中的命令原本會回復該交易，
這一點仍然成立。）
查詢處理會在同步點之後恢復。

一個操作依賴先前某個操作的結果是沒有問題的；
例如，一個查詢可以定義一個資料表，供同一管線中的下一個
查詢使用。同樣地，應用程式可以
建立具名的預備陳述式，並以同一管線中之後的
陳述式執行它。

<a id="LIBPQ-PIPELINE-RESULTS"></a>

#### 32.5.1.2. 處理結果 [#](#LIBPQ-PIPELINE-RESULTS)

若要處理管線中某一個查詢的結果，應用程式會重複呼叫
`PQgetResult` 並處理每個結果，
直到 `PQgetResult` 傳回 null 為止。
接著可以再次使用 `PQgetResult` 取得管線中下一個查詢的結果，
並重複此循環。
應用程式照常處理個別陳述式的結果。
當管線中所有查詢的結果都已傳回之後，
`PQgetResult` 會傳回一個
狀態值為 `PGRES_PIPELINE_SYNC` 的結果。

用戶端可以選擇延後處理結果，直到整個
管線都送出之後再處理，也可以將結果處理與送出管線中更多
查詢交錯進行；請參閱[第 32.5.1.4 節](libpq-pipeline-mode.md#LIBPQ-PIPELINE-INTERLEAVE)。

`PQgetResult` 的行為與一般
非同步處理時相同，差別在於它可能包含新的
`PGresult` 類型 `PGRES_PIPELINE_SYNC`
與 `PGRES_PIPELINE_ABORTED`。
對於每一次 `PQpipelineSync` 或
`PQsendPipelineSync`，都會在管線中對應的位置
恰好回報一次 `PGRES_PIPELINE_SYNC`。
從第一個錯誤開始，直到下一個 `PGRES_PIPELINE_SYNC` 為止，
所有後續結果都會以 `PGRES_PIPELINE_ABORTED` 取代一般的
查詢結果送出；
請參閱[第 32.5.1.3 節](libpq-pipeline-mode.md#LIBPQ-PIPELINE-ERRORS)。

譯註：原文此處寫作「從第一個錯誤開始」都以 PGRES_PIPELINE_ABORTED 取代，與第 32.5.1.3 節的說明不一致。實際行為是：第一個失敗的操作本身回報 PGRES_FATAL_ERROR，管線隨即被標記為已中止；之後被略過的各個操作才回報 PGRES_PIPELINE_ABORTED，直到下一個 PGRES_PIPELINE_SYNC 為止。

處理管線結果時，`PQisBusy`、`PQconsumeInput` 等
函式照常運作。特別是，
在管線中途呼叫 `PQisBusy` 時，
若到目前為止已發出之所有查詢的結果都已取用，就會傳回 0。

libpq 不會向應用程式提供
任何關於目前正在處理之查詢的資訊（除了
`PQgetResult` 會傳回 null，表示我們開始
傳回下一個查詢的結果之外）。應用程式必須記錄
它送出查詢的順序，才能將查詢與其
對應的結果關聯起來。
應用程式通常會使用狀態機或 FIFO 佇列來做到這一點。

<a id="LIBPQ-PIPELINE-ERRORS"></a>

#### 32.5.1.3. 錯誤處理 [#](#LIBPQ-PIPELINE-ERRORS)

從用戶端的角度來看，在 `PQresultStatus`
傳回 `PGRES_FATAL_ERROR` 之後，
管線就會被標記為已中止。
對於已中止之管線中每一個剩餘的佇列操作，
`PQresultStatus` 都會回報一個
`PGRES_PIPELINE_ABORTED` 結果。
`PQpipelineSync` 或
`PQsendPipelineSync` 的結果會回報為
`PGRES_PIPELINE_SYNC`，表示已中止的管線結束，
並恢復正常的結果處理。

在錯誤復原期間，用戶端*必須*使用
`PQgetResult` 處理結果。

若管線使用的是隱含交易，則已經執行的操作
會被回復，而排在失敗操作之後的操作
則會被完全略過。若管線開始並提交單一個明確交易
（也就是第一個陳述式為 `BEGIN`，最後一個為
`COMMIT`），行為也相同，差別在於管線結束時，
工作階段仍會停留在已中止的交易狀態。若管線包含
*多個明確交易*，所有在錯誤發生之前已提交的交易
都會維持已提交，目前正在進行的交易
會被中止，而所有後續的操作都會被完全略過，
包括後續的交易。若管線同步點
發生時有明確交易區塊處於已中止狀態，下一個管線
會立即變成已中止，除非下一個命令以 `ROLLBACK`
將交易恢復為正常模式。

### 注意

用戶端不可在*送出* `COMMIT` 時，
就假定工作已經提交——只有在收到
對應的結果、確認提交已完成時，才能如此假定。
由於錯誤是以非同步方式送達，應用程式需要能夠
在發生問題時，從最後一個*已收到*的已提交變更重新開始，
並重新送出在該點之後所做的工作。

<a id="LIBPQ-PIPELINE-INTERLEAVE"></a>

#### 32.5.1.4. 交錯進行結果處理與查詢送出 [#](#LIBPQ-PIPELINE-INTERLEAVE)

為了避免在大型管線上發生死結，用戶端應該
以非阻塞事件迴圈為核心來架構，並使用作業系統的機制，
例如 `select`、`poll`、
`WaitForMultipleObjectEx` 等。（原文此處寫作 WaitForMultipleObjectEx，Windows API 的正確名稱是 WaitForMultipleObjectsEx。）

用戶端應用程式通常應該維護一個尚待送出之工作的佇列，
以及一個已送出但
結果尚未處理之工作的佇列。當通訊端（socket）可寫入時，
它應該送出更多工作。當通訊端可讀取時，它應該
讀取結果並加以處理，將結果與
對應結果佇列中的下一個項目配對。依可用記憶體而定，
應該經常從通訊端讀取結果：不需要等到
管線結束才讀取結果。管線的範圍應該以邏輯
工作單位來界定，通常（但不一定）是每個管線一個交易。
在管線與管線之間，不需要先退出管線模式再重新進入，
也不需要等一個管線完成之後才送出下一個。

使用 `select()` 與簡單的狀態
機來追蹤已送出與已接收之工作的範例，位於
PostgreSQL 原始碼發行版的
`src/test/modules/libpq_pipeline/libpq_pipeline.c`
中。

<a id="LIBPQ-PIPELINE-FUNCTIONS"></a>

### 32.5.2. 與管線模式相關的函式 [#](#libpq-pipeline-functions) <a href="#libpq-pipeline-functions" id="libpq-pipeline-functions"></a>

<a id="LIBPQ-PQPIPELINESTATUS"></a>

`PQpipelineStatus`<a id="id-1.7.3.12.10.2.1.1.2"></a> [#](#LIBPQ-PQPIPELINESTATUS)

傳回 libpq 連線目前的管線模式狀態。

```

    PGpipelineStatus PQpipelineStatus(const PGconn *conn);
```

`PQpipelineStatus` 可能傳回下列其中一個值：

- `PQ_PIPELINE_ON`

  libpq 連線處於
  管線模式。

- `PQ_PIPELINE_OFF`

  libpq 連線*不*處於管線模式。

- `PQ_PIPELINE_ABORTED`

  libpq 連線處於管線
  模式，且在處理目前的管線時發生了錯誤。
  當 `PQgetResult`
  傳回 `PGRES_PIPELINE_SYNC` 類型的結果時，中止旗標就會被清除。

<a id="LIBPQ-PQENTERPIPELINEMODE"></a>

`PQenterPipelineMode`<a id="id-1.7.3.12.10.2.2.1.2"></a> [#](#LIBPQ-PQENTERPIPELINEMODE)

若連線目前處於閒置狀態或
已處於管線模式，則使連線進入管線模式。

```

    int PQenterPipelineMode(PGconn *conn);
```

成功時傳回 1。
若連線目前並非閒置（也就是已有結果就緒，
或正在等待伺服器傳來更多輸入等），則傳回 0 且不產生任何作用。
此函式實際上不會向伺服器送出任何東西，
它只會變更 libpq 連線的
狀態。

<a id="LIBPQ-PQEXITPIPELINEMODE"></a>

`PQexitPipelineMode`<a id="id-1.7.3.12.10.2.3.1.2"></a> [#](#LIBPQ-PQEXITPIPELINEMODE)

若連線目前處於管線模式，且佇列為空、沒有待處理的結果，
則使連線退出管線模式。

```

    int PQexitPipelineMode(PGconn *conn);
```

成功時傳回 1。若不處於
管線模式，則傳回 1 且不採取任何動作。若目前的陳述式尚未處理完畢，
或尚未呼叫 `PQgetResult` 收集
所有先前已送出之查詢的結果，則傳回 0（此時，
請使用 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage) 取得關於該失敗的
更多資訊）。

<a id="LIBPQ-PQPIPELINESYNC"></a>

`PQpipelineSync`<a id="id-1.7.3.12.10.2.4.1.2"></a> [#](#LIBPQ-PQPIPELINESYNC)

藉由送出
[同步訊息](../../internals/protocol/protocol-flow.md#protocol-flow-ext-query)
並刷寫送出緩衝區，在管線中標記一個同步點。這會作為
隱含交易的分界以及錯誤復原
點；請參閱[第 32.5.1.3 節](libpq-pipeline-mode.md#LIBPQ-PIPELINE-ERRORS)。

```

    int PQpipelineSync(PGconn *conn);
```

成功時傳回 1。若連線不處於
管線模式，或送出
[同步訊息](../../internals/protocol/protocol-flow.md#protocol-flow-ext-query)
失敗，則傳回 0。

<a id="LIBPQ-PQSENDPIPELINESYNC"></a>

`PQsendPipelineSync`<a id="id-1.7.3.12.10.2.5.1.2"></a> [#](#LIBPQ-PQSENDPIPELINESYNC)

藉由送出
[同步訊息](../../internals/protocol/protocol-flow.md#protocol-flow-ext-query)
但不刷寫送出緩衝區，在管線中標記一個同步點。這會作為
隱含交易的分界以及錯誤復原
點；請參閱[第 32.5.1.3 節](libpq-pipeline-mode.md#LIBPQ-PIPELINE-ERRORS)。

```

    int PQsendPipelineSync(PGconn *conn);
```

成功時傳回 1。若連線不處於
管線模式，或送出
[同步訊息](../../internals/protocol/protocol-flow.md#protocol-flow-ext-query)
失敗，則傳回 0。
請注意，該訊息本身不會自動刷寫到伺服器；
必要時請使用 `PQflush`。

<a id="LIBPQ-PQSENDFLUSHREQUEST"></a>

`PQsendFlushRequest`<a id="id-1.7.3.12.10.2.6.1.2"></a> [#](#LIBPQ-PQSENDFLUSHREQUEST)

送出請求，要求伺服器刷寫其輸出緩衝區。

```

    int PQsendFlushRequest(PGconn *conn);
```

成功時傳回 1。發生任何失敗時傳回 0。

伺服器會因為呼叫了
`PQpipelineSync` 而自動刷寫其輸出緩衝區，
在不處於管線模式時，也會針對任何請求自動刷寫；此函式可用來
在管線模式下讓伺服器刷寫其輸出緩衝區，
而不必建立同步點。
請注意，該請求本身不會自動刷寫到伺服器；
必要時請使用 `PQflush`。

<a id="LIBPQ-PIPELINE-TIPS"></a>

### 32.5.3. 何時使用管線模式 [#](#libpq-pipeline-tips) <a href="#libpq-pipeline-tips" id="libpq-pipeline-tips"></a>

與非同步查詢模式非常類似，使用管線模式不會帶來有意義的效能
額外負擔。它會增加用戶端應用程式的複雜度，
而且需要格外小心以避免用戶端與伺服器之間的死結，但
管線模式可以帶來相當可觀的效能提升，代價是
狀態保留較久而增加記憶體用量。

當伺服器距離遙遠，也就是網路延遲
（「ping 時間」）很高時，以及
快速連續執行許多小型操作時，管線模式最為有用。
當每個查詢的執行時間是用戶端／伺服器
往返時間的許多倍時，使用管線化命令的好處通常比較少。
在往返時間為 300 毫秒的伺服器上執行一個包含 100 個陳述式的操作，
若不使用管線，光是網路延遲就要花費 30 秒；
使用管線時，等待伺服器結果的時間可能少至 0.3 秒。

當你的應用程式執行大量小型的
`INSERT`、`UPDATE` 與
`DELETE` 操作，且這些操作無法輕易轉換
為集合操作或 `COPY` 操作時，請使用管線化命令。

當用戶端需要某個操作的資訊才能產生下一個操作時，
管線模式就沒有幫助。在這類情況下，用戶端
必須引入同步點，並等待一次完整的用戶端／伺服器
往返，才能取得所需的結果。不過，通常可以
調整用戶端的設計，改在伺服器端交換所需的資訊。
「讀取—修改—寫入」循環特別適合這樣調整；例如：

```

BEGIN;
SELECT x FROM mytable WHERE id = 42 FOR UPDATE;
-- result: x=2
-- client adds 1 to x:
UPDATE mytable SET x = 3 WHERE id = 42;
COMMIT;
```

可以用下列方式更有效率地完成：

```

UPDATE mytable SET x = x + 1 WHERE id = 42;
```

當單一管線包含
多個交易時，管線化的用處較小，也更複雜（請參閱[第 32.5.1.3 節](libpq-pipeline-mode.md#LIBPQ-PIPELINE-ERRORS)）。

<br>

---

<a id="ftn.id-1.7.3.12.9.3.1.3"></a>

[[15]](#id-1.7.3.12.9.3.1.3) 
用戶端會在嘗試向伺服器送出查詢時阻塞，而
伺服器則會在嘗試將它已處理之查詢的結果送給用戶端時阻塞。
只有當用戶端在切換為處理來自伺服器的輸入之前，
送出足夠多的查詢，填滿它自己的輸出緩衝區以及伺服器的接收
緩衝區時，才會發生這種情況，
但很難準確預測何時會發生。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-pipeline-mode.html)（原文版本：18.6；核對日期：2026-10-18）
