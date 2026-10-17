<a id="LIBPQ-SINGLE-ROW-MODE"></a>

## 32.6. 分塊取得查詢結果 [#](#LIBPQ-SINGLE-ROW-MODE)

<a id="id-1.7.3.13.2"></a><a id="id-1.7.3.13.3"></a>

一般情況下，libpq 會收集 SQL 命令的完整結果，再以單一個
`PGresult` 傳回給應用程式。對於會傳回大量資料列的命令，
這種做法可能行不通。在這類情況下，應用程式可以在
*單列模式*（single-row mode）或*分塊模式*（chunked
mode）下使用
[`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY) 與 [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT)。在這些模式下，結果資料列會在從伺服器接收到時即傳回給
應用程式：單列模式一次傳回一列，分塊模式則成組傳回。

要進入其中一種模式，請在成功呼叫 [`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY)
（或其同系列函式）之後，立即呼叫 [`PQsetSingleRowMode`](libpq-single-row-mode.md#LIBPQ-PQSETSINGLEROWMODE)
或 [`PQsetChunkedRowsMode`](libpq-single-row-mode.md#LIBPQ-PQSETCHUNKEDROWSMODE)。
這項模式選擇只對目前正在執行的查詢有效。接著如
[第 32.4 節](libpq-async.md)所述，重複呼叫 [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT)，
直到它傳回 null 為止。若查詢傳回任何資料列，這些資料列會以一個或多個
`PGresult` 物件傳回；這些物件看起來與一般查詢結果相同，
差別只在於狀態碼：單列模式為
`PGRES_SINGLE_TUPLE`，分塊模式為
`PGRES_TUPLES_CHUNK`，而不是
`PGRES_TUPLES_OK`。每個 `PGRES_SINGLE_TUPLE` 物件中恰好有一個結果資料列，
而 `PGRES_TUPLES_CHUNK` 物件則包含至少一列、
但不超過所指定之每塊資料列數的資料列。
在最後一列之後（若查詢傳回零列，則是立即），會傳回一個狀態為
`PGRES_TUPLES_OK` 的零列物件；這就是不會再有資料列送達的訊號。
（但請注意，仍然必須繼續呼叫
[`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT)，直到它傳回 null 為止。）所有
這些 `PGresult` 物件都會包含與該查詢的一般
`PGresult` 物件相同的資料列描述資料（欄位名稱、型別等）。
每個物件都應該照常以 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 釋放。

使用管線模式時，必須先對管線中的每個查詢啟用單列或分塊模式，
再以 `PQgetResult` 取得該查詢的結果。
詳細資訊請參閱[第 32.5 節](libpq-pipeline-mode.md)。

<a id="LIBPQ-PQSETSINGLEROWMODE"></a>

`PQsetSingleRowMode`<a id="id-1.7.3.13.7.1.1.1.2"></a> [#](#LIBPQ-PQSETSINGLEROWMODE)
:   為目前正在執行的查詢選擇單列模式。

    ```

    int PQsetSingleRowMode(PGconn *conn);
    ```

    此函式只能在
    [`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY) 或其某個同系列函式之後立即呼叫，
    且須在對該連線進行任何其他操作（例如
    [`PQconsumeInput`](libpq-async.md#LIBPQ-PQCONSUMEINPUT) 或
    [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT)）之前。若在正確的時機呼叫，
    此函式會為目前的查詢啟用單列模式並傳回 1。否則模式維持不變，
    函式傳回 0。無論哪種情況，目前的查詢完成後，模式都會恢復為一般模式。
<a id="LIBPQ-PQSETCHUNKEDROWSMODE"></a>

`PQsetChunkedRowsMode`<a id="id-1.7.3.13.7.1.2.1.2"></a> [#](#LIBPQ-PQSETCHUNKEDROWSMODE)
:   為目前正在執行的查詢選擇分塊模式。

    ```

    int PQsetChunkedRowsMode(PGconn *conn, int chunkSize);
    ```

    此函式與
    [`PQsetSingleRowMode`](libpq-single-row-mode.md#LIBPQ-PQSETSINGLEROWMODE) 類似，差別在於它
    指定每個 `PGresult` 最多取得 *`chunkSize`* 列，
    而不一定只有一列。
    此函式只能在
    [`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY) 或其某個同系列函式之後立即呼叫，
    且須在對該連線進行任何其他操作（例如
    [`PQconsumeInput`](libpq-async.md#LIBPQ-PQCONSUMEINPUT) 或
    [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT)）之前。若在正確的時機呼叫，
    此函式會為目前的查詢啟用分塊模式並傳回 1。否則模式維持不變，
    函式傳回 0。無論哪種情況，目前的查詢完成後，模式都會恢復為一般模式。

### 小心

在處理查詢時，伺服器可能先傳回部分資料列，接著遇到錯誤，導致查詢中止。
一般情況下，libpq 會捨棄這些資料列，只回報錯誤。
但在單列或分塊模式下，部分資料列可能已經傳回給應用程式。
因此，應用程式會先看到一些
`PGRES_SINGLE_TUPLE` 或 `PGRES_TUPLES_CHUNK`
`PGresult`
物件，接著是一個 `PGRES_FATAL_ERROR` 物件。
為了確保正確的交易行為，應用程式必須設計成：若查詢最終失敗，
就捨棄或復原先前已處理之資料列所做的一切。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-single-row-mode.html)（原文版本：18.6；核對日期：2026-10-17）
