<a id="LIBPQ-ASYNC"></a>

## 32.4. 非同步命令處理 [#](#libpq-async) <a href="#libpq-async" id="libpq-async"></a>

<a id="id-1.7.3.11.2"></a>

[`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 函式足以在一般的同步應用程式中
送出命令。然而它有一些不足之處，對某些使用者而言可能很重要：

* [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 會等待命令完成。
  應用程式可能還有其他工作要做（例如維護使用者介面），
  在這種情況下，它不會想要阻塞以等待回應。
* 由於用戶端應用程式在等待結果時會暫停執行，
  應用程式很難決定要嘗試取消正在進行的命令。
  （這可以從訊號處理常式中做到，但無法以其他方式做到。）
* [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 只能傳回一個
  `PGresult` 結構。若送出的命令字串
  包含多個 SQL 命令，除了最後一個
  `PGresult` 之外，其餘都會被
  [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 捨棄。
* [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 一律會收集命令的完整結果，
  並將其緩衝在單一的 `PGresult` 中。雖然
  這簡化了應用程式的錯誤處理邏輯，但對於包含大量資料列的結果
  可能不切實際。

不喜歡這些限制的應用程式，可以改用建構
[`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 的底層函式：
[`PQsendQuery`](libpq-async.md#libpq-pqsendquery) 與 [`PQgetResult`](libpq-async.md#libpq-pqgetresult)。
另外還有
[`PQsendQueryParams`](libpq-async.md#libpq-pqsendqueryparams)、
[`PQsendPrepare`](libpq-async.md#libpq-pqsendprepare)、
[`PQsendQueryPrepared`](libpq-async.md#libpq-pqsendqueryprepared)、
[`PQsendDescribePrepared`](libpq-async.md#libpq-pqsenddescribeprepared)、
[`PQsendDescribePortal`](libpq-async.md#libpq-pqsenddescribeportal)、
[`PQsendClosePrepared`](libpq-async.md#libpq-pqsendcloseprepared) 與
[`PQsendClosePortal`](libpq-async.md#libpq-pqsendcloseportal)，
它們可以搭配 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 使用，分別重現
[`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS)、
[`PQprepare`](libpq-exec.md#LIBPQ-PQPREPARE)、
[`PQexecPrepared`](libpq-exec.md#LIBPQ-PQEXECPREPARED)、
[`PQdescribePrepared`](libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED)、
[`PQdescribePortal`](libpq-exec.md#LIBPQ-PQDESCRIBEPORTAL)、
[`PQclosePrepared`](libpq-exec.md#LIBPQ-PQCLOSEPREPARED) 與
[`PQclosePortal`](libpq-exec.md#LIBPQ-PQCLOSEPORTAL)
的功能。

<a id="LIBPQ-PQSENDQUERY"></a>

### `PQsendQuery`<a id="id-1.7.3.11.4.19.1.1.2"></a> [#](#libpq-pqsendquery) <a href="#libpq-pqsendquery" id="libpq-pqsendquery"></a>

將命令送給伺服器，而不等待結果。
若命令成功送出則傳回 1，否則傳回 0
（在此情況下，請使用 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage) 取得
關於失敗的更多資訊）。

```

    int PQsendQuery(PGconn *conn, const char *command);
```

成功呼叫 [`PQsendQuery`](libpq-async.md#libpq-pqsendquery) 之後，請呼叫
[`PQgetResult`](libpq-async.md#libpq-pqgetresult) 一次或多次以取得
結果。在 [`PQgetResult`](libpq-async.md#libpq-pqgetresult)
傳回空指標（表示命令已完成）之前，不能（在同一個連線上）再次呼叫
[`PQsendQuery`](libpq-async.md#libpq-pqsendquery)。

在管線模式下，不允許使用此函式。

<a id="LIBPQ-PQSENDQUERYPARAMS"></a>

### `PQsendQueryParams`<a id="id-1.7.3.11.4.19.2.1.2"></a> [#](#libpq-pqsendqueryparams) <a href="#libpq-pqsendqueryparams" id="libpq-pqsendqueryparams"></a>

將命令與分開的參數送給伺服器，而不
等待結果。

```

    int PQsendQueryParams(PGconn *conn,
                          const char *command,
                          int nParams,
                          const Oid *paramTypes,
                          const char * const *paramValues,
                          const int *paramLengths,
                          const int *paramFormats,
                          int resultFormat);
```

此函式等同於 [`PQsendQuery`](libpq-async.md#libpq-pqsendquery)，差別在於
查詢參數可以與查詢字串分開指定。
此函式的參數處理方式與
[`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS) 完全相同。與
[`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS) 一樣，它只允許查詢字串中有
一個命令。

<a id="LIBPQ-PQSENDPREPARE"></a>

### `PQsendPrepare`<a id="id-1.7.3.11.4.19.3.1.2"></a> [#](#libpq-pqsendprepare) <a href="#libpq-pqsendprepare" id="libpq-pqsendprepare"></a>

送出以給定參數建立預備陳述式的請求，
而不等待完成。

```

    int PQsendPrepare(PGconn *conn,
                      const char *stmtName,
                      const char *query,
                      int nParams,
                      const Oid *paramTypes);
```

這是 [`PQprepare`](libpq-exec.md#LIBPQ-PQPREPARE) 的非同步版本：
若能送出請求則傳回 1，否則傳回 0。
呼叫成功後，請呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 來
判斷伺服器是否已成功建立預備陳述式。
此函式的參數處理方式與
[`PQprepare`](libpq-exec.md#LIBPQ-PQPREPARE) 完全相同。

<a id="LIBPQ-PQSENDQUERYPREPARED"></a>

### `PQsendQueryPrepared`<a id="id-1.7.3.11.4.19.4.1.2"></a> [#](#libpq-pqsendqueryprepared) <a href="#libpq-pqsendqueryprepared" id="libpq-pqsendqueryprepared"></a>

送出以給定參數執行預備陳述式的請求，
而不等待結果。

```

    int PQsendQueryPrepared(PGconn *conn,
                            const char *stmtName,
                            int nParams,
                            const char * const *paramValues,
                            const int *paramLengths,
                            const int *paramFormats,
                            int resultFormat);
```

此函式類似於 [`PQsendQueryParams`](libpq-async.md#libpq-pqsendqueryparams)，但
要執行的命令是以指名先前已預備的陳述式來指定，
而非給出查詢字串。
此函式的參數處理方式與
[`PQexecPrepared`](libpq-exec.md#LIBPQ-PQEXECPREPARED) 完全相同。

<a id="LIBPQ-PQSENDDESCRIBEPREPARED"></a>

### `PQsendDescribePrepared`<a id="id-1.7.3.11.4.19.5.1.2"></a> [#](#libpq-pqsenddescribeprepared) <a href="#libpq-pqsenddescribeprepared" id="libpq-pqsenddescribeprepared"></a>

送出取得指定預備陳述式相關資訊的請求，
而不等待完成。

```

    int PQsendDescribePrepared(PGconn *conn, const char *stmtName);
```

這是 [`PQdescribePrepared`](libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED) 的非同步版本：
若能送出請求則傳回 1，否則傳回 0。
呼叫成功後，請呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 來
取得結果。此函式的參數處理方式與
[`PQdescribePrepared`](libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED) 完全相同。

<a id="LIBPQ-PQSENDDESCRIBEPORTAL"></a>

### `PQsendDescribePortal`<a id="id-1.7.3.11.4.19.6.1.2"></a> [#](#libpq-pqsenddescribeportal) <a href="#libpq-pqsenddescribeportal" id="libpq-pqsenddescribeportal"></a>

送出取得指定 portal 相關資訊的請求，
而不等待完成。

```

    int PQsendDescribePortal(PGconn *conn, const char *portalName);
```

這是 [`PQdescribePortal`](libpq-exec.md#LIBPQ-PQDESCRIBEPORTAL) 的非同步版本：
若能送出請求則傳回 1，否則傳回 0。
呼叫成功後，請呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 來
取得結果。此函式的參數處理方式與
[`PQdescribePortal`](libpq-exec.md#LIBPQ-PQDESCRIBEPORTAL) 完全相同。

<a id="LIBPQ-PQSENDCLOSEPREPARED"></a>

### `PQsendClosePrepared`<a id="id-1.7.3.11.4.19.7.1.2"></a> [#](#libpq-pqsendcloseprepared) <a href="#libpq-pqsendcloseprepared" id="libpq-pqsendcloseprepared"></a>

送出關閉指定預備陳述式的請求，而不
等待完成。

```

    int PQsendClosePrepared(PGconn *conn, const char *stmtName);
```

這是 [`PQclosePrepared`](libpq-exec.md#LIBPQ-PQCLOSEPREPARED) 的非同步版本：
若能送出請求則傳回 1，否則傳回 0。
呼叫成功後，請呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 來
取得結果。此函式的參數處理方式與
[`PQclosePrepared`](libpq-exec.md#LIBPQ-PQCLOSEPREPARED) 完全相同。

<a id="LIBPQ-PQSENDCLOSEPORTAL"></a>

### `PQsendClosePortal`<a id="id-1.7.3.11.4.19.8.1.2"></a> [#](#libpq-pqsendcloseportal) <a href="#libpq-pqsendcloseportal" id="libpq-pqsendcloseportal"></a>

送出關閉指定 portal 的請求，而不等待
完成。

```

    int PQsendClosePortal(PGconn *conn, const char *portalName);
```

這是 [`PQclosePortal`](libpq-exec.md#LIBPQ-PQCLOSEPORTAL) 的非同步版本：
若能送出請求則傳回 1，否則傳回 0。
呼叫成功後，請呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 來
取得結果。此函式的參數處理方式與
[`PQclosePortal`](libpq-exec.md#LIBPQ-PQCLOSEPORTAL) 完全相同。

<a id="LIBPQ-PQGETRESULT"></a>

### `PQgetResult`<a id="id-1.7.3.11.4.19.9.1.2"></a> [#](#libpq-pqgetresult) <a href="#libpq-pqgetresult" id="libpq-pqgetresult"></a>

等待先前一次
[`PQsendQuery`](libpq-async.md#libpq-pqsendquery)、
[`PQsendQueryParams`](libpq-async.md#libpq-pqsendqueryparams)、
[`PQsendPrepare`](libpq-async.md#libpq-pqsendprepare)、
[`PQsendQueryPrepared`](libpq-async.md#libpq-pqsendqueryprepared)、
[`PQsendDescribePrepared`](libpq-async.md#libpq-pqsenddescribeprepared)、
[`PQsendDescribePortal`](libpq-async.md#libpq-pqsenddescribeportal)、
[`PQsendClosePrepared`](libpq-async.md#libpq-pqsendcloseprepared)、
[`PQsendClosePortal`](libpq-async.md#libpq-pqsendcloseportal)、
[`PQsendPipelineSync`](libpq-pipeline-mode.md#LIBPQ-PQSENDPIPELINESYNC) 或
[`PQpipelineSync`](libpq-pipeline-mode.md#LIBPQ-PQPIPELINESYNC)
呼叫的下一個結果，並將其傳回。
當命令已完成且不會再有更多結果時，會傳回空指標。

```

    PGresult *PQgetResult(PGconn *conn);
```

必須重複呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult)，直到
它傳回空指標為止，這表示命令已完成。
（若在沒有作用中命令時呼叫，
[`PQgetResult`](libpq-async.md#libpq-pqgetresult) 只會立即傳回空指標。）
來自 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 的每個非空結果，
都應該使用先前說明過的同一組 `PGresult` 存取函式
來處理。別忘了在處理完每個結果物件後，以
[`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 將其釋放。請注意，
只有在有作用中的命令，且所需的回應資料尚未被
[`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput) 讀取時，
[`PQgetResult`](libpq-async.md#libpq-pqgetresult) 才會阻塞。

在管線模式下，除非發生錯誤，否則 `PQgetResult` 會正常
傳回；對於在導致錯誤的查詢之後、直到下一個同步點（不含）
之前所送出的任何後續查詢，都會傳回型別為
`PGRES_PIPELINE_ABORTED` 的特殊結果，
並在其後傳回空指標。
到達管線同步點時，會傳回型別為
`PGRES_PIPELINE_SYNC` 的結果。
同步點之後下一個查詢的結果會緊接著出現
（也就是說，同步點之後不會傳回空指標）。

#### 注意

即使 [`PQresultStatus`](libpq-exec.md#LIBPQ-PQRESULTSTATUS) 指出發生致命
錯誤，仍應呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult)，直到它
傳回空指標為止，好讓 libpq
能完整處理錯誤資訊。

使用 [`PQsendQuery`](libpq-async.md#libpq-pqsendquery) 與
[`PQgetResult`](libpq-async.md#libpq-pqgetresult) 可以解決
[`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 的其中一個問題：若命令字串包含
多個 SQL 命令，可以個別取得這些命令的結果。
（順帶一提，這也提供了一種簡單形式的重疊處理：
用戶端可以在處理某個命令的結果時，
伺服器仍在處理同一命令字串中後續的查詢。）

另一個經常被需要、也可以透過
[`PQsendQuery`](libpq-async.md#libpq-pqsendquery) 與 [`PQgetResult`](libpq-async.md#libpq-pqgetresult)
取得的功能，是一次取回有限數量的資料列，以擷取大型查詢結果。
這會在[第 32.6 節](libpq-single-row-mode.md)中討論。

單獨呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult)
仍然會使用戶端阻塞，直到伺服器完成
下一個 SQL 命令為止。只要適當使用另外兩個函式，
就可以避免這種情況：

<a id="LIBPQ-PQCONSUMEINPUT"></a>

### `PQconsumeInput`<a id="id-1.7.3.11.7.3.1.1.2"></a> [#](#libpq-pqconsumeinput) <a href="#libpq-pqconsumeinput" id="libpq-pqconsumeinput"></a>

若有來自伺服器的輸入可用，則將其讀入。

```

    int PQconsumeInput(PGconn *conn);
```

[`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput) 通常會傳回 1，表示
「沒有錯誤」，但若發生某種問題則傳回 0
（在此情況下，可以查閱 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage)）。
請注意，此結果並不表示是否實際收集到任何輸入
資料。呼叫
[`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput) 之後，應用程式可以檢查
[`PQisBusy`](libpq-async.md#libpq-pqisbusy) 和／或
`PQnotifies`，看看它們的狀態是否已改變。

即使應用程式尚未準備好處理結果或通知，
也可以呼叫 [`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput)。
此函式會讀取可用的資料並將其存入
緩衝區，從而使 `select()`
的可讀取指示消失。因此，應用程式可以使用
[`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput) 立即清除
`select()` 狀況，然後
再從容地檢查結果。

<a id="LIBPQ-PQISBUSY"></a>

### `PQisBusy`<a id="id-1.7.3.11.7.3.2.1.2"></a> [#](#libpq-pqisbusy) <a href="#libpq-pqisbusy" id="libpq-pqisbusy"></a>

若命令忙碌中，亦即
[`PQgetResult`](libpq-async.md#libpq-pqgetresult) 會阻塞以等待輸入，則傳回 1。
傳回 0 表示可以呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult)，
並確定不會阻塞。

```

    int PQisBusy(PGconn *conn);
```

[`PQisBusy`](libpq-async.md#libpq-pqisbusy) 本身不會嘗試從伺服器讀取
資料；因此必須先呼叫 [`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput)，
否則忙碌狀態永遠不會結束。

使用這些函式的典型應用程式會有一個主迴圈，
使用 `select()` 或 `poll()` 等待
它必須回應的所有狀況。其中一個狀況
是來自伺服器的輸入可用，以
`select()` 而言，這表示由
[`PQsocket`](libpq-status.md#libpq-pqsocket) 所識別的檔案描述子上有可讀取的資料。
當主迴圈偵測到輸入已就緒時，它應該呼叫
[`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput) 讀取輸入。接著它可以
呼叫 [`PQisBusy`](libpq-async.md#libpq-pqisbusy)，若 [`PQisBusy`](libpq-async.md#libpq-pqisbusy)
傳回 false（0），再接著呼叫
[`PQgetResult`](libpq-async.md#libpq-pqgetresult)。它也可以呼叫 `PQnotifies`
來偵測 `NOTIFY` 訊息（請參閱[第 32.9 節](libpq-notify.md)）。

使用
[`PQsendQuery`](libpq-async.md#libpq-pqsendquery)/[`PQgetResult`](libpq-async.md#libpq-pqgetresult)
的用戶端，也可以嘗試取消伺服器仍在處理中的
命令；請參閱[第 32.7 節](libpq-cancel.md)。但無論
[`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) 的傳回值為何，應用程式
都必須繼續使用 [`PQgetResult`](libpq-async.md#libpq-pqgetresult)
進行一般的結果讀取流程。成功的取消
只會使命令比原本更早結束。

藉由使用上述函式，可以避免在等待資料庫伺服器的輸入時
阻塞。然而，
應用程式仍然有可能在等待將輸出送給伺服器時阻塞。
這種情況相對少見，但在送出
非常長的 SQL 命令或資料值時可能發生。（不過，若應用程式透過
`COPY IN` 送出資料，發生的可能性就高得多。）
為了避免這種可能性並達成完全
非阻塞的資料庫操作，可以使用下列額外的函式。

<a id="LIBPQ-PQSETNONBLOCKING"></a>

### `PQsetnonblocking`<a id="id-1.7.3.11.10.2.1.1.2"></a> [#](#libpq-pqsetnonblocking) <a href="#libpq-pqsetnonblocking" id="libpq-pqsetnonblocking"></a>

設定連線的非阻塞狀態。

```

    int PQsetnonblocking(PGconn *conn, int arg);
```

若 *`arg`* 為 1，則將連線狀態設為非阻塞；若
*`arg`* 為 0，則設為阻塞。成功時傳回 0，發生錯誤時傳回 -1。

在非阻塞狀態下，成功呼叫
[`PQsendQuery`](libpq-async.md#libpq-pqsendquery)、[`PQputline`](libpq-copy.md#LIBPQ-PQPUTLINE)、
[`PQputnbytes`](libpq-copy.md#LIBPQ-PQPUTNBYTES)、[`PQputCopyData`](libpq-copy.md#LIBPQ-PQPUTCOPYDATA)
與 [`PQendcopy`](libpq-copy.md#LIBPQ-PQENDCOPY) 都不會阻塞；它們的變更
會儲存在本機輸出緩衝區中，直到被刷寫出去為止。
不成功的呼叫會傳回錯誤，且必須重試。

請注意，[`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 不遵循非阻塞
模式；若呼叫它，它無論如何都會以阻塞方式運作。

<a id="LIBPQ-PQISNONBLOCKING"></a>

### `PQisnonblocking`<a id="id-1.7.3.11.10.2.2.1.2"></a> [#](#libpq-pqisnonblocking) <a href="#libpq-pqisnonblocking" id="libpq-pqisnonblocking"></a>

傳回資料庫連線的阻塞狀態。

```

    int PQisnonblocking(const PGconn *conn);
```

若連線設為非阻塞模式則傳回 1，若為
阻塞模式則傳回 0。

<a id="LIBPQ-PQFLUSH"></a>

### `PQflush`<a id="id-1.7.3.11.10.2.3.1.2"></a> [#](#libpq-pqflush) <a href="#libpq-pqflush" id="libpq-pqflush"></a>

嘗試將任何已排入佇列的輸出資料刷寫到伺服器。成功時
（或傳送佇列為空時）傳回 0；因某種原因失敗時傳回 -1；
若尚無法送出傳送佇列中的所有資料，則傳回 1
（這種情況只會在連線為非阻塞時發生）。

```

    int PQflush(PGconn *conn);
```

在非阻塞連線上送出任何命令或資料之後，請呼叫
[`PQflush`](libpq-async.md#libpq-pqflush)。若它傳回 1，請等待通訊端
變為可讀取或可寫入。若它變為可寫入，請再次呼叫
[`PQflush`](libpq-async.md#libpq-pqflush)。若它變為可讀取，請先呼叫
[`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput)，再呼叫
[`PQflush`](libpq-async.md#libpq-pqflush)。重複此步驟，直到
[`PQflush`](libpq-async.md#libpq-pqflush) 傳回 0 為止。（之所以必須檢查
是否可讀取，並以 [`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput) 排空輸入，
是因為伺服器可能會在嘗試傳送資料給我們（例如 NOTICE
訊息）時阻塞，並且在我們讀取它的資料之前，不會讀取我們的資料。）一旦
[`PQflush`](libpq-async.md#libpq-pqflush) 傳回 0，請等待通訊端變為
可讀取，然後依上述方式讀取回應。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-async.html)（原文版本：18.6；核對日期：2026-10-18）
