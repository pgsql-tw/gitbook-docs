<a id="LIBPQ-CONNECT"></a>

## 32.1. 資料庫連線控制函式 [#](#LIBPQ-CONNECT)

[32.1.1. 連線字串](libpq-connect.md#LIBPQ-CONNSTRING)

[32.1.2. 參數關鍵字](libpq-connect.md#LIBPQ-PARAMKEYWORDS)

下列函式用於建立與 PostgreSQL 後端伺服器的連線。一個應用程式可以同時開啟多個後端連線。（這麼做的原因之一是為了存取超過一個資料庫。）每個連線都以一個 `PGconn`<a id="id-1.7.3.8.2.3"></a> 物件表示，此物件可由函式 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB)、[`PQconnectdbParams`](libpq-connect.md#LIBPQ-PQCONNECTDBPARAMS) 或 [`PQsetdbLogin`](libpq-connect.md#LIBPQ-PQSETDBLOGIN) 取得。請注意，這些函式一律會傳回非空的物件指標，除非（或許）記憶體少到連 `PGconn` 物件都無法配置。在透過連線物件送出查詢之前，應該呼叫 [`PQstatus`](libpq-status.md#LIBPQ-PQSTATUS) 函式，檢查傳回值以確認連線成功。

### 警告

如果不受信任的使用者可以存取一個尚未採用[安全綱要使用模式](../../the-sql-language/ddl/ddl-schemas.md#DDL-SCHEMAS-PATTERNS)的資料庫，請在每個工作階段開始時，從 `search_path` 中移除可被公眾寫入的綱要。做法之一是將參數關鍵字 `options` 設為值 `-csearch_path=`。或者，也可以在連線後執行 `PQexec(conn, "SELECT
pg_catalog.set_config('search_path', '', false)")`。這項考量並非 libpq 所特有；它適用於每一種可執行任意 SQL 命令的介面。

### 警告

在 Unix 上，於持有已開啟 libpq 連線的情況下 fork 程序，可能導致無法預期的結果，因為父程序與子程序會共用相同的通訊端與作業系統資源。因此不建議這樣使用；不過，從子程序執行 `exec` 來載入新的執行檔是安全的。

<a id="LIBPQ-PQCONNECTDBPARAMS"></a>

`PQconnectdbParams`<a id="id-1.7.3.8.2.11.1.1.2"></a> [#](#LIBPQ-PQCONNECTDBPARAMS)
:   建立與資料庫伺服器的新連線。

    ```

    PGconn *PQconnectdbParams(const char * const *keywords,
                              const char * const *values,
                              int expand_dbname);
    ```

    此函式使用取自兩個以 `NULL` 結尾之陣列的參數來開啟新的資料庫連線。第一個陣列 `keywords` 定義為字串陣列，每個字串是一個關鍵字。第二個陣列 `values` 提供每個關鍵字的值。與下面的 [`PQsetdbLogin`](libpq-connect.md#LIBPQ-PQSETDBLOGIN) 不同，參數集合可以在不變更函式簽章的情況下擴充，因此開發新的應用程式時，建議使用此函式（或其非阻塞版本 [`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS) 與 `PQconnectPoll`）。

    目前可辨識的參數關鍵字列於[第 32.1.2 節](libpq-connect.md#LIBPQ-PARAMKEYWORDS)。

    傳入的陣列可以是空的，以使用全部的預設參數；也可以包含一個或多個參數設定。兩個陣列的長度必須相符。處理會在 `keywords` 陣列中第一個 `NULL` 項目處停止。此外，如果與某個非 `NULL` 之 `keywords` 項目相對應的 `values` 項目是 `NULL` 或空字串，該項目會被忽略，並繼續處理下一組陣列項目。

    當 `expand_dbname` 不為零時，會檢查第一個 *`dbname`* 關鍵字的值是否為*連線字串*。若是，就會將其「展開」為從字串中取出的個別連線參數。如果該值包含等號（`=`），或以 URI 架構（scheme）指示符開頭，就會被視為連線字串，而不只是資料庫名稱。（連線字串格式的更多細節見[第 32.1.1 節](libpq-connect.md#LIBPQ-CONNSTRING)。）只有第一次出現的 *`dbname`* 會以這種方式處理；之後的任何 *`dbname`* 參數都會當作一般的資料庫名稱處理。

    一般而言，參數陣列會從頭到尾依序處理。如果有任何關鍵字重複出現，會使用最後一個值（非 `NULL` 且非空者）。這項規則特別適用於連線字串中的關鍵字與 `keywords` 陣列中的關鍵字衝突的情況。因此，程式設計者可以決定陣列項目能否覆寫連線字串中取得的值，或能否被其覆寫。出現在展開的 *`dbname`* 項目之前的陣列項目，可以被連線字串的欄位覆寫；而這些欄位又會被出現在 *`dbname`* 之後的陣列項目覆寫（但同樣地，只有在這些項目提供非空值時才會如此）。

    處理完所有陣列項目與任何展開的連線字串之後，仍未設定的連線參數會以預設值填入。如果未設定之參數所對應的環境變數（請參閱[第 32.15 節](libpq-envars.md)）有設定，就使用它的值。如果環境變數也沒有設定，則使用該參數的內建預設值。
<a id="LIBPQ-PQCONNECTDB"></a>

`PQconnectdb`<a id="id-1.7.3.8.2.11.2.1.2"></a> [#](#LIBPQ-PQCONNECTDB)
:   建立與資料庫伺服器的新連線。

    ```

    PGconn *PQconnectdb(const char *conninfo);
    ```

    此函式使用取自字串 `conninfo` 的參數來開啟新的資料庫連線。

    傳入的字串可以是空的，以使用全部的預設參數；也可以包含一個或多個以空白分隔的參數設定；或者可以包含一個 URI。詳細資訊請參閱[第 32.1.1 節](libpq-connect.md#LIBPQ-CONNSTRING)。
<a id="LIBPQ-PQSETDBLOGIN"></a>

`PQsetdbLogin`<a id="id-1.7.3.8.2.11.3.1.2"></a> [#](#LIBPQ-PQSETDBLOGIN)
:   建立與資料庫伺服器的新連線。

    ```

    PGconn *PQsetdbLogin(const char *pghost,
                         const char *pgport,
                         const char *pgoptions,
                         const char *pgtty,
                         const char *dbName,
                         const char *login,
                         const char *pwd);
    ```

    這是 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB) 的前身，具有固定的參數集合。它的功能相同，只是缺少的參數一律會採用預設值。對於任何要使用預設值的固定參數，請寫入 `NULL` 或空字串。

    如果 *`dbName`* 包含 `=` 符號或具有有效的連線 URI 前綴，它會被當作 *`conninfo`* 字串，處理方式與傳給 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB) 時完全相同，接著其餘參數再依 [`PQconnectdbParams`](libpq-connect.md#LIBPQ-PQCONNECTDBPARAMS) 所述的方式套用。

    `pgtty` 已不再使用，傳入的任何值都會被忽略。
<a id="LIBPQ-PQSETDB"></a>

`PQsetdb`<a id="id-1.7.3.8.2.11.4.1.2"></a> [#](#LIBPQ-PQSETDB)
:   建立與資料庫伺服器的新連線。

    ```

    PGconn *PQsetdb(char *pghost,
                    char *pgport,
                    char *pgoptions,
                    char *pgtty,
                    char *dbName);
    ```

    這是一個巨集，它呼叫 [`PQsetdbLogin`](libpq-connect.md#LIBPQ-PQSETDBLOGIN)，並以空指標作為 *`login`* 與 *`pwd`* 參數。提供它是為了與非常舊的程式保持向後相容性。
<a id="LIBPQ-PQCONNECTSTARTPARAMS"></a>

`PQconnectStartParams`<a id="id-1.7.3.8.2.11.5.1.2"></a><br>`PQconnectStart`<a id="id-1.7.3.8.2.11.5.2.2"></a><br><a id="LIBPQ-PQCONNECTPOLL"></a>`PQconnectPoll`<a id="id-1.7.3.8.2.11.5.3.2"></a> [#](#LIBPQ-PQCONNECTSTARTPARAMS)
:   <a id="id-1.7.3.8.2.11.5.4.1.1"></a>
    以非阻塞方式建立與資料庫伺服器的連線。

    ```

    PGconn *PQconnectStartParams(const char * const *keywords,
                                 const char * const *values,
                                 int expand_dbname);

    PGconn *PQconnectStart(const char *conninfo);

    PostgresPollingStatusType PQconnectPoll(PGconn *conn);
    ```

    這三個函式用於開啟與資料庫伺服器的連線，且在過程中不會讓應用程式的執行緒因遠端 I/O 而阻塞。這種做法的重點在於，等待 I/O 完成的動作可以發生在應用程式的主迴圈中，而不是在 [`PQconnectdbParams`](libpq-connect.md#LIBPQ-PQCONNECTDBPARAMS) 或 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB) 內部，因此應用程式可以在進行此操作的同時處理其他工作。

    使用 [`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS) 時，資料庫連線會使用取自 `keywords` 與 `values` 陣列的參數建立，並由 `expand_dbname` 控制，如前面 [`PQconnectdbParams`](libpq-connect.md#LIBPQ-PQCONNECTDBPARAMS) 所述。

    使用 `PQconnectStart` 時，資料庫連線會使用取自字串 `conninfo` 的參數建立，如前面 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB) 所述。

    只要滿足下列幾項限制，[`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS)、`PQconnectStart` 與 `PQconnectPoll` 都不會阻塞：

    * 必須適當地使用 `hostaddr` 參數，以避免進行 DNS 查詢。詳細資訊請參閱[第 32.1.2 節](libpq-connect.md#LIBPQ-PARAMKEYWORDS)中此參數的說明。
    * 如果你呼叫 [`PQtrace`](libpq-control.md#LIBPQ-PQTRACE)，請確保追蹤輸出所寫入的串流物件不會阻塞。
    * 你必須確保在呼叫 `PQconnectPoll` 之前，通訊端處於適當的狀態，如下所述。

    要開始一個非阻塞的連線請求，請呼叫 `PQconnectStart` 或 [`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS)。如果結果為空（null），表示 libpq 無法配置新的 `PGconn` 結構。否則會傳回一個有效的 `PGconn` 指標（不過它尚未代表一個有效的資料庫連線）。接著呼叫 `PQstatus(conn)`。如果結果是 `CONNECTION_BAD`，表示連線嘗試已經失敗，通常是因為連線參數無效。

    如果 `PQconnectStart` 或 [`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS) 成功，下一階段是輪詢 libpq，讓它可以繼續進行連線程序。使用 `PQsocket(conn)` 取得資料庫連線底層通訊端的描述子。（注意：不要假設通訊端在多次 `PQconnectPoll` 呼叫之間保持不變。）依下列方式循環：如果 `PQconnectPoll(conn)` 上一次傳回 `PGRES_POLLING_READING`，就等待通訊端可供讀取（由 `select()`、`poll()` 或類似的系統函式指出）。請注意，如果你的系統上有 `select(2)` 或 `poll(2)`，`PQsocketPoll` 可以將其設定抽象化，有助於減少樣板程式碼。然後再次呼叫 `PQconnectPoll(conn)`。反之，如果 `PQconnectPoll(conn)` 上一次傳回 `PGRES_POLLING_WRITING`，就等待通訊端可供寫入，然後再次呼叫 `PQconnectPoll(conn)`。在第一次循環時，也就是你尚未呼叫 `PQconnectPoll` 時，請視為它上一次傳回了 `PGRES_POLLING_WRITING`。持續此循環，直到 `PQconnectPoll(conn)` 傳回 `PGRES_POLLING_FAILED`（表示連線程序已失敗），或傳回 `PGRES_POLLING_OK`（表示連線已成功建立）。

    在連線過程中的任何時刻，都可以呼叫 [`PQstatus`](libpq-status.md#LIBPQ-PQSTATUS) 來檢查連線的狀態。如果此呼叫傳回 `CONNECTION_BAD`，表示連線程序已失敗；如果傳回 `CONNECTION_OK`，表示連線已就緒。這兩種狀態同樣可以從前述 `PQconnectPoll` 的傳回值偵測出來。在非同步連線程序期間（且只在此期間），也可能出現其他狀態。這些狀態指出連線程序目前所處的階段，例如可能有助於向使用者提供回饋。這些狀態如下：

    <a id="LIBPQ-CONNECTION-STARTED"></a>

    `CONNECTION_STARTED` [#](#LIBPQ-CONNECTION-STARTED)
    :   正在等待連線建立。
    <a id="LIBPQ-CONNECTION-MADE"></a>

    `CONNECTION_MADE` [#](#LIBPQ-CONNECTION-MADE)
    :   連線正常；正在等待傳送。
    <a id="LIBPQ-CONNECTION-AWAITING-RESPONSE"></a>

    `CONNECTION_AWAITING_RESPONSE` [#](#LIBPQ-CONNECTION-AWAITING-RESPONSE)
    :   正在等待伺服器的回應。
    <a id="LIBPQ-CONNECTION-AUTH-OK"></a>

    `CONNECTION_AUTH_OK` [#](#LIBPQ-CONNECTION-AUTH-OK)
    :   已收到認證；正在等待後端完成啟動。
    <a id="LIBPQ-CONNECTION-SSL-STARTUP"></a>

    `CONNECTION_SSL_STARTUP` [#](#LIBPQ-CONNECTION-SSL-STARTUP)
    :   正在協商 SSL 加密。
    <a id="LIBPQ-CONNECTION-GSS-STARTUP"></a>

    `CONNECTION_GSS_STARTUP` [#](#LIBPQ-CONNECTION-GSS-STARTUP)
    :   正在協商 GSS 加密。
    <a id="LIBPQ-CONNECTION-CHECK-WRITABLE"></a>

    `CONNECTION_CHECK_WRITABLE` [#](#LIBPQ-CONNECTION-CHECK-WRITABLE)
    :   正在檢查連線能否處理寫入交易。
    <a id="LIBPQ-CONNECTION-CHECK-STANDBY"></a>

    `CONNECTION_CHECK_STANDBY` [#](#LIBPQ-CONNECTION-CHECK-STANDBY)
    :   正在檢查連線的對象是否為處於備用模式的伺服器。
    <a id="LIBPQ-CONNECTION-CONSUME"></a>

    `CONNECTION_CONSUME` [#](#LIBPQ-CONNECTION-CONSUME)
    :   正在接收連線上剩餘的所有回應訊息。

    請注意，雖然這些常數會保留下來（以維持相容性），但應用程式絕不應該依賴這些狀態以特定順序出現或一定會出現，也不應該依賴狀態一律是這些已記載的值之一。應用程式可以像這樣處理：

    ```

    switch(PQstatus(conn))
    {
            case CONNECTION_STARTED:
                feedback = "Connecting...";
                break;

            case CONNECTION_MADE:
                feedback = "Connected to server...";
                break;
    .
    .
    .
            default:
                feedback = "Connecting...";
    }
    ```

    使用 `PQconnectPoll` 時，`connect_timeout` 連線參數會被忽略；判斷是否已經過太長的時間，是應用程式的責任。除此之外，`PQconnectStart` 加上 `PQconnectPoll` 迴圈等同於 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB)。

    請注意，當 `PQconnectStart` 或 [`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS) 傳回非空指標時，你在使用完畢後必須呼叫 [`PQfinish`](libpq-connect.md#LIBPQ-PQFINISH)，以釋放該結構及任何相關聯的記憶體區塊。即使連線嘗試失敗或被放棄，也必須這麼做。
<a id="LIBPQ-PQSOCKETPOLL"></a>

`PQsocketPoll`<a id="id-1.7.3.8.2.11.6.1.2"></a> [#](#LIBPQ-PQSOCKETPOLL)
:   <a id="id-1.7.3.8.2.11.6.2.1.1"></a>
    輪詢以 [`PQsocket`](libpq-status.md#LIBPQ-PQSOCKET) 取得的連線底層通訊端描述子。此函式的主要用途是逐步完成 [`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS) 說明中所述的連線程序。

    ```

    typedef int64_t pg_usec_time_t;

    int PQsocketPoll(int sock, int forRead, int forWrite,
                     pg_usec_time_t end_time);
    ```

    此函式對檔案描述子進行輪詢，並可選擇設定逾時。如果 *`forRead`* 不為零，函式會在通訊端可供讀取時結束。如果 *`forWrite`* 不為零，函式會在通訊端可供寫入時結束。

    逾時由 *`end_time`* 指定，也就是停止等待的時間，以自 Unix 紀元起算的微秒數表示（亦即 `time_t` 乘以 1 百萬）。如果 *`end_time`* 是 `-1`，逾時為無限。如果 *`end_time`* 是 `0`（或者實際上是現在之前的任何時間），則立即逾時（不阻塞）。逾時值可以方便地透過將所需的微秒數加到 [`PQgetCurrentTimeUSec`](libpq-misc.md#LIBPQ-PQGETCURRENTTIMEUSEC) 的結果上來計算。請注意，底層系統呼叫的精確度可能低於微秒，因此實際的延遲可能不精確。

    如果指定的條件已滿足，函式會傳回大於 `0` 的值；如果發生逾時，傳回 `0`；如果發生錯誤，則傳回 `-1`。錯誤可以透過檢查 `errno(3)` 的值取得。如果 *`forRead`* 與 *`forWrite`* 都為零，函式會立即傳回逾時指示。

    `PQsocketPoll` 依平台不同，以 `poll(2)` 或 `select(2)` 實作。更多資訊請參閱 `poll(2)` 中的 `POLLIN` 與 `POLLOUT`，或 `select(2)` 中的 *`readfds`* 與 *`writefds`*。
<a id="LIBPQ-PQCONNDEFAULTS"></a>

`PQconndefaults`<a id="id-1.7.3.8.2.11.7.1.2"></a> [#](#LIBPQ-PQCONNDEFAULTS)
:   傳回預設的連線選項。

    ```

    PQconninfoOption *PQconndefaults(void);

    typedef struct
    {
        char   *keyword;   /* The keyword of the option */
        char   *envvar;    /* Fallback environment variable name */
        char   *compiled;  /* Fallback compiled in default value */
        char   *val;       /* Option's current value, or NULL */
        char   *label;     /* Label for field in connect dialog */
        char   *dispchar;  /* Indicates how to display this field
                              in a connect dialog. Values are:
                              ""        Display entered value as is
                              "*"       Password field - hide value
                              "D"       Debug option - don't show by default */
        int     dispsize;  /* Field size in characters for dialog */
    } PQconninfoOption;
    ```

    傳回一個連線選項陣列。這可用來找出所有可能的 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB) 選項及其目前的預設值。傳回值指向一個 `PQconninfoOption` 結構的陣列，該陣列以一個 `keyword` 為空指標的項目結尾。如果無法配置記憶體，則傳回空指標。請注意，目前的預設值（`val` 欄位）會取決於環境變數及其他環境狀態。缺少或無效的服務檔會被默默忽略。呼叫者必須將連線選項資料視為唯讀。

    處理完選項陣列之後，請將它傳給 [`PQconninfoFree`](libpq-misc.md#LIBPQ-PQCONNINFOFREE) 以釋放它。如果沒有這麼做，每次呼叫 [`PQconndefaults`](libpq-connect.md#LIBPQ-PQCONNDEFAULTS) 都會洩漏少量記憶體。
<a id="LIBPQ-PQCONNINFO"></a>

`PQconninfo`<a id="id-1.7.3.8.2.11.8.1.2"></a> [#](#LIBPQ-PQCONNINFO)
:   傳回作用中連線所使用的連線選項。

    ```

    PQconninfoOption *PQconninfo(PGconn *conn);
    ```

    傳回一個連線選項陣列。這可用來找出所有可能的 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB) 選項，以及連線到伺服器時所使用的值。傳回值指向一個 `PQconninfoOption` 結構的陣列，該陣列以一個 `keyword` 為空指標的項目結尾。前面關於 [`PQconndefaults`](libpq-connect.md#LIBPQ-PQCONNDEFAULTS) 的所有說明，也適用於 [`PQconninfo`](libpq-connect.md#LIBPQ-PQCONNINFO) 的結果。
<a id="LIBPQ-PQCONNINFOPARSE"></a>

`PQconninfoParse`<a id="id-1.7.3.8.2.11.9.1.2"></a> [#](#LIBPQ-PQCONNINFOPARSE)
:   傳回從所提供之連線字串剖析出的連線選項。

    ```

    PQconninfoOption *PQconninfoParse(const char *conninfo, char **errmsg);
    ```

    剖析連線字串，並以陣列形式傳回產生的選項；如果連線字串有問題，則傳回 `NULL`。此函式可用來取出所提供之連線字串中的 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB) 選項。傳回值指向一個 `PQconninfoOption` 結構的陣列，該陣列以一個 `keyword` 為空指標的項目結尾。

    所有合法的選項都會出現在結果陣列中，但對於連線字串中沒有出現的選項，其 `PQconninfoOption` 的 `val` 會設為 `NULL`；不會填入預設值。

    如果 `errmsg` 不是 `NULL`，那麼成功時 `*errmsg` 會設為 `NULL`，否則設為一個以 `malloc` 配置、說明問題所在的錯誤字串。（`*errmsg` 也可能被設為 `NULL` 而函式傳回 `NULL`；這表示記憶體不足。）

    處理完選項陣列之後，請將它傳給 [`PQconninfoFree`](libpq-misc.md#LIBPQ-PQCONNINFOFREE) 以釋放它。如果沒有這麼做，每次呼叫 [`PQconninfoParse`](libpq-connect.md#LIBPQ-PQCONNINFOPARSE) 都會洩漏一些記憶體。反之，如果發生錯誤且 `errmsg` 不是 `NULL`，請務必使用 [`PQfreemem`](libpq-misc.md#LIBPQ-PQFREEMEM) 釋放錯誤字串。
<a id="LIBPQ-PQFINISH"></a>

`PQfinish`<a id="id-1.7.3.8.2.11.10.1.2"></a> [#](#LIBPQ-PQFINISH)
:   關閉與伺服器的連線。同時釋放 `PGconn` 物件所使用的記憶體。

    ```

    void PQfinish(PGconn *conn);
    ```

    請注意，即使伺服器連線嘗試失敗（由 [`PQstatus`](libpq-status.md#LIBPQ-PQSTATUS) 指出），應用程式仍應呼叫 [`PQfinish`](libpq-connect.md#LIBPQ-PQFINISH) 以釋放 `PGconn` 物件所使用的記憶體。呼叫 [`PQfinish`](libpq-connect.md#LIBPQ-PQFINISH) 之後，就不得再使用 `PGconn` 指標。
<a id="LIBPQ-PQRESET"></a>

`PQreset`<a id="id-1.7.3.8.2.11.11.1.2"></a> [#](#LIBPQ-PQRESET)
:   重設與伺服器之間的通訊通道。

    ```

    void PQreset(PGconn *conn);
    ```

    此函式會關閉與伺服器的連線，並嘗試使用先前用過的所有相同參數建立新連線。如果正常運作的連線中斷，這可能有助於錯誤復原。
<a id="LIBPQ-PQRESETSTART"></a>

`PQresetStart`<a id="id-1.7.3.8.2.11.12.1.2"></a><br>`PQresetPoll`<a id="id-1.7.3.8.2.11.12.2.2"></a> [#](#LIBPQ-PQRESETSTART)
:   以非阻塞方式重設與伺服器之間的通訊通道。

    ```

    int PQresetStart(PGconn *conn);

    PostgresPollingStatusType PQresetPoll(PGconn *conn);
    ```

    這些函式會關閉與伺服器的連線，並嘗試使用先前用過的所有相同參數建立新連線。如果正常運作的連線中斷，這可以用來進行錯誤復原。它們與 [`PQreset`](libpq-connect.md#LIBPQ-PQRESET)（前述）的差別在於它們以非阻塞方式運作。這些函式受到與 [`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS)、`PQconnectStart` 及 `PQconnectPoll` 相同的限制。

    要開始重設連線，請呼叫 [`PQresetStart`](libpq-connect.md#LIBPQ-PQRESETSTART)。如果它傳回 0，表示重設失敗。如果它傳回 1，就使用 `PQresetPoll` 輪詢重設過程，方式與使用 `PQconnectPoll` 建立連線時完全相同。
<a id="LIBPQ-PQPINGPARAMS"></a>

`PQpingParams`<a id="id-1.7.3.8.2.11.13.1.2"></a> [#](#LIBPQ-PQPINGPARAMS)
:   [`PQpingParams`](libpq-connect.md#LIBPQ-PQPINGPARAMS) 回報伺服器的狀態。它接受與前述 [`PQconnectdbParams`](libpq-connect.md#LIBPQ-PQCONNECTDBPARAMS) 完全相同的連線參數。要取得伺服器狀態，不需要提供正確的使用者名稱、密碼或資料庫名稱值；不過，如果提供的值不正確，伺服器會記錄一次失敗的連線嘗試。

    ```

    PGPing PQpingParams(const char * const *keywords,
                        const char * const *values,
                        int expand_dbname);
    ```

    此函式傳回下列值之一：

    <a id="LIBPQ-PQPINGPARAMS-PQPING_OK"></a>

    `PQPING_OK` [#](#LIBPQ-PQPINGPARAMS-PQPING_OK)
    :   伺服器正在執行，而且看起來正在接受連線。
    <a id="LIBPQ-PQPINGPARAMS-PQPING_REJECT"></a>

    `PQPING_REJECT` [#](#LIBPQ-PQPINGPARAMS-PQPING_REJECT)
    :   伺服器正在執行，但處於不允許連線的狀態（啟動中、關閉中或當機復原中）。
    <a id="LIBPQ-PQPINGPARAMS-PQPING_NO_RESPONSE"></a>

    `PQPING_NO_RESPONSE` [#](#LIBPQ-PQPINGPARAMS-PQPING_NO_RESPONSE)
    :   無法與伺服器聯繫。這可能表示伺服器沒有在執行，或者所提供的連線參數有問題（例如連接埠號碼錯誤），或者有網路連通性問題（例如防火牆阻擋了連線請求）。
    <a id="LIBPQ-PQPINGPARAMS-PQPING_NO_ATTEMPT"></a>

    `PQPING_NO_ATTEMPT` [#](#LIBPQ-PQPINGPARAMS-PQPING_NO_ATTEMPT)
    :   沒有嘗試聯繫伺服器，因為所提供的參數明顯不正確，或者用戶端有某些問題（例如記憶體不足）。
<a id="LIBPQ-PQPING"></a>

`PQping`<a id="id-1.7.3.8.2.11.14.1.2"></a> [#](#LIBPQ-PQPING)
:   [`PQping`](libpq-connect.md#LIBPQ-PQPING) 回報伺服器的狀態。它接受與前述 [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB) 完全相同的連線參數。要取得伺服器狀態，不需要提供正確的使用者名稱、密碼或資料庫名稱值；不過，如果提供的值不正確，伺服器會記錄一次失敗的連線嘗試。

    ```

    PGPing PQping(const char *conninfo);
    ```

    傳回值與 [`PQpingParams`](libpq-connect.md#LIBPQ-PQPINGPARAMS) 相同。
<a id="LIBPQ-PQSETSSLKEYPASSHOOK-OPENSSL"></a>

`PQsetSSLKeyPassHook_OpenSSL`<a id="id-1.7.3.8.2.11.15.1.2"></a> [#](#LIBPQ-PQSETSSLKEYPASSHOOK-OPENSSL)
:   `PQsetSSLKeyPassHook_OpenSSL` 讓應用程式可以覆寫 libpq 對[加密之用戶端憑證金鑰檔的預設處理方式](libpq-ssl.md#LIBPQ-SSL-CLIENTCERT)，也就是使用 [sslpassword](libpq-connect.md#LIBPQ-CONNECT-SSLPASSWORD) 或互動式提示。

    ```

    void PQsetSSLKeyPassHook_OpenSSL(PQsslKeyPassHook_OpenSSL_type hook);
    ```

    應用程式傳入一個指向回呼函式的指標，其簽章為：

    ```

    int callback_fn(char *buf, int size, PGconn *conn);
    ```

    之後 libpq 就會呼叫此回呼函式，*取代*其預設的 `PQdefaultSSLKeyPassHook_OpenSSL` 處理函式。回呼函式應該決定金鑰的密碼，並將它複製到大小為 *`size`* 的結果緩衝區 *`buf`*。*`buf`* 中的字串必須以 null 結尾。回呼函式必須傳回儲存在 *`buf`* 中之密碼的長度，不含 null 結尾字元。失敗時，回呼函式應該設定 `buf[0] = '\0'` 並傳回 0。範例請參閱 libpq 原始碼中的 `PQdefaultSSLKeyPassHook_OpenSSL`。

    如果使用者明確指定了金鑰位置，在呼叫回呼函式時，其路徑會存放在 `conn->sslkey` 中。如果使用的是預設金鑰路徑，此值會是空的。對於屬於引擎指定符的金鑰，是否使用 OpenSSL 密碼回呼函式或自行定義處理方式，由引擎實作決定。

    應用程式的回呼函式可以選擇將未處理的情況委派給 `PQdefaultSSLKeyPassHook_OpenSSL`，或者先呼叫它，若它傳回 0 再嘗試其他做法，或者完全覆寫它。

    回呼函式*不得*以例外、`longjmp(...)` 等方式跳脫正常的流程控制。它必須正常地返回。
<a id="LIBPQ-PQGETSSLKEYPASSHOOK-OPENSSL"></a>

`PQgetSSLKeyPassHook_OpenSSL`<a id="id-1.7.3.8.2.11.16.1.2"></a> [#](#LIBPQ-PQGETSSLKEYPASSHOOK-OPENSSL)
:   `PQgetSSLKeyPassHook_OpenSSL` 傳回目前的用戶端憑證金鑰密碼掛鉤；如果尚未設定任何掛鉤，則傳回 `NULL`。

    ```

    PQsslKeyPassHook_OpenSSL_type PQgetSSLKeyPassHook_OpenSSL(void);
    ```

<a id="LIBPQ-CONNSTRING"></a>

### 32.1.1. 連線字串 [#](#LIBPQ-CONNSTRING)

<a id="id-1.7.3.8.3.2"></a><a id="id-1.7.3.8.3.3"></a>

有幾個 libpq 函式會剖析使用者指定的字串以取得連線參數。這些字串有兩種可接受的格式：一般的關鍵字／值字串與 URI。URI 大致上遵循 [RFC
3986](https://datatracker.ietf.org/doc/html/rfc3986)，但允許如下文進一步所述的多主機連線字串。

<a id="LIBPQ-CONNSTRING-KEYWORD-VALUE"></a>

#### 32.1.1.1. 關鍵字／值連線字串 [#](#LIBPQ-CONNSTRING-KEYWORD-VALUE)

在關鍵字／值格式中，每個參數設定的形式為 *`keyword`* `=` *`value`*，設定之間以空白分隔。設定中等號兩側的空白可有可無。要寫入空值或包含空白的值，請以單引號括住，例如 `keyword = 'a value'`。值中的單引號與反斜線必須以反斜線跳脫，也就是 `\'` 與 `\\`。

範例：

```

host=localhost port=5432 dbname=mydb connect_timeout=10
```

可辨識的參數關鍵字列於[第 32.1.2 節](libpq-connect.md#LIBPQ-PARAMKEYWORDS)。

<a id="LIBPQ-CONNSTRING-URIS"></a>

#### 32.1.1.2. 連線 URI [#](#LIBPQ-CONNSTRING-URIS)

連線 URI 的一般形式為：

```

postgresql://[userspec@][hostspec][/dbname][?paramspec]

where userspec is:

user[:password]

and hostspec is:

[host][:port][,...]

and paramspec is:

name=value[&...]
```

URI 架構（scheme）指示符可以是 `postgresql://` 或 `postgres://`。URI 其餘的每個部分都是選用的。下列範例示範有效的 URI 語法：

```

postgresql://
postgresql://localhost
postgresql://localhost:5433
postgresql://localhost/mydb
postgresql://user@localhost
postgresql://user:secret@localhost
postgresql://other@localhost/otherdb?connect_timeout=10&application_name=myapp
postgresql://host1:123,host2:456/somedb?target_session_attrs=any&application_name=myapp
```

通常出現在 URI 階層部分的值，也可以改用具名參數提供。例如：

```

postgresql:///mydb?host=localhost&port=5433
```

所有具名參數都必須符合[第 32.1.2 節](libpq-connect.md#LIBPQ-PARAMKEYWORDS)所列的關鍵字，但為了與 JDBC 連線 URI 相容，`ssl=true` 會被轉換為 `sslmode=require`。

如果連線 URI 的任何部分包含具有特殊意義的符號，就需要以[百分比編碼](https://datatracker.ietf.org/doc/html/rfc3986#section-2.1)進行編碼。以下範例中，等號（`=`）被替換為 `%3D`，空白字元被替換為 `%20`：

```

postgresql://user@localhost:5433/mydb?options=-c%20synchronous_commit%3Doff
```

主機部分可以是主機名稱或 IP 位址。要指定 IPv6 位址，請以方括號括住：

```

postgresql://[2001:db8::1234]/database
```

主機部分的解讀方式與參數 [host](libpq-connect.md#LIBPQ-CONNECT-HOST) 的說明相同。特別是，如果主機部分是空的或看起來像絕對路徑名稱，就會選擇 Unix 網域通訊端連線，否則會發起 TCP/IP 連線。不過請注意，斜線在 URI 的階層部分中是保留字元。因此，要指定非標準的 Unix 網域通訊端目錄，可以省略 URI 的主機部分並將主機指定為具名參數，或者在 URI 的主機部分中對路徑進行百分比編碼：

```

postgresql:///dbname?host=/var/lib/postgresql
postgresql://%2Fvar%2Flib%2Fpostgresql/dbname
```

可以在單一 URI 中指定多個主機元件，每個主機元件都可以選擇性地搭配連接埠元件。形式為 `postgresql://host1:port1,host2:port2,host3:port3/` 的 URI，等同於形式為 `host=host1,host2,host3 port=port1,port2,port3` 的連線字串。如下文進一步所述，會依序嘗試每個主機，直到成功建立連線為止。

<a id="LIBPQ-MULTIPLE-HOSTS"></a>

#### 32.1.1.3. 指定多個主機 [#](#LIBPQ-MULTIPLE-HOSTS)

可以指定多個要連線的主機，讓它們依指定的順序嘗試。在關鍵字／值格式中，`host`、`hostaddr` 與 `port` 選項接受以逗號分隔的值清單。在每個有指定的選項中，必須提供相同數量的元素，例如第一個 `hostaddr` 對應第一個主機名稱，第二個 `hostaddr` 對應第二個主機名稱，依此類推。例外的是，如果只指定了一個 `port`，它會套用到所有主機。

在連線 URI 格式中，你可以在 URI 的 `host` 元件中列出多個以逗號分隔的 `host:port` 配對。

無論使用哪種格式，單一主機名稱都可能解析為多個網路位址。常見的例子是一台同時具有 IPv4 與 IPv6 位址的主機。

當指定了多個主機，或單一主機名稱解析為多個位址時，會依序嘗試所有的主機與位址，直到其中一個成功為止。如果所有主機都無法連上，連線就會失敗。如果成功建立了連線但認證失敗，就不會再嘗試清單中其餘的主機。

如果使用密碼檔，你可以為不同的主機設定不同的密碼。其他所有連線選項對清單中的每個主機都相同；例如，無法為不同的主機指定不同的使用者名稱。

<a id="LIBPQ-PARAMKEYWORDS"></a>

### 32.1.2. 參數關鍵字 [#](#LIBPQ-PARAMKEYWORDS)

目前可辨識的參數關鍵字如下：

<a id="LIBPQ-CONNECT-HOST"></a>

`host` [#](#LIBPQ-CONNECT-HOST)
:   要連線的主機名稱。<a id="id-1.7.3.8.4.2.1.1.2.1.1"></a>如果主機名稱看起來像絕對路徑名稱，它代表使用 Unix 網域通訊而非 TCP/IP 通訊；其值為存放通訊端檔案的目錄名稱。（在 Unix 上，絕對路徑名稱以斜線開頭。在 Windows 上，以磁碟機代號開頭的路徑也會被辨識。）如果主機名稱以 `@` 開頭，它會被視為抽象命名空間中的 Unix 網域通訊端（目前在 Linux 與 Windows 上支援）。未指定 `host` 或其為空時，預設行為是連線到 `/tmp`（或建置 PostgreSQL 時所指定的任何通訊端目錄）中的 Unix 網域通訊端<a id="id-1.7.3.8.4.2.1.1.2.1.4"></a>。在 Windows 上，預設是連線到 `localhost`。

    也接受以逗號分隔的主機名稱清單，此時會依序嘗試清單中的每個主機名稱；清單中的空項目會選用上述的預設行為。詳細資訊請參閱[第 32.1.1.3 節](libpq-connect.md#LIBPQ-MULTIPLE-HOSTS)。
<a id="LIBPQ-CONNECT-HOSTADDR"></a>

`hostaddr` [#](#LIBPQ-CONNECT-HOSTADDR)
:   要連線之主機的數字 IP 位址。它應該採用標準的 IPv4 位址格式，例如 `172.28.40.9`。如果你的機器支援 IPv6，也可以使用 IPv6 位址。當此參數指定為非空字串時，一律使用 TCP/IP 通訊。如果未指定此參數，會查詢 `host` 的值以找出對應的 IP 位址；或者，如果 `host` 指定的是 IP 位址，就直接使用該值。

    使用 `hostaddr` 可讓應用程式避免查詢主機名稱，這對有時間限制的應用程式可能很重要。不過，GSSAPI 或 SSPI 認證方法，以及 `verify-full` SSL 憑證驗證，都需要主機名稱。適用下列規則：

    * 如果指定了 `host` 而沒有指定 `hostaddr`，就會進行主機名稱查詢。（使用 `PQconnectPoll` 時，查詢會在 `PQconnectPoll` 第一次處理此主機名稱時進行，而且可能導致 `PQconnectPoll` 阻塞相當長的時間。）
    * 如果指定了 `hostaddr` 而沒有指定 `host`，`hostaddr` 的值即為伺服器的網路位址。如果認證方法需要主機名稱，連線嘗試將會失敗。
    * 如果同時指定了 `host` 與 `hostaddr`，`hostaddr` 的值即為伺服器的網路位址。除非認證方法需要，否則 `host` 的值會被忽略；若認證方法需要，則它會被用作主機名稱。

    請注意，如果 `host` 不是網路位址 `hostaddr` 上伺服器的名稱，認證很可能會失敗。此外，當同時指定了 `host` 與 `hostaddr` 時，會使用 `host` 在密碼檔中識別此連線（請參閱[第 32.16 節](libpq-pgpass.md)）。

    也接受以逗號分隔的 `hostaddr` 值清單，此時會依序嘗試清單中的每個主機。清單中的空項目會使用對應的主機名稱；如果該主機名稱也是空的，則使用預設主機名稱。詳細資訊請參閱[第 32.1.1.3 節](libpq-connect.md#LIBPQ-MULTIPLE-HOSTS)。

    如果既沒有主機名稱也沒有主機位址，libpq 會使用本機的 Unix 網域通訊端連線；在 Windows 上，則會嘗試連線到 `localhost`。
<a id="LIBPQ-CONNECT-PORT"></a>

`port` [#](#LIBPQ-CONNECT-PORT)
:   伺服器主機上要連線的連接埠號碼，或 Unix 網域連線所用的通訊端檔名副檔名。<a id="id-1.7.3.8.4.2.1.3.2.1.1"></a>如果在 `host` 或 `hostaddr` 參數中提供了多個主機，此參數可以指定一個與主機清單等長、以逗號分隔的連接埠清單，也可以指定一個用於所有主機的單一連接埠號碼。空字串或以逗號分隔之清單中的空項目，代表建置 PostgreSQL 時所設定的預設連接埠號碼。
<a id="LIBPQ-CONNECT-DBNAME"></a>

`dbname` [#](#LIBPQ-CONNECT-DBNAME)
:   資料庫名稱。預設與使用者名稱相同。在某些情境下，會檢查此值是否為延伸格式；這些格式的更多細節請參閱[第 32.1.1 節](libpq-connect.md#LIBPQ-CONNSTRING)。
<a id="LIBPQ-CONNECT-USER"></a>

`user` [#](#LIBPQ-CONNECT-USER)
:   用來連線的 PostgreSQL 使用者名稱。預設與執行應用程式之使用者的作業系統名稱相同。
<a id="LIBPQ-CONNECT-PASSWORD"></a>

`password` [#](#LIBPQ-CONNECT-PASSWORD)
:   伺服器要求密碼認證時所使用的密碼。
<a id="LIBPQ-CONNECT-PASSFILE"></a>

`passfile` [#](#LIBPQ-CONNECT-PASSFILE)
:   指定用來儲存密碼之檔案的名稱（請參閱[第 32.16 節](libpq-pgpass.md)）。預設為 `~/.pgpass`，在 Microsoft Windows 上則為 `%APPDATA%\postgresql\pgpass.conf`。（如果此檔案不存在，不會回報錯誤。）
<a id="LIBPQ-CONNECT-REQUIRE-AUTH"></a>

`require_auth` [#](#LIBPQ-CONNECT-REQUIRE-AUTH)
:   指定用戶端要求伺服器使用的認證方法。如果伺服器沒有使用所要求的方法來認證用戶端，或者伺服器沒有完整完成認證交握，連線就會失敗。也可以提供以逗號分隔的方法清單，伺服器必須恰好使用其中一種方法，連線才會成功。預設情況下，接受任何認證方法，而且伺服器可以完全略過認證。

    方法可以加上 `!` 前綴來表示否定，此時伺服器*不得*嘗試所列的方法；接受任何其他方法，而且伺服器可以完全不認證用戶端。如果提供的是以逗號分隔的清單，伺服器不得嘗試所列否定方法中的*任何*一種。否定形式與非否定形式不可在同一個設定中混用。

    最後一個特殊情況是，`none` 方法要求伺服器不得使用認證挑戰。（它也可以被否定，以要求某種形式的認證。）

    可以指定下列方法：

    `password`
    :   伺服器必須要求明文密碼認證。

    `md5`
    :   伺服器必須要求 MD5 雜湊密碼認證。

        ### 警告

        MD5 加密密碼的支援已被棄用，並將在 PostgreSQL 的未來版本中移除。關於遷移到其他密碼類型的細節，請參閱[第 20.5 節](../../server-administration/client-authentication/auth-password.md)。

    `gss`
    :   伺服器必須透過 GSSAPI 要求 Kerberos 交握，或建立 GSS 加密通道（另請參閱 [gssencmode](libpq-connect.md#LIBPQ-CONNECT-GSSENCMODE)）。

    `sspi`
    :   伺服器必須要求 Windows SSPI 認證。

    `scram-sha-256`
    :   伺服器必須與用戶端成功完成 SCRAM-SHA-256 認證交換。

    `oauth`
    :   伺服器必須向用戶端要求 OAuth 持有者權杖。

    `none`
    :   伺服器不得要求用戶端進行認證交換。（這既不禁止透過 TLS 的用戶端憑證認證，也不禁止透過其加密傳輸的 GSS 認證。）
<a id="LIBPQ-CONNECT-CHANNEL-BINDING"></a>

`channel_binding` [#](#LIBPQ-CONNECT-CHANNEL-BINDING)
:   此選項控制用戶端對通道綁定的使用。設定為 `require` 表示連線必須採用通道綁定；`prefer` 表示若可用，用戶端會選擇通道綁定；`disable` 則禁止使用通道綁定。如果 PostgreSQL 編譯時有 SSL 支援，預設值為 `prefer`；否則預設值為 `disable`。

    通道綁定是伺服器向用戶端認證自身的一種方法。只有在透過 SSL 連線、連到使用 `SCRAM` 認證方法的 PostgreSQL 11 或更新版本伺服器時，才支援此功能。
<a id="LIBPQ-CONNECT-CONNECT-TIMEOUT"></a>

`connect_timeout` [#](#LIBPQ-CONNECT-CONNECT-TIMEOUT)
:   連線時等待的最長時間，以秒為單位（寫成十進位整數，例如 `10`）。零、負值或未指定表示無限期等待。此逾時分別套用於每個主機名稱或 IP 位址。例如，如果你指定了兩個主機，且 `connect_timeout` 為 5，那麼每個主機在 5 秒內沒有建立連線就會逾時，因此等待連線所花的總時間最多可能達 10 秒。
<a id="LIBPQ-CONNECT-CLIENT-ENCODING"></a>

`client_encoding` [#](#LIBPQ-CONNECT-CLIENT-ENCODING)
:   為此連線設定 `client_encoding` 組態參數。除了對應的伺服器選項所接受的值之外，你也可以使用 `auto`，從用戶端目前的區域設定（在 Unix 系統上為 `LC_CTYPE` 環境變數）判斷正確的編碼。
<a id="LIBPQ-CONNECT-OPTIONS"></a>

`options` [#](#LIBPQ-CONNECT-OPTIONS)
:   指定在連線開始時要傳送給伺服器的命令列選項。例如，將此設為 `-c geqo=off` 或 `--geqo=off`，會將工作階段中 `geqo` 參數的值設為 `off`。此字串中的空白會被視為命令列引數的分隔符，除非以反斜線（`\`）跳脫；要表示字面上的反斜線，請寫 `\\`。關於可用選項的詳細討論，請參閱[第 19 章](../../server-administration/runtime-config/README.md)。
<a id="LIBPQ-CONNECT-APPLICATION-NAME"></a>

`application_name` [#](#LIBPQ-CONNECT-APPLICATION-NAME)
:   指定 [application_name](../../server-administration/runtime-config/runtime-config-logging.md#GUC-APPLICATION-NAME) 組態參數的值。
<a id="LIBPQ-CONNECT-FALLBACK-APPLICATION-NAME"></a>

`fallback_application_name` [#](#LIBPQ-CONNECT-FALLBACK-APPLICATION-NAME)
:   指定 [application_name](../../server-administration/runtime-config/runtime-config-logging.md#GUC-APPLICATION-NAME) 組態參數的備用值。如果沒有透過連線參數或 `PGAPPNAME` 環境變數為 `application_name` 提供值，就會使用此值。對於希望設定預設應用程式名稱、但允許使用者覆寫的通用工具程式而言，指定備用名稱很有用。
<a id="LIBPQ-KEEPALIVES"></a>

`keepalives` [#](#LIBPQ-KEEPALIVES)
:   控制是否使用用戶端的 TCP keepalive。預設值為 1，表示開啟；但如果不需要 keepalive，你可以將它改為 0，表示關閉。對於透過 Unix 網域通訊端建立的連線，此參數會被忽略。
<a id="LIBPQ-KEEPALIVES-IDLE"></a>

`keepalives_idle` [#](#LIBPQ-KEEPALIVES-IDLE)
:   控制閒置多少秒之後，TCP 應該向伺服器傳送 keepalive 訊息。值為零表示使用系統預設值。對於透過 Unix 網域通訊端建立的連線，或者停用了 keepalive 時，此參數會被忽略。只有在提供 `TCP_KEEPIDLE` 或同等通訊端選項的系統上，以及在 Windows 上才支援此參數；在其他系統上沒有作用。
<a id="LIBPQ-KEEPALIVES-INTERVAL"></a>

`keepalives_interval` [#](#LIBPQ-KEEPALIVES-INTERVAL)
:   控制未獲伺服器確認的 TCP keepalive 訊息應在多少秒之後重新傳送。值為零表示使用系統預設值。對於透過 Unix 網域通訊端建立的連線，或者停用了 keepalive 時，此參數會被忽略。只有在提供 `TCP_KEEPINTVL` 或同等通訊端選項的系統上，以及在 Windows 上才支援此參數；在其他系統上沒有作用。
<a id="LIBPQ-KEEPALIVES-COUNT"></a>

`keepalives_count` [#](#LIBPQ-KEEPALIVES-COUNT)
:   控制在用戶端與伺服器的連線被視為中斷之前，可以遺失多少個 TCP keepalive。值為零表示使用系統預設值。對於透過 Unix 網域通訊端建立的連線，或者停用了 keepalive 時，此參數會被忽略。只有在提供 `TCP_KEEPCNT` 或同等通訊端選項的系統上才支援此參數；在其他系統上沒有作用。
<a id="LIBPQ-TCP-USER-TIMEOUT"></a>

`tcp_user_timeout` [#](#LIBPQ-TCP-USER-TIMEOUT)
:   控制已傳送的資料在連線被強制關閉之前，可以維持未確認狀態多少毫秒。值為零表示使用系統預設值。對於透過 Unix 網域通訊端建立的連線，此參數會被忽略。只有在提供 `TCP_USER_TIMEOUT` 的系統上才支援此參數；在其他系統上沒有作用。
<a id="LIBPQ-CONNECT-REPLICATION"></a>

`replication` [#](#LIBPQ-CONNECT-REPLICATION)
:   此選項決定連線是否應該使用複寫協定而非一般協定。PostgreSQL 的複寫連線以及 pg_basebackup 等工具在內部使用的就是這個協定，但第三方應用程式也可以使用它。關於複寫協定的說明，請參閱[第 54.4 節](../../internals/protocol/protocol-replication.md)。

    支援下列值，不區分大小寫：

    `true`, `on`, `yes`, `1`
    :   連線進入實體複寫模式。

    `database`
    :   連線進入邏輯複寫模式，連線到 `dbname` 參數所指定的資料庫。

    `false`, `off`, `no`, `0`
    :   連線為一般連線，這是預設行為。

    在實體或邏輯複寫模式中，只能使用簡單查詢協定。
<a id="LIBPQ-CONNECT-GSSENCMODE"></a>

`gssencmode` [#](#LIBPQ-CONNECT-GSSENCMODE)
:   此選項決定是否要與伺服器協商安全的 GSS TCP/IP 連線，或以何種優先順序協商。共有三種模式：

    `disable`
    :   只嘗試未使用 GSSAPI 加密的連線

    `prefer`（預設）
    :   如果存在 GSSAPI 憑證（也就是在憑證快取中），先嘗試 GSSAPI 加密連線；如果失敗或沒有憑證，再嘗試未使用 GSSAPI 加密的連線。當 PostgreSQL 編譯時有 GSSAPI 支援，這是預設值。

    `require`
    :   只嘗試 GSSAPI 加密連線

    對於 Unix 網域通訊端通訊，`gssencmode` 會被忽略。如果 PostgreSQL 編譯時沒有 GSSAPI 支援，使用 `require` 選項會導致錯誤，而 `prefer` 雖會被接受，但 libpq 實際上不會嘗試 GSSAPI 加密連線。<a id="id-1.7.3.8.4.2.1.21.2.2.7"></a>
<a id="LIBPQ-CONNECT-SSLMODE"></a>

`sslmode` [#](#LIBPQ-CONNECT-SSLMODE)
:   此選項決定是否要與伺服器協商安全的 SSL TCP/IP 連線，或以何種優先順序協商。共有六種模式：

    `disable`
    :   只嘗試非 SSL 連線

    `allow`
    :   先嘗試非 SSL 連線；如果失敗，再嘗試 SSL 連線

    `prefer`（預設）
    :   先嘗試 SSL 連線；如果失敗，再嘗試非 SSL 連線

    `require`
    :   只嘗試 SSL 連線。如果存在根 CA 檔，就以與指定 `verify-ca` 時相同的方式驗證憑證

    `verify-ca`
    :   只嘗試 SSL 連線，並驗證伺服器憑證是由受信任的憑證授權單位（CA）所簽發

    `verify-full`
    :   只嘗試 SSL 連線，驗證伺服器憑證是由受信任的 CA 所簽發，並且所要求的伺服器主機名稱與憑證中的名稱相符

    關於這些選項如何運作的詳細說明，請參閱[第 32.19 節](libpq-ssl.md)。

    對於 Unix 網域通訊端通訊，`sslmode` 會被忽略。如果 PostgreSQL 編譯時沒有 SSL 支援，使用 `require`、`verify-ca` 或 `verify-full` 選項會導致錯誤，而 `allow` 與 `prefer` 選項雖會被接受，但 libpq 實際上不會嘗試 SSL 連線。<a id="id-1.7.3.8.4.2.1.22.2.2.10"></a>

    請注意，如果可以使用 GSSAPI 加密，無論 `sslmode` 的值為何，都會優先使用它而非 SSL 加密。要在具有可運作之 GSSAPI 基礎架構（例如 Kerberos 伺服器）的環境中強制使用 SSL 加密，請同時將 `gssencmode` 設為 `disable`。
<a id="LIBPQ-CONNECT-REQUIRESSL"></a>

`requiressl` [#](#LIBPQ-CONNECT-REQUIRESSL)
:   此選項已被棄用，請改用 `sslmode` 設定。

    如果設為 1，就要求與伺服器建立 SSL 連線（這等同於 `sslmode` `require`）。此時如果伺服器不接受 SSL 連線，libpq 會拒絕連線。如果設為 0（預設），libpq 會與伺服器協商連線類型（等同於 `sslmode` `prefer`）。只有在 PostgreSQL 編譯時有 SSL 支援的情況下，才能使用此選項。
<a id="LIBPQ-CONNECT-SSLNEGOTIATION"></a>

`sslnegotiation` [#](#LIBPQ-CONNECT-SSLNEGOTIATION)
:   如果使用 SSL，此選項控制如何與伺服器協商 SSL 加密。在預設的 `postgres` 模式中，用戶端會先詢問伺服器是否支援 SSL。在 `direct` 模式中，用戶端會在建立 TCP/IP 連線後直接開始標準的 SSL 交握。傳統的 PostgreSQL 協定協商對於各種伺服器設定最具彈性。如果已知伺服器支援直接 SSL 連線，後者可以少一次往返，降低連線延遲，也允許使用與協定無關的 SSL 網路工具。直接 SSL 選項是在 PostgreSQL 第 17 版引入的。

    `postgres`
    :   執行 PostgreSQL 協定協商。如果未提供此選項，這是預設值。

    `direct`
    :   在建立 TCP/IP 連線後直接開始 SSL 交握。只有在 `sslmode=require` 或更高等級時才允許這麼做，因為較弱的設定可能在伺服器不支援直接 SSL 交握時，導致非預期地退回明文認證。
<a id="LIBPQ-CONNECT-SSLCOMPRESSION"></a>

`sslcompression` [#](#LIBPQ-CONNECT-SSLCOMPRESSION)
:   如果設為 1，透過 SSL 連線傳送的資料會被壓縮。如果設為 0，則停用壓縮。預設值為 0。如果建立的是沒有 SSL 的連線，此參數會被忽略。

    SSL 壓縮如今被認為不安全，已不再建議使用。OpenSSL 1.1.0 預設停用壓縮，許多作業系統發行版在更早的版本中也停用了壓縮，因此如果伺服器不接受壓縮，將此參數設為開啟不會有任何效果。PostgreSQL 14 已在後端完全停用壓縮。

    如果安全性不是首要考量，在網路是瓶頸的情況下，壓縮可以提升傳輸量。如果 CPU 效能是限制因素，停用壓縮可以改善回應時間與傳輸量。
<a id="LIBPQ-CONNECT-SSLCERT"></a>

`sslcert` [#](#LIBPQ-CONNECT-SSLCERT)
:   此參數指定用戶端 SSL 憑證的檔案名稱，取代預設的 `~/.postgresql/postgresql.crt`。如果沒有建立 SSL 連線，此參數會被忽略。
<a id="LIBPQ-CONNECT-SSLKEY"></a>

`sslkey` [#](#LIBPQ-CONNECT-SSLKEY)
:   此參數指定用戶端憑證所用之私密金鑰的位置。它可以指定一個檔案名稱，用來取代預設的 `~/.postgresql/postgresql.key`；也可以指定從外部「引擎」取得的金鑰（引擎是 OpenSSL 的可載入模組）。外部引擎的指定應由以冒號分隔的引擎名稱與引擎特定的金鑰識別碼組成。如果沒有建立 SSL 連線，此參數會被忽略。
<a id="LIBPQ-CONNECT-SSLKEYLOGFILE"></a>

`sslkeylogfile` [#](#LIBPQ-CONNECT-SSLKEYLOGFILE)
:   此參數指定 libpq 記錄此 SSL 上下文中所用金鑰的位置。這對於使用 Wireshark 等網路檢測工具對 PostgreSQL 協定互動或用戶端連線進行除錯很有用。如果沒有建立 SSL 連線，或者使用的是 LibreSSL（LibreSSL 不支援金鑰記錄），此參數會被忽略。金鑰會以 NSS 格式記錄。

    ### 警告

    金鑰記錄會在金鑰記錄檔（keylog file）中暴露可能敏感的資訊。金鑰記錄檔應該與 [sslkey](libpq-connect.md#LIBPQ-CONNECT-SSLKEY) 檔案一樣謹慎處理。
<a id="LIBPQ-CONNECT-SSLPASSWORD"></a>

`sslpassword` [#](#LIBPQ-CONNECT-SSLPASSWORD)
:   此參數指定 `sslkey` 中所指定之私密金鑰的密碼，讓用戶端憑證的私鑰即使在無法實際以互動方式輸入通關密語時，也能以加密形式儲存在磁碟上。

    以任何非空值指定此參數，都會抑制 OpenSSL 在加密的用戶端憑證金鑰提供給 libpq 時預設會發出的 `Enter PEM pass phrase:` 提示。

    如果金鑰沒有加密，此參數會被忽略。此參數對由 OpenSSL 引擎指定的金鑰沒有作用，除非該引擎使用 OpenSSL 的密碼回呼機制來進行提示。

    此選項沒有對應的環境變數，也沒有在 `.pgpass` 中查詢它的機制。它可以用在服務檔的連線定義中。用途較複雜的使用者應該考慮使用 OpenSSL 引擎，以及 PKCS#11 或 USB 加密卸載裝置等工具。
<a id="LIBPQ-CONNECT-SSLCERTMODE"></a>

`sslcertmode` [#](#LIBPQ-CONNECT-SSLCERTMODE)
:   此選項決定是否可以將用戶端憑證傳送給伺服器，以及伺服器是否必須要求憑證。共有三種模式：

    `disable`
    :   即使有可用的用戶端憑證（位於預設位置或透過 [sslcert](libpq-connect.md#LIBPQ-CONNECT-SSLCERT) 提供），也絕不傳送。

    `allow`（預設）
    :   如果伺服器要求憑證，而且用戶端有憑證可傳送，就可以傳送憑證。

    `require`
    :   伺服器*必須*要求憑證。如果用戶端沒有傳送憑證，而伺服器仍成功認證了用戶端，連線就會失敗。

    ### 注意

    `sslcertmode=require` 並不會增加任何額外的安全性，因為無法保證伺服器會正確驗證憑證；無論 PostgreSQL 伺服器是否驗證用戶端的 TLS 憑證，通常都會向用戶端要求憑證。在為較複雜的 TLS 設定進行疑難排解時，此選項可能有用。
<a id="LIBPQ-CONNECT-SSLROOTCERT"></a>

`sslrootcert` [#](#LIBPQ-CONNECT-SSLROOTCERT)
:   此參數指定包含 SSL 憑證授權單位（CA）憑證的檔案名稱。如果該檔案存在，會驗證伺服器的憑證是否由這些授權單位之一所簽署。預設值為 `~/.postgresql/root.crt`。

    也可以改為指定特殊值 `system`，此時會載入 SSL 實作所提供的受信任 CA 根憑證。這些根憑證的確切位置因 SSL 實作與平台而異。特別是對 OpenSSL 而言，這些位置還可以再由 `SSL_CERT_DIR` 與 `SSL_CERT_FILE` 環境變數修改。

    ### 注意

    使用 `sslrootcert=system` 時，預設的 `sslmode` 會改為 `verify-full`，而任何較弱的設定都會導致錯誤。在大多數情況下，任何人都能輕易地為自己所控制的主機名稱取得受系統信任的憑證，使得 `verify-ca` 及所有更弱的模式毫無用處。

    特殊的 `system` 值會優先於同名的本機憑證檔。如果因為某些原因你遇到這種情況，請改用其他路徑，例如 `sslrootcert=./system`。
<a id="LIBPQ-CONNECT-SSLCRL"></a>

`sslcrl` [#](#LIBPQ-CONNECT-SSLCRL)
:   此參數指定 SSL 伺服器憑證撤銷清單（CRL）的檔案名稱。在嘗試認證伺服器憑證時，會拒絕此檔案（若存在）中所列的憑證。如果 [sslcrl](libpq-connect.md#LIBPQ-CONNECT-SSLCRL) 與 [sslcrldir](libpq-connect.md#LIBPQ-CONNECT-SSLCRLDIR) 都沒有設定，此設定會被視為 `~/.postgresql/root.crl`。
<a id="LIBPQ-CONNECT-SSLCRLDIR"></a>

`sslcrldir` [#](#LIBPQ-CONNECT-SSLCRLDIR)
:   此參數指定 SSL 伺服器憑證撤銷清單（CRL）的目錄名稱。在嘗試認證伺服器憑證時，會拒絕此目錄（若存在）中各檔案所列的憑證。

    此目錄需要以 OpenSSL 命令 `openssl rehash` 或 `c_rehash` 準備。詳細資訊請參閱其文件。

    `sslcrl` 與 `sslcrldir` 可以同時指定。
<a id="LIBPQ-CONNECT-SSLSNI"></a>

`sslsni`<a id="id-1.7.3.8.4.2.1.34.1.2"></a> [#](#LIBPQ-CONNECT-SSLSNI)
:   如果設為 1（預設），libpq 會在啟用 SSL 的連線上設定 TLS 擴充「伺服器名稱指示」（Server Name Indication，SNI）。將此參數設為 0 即可關閉此功能。

    支援 SSL 的代理伺服器可以利用伺服器名稱指示來路由連線，而不必解密 SSL 串流。（請注意，除非代理伺服器能夠識別 PostgreSQL 協定交握，否則這需要將 `sslnegotiation` 設為 `direct`。）不過，SNI 會讓目的主機名稱以明文出現在網路流量中，因此在某些情況下可能並不理想。
<a id="LIBPQ-CONNECT-REQUIREPEER"></a>

`requirepeer` [#](#LIBPQ-CONNECT-REQUIREPEER)
:   此參數指定伺服器的作業系統使用者名稱，例如 `requirepeer=postgres`。建立 Unix 網域通訊端連線時，如果設定了此參數，用戶端會在連線開始時檢查伺服器程序是否以指定的使用者名稱執行；如果不是，連線會因錯誤而中止。此參數可用來提供伺服器認證，類似於 TCP/IP 連線上以 SSL 憑證所提供的認證。（請注意，如果 Unix 網域通訊端位於 `/tmp` 或其他可被公眾寫入的位置，任何使用者都可以啟動一個在該處監聽的伺服器。請使用此參數確保你所連線的是由受信任使用者執行的伺服器。）只有在已實作 `peer` 認證方法的平台上才支援此選項；請參閱[第 20.9 節](../../server-administration/client-authentication/auth-peer.md)。
<a id="LIBPQ-CONNECT-SSL-MIN-PROTOCOL-VERSION"></a>

`ssl_min_protocol_version` [#](#LIBPQ-CONNECT-SSL-MIN-PROTOCOL-VERSION)
:   此參數指定連線所允許的最低 SSL/TLS 協定版本。有效值為 `TLSv1`、`TLSv1.1`、`TLSv1.2` 與 `TLSv1.3`。所支援的協定取決於所使用的 OpenSSL 版本，較舊的版本不支援最新的協定版本。如果未指定，預設值為 `TLSv1.2`，這符合撰寫本文時的業界最佳實務。
<a id="LIBPQ-CONNECT-SSL-MAX-PROTOCOL-VERSION"></a>

`ssl_max_protocol_version` [#](#LIBPQ-CONNECT-SSL-MAX-PROTOCOL-VERSION)
:   此參數指定連線所允許的最高 SSL/TLS 協定版本。有效值為 `TLSv1`、`TLSv1.1`、`TLSv1.2` 與 `TLSv1.3`。所支援的協定取決於所使用的 OpenSSL 版本，較舊的版本不支援最新的協定版本。如果未設定，此參數會被忽略，連線將使用後端所定義的上限（如果有設定的話）。設定最高協定版本主要用於測試，或某些元件在使用較新的協定時有問題的情況。
<a id="LIBPQ-CONNECT-MIN-PROTOCOL-VERSION"></a>

`min_protocol_version` [#](#LIBPQ-CONNECT-MIN-PROTOCOL-VERSION)
:   指定連線所允許的最低協定版本。預設允許 libpq 所支援的任何 PostgreSQL 協定版本，目前也就是 `3.0`。如果伺服器連這個協定版本都不支援，連線將會被關閉。

    目前支援的值為 `3.0`、`3.2` 與 `latest`。`latest` 值等同於所使用之 libpq 版本所支援的最新協定版本，目前為 `3.2`。
<a id="LIBPQ-CONNECT-MAX-PROTOCOL-VERSION"></a>

`max_protocol_version` [#](#LIBPQ-CONNECT-MAX-PROTOCOL-VERSION)
:   指定要向伺服器請求的協定版本。預設使用 PostgreSQL 協定的 `3.0` 版，除非連線字串指定了依賴更高協定版本的功能，此時會使用 libpq 所支援的最新版本。如果伺服器不支援用戶端所請求的協定版本，連線會自動降級為伺服器所支援的較低次要協定版本。連線嘗試完成後，你可以使用 [`PQfullProtocolVersion`](libpq-status.md#LIBPQ-PQFULLPROTOCOLVERSION) 找出實際協商出的確切協定版本。

    目前支援的值為 `3.0`、`3.2` 與 `latest`。`latest` 值等同於所使用之 libpq 版本所支援的最新協定版本，目前為 `3.2`。
<a id="LIBPQ-CONNECT-KRBSRVNAME"></a>

`krbsrvname` [#](#LIBPQ-CONNECT-KRBSRVNAME)
:   以 GSSAPI 進行認證時所使用的 Kerberos 服務名稱。它必須與伺服器設定中所指定的服務名稱相符，Kerberos 認證才能成功。（另請參閱[第 20.6 節](../../server-administration/client-authentication/gssapi-auth.md)。）預設值通常是 `postgres`，但可以在建置 PostgreSQL 時透過 configure 的 `--with-krb-srvnam` 選項變更。在大多數環境中，此參數從來不需要變更。某些 Kerberos 實作可能需要不同的服務名稱，例如 Microsoft Active Directory 要求服務名稱為大寫（`POSTGRES`）。
<a id="LIBPQ-CONNECT-GSSLIB"></a>

`gsslib` [#](#LIBPQ-CONNECT-GSSLIB)
:   用於 GSSAPI 認證的 GSS 函式庫。目前除了同時包含 GSSAPI 與 SSPI 支援的 Windows 建置版本之外，此參數都會被忽略。在該情況下，將此參數設為 `gssapi`，可讓 libpq 使用 GSSAPI 函式庫進行認證，而不是使用預設的 SSPI。
<a id="LIBPQ-CONNECT-GSSDELEGATION"></a>

`gssdelegation` [#](#LIBPQ-CONNECT-GSSDELEGATION)
:   將 GSS 憑證轉送（委派）給伺服器。預設值為 `0`，表示不會將憑證轉送給伺服器。將此設為 `1`，可在可能時轉送憑證。
<a id="LIBPQ-CONNECT-SCRAM-CLIENT-KEY"></a>

`scram_client_key` [#](#LIBPQ-CONNECT-SCRAM-CLIENT-KEY)
:   以 base64 編碼的 SCRAM 用戶端金鑰。外部資料包裝器或類似的中介軟體可以用它來啟用 SCRAM 直通（pass-through）認證。其中一種實作請參閱[第 F.38.1.10 節](../../appendixes/contrib/postgres-fdw.md#POSTGRES-FDW-OPTIONS-CONNECTION-MANAGEMENT)。它並非供使用者或用戶端應用程式直接指定。
<a id="LIBPQ-CONNECT-SCRAM-SERVER-KEY"></a>

`scram_server_key` [#](#LIBPQ-CONNECT-SCRAM-SERVER-KEY)
:   以 base64 編碼的 SCRAM 伺服器金鑰。外部資料包裝器或類似的中介軟體可以用它來啟用 SCRAM 直通（pass-through）認證。其中一種實作請參閱[第 F.38.1.10 節](../../appendixes/contrib/postgres-fdw.md#POSTGRES-FDW-OPTIONS-CONNECTION-MANAGEMENT)。它並非供使用者或用戶端應用程式直接指定。
<a id="LIBPQ-CONNECT-SERVICE"></a>

`service` [#](#LIBPQ-CONNECT-SERVICE)
:   用於取得額外參數的服務名稱。它指定 `pg_service.conf` 中保存額外連線參數的服務名稱。這讓應用程式只需指定服務名稱，連線參數便可集中維護。請參閱[第 32.17 節](libpq-pgservice.md)。
<a id="LIBPQ-CONNECT-TARGET-SESSION-ATTRS"></a>

`target_session_attrs` [#](#LIBPQ-CONNECT-TARGET-SESSION-ATTRS)
:   此選項決定工作階段是否必須具備某些屬性才可被接受。它通常與多個主機名稱搭配使用，以便在數個主機中選出第一個可接受的候選。共有六種模式：

    `any`（預設）
    :   任何成功的連線都可接受

    `read-write`
    :   工作階段預設必須接受讀寫交易（也就是說，伺服器不得處於熱待命模式，而且 `default_transaction_read_only` 參數必須為 `off`）

    `read-only`
    :   工作階段預設不得接受讀寫交易（與前者相反）

    `primary`
    :   伺服器不得處於熱待命模式

    `standby`
    :   伺服器必須處於熱待命模式

    `prefer-standby`
    :   先嘗試尋找待命伺服器，但如果所列的主機都不是待命伺服器，就以 `any` 模式再試一次
<a id="LIBPQ-CONNECT-LOAD-BALANCE-HOSTS"></a>

`load_balance_hosts` [#](#LIBPQ-CONNECT-LOAD-BALANCE-HOSTS)
:   控制用戶端嘗試連線到可用主機與位址的順序。一旦某次連線嘗試成功，就不會再嘗試其他主機與位址。此參數通常與多個主機名稱，或會傳回多個 IP 的 DNS 紀錄搭配使用。此參數可以與 [target_session_attrs](libpq-connect.md#LIBPQ-CONNECT-TARGET-SESSION-ATTRS) 搭配使用，例如只在待命伺服器之間進行負載平衡。成功連線後，在傳回之連線上的後續查詢都會送到同一台伺服器。目前有兩種模式：

    `disable`（預設）
    :   不在主機之間進行負載平衡。主機會依提供的順序嘗試，位址則依從 DNS 或 hosts 檔案收到的順序嘗試。

    `random`
    :   主機與位址會以隨機順序嘗試。此值主要適用於同時開啟多個連線的情況，這些連線可能來自不同的機器。如此一來，連線便可在多台 PostgreSQL 伺服器之間進行負載平衡。

        雖然隨機負載平衡由於其隨機的本質，幾乎永遠不會產生完全均勻的分布，但在統計上會相當接近。這裡有一個重要的面向：此演算法使用兩層隨機選擇。首先，主機會以隨機順序解析。其次，在解析下一個主機之前，會以隨機順序嘗試目前主機的所有已解析位址。在某些情況下，這種行為可能會大幅扭曲每個節點所獲得的連線數量，例如某些主機解析出的位址比其他主機多的時候。但也可以刻意利用這種偏差，例如在主機字串中多次提供較大型伺服器的主機名稱，以增加它所獲得的連線數量。

        使用此值時，建議同時為 [connect_timeout](libpq-connect.md#LIBPQ-CONNECT-CONNECT-TIMEOUT) 設定一個合理的值。如此一來，如果用於負載平衡的某個節點沒有回應，就會嘗試新的節點。
<a id="LIBPQ-CONNECT-OAUTH-ISSUER"></a>

`oauth_issuer` [#](#LIBPQ-CONNECT-OAUTH-ISSUER)
:   伺服器為此連線要求 OAuth 權杖時，所要聯繫之受信任核發者的 HTTPS URL。此參數對所有 OAuth 連線都是必要的；它應該與[伺服器 HBA 設定](../../server-administration/client-authentication/auth-oauth.md)中的 `issuer` 設定完全相符。

    在標準認證交握的過程中，libpq 會向伺服器索取一份*發現文件（discovery document）：*也就是提供一組 OAuth 設定參數的 URL。伺服器必須提供一個直接由 `oauth_issuer` 的各組成部分建構而成的 URL，而且此值必須與發現文件本身所宣告的核發者識別碼完全相符，否則連線將會失敗。這是為了防範針對 OAuth 用戶端的一類[「混淆攻擊」（mix-up attacks）](https://mailarchive.ietf.org/arch/msg/oauth/JIVxFBGsJBVtm7ljwJhPUm3Fr-w/)所必需的。

    你也可以將 `oauth_issuer` 明確設為用於 OAuth 發現的 `/.well-known/` URI。在這種情況下，如果伺服器要求不同的 URL，連線將會失敗，但[自訂 OAuth 流程](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS)也許能透過使用先前快取的權杖來加快標準交握。（在這種情況下，建議也設定 [oauth_scope](libpq-connect.md#LIBPQ-CONNECT-OAUTH-SCOPE)，因為用戶端將沒有機會向伺服器詢問正確的範圍設定，而權杖的預設範圍可能不足以建立連線。）libpq 目前支援下列眾所周知的端點：

    * `/.well-known/openid-configuration`
    * `/.well-known/oauth-authorization-server`

    ### 警告

    在 OAuth 連線交握期間，核發者擁有很高的權限。根據經驗法則，如果你不信任某個 URL 的營運者處理對你伺服器的存取，或直接冒充你，那麼該 URL 就不應被信任為 `oauth_issuer`。
<a id="LIBPQ-CONNECT-OAUTH-CLIENT-ID"></a>

`oauth_client_id` [#](#LIBPQ-CONNECT-OAUTH-CLIENT-ID)
:   由授權伺服器所核發的 OAuth 2.0 用戶端識別碼。如果 PostgreSQL 伺服器為此連線[要求 OAuth 權杖](../../server-administration/client-authentication/auth-oauth.md)（而且沒有安裝[自訂 OAuth 掛鉤](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS)來提供權杖），就必須設定此參數；否則連線將會失敗。
<a id="LIBPQ-CONNECT-OAUTH-CLIENT-SECRET"></a>

`oauth_client_secret` [#](#LIBPQ-CONNECT-OAUTH-CLIENT-SECRET)
:   聯繫 OAuth 授權伺服器時所使用的用戶端密碼（如果有的話）。此參數是否為必要，由 OAuth 提供者決定；「公開」（public）用戶端通常不使用祕密（secret），而「機密」（confidential）用戶端通常會使用。
<a id="LIBPQ-CONNECT-OAUTH-SCOPE"></a>

`oauth_scope` [#](#LIBPQ-CONNECT-OAUTH-SCOPE)
:   傳送給授權伺服器之存取請求的範圍，以 OAuth 範圍識別碼組成、以空白分隔的清單（可能為空）來指定。此參數是選用的，供進階用途使用。

    通常用戶端會從 PostgreSQL 伺服器取得適當的範圍設定。如果使用了此參數，伺服器所要求的範圍清單將被忽略。這可以防止較不受信任的伺服器向終端使用者要求不適當的存取範圍。不過，如果用戶端的範圍設定沒有包含伺服器所需的範圍，伺服器很可能會拒絕所核發的權杖，連線也將會失敗。

    空範圍清單的意義取決於提供者。OAuth 授權伺服器可以選擇核發具有「預設範圍」（無論那恰好是什麼）的權杖，也可能完全拒絕該權杖請求。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-connect.html)（原文版本：18.6；核對日期：2026-10-18）
