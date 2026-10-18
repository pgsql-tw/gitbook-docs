<a id="LIBPQ-EXEC"></a>

## 32.3. 命令執行函式 [#](#LIBPQ-EXEC)

[32.3.1. 主要函式](libpq-exec.md#LIBPQ-EXEC-MAIN)

[32.3.2. 取得查詢結果資訊](libpq-exec.md#LIBPQ-EXEC-SELECT-INFO)

[32.3.3. 取得其他結果資訊](libpq-exec.md#LIBPQ-EXEC-NONSELECT)

[32.3.4. 跳脫要放入 SQL 命令的字串](libpq-exec.md#LIBPQ-EXEC-ESCAPE-STRING)

成功建立與資料庫伺服器的連線之後，就可以使用這裡所述的函式來執行 SQL 查詢與命令。

<a id="LIBPQ-EXEC-MAIN"></a>

### 32.3.1. 主要函式 [#](#LIBPQ-EXEC-MAIN)

<a id="LIBPQ-PQEXEC"></a>

`PQexec`<a id="id-1.7.3.10.3.2.1.1.1.2"></a> [#](#LIBPQ-PQEXEC)
:   將命令送交伺服器並等待結果。

    ```

    PGresult *PQexec(PGconn *conn, const char *command);
    ```

    傳回 `PGresult` 指標，也可能傳回空指標。除了記憶體不足，或是無法將命令送到伺服器之類的嚴重錯誤之外，通常會傳回非空指標。應該呼叫 [`PQresultStatus`](libpq-exec.md#LIBPQ-PQRESULTSTATUS) 函式來檢查傳回值是否有任何錯誤（包括空指標的情況，此時它會傳回 `PGRES_FATAL_ERROR`）。請使用 [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) 取得這類錯誤的更多資訊。

命令字串可以包含多個 SQL 命令（以分號分隔）。在單一次 [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 呼叫中送出的多個查詢會在單一交易中處理，除非查詢字串中含有明確的 `BEGIN`/`COMMIT` 命令，將它分成多個交易。（關於伺服器如何處理多重查詢字串的更多細節，請參閱[第 54.2.2.1 節](../../internals/protocol/protocol-flow.md#PROTOCOL-FLOW-MULTI-STATEMENT)。）但請注意，傳回的 `PGresult` 結構只描述字串中最後執行的那個命令的結果。若其中某個命令失敗，字串的處理就會在該命令停止，而傳回的 `PGresult` 會描述該錯誤狀況。

<a id="LIBPQ-PQEXECPARAMS"></a>

`PQexecParams`<a id="id-1.7.3.10.3.3.1.1.1.2"></a> [#](#LIBPQ-PQEXECPARAMS)
:   將命令送交伺服器並等待結果，且能夠將參數與 SQL 命令文字分開傳遞。

    ```

    PGresult *PQexecParams(PGconn *conn,
                           const char *command,
                           int nParams,
                           const Oid *paramTypes,
                           const char * const *paramValues,
                           const int *paramLengths,
                           const int *paramFormats,
                           int resultFormat);
    ```

    [`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS) 與 [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 類似，但提供額外的功能：參數值可以與命令字串本身分開指定，而且可以要求以文字或二進位格式傳回查詢結果。

    函式的引數如下：

    *`conn`*
    :   用來傳送命令的連線物件。

    *`command`*
    :   要執行的 SQL 命令字串。若使用參數，在命令字串中以 `$1`、`$2` 等方式參照它們。

    *`nParams`*
    :   所提供的參數個數；它是陣列 *`paramTypes[]`*、*`paramValues[]`*、*`paramLengths[]`* 與 *`paramFormats[]`* 的長度。（當 *`nParams`* 為零時，這些陣列指標可以是 `NULL`。）

    *`paramTypes[]`*
    :   以 OID 指定要指派給各參數符號的資料型別。若 *`paramTypes`* 為 `NULL`，或陣列中的某個元素為零，伺服器會以處理無型別字面字串的相同方式，為該參數符號推斷資料型別。

    *`paramValues[]`*
    :   指定參數的實際值。此陣列中的空指標表示對應的參數為 null；否則該指標指向以零結尾的文字字串（文字格式），或是伺服器所預期格式的二進位資料（二進位格式）。

    *`paramLengths[]`*
    :   指定二進位格式參數的實際資料長度。對於 null 參數與文字格式參數，此值會被忽略。沒有二進位參數時，此陣列指標可以是空指標。

    *`paramFormats[]`*
    :   指定各參數為文字（在對應參數的陣列元素中放 0）或二進位（在對應參數的陣列元素中放 1）。若陣列指標為空指標，則所有參數都假定為文字字串。

        以二進位格式傳遞的值，需要了解後端所預期的內部表示法。例如，整數必須以網路位元組順序傳遞。傳遞 `numeric` 值則需要了解伺服器的儲存格式，其實作位於 `src/backend/utils/adt/numeric.c::numeric_send()` 與 `src/backend/utils/adt/numeric.c::numeric_recv()`。

    *`resultFormat`*
    :   指定 0 以取得文字格式的結果，或指定 1 以取得二進位格式的結果。（目前沒有提供以不同格式取得不同結果欄位的機制，雖然底層協定可以做到。）

[`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS) 相較於 [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 的主要優點是參數值可以與命令字串分開，因此不需要繁瑣又容易出錯的引號處理與跳脫。

與 [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 不同，[`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS) 在給定的字串中最多只允許一個 SQL 命令。（字串中可以有分號，但非空命令不可超過一個。）這是底層協定的限制，但作為防範 SQL 注入攻擊的額外防線也有些用處。

### 提示

以 OID 指定參數型別相當繁瑣，尤其是如果你不想把特定的 OID 值寫死在程式中。不過，即使伺服器本身無法判斷參數的型別，或選擇了與你所要不同的型別，你仍然可以避免這麼做。在 SQL 命令文字中，為參數符號加上明確的型別轉換，以表明你將傳送的資料型別。例如：

```

SELECT * FROM mytable WHERE x = $1::bigint;
```

這會強制將參數 `$1` 視為 `bigint`，而在預設情況下，它會被指派為與 `x` 相同的型別。以二進位格式傳送參數值時，強烈建議以這種方式或以數字指定型別 OID 的方式強制決定參數型別，因為二進位格式的冗餘比文字格式少，伺服器替你偵測出型別不符錯誤的機會也就比較小。

<a id="LIBPQ-PQPREPARE"></a>

`PQprepare`<a id="id-1.7.3.10.3.7.1.1.1.2"></a> [#](#LIBPQ-PQPREPARE)
:   送出以給定參數建立預備陳述式的請求，並等待其完成。

    ```

    PGresult *PQprepare(PGconn *conn,
                        const char *stmtName,
                        const char *query,
                        int nParams,
                        const Oid *paramTypes);
    ```

    [`PQprepare`](libpq-exec.md#LIBPQ-PQPREPARE) 會建立一個預備陳述式，供稍後以 [`PQexecPrepared`](libpq-exec.md#LIBPQ-PQEXECPREPARED) 執行。此功能讓命令可以重複執行，而不必每次都經過剖析與規劃；詳情請參閱 [PREPARE](../../reference/sql-commands/sql-prepare.md)。

    此函式會從 *`query`* 字串建立名為 *`stmtName`* 的預備陳述式，該字串必須只包含單一 SQL 命令。*`stmtName`* 可以是 `""`，以建立未命名陳述式，此時任何既有的未命名陳述式都會被自動取代；否則，若該陳述式名稱已在目前工作階段中定義，就會發生錯誤。若使用任何參數，在查詢中以 `$1`、`$2` 等方式參照它們。*`nParams`* 是在陣列 *`paramTypes[]`* 中預先指定型別的參數個數。（當 *`nParams`* 為零時，此陣列指標可以是 `NULL`。）*`paramTypes[]`* 以 OID 指定要指派給各參數符號的資料型別。若 *`paramTypes`* 為 `NULL`，或陣列中的某個元素為零，伺服器會以處理無型別字面字串的相同方式，為該參數符號指派資料型別。此外，查詢中也可以使用編號大於 *`nParams`* 的參數符號；這些符號的資料型別同樣會被推斷出來。（要查出推斷出的資料型別，請參閱 [`PQdescribePrepared`](libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED)。）

    與 [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 相同，結果通常是一個 `PGresult` 物件，其內容表示伺服器端的成功或失敗。空結果表示記憶體不足，或完全無法傳送命令。請使用 [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) 取得這類錯誤的更多資訊。

供 [`PQexecPrepared`](libpq-exec.md#LIBPQ-PQEXECPREPARED) 使用的預備陳述式，也可以透過執行 SQL [PREPARE](../../reference/sql-commands/sql-prepare.md) 陳述式來建立。

<a id="LIBPQ-PQEXECPREPARED"></a>

`PQexecPrepared`<a id="id-1.7.3.10.3.8.1.1.1.2"></a> [#](#LIBPQ-PQEXECPREPARED)
:   送出以給定參數執行預備陳述式的請求，並等待結果。

    ```

    PGresult *PQexecPrepared(PGconn *conn,
                             const char *stmtName,
                             int nParams,
                             const char * const *paramValues,
                             const int *paramLengths,
                             const int *paramFormats,
                             int resultFormat);
    ```

    [`PQexecPrepared`](libpq-exec.md#LIBPQ-PQEXECPREPARED) 與 [`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS) 類似，但要執行的命令是以指名先前已準備好的陳述式來指定，而不是給定查詢字串。此功能讓要重複使用的命令只需剖析與規劃一次，而不必在每次執行時都進行。該陳述式必須已在目前工作階段中事先準備好。

    參數與 [`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS) 相同，差別在於給定的是預備陳述式的名稱而不是查詢字串，而且沒有 *`paramTypes[]`* 參數（不需要它，因為預備陳述式的參數型別在建立時就已決定）。
<a id="LIBPQ-PQDESCRIBEPREPARED"></a>

`PQdescribePrepared`<a id="id-1.7.3.10.3.8.1.2.1.2"></a> [#](#LIBPQ-PQDESCRIBEPREPARED)
:   送出取得指定預備陳述式相關資訊的請求，並等待其完成。

    ```

    PGresult *PQdescribePrepared(PGconn *conn, const char *stmtName);
    ```

    [`PQdescribePrepared`](libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED) 讓應用程式取得先前預備陳述式的相關資訊。

    *`stmtName`* 可以是 `""` 或 `NULL`，以參照未命名陳述式，否則必須是既有預備陳述式的名稱。成功時會傳回狀態為 `PGRES_COMMAND_OK` 的 `PGresult`。可以對此 `PGresult` 套用函式 [`PQnparams`](libpq-exec.md#LIBPQ-PQNPARAMS) 與 [`PQparamtype`](libpq-exec.md#LIBPQ-PQPARAMTYPE) 來取得預備陳述式參數的相關資訊，而函式 [`PQnfields`](libpq-exec.md#LIBPQ-PQNFIELDS)、[`PQfname`](libpq-exec.md#LIBPQ-PQFNAME)、[`PQftype`](libpq-exec.md#LIBPQ-PQFTYPE) 等則提供該陳述式結果欄位（若有的話）的相關資訊。
<a id="LIBPQ-PQDESCRIBEPORTAL"></a>

`PQdescribePortal`<a id="id-1.7.3.10.3.8.1.3.1.2"></a> [#](#LIBPQ-PQDESCRIBEPORTAL)
:   送出取得指定 portal 相關資訊的請求，並等待其完成。

    ```

    PGresult *PQdescribePortal(PGconn *conn, const char *portalName);
    ```

    [`PQdescribePortal`](libpq-exec.md#LIBPQ-PQDESCRIBEPORTAL) 讓應用程式取得先前建立的 portal 的相關資訊。（libpq 並未提供任何直接存取 portal 的方式，但你可以使用此函式檢視以 `DECLARE CURSOR` SQL 命令建立的游標的屬性。）

    *`portalName`* 可以是 `""` 或 `NULL`，以參照未命名 portal，否則必須是既有 portal 的名稱。成功時會傳回狀態為 `PGRES_COMMAND_OK` 的 `PGresult`。可以對此 `PGresult` 套用函式 [`PQnfields`](libpq-exec.md#LIBPQ-PQNFIELDS)、[`PQfname`](libpq-exec.md#LIBPQ-PQFNAME)、[`PQftype`](libpq-exec.md#LIBPQ-PQFTYPE) 等，以取得該 portal 結果欄位（若有的話）的相關資訊。
<a id="LIBPQ-PQCLOSEPREPARED"></a>

`PQclosePrepared`<a id="id-1.7.3.10.3.8.1.4.1.2"></a> [#](#LIBPQ-PQCLOSEPREPARED)
:   送出關閉指定預備陳述式的請求，並等待其完成。

    ```

    PGresult *PQclosePrepared(PGconn *conn, const char *stmtName);
    ```

    [`PQclosePrepared`](libpq-exec.md#LIBPQ-PQCLOSEPREPARED) 讓應用程式關閉先前預備的陳述式。關閉陳述式會釋放它在伺服器上的所有相關資源，並讓它的名稱可以再次使用。

    *`stmtName`* 可以是 `""` 或 `NULL`，以參照未命名陳述式。即使不存在此名稱的陳述式也沒有關係，此時該操作不做任何事。成功時會傳回狀態為 `PGRES_COMMAND_OK` 的 `PGresult`。
<a id="LIBPQ-PQCLOSEPORTAL"></a>

`PQclosePortal`<a id="id-1.7.3.10.3.8.1.5.1.2"></a> [#](#LIBPQ-PQCLOSEPORTAL)
:   送出關閉指定 portal 的請求，並等待其完成。

    ```

    PGresult *PQclosePortal(PGconn *conn, const char *portalName);
    ```

    [`PQclosePortal`](libpq-exec.md#LIBPQ-PQCLOSEPORTAL) 讓應用程式觸發關閉先前建立的 portal。關閉 portal 會釋放它在伺服器上的所有相關資源，並讓它的名稱可以再次使用。（libpq 並未提供任何直接存取 portal 的方式，但你可以使用此函式關閉以 `DECLARE CURSOR` SQL 命令建立的游標。）

    *`portalName`* 可以是 `""` 或 `NULL`，以參照未命名 portal。即使不存在此名稱的 portal 也沒有關係，此時該操作不做任何事。成功時會傳回狀態為 `PGRES_COMMAND_OK` 的 `PGresult`。

`PGresult`<a id="id-1.7.3.10.3.9.2"></a> 結構封裝了伺服器傳回的結果。libpq 應用程式的程式設計者應該小心維持 `PGresult` 的抽象性。請使用下列存取函式來取得 `PGresult` 的內容。避免直接參照 `PGresult` 結構的欄位，因為這些欄位未來可能會變更。

<a id="LIBPQ-PQRESULTSTATUS"></a>

`PQresultStatus`<a id="id-1.7.3.10.3.9.7.1.1.2"></a> [#](#LIBPQ-PQRESULTSTATUS)
:   傳回命令的結果狀態。

    ```

    ExecStatusType PQresultStatus(const PGresult *res);
    ```

    [`PQresultStatus`](libpq-exec.md#LIBPQ-PQRESULTSTATUS) 可能傳回下列其中一個值：

    <a id="LIBPQ-PGRES-EMPTY-QUERY"></a>

    `PGRES_EMPTY_QUERY` [#](#LIBPQ-PGRES-EMPTY-QUERY)
    :   送到伺服器的字串是空的。
    <a id="LIBPQ-PGRES-COMMAND-OK"></a>

    `PGRES_COMMAND_OK` [#](#LIBPQ-PGRES-COMMAND-OK)
    :   不傳回資料的命令已成功完成。
    <a id="LIBPQ-PGRES-TUPLES-OK"></a>

    `PGRES_TUPLES_OK` [#](#LIBPQ-PGRES-TUPLES-OK)
    :   傳回資料的命令（例如 `SELECT` 或 `SHOW`）已成功完成。
    <a id="LIBPQ-PGRES-COPY-OUT"></a>

    `PGRES_COPY_OUT` [#](#LIBPQ-PGRES-COPY-OUT)
    :   已開始 Copy Out（自伺服器）資料傳輸。
    <a id="LIBPQ-PGRES-COPY-IN"></a>

    `PGRES_COPY_IN` [#](#LIBPQ-PGRES-COPY-IN)
    :   已開始 Copy In（往伺服器）資料傳輸。
    <a id="LIBPQ-PGRES-BAD-RESPONSE"></a>

    `PGRES_BAD_RESPONSE` [#](#LIBPQ-PGRES-BAD-RESPONSE)
    :   無法理解伺服器的回應。
    <a id="LIBPQ-PGRES-NONFATAL-ERROR"></a>

    `PGRES_NONFATAL_ERROR` [#](#LIBPQ-PGRES-NONFATAL-ERROR)
    :   發生非致命錯誤（通知訊息或警告）。
    <a id="LIBPQ-PGRES-FATAL-ERROR"></a>

    `PGRES_FATAL_ERROR` [#](#LIBPQ-PGRES-FATAL-ERROR)
    :   發生致命錯誤。
    <a id="LIBPQ-PGRES-COPY-BOTH"></a>

    `PGRES_COPY_BOTH` [#](#LIBPQ-PGRES-COPY-BOTH)
    :   已開始 Copy In/Out（往返伺服器）資料傳輸。此功能目前只用於串流複寫，因此一般應用程式中應該不會出現此狀態。
    <a id="LIBPQ-PGRES-SINGLE-TUPLE"></a>

    `PGRES_SINGLE_TUPLE` [#](#LIBPQ-PGRES-SINGLE-TUPLE)
    :   `PGresult` 包含目前命令的單一個結果元組。只有在為該查詢選擇了單列模式時，才會出現此狀態（請參閱[第 32.6 節](libpq-single-row-mode.md)）。
    <a id="LIBPQ-PGRES-TUPLES-CHUNK"></a>

    `PGRES_TUPLES_CHUNK` [#](#LIBPQ-PGRES-TUPLES-CHUNK)
    :   `PGresult` 包含目前命令的數個結果元組。只有在為該查詢選擇了分塊模式時，才會出現此狀態（請參閱[第 32.6 節](libpq-single-row-mode.md)）。元組數不會超過傳給 [`PQsetChunkedRowsMode`](libpq-single-row-mode.md#LIBPQ-PQSETCHUNKEDROWSMODE) 的上限。
    <a id="LIBPQ-PGRES-PIPELINE-SYNC"></a>

    `PGRES_PIPELINE_SYNC` [#](#LIBPQ-PGRES-PIPELINE-SYNC)
    :   `PGresult` 代表管線模式中的一個同步點，由 [`PQpipelineSync`](libpq-pipeline-mode.md#LIBPQ-PQPIPELINESYNC) 或 [`PQsendPipelineSync`](libpq-pipeline-mode.md#LIBPQ-PQSENDPIPELINESYNC) 所要求。只有在選擇了管線模式時，才會出現此狀態。
    <a id="LIBPQ-PGRES-PIPELINE-ABORTED"></a>

    `PGRES_PIPELINE_ABORTED` [#](#LIBPQ-PGRES-PIPELINE-ABORTED)
    :   `PGresult` 代表一個已從伺服器收到錯誤的管線。必須重複呼叫 `PQgetResult`，每次呼叫都會傳回此狀態碼，直到目前管線結束為止，屆時它會傳回 `PGRES_PIPELINE_SYNC`，並可恢復正常處理。

    若結果狀態為 `PGRES_TUPLES_OK`、`PGRES_SINGLE_TUPLE` 或 `PGRES_TUPLES_CHUNK`，就可以使用下面所述的函式取得查詢傳回的資料列。請注意，剛好取得零筆資料列的 `SELECT` 命令仍然會顯示 `PGRES_TUPLES_OK`。`PGRES_COMMAND_OK` 用於永遠不可能傳回資料列的命令（不含 `RETURNING` 子句的 `INSERT` 或 `UPDATE` 等）。回應 `PGRES_EMPTY_QUERY` 可能表示用戶端軟體有錯誤。

    狀態為 `PGRES_NONFATAL_ERROR` 的結果永遠不會由 [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 或其他查詢執行函式直接傳回；這類結果會改為傳遞給通知訊息處理函式（請參閱[第 32.13 節](libpq-notice-processing.md)）。
<a id="LIBPQ-PQRESSTATUS"></a>

`PQresStatus`<a id="id-1.7.3.10.3.9.7.2.1.2"></a> [#](#LIBPQ-PQRESSTATUS)
:   將 [`PQresultStatus`](libpq-exec.md#LIBPQ-PQRESULTSTATUS) 傳回的列舉型別轉換為描述該狀態碼的字串常數。呼叫者不應釋放此結果。

    ```

    char *PQresStatus(ExecStatusType status);
    ```
<a id="LIBPQ-PQRESULTERRORMESSAGE"></a>

`PQresultErrorMessage`<a id="id-1.7.3.10.3.9.7.3.1.2"></a> [#](#LIBPQ-PQRESULTERRORMESSAGE)
:   傳回與該命令相關的錯誤訊息；若沒有錯誤，則傳回空字串。

    ```

    char *PQresultErrorMessage(const PGresult *res);
    ```

    若發生錯誤，傳回的字串會以換行字元結尾。呼叫者不應直接釋放此結果。當相關聯的 `PGresult` 控制代碼傳給 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 時，它就會被釋放。

    緊接在 [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) 或 [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT) 呼叫之後，[`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE)（針對連線）會傳回與 [`PQresultErrorMessage`](libpq-exec.md#LIBPQ-PQRESULTERRORMESSAGE)（針對結果）相同的字串。不過，`PGresult` 會保留它的錯誤訊息直到被銷毀為止，而連線的錯誤訊息則會在進行後續操作時改變。當你想知道與特定 `PGresult` 相關的狀態時，請使用 [`PQresultErrorMessage`](libpq-exec.md#LIBPQ-PQRESULTERRORMESSAGE)；當你想知道連線上最近一次操作的狀態時，請使用 [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE)。
<a id="LIBPQ-PQRESULTVERBOSEERRORMESSAGE"></a>

`PQresultVerboseErrorMessage`<a id="id-1.7.3.10.3.9.7.4.1.2"></a> [#](#LIBPQ-PQRESULTVERBOSEERRORMESSAGE)
:   傳回與 `PGresult` 物件相關之錯誤訊息的重新格式化版本。

    ```

    char *PQresultVerboseErrorMessage(const PGresult *res,
                                      PGVerbosity verbosity,
                                      PGContextVisibility show_context);
    ```

    在某些情況下，用戶端可能希望取得先前已回報之錯誤的更詳細版本。[`PQresultVerboseErrorMessage`](libpq-exec.md#LIBPQ-PQRESULTVERBOSEERRORMESSAGE) 滿足了這個需求：它會計算出若在產生給定的 `PGresult` 時，連線已採用指定的詳細程度設定，[`PQresultErrorMessage`](libpq-exec.md#LIBPQ-PQRESULTERRORMESSAGE) 原本會產生的訊息。若 `PGresult` 不是錯誤結果，則改為回報「PGresult is not an error result」。傳回的字串會以換行字元結尾。

    與大多數其他從 `PGresult` 擷取資料的函式不同，此函式的結果是新配置的字串。不再需要該字串時，呼叫者必須使用 `PQfreemem()` 將它釋放。

    記憶體不足時，可能傳回 NULL。
<a id="LIBPQ-PQRESULTERRORFIELD"></a>

`PQresultErrorField`<a id="id-1.7.3.10.3.9.7.5.1.2"></a> [#](#LIBPQ-PQRESULTERRORFIELD)
:   傳回錯誤報告中的單一欄位。

    ```

    char *PQresultErrorField(const PGresult *res, int fieldcode);
    ```

    *`fieldcode`* 是錯誤欄位識別碼；請參閱下列符號。若 `PGresult` 不是錯誤或警告結果，或不包含指定的欄位，則傳回 `NULL`。欄位值通常不會以換行字元結尾。呼叫者不應直接釋放此結果。當相關聯的 `PGresult` 控制代碼傳給 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 時，它就會被釋放。

    可用的欄位代碼如下：

    <a id="LIBPQ-PG-DIAG-SEVERITY"></a>

    `PG_DIAG_SEVERITY` [#](#LIBPQ-PG-DIAG-SEVERITY)
    :   嚴重程度；欄位內容為 `ERROR`、`FATAL` 或 `PANIC`（在錯誤訊息中），或 `WARNING`、`NOTICE`、`DEBUG`、`INFO` 或 `LOG`（在通知訊息中），或是其中之一的在地化翻譯。一律存在。
    <a id="LIBPQ-PG-DIAG-SEVERITY-NONLOCALIZED"></a>

    `PG_DIAG_SEVERITY_NONLOCALIZED` [#](#LIBPQ-PG-DIAG-SEVERITY-NONLOCALIZED)
    :   嚴重程度；欄位內容為 `ERROR`、`FATAL` 或 `PANIC`（在錯誤訊息中），或 `WARNING`、`NOTICE`、`DEBUG`、`INFO` 或 `LOG`（在通知訊息中）。它與 `PG_DIAG_SEVERITY` 欄位相同，差別在於其內容永遠不會在地化。只有 PostgreSQL 9.6 及更新版本產生的報告中才會有此欄位。
    <a id="LIBPQ-PG-DIAG-SQLSTATE"></a>

    `PG_DIAG_SQLSTATE`<a id="id-1.7.3.10.3.9.7.5.2.2.1.3.1.2"></a> [#](#LIBPQ-PG-DIAG-SQLSTATE)
    :   錯誤的 SQLSTATE 代碼。SQLSTATE 代碼用來識別所發生錯誤的類型；前端應用程式可以用它來針對特定資料庫錯誤執行特定的操作（例如錯誤處理）。可能的 SQLSTATE 代碼清單請參閱[附錄 A](../../appendixes/errcodes-appendix/README.md)。此欄位無法在地化，而且一律存在。
    <a id="LIBPQ-PG-DIAG-MESSAGE-PRIMARY"></a>

    `PG_DIAG_MESSAGE_PRIMARY` [#](#LIBPQ-PG-DIAG-MESSAGE-PRIMARY)
    :   供人閱讀的主要錯誤訊息（通常為一行）。一律存在。
    <a id="LIBPQ-PG-DIAG-MESSAGE-DETAIL"></a>

    `PG_DIAG_MESSAGE_DETAIL` [#](#LIBPQ-PG-DIAG-MESSAGE-DETAIL)
    :   詳細資訊：選用的次要錯誤訊息，提供有關該問題的更多細節。可能有多行。
    <a id="LIBPQ-PG-DIAG-MESSAGE-HINT"></a>

    `PG_DIAG_MESSAGE_HINT` [#](#LIBPQ-PG-DIAG-MESSAGE-HINT)
    :   提示：選用的建議，說明如何處理該問題。它與詳細資訊的不同之處在於它提供的是建議（可能並不恰當），而不是確切的事實。可能有多行。
    <a id="LIBPQ-PG-DIAG-STATEMENT-POSITION"></a>

    `PG_DIAG_STATEMENT_POSITION` [#](#LIBPQ-PG-DIAG-STATEMENT-POSITION)
    :   包含十進位整數的字串，表示錯誤游標位置，也就是在原始陳述式字串中的索引。第一個字元的索引為 1，而位置是以字元而非位元組計算。
    <a id="LIBPQ-PG-DIAG-INTERNAL-POSITION"></a>

    `PG_DIAG_INTERNAL_POSITION` [#](#LIBPQ-PG-DIAG-INTERNAL-POSITION)
    :   定義與 `PG_DIAG_STATEMENT_POSITION` 欄位相同，但用於游標位置指向內部產生的命令，而不是用戶端所送出命令的情況。出現此欄位時，一定也會出現 `PG_DIAG_INTERNAL_QUERY` 欄位。
    <a id="LIBPQ-PG-DIAG-INTERNAL-QUERY"></a>

    `PG_DIAG_INTERNAL_QUERY` [#](#LIBPQ-PG-DIAG-INTERNAL-QUERY)
    :   失敗的內部產生命令的文字。例如，這可能是由 PL/pgSQL 函式發出的 SQL 查詢。
    <a id="LIBPQ-PG-DIAG-CONTEXT"></a>

    `PG_DIAG_CONTEXT` [#](#LIBPQ-PG-DIAG-CONTEXT)
    :   錯誤發生時所在上下文的指示。目前這包括作用中的程序語言函式與內部產生查詢的呼叫堆疊追蹤。追蹤每行一個項目，最近的排在最前面。
    <a id="LIBPQ-PG-DIAG-SCHEMA-NAME"></a>

    `PG_DIAG_SCHEMA_NAME` [#](#LIBPQ-PG-DIAG-SCHEMA-NAME)
    :   若錯誤與特定資料庫物件相關，則為包含該物件的綱要名稱（若有的話）。
    <a id="LIBPQ-PG-DIAG-TABLE-NAME"></a>

    `PG_DIAG_TABLE_NAME` [#](#LIBPQ-PG-DIAG-TABLE-NAME)
    :   若錯誤與特定資料表相關，則為該資料表的名稱。（資料表所屬綱要的名稱請參閱綱要名稱欄位。）
    <a id="LIBPQ-PG-DIAG-COLUMN-NAME"></a>

    `PG_DIAG_COLUMN_NAME` [#](#LIBPQ-PG-DIAG-COLUMN-NAME)
    :   若錯誤與特定資料表欄位相關，則為該欄位的名稱。（請參閱綱要名稱與資料表名稱欄位以識別該資料表。）
    <a id="LIBPQ-PG-DIAG-DATATYPE-NAME"></a>

    `PG_DIAG_DATATYPE_NAME` [#](#LIBPQ-PG-DIAG-DATATYPE-NAME)
    :   若錯誤與特定資料型別相關，則為該資料型別的名稱。（資料型別所屬綱要的名稱請參閱綱要名稱欄位。）
    <a id="LIBPQ-PG-DIAG-CONSTRAINT-NAME"></a>

    `PG_DIAG_CONSTRAINT_NAME` [#](#LIBPQ-PG-DIAG-CONSTRAINT-NAME)
    :   若錯誤與特定限制條件相關，則為該限制條件的名稱。相關聯的資料表或網域請參閱上面列出的欄位。（就此而言，索引也被視為限制條件，即使它們並非以限制條件語法建立。）
    <a id="LIBPQ-PG-DIAG-SOURCE-FILE"></a>

    `PG_DIAG_SOURCE_FILE` [#](#LIBPQ-PG-DIAG-SOURCE-FILE)
    :   回報錯誤之原始碼位置的檔案名稱。
    <a id="LIBPQ-PG-DIAG-SOURCE-LINE"></a>

    `PG_DIAG_SOURCE_LINE` [#](#LIBPQ-PG-DIAG-SOURCE-LINE)
    :   回報錯誤之原始碼位置的行號。
    <a id="LIBPQ-PG-DIAG-SOURCE-FUNCTION"></a>

    `PG_DIAG_SOURCE_FUNCTION` [#](#LIBPQ-PG-DIAG-SOURCE-FUNCTION)
    :   回報錯誤之原始碼函式的名稱。

    ### 注意

    綱要名稱、資料表名稱、欄位名稱、資料型別名稱與限制條件名稱等欄位只會針對有限的幾種錯誤類型提供；請參閱[附錄 A](../../appendixes/errcodes-appendix/README.md)。不要假定其中任何一個欄位存在，就保證另一個欄位也存在。核心的錯誤來源會遵守上面所述的相互關係，但使用者定義的函式可能會以其他方式使用這些欄位。同樣地，也不要假定這些欄位所指的是目前資料庫中當下存在的物件。

    用戶端負責依自身需求格式化所顯示的資訊；特別是，它應該視需要將長行斷行。錯誤訊息欄位中出現的換行字元應該視為段落分隔，而不是換行。

    libpq 內部產生的錯誤會有嚴重程度與主要訊息，但通常沒有其他欄位。

    請注意，錯誤欄位只能從 `PGresult` 物件取得，無法從 `PGconn` 物件取得；並沒有 `PQerrorField` 函式。
<a id="LIBPQ-PQCLEAR"></a>

`PQclear`<a id="id-1.7.3.10.3.9.7.6.1.2"></a> [#](#LIBPQ-PQCLEAR)
:   釋放與 `PGresult` 相關聯的儲存空間。每個命令結果在不再需要時，都應該以 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 釋放。

    ```

    void PQclear(PGresult *res);
    ```

    若引數為 `NULL` 指標，則不執行任何操作。

    你可以將 `PGresult` 物件保留任意長的時間；發出新命令時它不會消失，即使關閉連線也不會。要擺脫它，你必須呼叫 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR)。若未這麼做，會導致應用程式發生記憶體洩漏。

<a id="LIBPQ-EXEC-SELECT-INFO"></a>

### 32.3.2. 取得查詢結果資訊 [#](#LIBPQ-EXEC-SELECT-INFO)

這些函式用來從代表成功查詢結果（也就是狀態為 `PGRES_TUPLES_OK`、`PGRES_SINGLE_TUPLE` 或 `PGRES_TUPLES_CHUNK` 的結果）的 `PGresult` 物件中擷取資訊。它們也可以用來從成功的 Describe 操作中擷取資訊：Describe 的結果具有與實際執行該查詢時所提供的完全相同的欄位資訊，但沒有任何資料列。對於其他狀態值的物件，這些函式的行為會如同結果有零筆資料列與零個欄位。

<a id="LIBPQ-PQNTUPLES"></a>

`PQntuples`<a id="id-1.7.3.10.4.3.1.1.2"></a> [#](#LIBPQ-PQNTUPLES)
:   傳回查詢結果中的資料列（元組）數。（請注意，`PGresult` 物件最多只能有 `INT_MAX` 筆資料列，因此 `int` 型別的結果就足夠了。）

    ```

    int PQntuples(const PGresult *res);
    ```
<a id="LIBPQ-PQNFIELDS"></a>

`PQnfields`<a id="id-1.7.3.10.4.3.2.1.2"></a> [#](#LIBPQ-PQNFIELDS)
:   傳回查詢結果中每筆資料列的欄位數。

    ```

    int PQnfields(const PGresult *res);
    ```
<a id="LIBPQ-PQFNAME"></a>

`PQfname`<a id="id-1.7.3.10.4.3.3.1.2"></a> [#](#LIBPQ-PQFNAME)
:   傳回與給定欄位編號相關聯的欄位名稱。欄位編號從 0 開始。呼叫者不應直接釋放此結果。當相關聯的 `PGresult` 控制代碼傳給 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 時，它就會被釋放。

    ```

    char *PQfname(const PGresult *res,
                  int column_number);
    ```

    若欄位編號超出範圍，則傳回 `NULL`。
<a id="LIBPQ-PQFNUMBER"></a>

`PQfnumber`<a id="id-1.7.3.10.4.3.4.1.2"></a> [#](#LIBPQ-PQFNUMBER)
:   傳回與給定欄位名稱相關聯的欄位編號。

    ```

    int PQfnumber(const PGresult *res,
                  const char *column_name);
    ```

    若給定的名稱不符合任何欄位，則傳回 -1。

    給定的名稱會被視為 SQL 命令中的識別字，也就是說，除非加上雙引號，否則會轉為小寫。例如，給定由下列 SQL 命令產生的查詢結果：

    ```

    SELECT 1 AS FOO, 2 AS "BAR";
    ```

    會得到下列結果：

    ```

    PQfname(res, 0)              foo
    PQfname(res, 1)              BAR
    PQfnumber(res, "FOO")        0
    PQfnumber(res, "foo")        0
    PQfnumber(res, "BAR")        -1
    PQfnumber(res, "\"BAR\"")    1
    ```
<a id="LIBPQ-PQFTABLE"></a>

`PQftable`<a id="id-1.7.3.10.4.3.5.1.2"></a> [#](#LIBPQ-PQFTABLE)
:   傳回給定欄位所擷取自的資料表的 OID。欄位編號從 0 開始。

    ```

    Oid PQftable(const PGresult *res,
                 int column_number);
    ```

    若欄位編號超出範圍，或指定的欄位不是對資料表欄位的單純參照，則傳回 `InvalidOid`。你可以查詢系統資料表 `pg_class`，以確切判斷所參照的是哪個資料表。

    引入 libpq 標頭檔時，就會定義型別 `Oid` 與常數 `InvalidOid`。兩者都會是某種整數型別。
<a id="LIBPQ-PQFTABLECOL"></a>

`PQftablecol`<a id="id-1.7.3.10.4.3.6.1.2"></a> [#](#LIBPQ-PQFTABLECOL)
:   傳回構成指定查詢結果欄位的那個欄位（在其資料表內）的欄位編號。查詢結果的欄位編號從 0 開始，但資料表欄位的編號不為零。

    ```

    int PQftablecol(const PGresult *res,
                    int column_number);
    ```

    若欄位編號超出範圍，或指定的欄位不是對資料表欄位的單純參照，則傳回零。
<a id="LIBPQ-PQFFORMAT"></a>

`PQfformat`<a id="id-1.7.3.10.4.3.7.1.2"></a> [#](#LIBPQ-PQFFORMAT)
:   傳回表示給定欄位格式的格式代碼。欄位編號從 0 開始。

    ```

    int PQfformat(const PGresult *res,
                  int column_number);
    ```

    格式代碼 0 表示文字資料表示法，格式代碼 1 則表示二進位表示法。（其他代碼保留供未來定義。）
<a id="LIBPQ-PQFTYPE"></a>

`PQftype`<a id="id-1.7.3.10.4.3.8.1.2"></a> [#](#LIBPQ-PQFTYPE)
:   傳回與給定欄位編號相關聯的資料型別。傳回的整數是該型別的內部 OID 編號。欄位編號從 0 開始。

    ```

    Oid PQftype(const PGresult *res,
                int column_number);
    ```

    你可以查詢系統資料表 `pg_type`，以取得各種資料型別的名稱與屬性。內建資料型別的 OID 定義在 PostgreSQL 安裝目錄的 `include` 目錄中的 `catalog/pg_type_d.h` 檔案裡。
<a id="LIBPQ-PQFMOD"></a>

`PQfmod`<a id="id-1.7.3.10.4.3.9.1.2"></a> [#](#LIBPQ-PQFMOD)
:   傳回與給定欄位編號相關聯之欄位的型別修飾詞。欄位編號從 0 開始。

    ```

    int PQfmod(const PGresult *res,
               int column_number);
    ```

    修飾詞值的解讀方式依型別而定；它們通常表示精確度或大小限制。值 -1 用來表示「沒有可用的資訊」。大多數資料型別不使用修飾詞，此時該值一律為 -1。
<a id="LIBPQ-PQFSIZE"></a>

`PQfsize`<a id="id-1.7.3.10.4.3.10.1.2"></a> [#](#LIBPQ-PQFSIZE)
:   傳回與給定欄位編號相關聯之欄位的大小（以位元組為單位）。欄位編號從 0 開始。

    ```

    int PQfsize(const PGresult *res,
                int column_number);
    ```

    [`PQfsize`](libpq-exec.md#LIBPQ-PQFSIZE) 傳回資料庫資料列中為此欄位配置的空間，換句話說，就是該資料型別在伺服器內部表示法的大小。（因此，它對用戶端其實沒有太大用處。）負值表示該資料型別為變動長度。
<a id="LIBPQ-PQBINARYTUPLES"></a>

`PQbinaryTuples`<a id="id-1.7.3.10.4.3.11.1.2"></a> [#](#LIBPQ-PQBINARYTUPLES)
:   若 `PGresult` 包含二進位資料，則傳回 1；若包含文字資料，則傳回 0。

    ```

    int PQbinaryTuples(const PGresult *res);
    ```

    此函式已不建議使用（但與 `COPY` 搭配使用的情況除外），因為單一個 `PGresult` 可能在某些欄位中包含文字資料，而在其他欄位中包含二進位資料。建議改用 [`PQfformat`](libpq-exec.md#LIBPQ-PQFFORMAT)。只有在結果的所有欄位都是二進位（格式 1）時，[`PQbinaryTuples`](libpq-exec.md#LIBPQ-PQBINARYTUPLES) 才會傳回 1。
<a id="LIBPQ-PQGETVALUE"></a>

`PQgetvalue`<a id="id-1.7.3.10.4.3.12.1.2"></a> [#](#LIBPQ-PQGETVALUE)
:   傳回 `PGresult` 中某一筆資料列的單一欄位值。資料列與欄位編號從 0 開始。呼叫者不應直接釋放此結果。當相關聯的 `PGresult` 控制代碼傳給 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 時，它就會被釋放。

    ```

    char *PQgetvalue(const PGresult *res,
                     int row_number,
                     int column_number);
    ```

    對於文字格式的資料，[`PQgetvalue`](libpq-exec.md#LIBPQ-PQGETVALUE) 傳回的值是該欄位值以 null 結尾的字元字串表示法。對於二進位格式的資料，該值採用由該資料型別的 `typsend` 與 `typreceive` 函式所決定的二進位表示法。（在此情況下，該值後面其實也會接著一個零位元組，但這通常沒有用處，因為該值很可能含有內嵌的 null。）

    若欄位值為 null，則傳回空字串。要區分 null 值與空字串值，請參閱 [`PQgetisnull`](libpq-exec.md#LIBPQ-PQGETISNULL)。

    [`PQgetvalue`](libpq-exec.md#LIBPQ-PQGETVALUE) 傳回的指標指向屬於 `PGresult` 結構一部分的儲存空間。不應修改它所指向的資料，而且若要在 `PGresult` 結構本身的生命週期之後繼續使用這些資料，必須明確地將它們複製到其他儲存空間。
<a id="LIBPQ-PQGETISNULL"></a>

`PQgetisnull`<a id="id-1.7.3.10.4.3.13.1.2"></a><a id="id-1.7.3.10.4.3.13.1.3"></a> [#](#LIBPQ-PQGETISNULL)
:   測試欄位是否為 null 值。資料列與欄位編號從 0 開始。

    ```

    int PQgetisnull(const PGresult *res,
                    int row_number,
                    int column_number);
    ```

    若欄位為 null，此函式傳回 1；若包含非 null 值，則傳回 0。（請注意，對於 null 欄位，[`PQgetvalue`](libpq-exec.md#LIBPQ-PQGETVALUE) 會傳回空字串，而不是空指標。）
<a id="LIBPQ-PQGETLENGTH"></a>

`PQgetlength`<a id="id-1.7.3.10.4.3.14.1.2"></a> [#](#LIBPQ-PQGETLENGTH)
:   傳回欄位值的實際長度（以位元組為單位）。資料列與欄位編號從 0 開始。

    ```

    int PQgetlength(const PGresult *res,
                    int row_number,
                    int column_number);
    ```

    這是該特定資料值的實際資料長度，也就是 [`PQgetvalue`](libpq-exec.md#LIBPQ-PQGETVALUE) 所指向之物件的大小。對於文字資料格式，此值與 `strlen()` 相同。對於二進位格式，這是不可或缺的資訊。請注意，*不*應該依賴 [`PQfsize`](libpq-exec.md#LIBPQ-PQFSIZE) 來取得實際的資料長度。
<a id="LIBPQ-PQNPARAMS"></a>

`PQnparams`<a id="id-1.7.3.10.4.3.15.1.2"></a> [#](#LIBPQ-PQNPARAMS)
:   傳回預備陳述式的參數個數。

    ```

    int PQnparams(const PGresult *res);
    ```

    此函式只有在檢視 [`PQdescribePrepared`](libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED) 的結果時才有用。對於其他類型的結果，它會傳回零。
<a id="LIBPQ-PQPARAMTYPE"></a>

`PQparamtype`<a id="id-1.7.3.10.4.3.16.1.2"></a> [#](#LIBPQ-PQPARAMTYPE)
:   傳回指定陳述式參數的資料型別。參數編號從 0 開始。

    ```

    Oid PQparamtype(const PGresult *res, int param_number);
    ```

    此函式只有在檢視 [`PQdescribePrepared`](libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED) 的結果時才有用。對於其他類型的結果，它會傳回零。
<a id="LIBPQ-PQPRINT"></a>

`PQprint`<a id="id-1.7.3.10.4.3.17.1.2"></a> [#](#LIBPQ-PQPRINT)
:   將所有資料列，以及可選擇的欄位名稱，輸出到指定的輸出串流。

    ```

    void PQprint(FILE *fout,      /* output stream */
                 const PGresult *res,
                 const PQprintOpt *po);
    typedef struct
    {
        pqbool  header;      /* print output field headings and row count */
        pqbool  align;       /* fill align the fields */
        pqbool  standard;    /* old brain dead format */
        pqbool  html3;       /* output HTML tables */
        pqbool  expanded;    /* expand tables */
        pqbool  pager;       /* use pager for output if needed */
        char    *fieldSep;   /* field separator */
        char    *tableOpt;   /* attributes for HTML table element */
        char    *caption;    /* HTML table caption */
        char    **fieldName; /* null-terminated array of replacement field names */
    } PQprintOpt;
    ```

    此函式以前被 psql 用來輸出查詢結果，但現在已不是如此。請注意，它假定所有資料都是文字格式。

<a id="LIBPQ-EXEC-NONSELECT"></a>

### 32.3.3. 取得其他結果資訊 [#](#LIBPQ-EXEC-NONSELECT)

這些函式用來從 `PGresult` 物件中擷取其他資訊。

<a id="LIBPQ-PQCMDSTATUS"></a>

`PQcmdStatus`<a id="id-1.7.3.10.5.3.1.1.2"></a> [#](#LIBPQ-PQCMDSTATUS)
:   傳回產生該 `PGresult` 之 SQL 命令的命令狀態標籤。

    ```

    char *PQcmdStatus(PGresult *res);
    ```

    通常這只是命令的名稱，但也可能包含額外的資料，例如處理的資料列數。呼叫者不應直接釋放此結果。當相關聯的 `PGresult` 控制代碼傳給 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 時，它就會被釋放。
<a id="LIBPQ-PQCMDTUPLES"></a>

`PQcmdTuples`<a id="id-1.7.3.10.5.3.2.1.2"></a> [#](#LIBPQ-PQCMDTUPLES)
:   傳回受該 SQL 命令影響的資料列數。

    ```

    char *PQcmdTuples(PGresult *res);
    ```

    此函式傳回一個字串，內容為受產生該 `PGresult` 之 SQL 陳述式影響的資料列數。此函式只能在執行 `SELECT`、`CREATE TABLE AS`、`INSERT`、`UPDATE`、`DELETE`、`MERGE`、`MOVE`、`FETCH` 或 `COPY` 陳述式之後，或是以 `EXECUTE` 執行包含 `INSERT`、`UPDATE`、`DELETE` 或 `MERGE` 陳述式的預備查詢之後使用。若產生該 `PGresult` 的是其他任何命令，[`PQcmdTuples`](libpq-exec.md#LIBPQ-PQCMDTUPLES) 會傳回空字串。呼叫者不應直接釋放此傳回值。當相關聯的 `PGresult` 控制代碼傳給 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 時，它就會被釋放。
<a id="LIBPQ-PQOIDVALUE"></a>

`PQoidValue`<a id="id-1.7.3.10.5.3.3.1.2"></a> [#](#LIBPQ-PQOIDVALUE)
:   若該 SQL 命令是將恰好一筆資料列插入具有 OID 之資料表的 `INSERT`，或是以 `EXECUTE` 執行包含適當 `INSERT` 陳述式的預備查詢，則傳回所插入資料列的 OID<a id="id-1.7.3.10.5.3.3.2.1.1"></a>。否則，此函式傳回 `InvalidOid`。若受 `INSERT` 陳述式影響的資料表不包含 OID，此函式也會傳回 `InvalidOid`。

    ```

    Oid PQoidValue(const PGresult *res);
    ```
<a id="LIBPQ-PQOIDSTATUS"></a>

`PQoidStatus`<a id="id-1.7.3.10.5.3.4.1.2"></a> [#](#LIBPQ-PQOIDSTATUS)
:   此函式已不建議使用，請改用 [`PQoidValue`](libpq-exec.md#LIBPQ-PQOIDVALUE)，而且它並非執行緒安全。它傳回含有所插入資料列 OID 的字串，而 [`PQoidValue`](libpq-exec.md#LIBPQ-PQOIDVALUE) 則傳回 OID 值。

    ```

    char *PQoidStatus(const PGresult *res);
    ```

<a id="LIBPQ-EXEC-ESCAPE-STRING"></a>

### 32.3.4. 跳脫要放入 SQL 命令的字串 [#](#LIBPQ-EXEC-ESCAPE-STRING)

<a id="id-1.7.3.10.6.2"></a>

<a id="LIBPQ-PQESCAPELITERAL"></a>

`PQescapeLiteral`<a id="id-1.7.3.10.6.3.1.1.2"></a> [#](#LIBPQ-PQESCAPELITERAL)
:   ```

    char *PQescapeLiteral(PGconn *conn, const char *str, size_t length);
    ```

    [`PQescapeLiteral`](libpq-exec.md#LIBPQ-PQESCAPELITERAL) 會跳脫字串，以便在 SQL 命令中使用。在 SQL 命令中以字面常數插入資料值時，這很有用。某些字元（例如引號與反斜線）必須跳脫，以避免被 SQL 剖析器做特殊解讀。[`PQescapeLiteral`](libpq-exec.md#LIBPQ-PQESCAPELITERAL) 就是執行這項操作。

    [`PQescapeLiteral`](libpq-exec.md#LIBPQ-PQESCAPELITERAL) 在以 `malloc()` 配置的記憶體中傳回 *`str`* 參數的跳脫版本。不再需要該結果時，應該使用 `PQfreemem()` 釋放這塊記憶體。結尾的零位元組不是必要的，也不應計入 *`length`*。（若在處理完 *`length`* 個位元組之前就遇到結尾的零位元組，[`PQescapeLiteral`](libpq-exec.md#LIBPQ-PQESCAPELITERAL) 會在該零位元組處停止；因此其行為與 `strncpy` 相當類似。）傳回的字串中所有特殊字元都已被替換，因此能被 PostgreSQL 字串字面值剖析器正確處理。結尾也會加上零位元組。PostgreSQL 字串字面值兩側必須加上的單引號也包含在結果字串中。

    發生錯誤時，[`PQescapeLiteral`](libpq-exec.md#LIBPQ-PQESCAPELITERAL) 會傳回 `NULL`，並在 *`conn`* 物件中存入適當的訊息。

    ### 提示

    處理從不可信來源收到的字串時，進行適當的跳脫尤其重要。否則會有安全風險：你容易遭受「SQL 注入」攻擊，也就是有不想要的 SQL 命令被送進你的資料庫。

    請注意，當資料值以 [`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS) 或其同類常式中的獨立參數傳遞時，進行跳脫既不必要，也不正確。
<a id="LIBPQ-PQESCAPEIDENTIFIER"></a>

`PQescapeIdentifier`<a id="id-1.7.3.10.6.3.2.1.2"></a> [#](#LIBPQ-PQESCAPEIDENTIFIER)
:   ```

    char *PQescapeIdentifier(PGconn *conn, const char *str, size_t length);
    ```

    [`PQescapeIdentifier`](libpq-exec.md#LIBPQ-PQESCAPEIDENTIFIER) 會跳脫字串，以便作為 SQL 識別字使用，例如資料表、欄位或函式名稱。當使用者提供的識別字可能含有特殊字元，而這些字元原本不會被 SQL 剖析器解讀為識別字的一部分時，或是當識別字可能含有應保留大小寫的大寫字元時，這很有用。

    [`PQescapeIdentifier`](libpq-exec.md#LIBPQ-PQESCAPEIDENTIFIER) 在以 `malloc()` 配置的記憶體中，傳回 *`str`* 參數跳脫為 SQL 識別字後的版本。不再需要該結果時，必須使用 `PQfreemem()` 釋放這塊記憶體。結尾的零位元組不是必要的，也不應計入 *`length`*。（若在處理完 *`length`* 個位元組之前就遇到結尾的零位元組，[`PQescapeIdentifier`](libpq-exec.md#LIBPQ-PQESCAPEIDENTIFIER) 會在該零位元組處停止；因此其行為與 `strncpy` 相當類似。）傳回的字串中所有特殊字元都已被替換，因此能被正確地當作 SQL 識別字處理。結尾也會加上零位元組。傳回的字串兩側也會加上雙引號。

    發生錯誤時，[`PQescapeIdentifier`](libpq-exec.md#LIBPQ-PQESCAPEIDENTIFIER) 會傳回 `NULL`，並在 *`conn`* 物件中存入適當的訊息。

    ### 提示

    與字串字面值相同，為了防止 SQL 注入攻擊，從不可信來源收到的 SQL 識別字必須加以跳脫。
<a id="LIBPQ-PQESCAPESTRINGCONN"></a>

`PQescapeStringConn`<a id="id-1.7.3.10.6.3.3.1.2"></a> [#](#LIBPQ-PQESCAPESTRINGCONN)
:   ```

    size_t PQescapeStringConn(PGconn *conn,
                              char *to, const char *from, size_t length,
                              int *error);
    ```

    [`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) 會跳脫字串字面值，與 [`PQescapeLiteral`](libpq-exec.md#LIBPQ-PQESCAPELITERAL) 非常類似。與 [`PQescapeLiteral`](libpq-exec.md#LIBPQ-PQESCAPELITERAL) 不同的是，呼叫者必須負責提供大小適當的緩衝區。此外，[`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) 不會產生 PostgreSQL 字串字面值兩側必須加上的單引號；這些單引號應該由要插入該結果的 SQL 命令提供。參數 *`from`* 指向要跳脫之字串的第一個字元，而參數 *`length`* 則給出此字串的位元組數。結尾的零位元組不是必要的，也不應計入 *`length`*。（若在處理完 *`length`* 個位元組之前就遇到結尾的零位元組，[`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) 會在該零位元組處停止；因此其行為與 `strncpy` 相當類似。）*`to`* 必須指向一個至少能容納比 *`length`* 值的兩倍再多一個位元組的緩衝區，否則行為未定義。若 *`to`* 與 *`from`* 字串互相重疊，行為同樣未定義。

    若 *`error`* 參數不是 `NULL`，則成功時 `*error` 會設為零，發生錯誤時設為非零。目前唯一可能的錯誤狀況是來源字串中有無效的多位元組編碼。發生錯誤時仍會產生輸出字串，但可以預期伺服器會因格式錯誤而拒絕它。發生錯誤時，無論 *`error`* 是否為 `NULL`，都會在 *`conn`* 物件中存入適當的訊息。

    [`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) 傳回寫入 *`to`* 的位元組數，不包括結尾的零位元組。
<a id="LIBPQ-PQESCAPESTRING"></a>

`PQescapeString`<a id="id-1.7.3.10.6.3.4.1.2"></a> [#](#LIBPQ-PQESCAPESTRING)
:   [`PQescapeString`](libpq-exec.md#LIBPQ-PQESCAPESTRING) 是 [`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) 較舊且已不建議使用的版本。

    ```

    size_t PQescapeString (char *to, const char *from, size_t length);
    ```

    與 [`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) 唯一的差別在於 [`PQescapeString`](libpq-exec.md#LIBPQ-PQESCAPESTRING) 不接受 `PGconn` 或 *`error`* 參數。因此，它無法依據連線屬性（例如字元編碼）調整其行為，所以*可能產生錯誤的結果*。此外，它也無法回報錯誤狀況。

    在一次只使用一個 PostgreSQL 連線的用戶端程式中，可以安全地使用 [`PQescapeString`](libpq-exec.md#LIBPQ-PQESCAPESTRING)（此時它可以在「幕後」查出它需要知道的資訊）。在其他情況下，它是一種安全隱患，應該避免使用，改用 [`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN)。
<a id="LIBPQ-PQESCAPEBYTEACONN"></a>

`PQescapeByteaConn`<a id="id-1.7.3.10.6.3.5.1.2"></a> [#](#LIBPQ-PQESCAPEBYTEACONN)
:   跳脫二進位資料，以便在 SQL 命令中以 `bytea` 型別使用。與 [`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) 相同，只有在將資料直接插入 SQL 命令字串時才會使用它。

    ```

    unsigned char *PQescapeByteaConn(PGconn *conn,
                                     const unsigned char *from,
                                     size_t from_length,
                                     size_t *to_length);
    ```

    在 SQL 陳述式中作為 `bytea` 字面值的一部分使用時，某些位元組值必須加以跳脫。[`PQescapeByteaConn`](libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN) 會使用十六進位編碼或反斜線跳脫來跳脫位元組。更多資訊請參閱[第 8.4 節](../../the-sql-language/datatype/datatype-binary.md)。

    參數 *`from`* 指向要跳脫之字串的第一個位元組，而參數 *`from_length`* 則給出此二進位字串的位元組數。（結尾的零位元組既不必要，也不計入。）參數 *`to_length`* 指向一個變數，用來存放跳脫後字串的長度。此結果字串長度包含結果結尾的零位元組。

    [`PQescapeByteaConn`](libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN) 在以 `malloc()` 配置的記憶體中傳回 *`from`* 參數二進位字串的跳脫版本。不再需要該結果時，應該使用 `PQfreemem()` 釋放這塊記憶體。傳回的字串中所有特殊字元都已被替換，因此能被 PostgreSQL 字串字面值剖析器以及 `bytea` 輸入函式正確處理。結尾也會加上零位元組。PostgreSQL 字串字面值兩側必須加上的單引號不屬於結果字串的一部分。

    發生錯誤時，會傳回空指標，並在 *`conn`* 物件中存入適當的錯誤訊息。目前唯一可能的錯誤是記憶體不足以容納結果字串。
<a id="LIBPQ-PQESCAPEBYTEA"></a>

`PQescapeBytea`<a id="id-1.7.3.10.6.3.6.1.2"></a> [#](#LIBPQ-PQESCAPEBYTEA)
:   [`PQescapeBytea`](libpq-exec.md#LIBPQ-PQESCAPEBYTEA) 是 [`PQescapeByteaConn`](libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN) 較舊且已不建議使用的版本。

    ```

    unsigned char *PQescapeBytea(const unsigned char *from,
                                 size_t from_length,
                                 size_t *to_length);
    ```

    與 [`PQescapeByteaConn`](libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN) 唯一的差別在於 [`PQescapeBytea`](libpq-exec.md#LIBPQ-PQESCAPEBYTEA) 不接受 `PGconn` 參數。因此，只有在一次只使用單一 PostgreSQL 連線的用戶端程式中，才能安全地使用 [`PQescapeBytea`](libpq-exec.md#LIBPQ-PQESCAPEBYTEA)（此時它可以在「幕後」查出它需要知道的資訊）。若在使用多個資料庫連線的程式中使用，它*可能產生錯誤的結果*（這種情況請使用 [`PQescapeByteaConn`](libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN)）。
<a id="LIBPQ-PQUNESCAPEBYTEA"></a>

`PQunescapeBytea`<a id="id-1.7.3.10.6.3.7.1.2"></a> [#](#LIBPQ-PQUNESCAPEBYTEA)
:   將二進位資料的字串表示法轉換為二進位資料——與 [`PQescapeBytea`](libpq-exec.md#LIBPQ-PQESCAPEBYTEA) 相反。以文字格式取得 `bytea` 資料時需要這麼做，但以二進位格式取得時則不需要。

    ```

    unsigned char *PQunescapeBytea(const unsigned char *from, size_t *to_length);
    ```

    參數 *`from`* 指向一個字串，例如對 `bytea` 欄位套用 [`PQgetvalue`](libpq-exec.md#LIBPQ-PQGETVALUE) 時可能傳回的字串。[`PQunescapeBytea`](libpq-exec.md#LIBPQ-PQUNESCAPEBYTEA) 會將此字串表示法轉換為其二進位表示法。它傳回一個指向以 `malloc()` 配置之緩衝區的指標，發生錯誤時則傳回 `NULL`，並將緩衝區的大小放入 *`to_length`*。不再需要該結果時，必須使用 [`PQfreemem`](libpq-misc.md#LIBPQ-PQFREEMEM) 將它釋放。

    此轉換並非 [`PQescapeBytea`](libpq-exec.md#LIBPQ-PQESCAPEBYTEA) 的完全逆運算，因為從 [`PQgetvalue`](libpq-exec.md#LIBPQ-PQGETVALUE) 收到的字串並不預期是「已跳脫」的。特別是，這表示不需要考慮字串的引號處理，因此也不需要 `PGconn` 參數。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-exec.html)（原文版本：18.6；核對日期：2026-10-18）
