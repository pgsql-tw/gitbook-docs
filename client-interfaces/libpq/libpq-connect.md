<a id="LIBPQ-CONNECT"></a>

## 32.1. 資料庫連線控制函式 [#](#libpq-connect) <a href="#libpq-connect" id="libpq-connect"></a>

[32.1.1. 連線字串](libpq-connstring.md#libpq-connstring)

[32.1.2. 參數關鍵字](libpq-paramkeywords.md#libpq-paramkeywords)

下列函式用於建立與 PostgreSQL 後端伺服器的連線。一個應用程式可以同時開啟多個後端連線。（這麼做的原因之一是為了存取超過一個資料庫。）每個連線都以一個 `PGconn`<a id="id-1.7.3.8.2.3"></a> 物件表示，此物件可由函式 [`PQconnectdb`](libpq-connect.md#libpq-pqconnectdb)、[`PQconnectdbParams`](libpq-connect.md#libpq-pqconnectdbparams) 或 [`PQsetdbLogin`](libpq-connect.md#libpq-pqsetdblogin) 取得。請注意，這些函式一律會傳回非空的物件指標，除非（或許）記憶體少到連 `PGconn` 物件都無法配置。在透過連線物件送出查詢之前，應該呼叫 [`PQstatus`](libpq-status.md#libpq-pqstatus) 函式，檢查傳回值以確認連線成功。

### 警告

如果不受信任的使用者可以存取一個尚未採用[安全綱要使用模式](../../the-sql-language/ddl/ddl-schemas.md#DDL-SCHEMAS-PATTERNS)的資料庫，請在每個工作階段開始時，從 `search_path` 中移除可被公眾寫入的綱要。做法之一是將參數關鍵字 `options` 設為值 `-csearch_path=`。或者，也可以在連線後執行 `PQexec(conn, "SELECT
pg_catalog.set_config('search_path', '', false)")`。這項考量並非 libpq 所特有；它適用於每一種可執行任意 SQL 命令的介面。

### 警告

在 Unix 上，於持有已開啟 libpq 連線的情況下 fork 程序，可能導致無法預期的結果，因為父程序與子程序會共用相同的通訊端與作業系統資源。因此不建議這樣使用；不過，從子程序執行 `exec` 來載入新的執行檔是安全的。

<a id="LIBPQ-PQCONNECTDBPARAMS"></a>

### `PQconnectdbParams`<a id="id-1.7.3.8.2.11.1.1.2"></a> [#](#libpq-pqconnectdbparams) <a href="#libpq-pqconnectdbparams" id="libpq-pqconnectdbparams"></a>

建立與資料庫伺服器的新連線。

```

    PGconn *PQconnectdbParams(const char * const *keywords,
                              const char * const *values,
                              int expand_dbname);
```

此函式使用取自兩個以 `NULL` 結尾之陣列的參數來開啟新的資料庫連線。第一個陣列 `keywords` 定義為字串陣列，每個字串是一個關鍵字。第二個陣列 `values` 提供每個關鍵字的值。與下面的 [`PQsetdbLogin`](libpq-connect.md#libpq-pqsetdblogin) 不同，參數集合可以在不變更函式簽章的情況下擴充，因此開發新的應用程式時，建議使用此函式（或其非阻塞版本 [`PQconnectStartParams`](libpq-connect.md#libpq-pqconnectstartparams) 與 `PQconnectPoll`）。

目前可辨識的參數關鍵字列於[第 32.1.2 節](libpq-paramkeywords.md#libpq-paramkeywords)。

傳入的陣列可以是空的，以使用全部的預設參數；也可以包含一個或多個參數設定。兩個陣列的長度必須相符。處理會在 `keywords` 陣列中第一個 `NULL` 項目處停止。此外，如果與某個非 `NULL` 之 `keywords` 項目相對應的 `values` 項目是 `NULL` 或空字串，該項目會被忽略，並繼續處理下一組陣列項目。

當 `expand_dbname` 不為零時，會檢查第一個 *`dbname`* 關鍵字的值是否為*連線字串*。若是，就會將其「展開」為從字串中取出的個別連線參數。如果該值包含等號（`=`），或以 URI 架構（scheme）指示符開頭，就會被視為連線字串，而不只是資料庫名稱。（連線字串格式的更多細節見[第 32.1.1 節](libpq-connstring.md#libpq-connstring)。）只有第一次出現的 *`dbname`* 會以這種方式處理；之後的任何 *`dbname`* 參數都會當作一般的資料庫名稱處理。

一般而言，參數陣列會從頭到尾依序處理。如果有任何關鍵字重複出現，會使用最後一個值（非 `NULL` 且非空者）。這項規則特別適用於連線字串中的關鍵字與 `keywords` 陣列中的關鍵字衝突的情況。因此，程式設計者可以決定陣列項目能否覆寫連線字串中取得的值，或能否被其覆寫。出現在展開的 *`dbname`* 項目之前的陣列項目，可以被連線字串的欄位覆寫；而這些欄位又會被出現在 *`dbname`* 之後的陣列項目覆寫（但同樣地，只有在這些項目提供非空值時才會如此）。

處理完所有陣列項目與任何展開的連線字串之後，仍未設定的連線參數會以預設值填入。如果未設定之參數所對應的環境變數（請參閱[第 32.15 節](libpq-envars.md)）有設定，就使用它的值。如果環境變數也沒有設定，則使用該參數的內建預設值。

<a id="LIBPQ-PQCONNECTDB"></a>

### `PQconnectdb`<a id="id-1.7.3.8.2.11.2.1.2"></a> [#](#libpq-pqconnectdb) <a href="#libpq-pqconnectdb" id="libpq-pqconnectdb"></a>

建立與資料庫伺服器的新連線。

```

    PGconn *PQconnectdb(const char *conninfo);
```

此函式使用取自字串 `conninfo` 的參數來開啟新的資料庫連線。

傳入的字串可以是空的，以使用全部的預設參數；也可以包含一個或多個以空白分隔的參數設定；或者可以包含一個 URI。詳細資訊請參閱[第 32.1.1 節](libpq-connstring.md#libpq-connstring)。

<a id="LIBPQ-PQSETDBLOGIN"></a>

### `PQsetdbLogin`<a id="id-1.7.3.8.2.11.3.1.2"></a> [#](#libpq-pqsetdblogin) <a href="#libpq-pqsetdblogin" id="libpq-pqsetdblogin"></a>

建立與資料庫伺服器的新連線。

```

    PGconn *PQsetdbLogin(const char *pghost,
                         const char *pgport,
                         const char *pgoptions,
                         const char *pgtty,
                         const char *dbName,
                         const char *login,
                         const char *pwd);
```

這是 [`PQconnectdb`](libpq-connect.md#libpq-pqconnectdb) 的前身，具有固定的參數集合。它的功能相同，只是缺少的參數一律會採用預設值。對於任何要使用預設值的固定參數，請寫入 `NULL` 或空字串。

如果 *`dbName`* 包含 `=` 符號或具有有效的連線 URI 前綴，它會被當作 *`conninfo`* 字串，處理方式與傳給 [`PQconnectdb`](libpq-connect.md#libpq-pqconnectdb) 時完全相同，接著其餘參數再依 [`PQconnectdbParams`](libpq-connect.md#libpq-pqconnectdbparams) 所述的方式套用。

`pgtty` 已不再使用，傳入的任何值都會被忽略。

<a id="LIBPQ-PQSETDB"></a>

### `PQsetdb`<a id="id-1.7.3.8.2.11.4.1.2"></a> [#](#libpq-pqsetdb) <a href="#libpq-pqsetdb" id="libpq-pqsetdb"></a>

建立與資料庫伺服器的新連線。

```

    PGconn *PQsetdb(char *pghost,
                    char *pgport,
                    char *pgoptions,
                    char *pgtty,
                    char *dbName);
```

這是一個巨集，它呼叫 [`PQsetdbLogin`](libpq-connect.md#libpq-pqsetdblogin)，並以空指標作為 *`login`* 與 *`pwd`* 參數。提供它是為了與非常舊的程式保持向後相容性。

<a id="LIBPQ-PQCONNECTSTARTPARAMS"></a>

### `PQconnectStartParams`<a id="id-1.7.3.8.2.11.5.1.2"></a><br>`PQconnectStart`<a id="id-1.7.3.8.2.11.5.2.2"></a><br><a id="LIBPQ-PQCONNECTPOLL"></a>`PQconnectPoll`<a id="id-1.7.3.8.2.11.5.3.2"></a> [#](#libpq-pqconnectstartparams) <a href="#libpq-pqconnectstartparams" id="libpq-pqconnectstartparams"></a>

<a id="id-1.7.3.8.2.11.5.4.1.1"></a>
以非阻塞方式建立與資料庫伺服器的連線。

```

    PGconn *PQconnectStartParams(const char * const *keywords,
                                 const char * const *values,
                                 int expand_dbname);

    PGconn *PQconnectStart(const char *conninfo);

    PostgresPollingStatusType PQconnectPoll(PGconn *conn);
```

這三個函式用於開啟與資料庫伺服器的連線，且在過程中不會讓應用程式的執行緒因遠端 I/O 而阻塞。這種做法的重點在於，等待 I/O 完成的動作可以發生在應用程式的主迴圈中，而不是在 [`PQconnectdbParams`](libpq-connect.md#libpq-pqconnectdbparams) 或 [`PQconnectdb`](libpq-connect.md#libpq-pqconnectdb) 內部，因此應用程式可以在進行此操作的同時處理其他工作。

使用 [`PQconnectStartParams`](libpq-connect.md#libpq-pqconnectstartparams) 時，資料庫連線會使用取自 `keywords` 與 `values` 陣列的參數建立，並由 `expand_dbname` 控制，如前面 [`PQconnectdbParams`](libpq-connect.md#libpq-pqconnectdbparams) 所述。

使用 `PQconnectStart` 時，資料庫連線會使用取自字串 `conninfo` 的參數建立，如前面 [`PQconnectdb`](libpq-connect.md#libpq-pqconnectdb) 所述。

只要滿足下列幾項限制，[`PQconnectStartParams`](libpq-connect.md#libpq-pqconnectstartparams)、`PQconnectStart` 與 `PQconnectPoll` 都不會阻塞：

* 必須適當地使用 `hostaddr` 參數，以避免進行 DNS 查詢。詳細資訊請參閱[第 32.1.2 節](libpq-paramkeywords.md#libpq-paramkeywords)中此參數的說明。
* 如果你呼叫 [`PQtrace`](libpq-control.md#libpq-pqtrace)，請確保追蹤輸出所寫入的串流物件不會阻塞。
* 你必須確保在呼叫 `PQconnectPoll` 之前，通訊端處於適當的狀態，如下所述。

要開始一個非阻塞的連線請求，請呼叫 `PQconnectStart` 或 [`PQconnectStartParams`](libpq-connect.md#libpq-pqconnectstartparams)。如果結果為空（null），表示 libpq 無法配置新的 `PGconn` 結構。否則會傳回一個有效的 `PGconn` 指標（不過它尚未代表一個有效的資料庫連線）。接著呼叫 `PQstatus(conn)`。如果結果是 `CONNECTION_BAD`，表示連線嘗試已經失敗，通常是因為連線參數無效。

如果 `PQconnectStart` 或 [`PQconnectStartParams`](libpq-connect.md#libpq-pqconnectstartparams) 成功，下一階段是輪詢 libpq，讓它可以繼續進行連線程序。使用 `PQsocket(conn)` 取得資料庫連線底層通訊端的描述子。（注意：不要假設通訊端在多次 `PQconnectPoll` 呼叫之間保持不變。）依下列方式循環：如果 `PQconnectPoll(conn)` 上一次傳回 `PGRES_POLLING_READING`，就等待通訊端可供讀取（由 `select()`、`poll()` 或類似的系統函式指出）。請注意，如果你的系統上有 `select(2)` 或 `poll(2)`，`PQsocketPoll` 可以將其設定抽象化，有助於減少樣板程式碼。然後再次呼叫 `PQconnectPoll(conn)`。反之，如果 `PQconnectPoll(conn)` 上一次傳回 `PGRES_POLLING_WRITING`，就等待通訊端可供寫入，然後再次呼叫 `PQconnectPoll(conn)`。在第一次循環時，也就是你尚未呼叫 `PQconnectPoll` 時，請視為它上一次傳回了 `PGRES_POLLING_WRITING`。持續此循環，直到 `PQconnectPoll(conn)` 傳回 `PGRES_POLLING_FAILED`（表示連線程序已失敗），或傳回 `PGRES_POLLING_OK`（表示連線已成功建立）。

在連線過程中的任何時刻，都可以呼叫 [`PQstatus`](libpq-status.md#libpq-pqstatus) 來檢查連線的狀態。如果此呼叫傳回 `CONNECTION_BAD`，表示連線程序已失敗；如果傳回 `CONNECTION_OK`，表示連線已就緒。這兩種狀態同樣可以從前述 `PQconnectPoll` 的傳回值偵測出來。在非同步連線程序期間（且只在此期間），也可能出現其他狀態。這些狀態指出連線程序目前所處的階段，例如可能有助於向使用者提供回饋。這些狀態如下：

- <a id="LIBPQ-CONNECTION-STARTED"></a>`CONNECTION_STARTED` [#](#LIBPQ-CONNECTION-STARTED)

  正在等待連線建立。

- <a id="LIBPQ-CONNECTION-MADE"></a>`CONNECTION_MADE` [#](#LIBPQ-CONNECTION-MADE)

  連線正常；正在等待傳送。

- <a id="LIBPQ-CONNECTION-AWAITING-RESPONSE"></a>`CONNECTION_AWAITING_RESPONSE` [#](#LIBPQ-CONNECTION-AWAITING-RESPONSE)

  正在等待伺服器的回應。

- <a id="LIBPQ-CONNECTION-AUTH-OK"></a>`CONNECTION_AUTH_OK` [#](#LIBPQ-CONNECTION-AUTH-OK)

  已收到認證；正在等待後端完成啟動。

- <a id="LIBPQ-CONNECTION-SSL-STARTUP"></a>`CONNECTION_SSL_STARTUP` [#](#LIBPQ-CONNECTION-SSL-STARTUP)

  正在協商 SSL 加密。

- <a id="LIBPQ-CONNECTION-GSS-STARTUP"></a>`CONNECTION_GSS_STARTUP` [#](#LIBPQ-CONNECTION-GSS-STARTUP)

  正在協商 GSS 加密。

- <a id="LIBPQ-CONNECTION-CHECK-WRITABLE"></a>`CONNECTION_CHECK_WRITABLE` [#](#LIBPQ-CONNECTION-CHECK-WRITABLE)

  正在檢查連線能否處理寫入交易。

- <a id="LIBPQ-CONNECTION-CHECK-STANDBY"></a>`CONNECTION_CHECK_STANDBY` [#](#LIBPQ-CONNECTION-CHECK-STANDBY)

  正在檢查連線的對象是否為處於備用模式的伺服器。

- <a id="LIBPQ-CONNECTION-CONSUME"></a>`CONNECTION_CONSUME` [#](#LIBPQ-CONNECTION-CONSUME)

  正在接收連線上剩餘的所有回應訊息。

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

使用 `PQconnectPoll` 時，`connect_timeout` 連線參數會被忽略；判斷是否已經過太長的時間，是應用程式的責任。除此之外，`PQconnectStart` 加上 `PQconnectPoll` 迴圈等同於 [`PQconnectdb`](libpq-connect.md#libpq-pqconnectdb)。

請注意，當 `PQconnectStart` 或 [`PQconnectStartParams`](libpq-connect.md#libpq-pqconnectstartparams) 傳回非空指標時，你在使用完畢後必須呼叫 [`PQfinish`](libpq-connect.md#libpq-pqfinish)，以釋放該結構及任何相關聯的記憶體區塊。即使連線嘗試失敗或被放棄，也必須這麼做。

<a id="LIBPQ-PQSOCKETPOLL"></a>

### `PQsocketPoll`<a id="id-1.7.3.8.2.11.6.1.2"></a> [#](#libpq-pqsocketpoll) <a href="#libpq-pqsocketpoll" id="libpq-pqsocketpoll"></a>

<a id="id-1.7.3.8.2.11.6.2.1.1"></a>
輪詢以 [`PQsocket`](libpq-status.md#libpq-pqsocket) 取得的連線底層通訊端描述子。此函式的主要用途是逐步完成 [`PQconnectStartParams`](libpq-connect.md#libpq-pqconnectstartparams) 說明中所述的連線程序。

```

    typedef int64_t pg_usec_time_t;

    int PQsocketPoll(int sock, int forRead, int forWrite,
                     pg_usec_time_t end_time);
```

此函式對檔案描述子進行輪詢，並可選擇設定逾時。如果 *`forRead`* 不為零，函式會在通訊端可供讀取時結束。如果 *`forWrite`* 不為零，函式會在通訊端可供寫入時結束。

逾時由 *`end_time`* 指定，也就是停止等待的時間，以自 Unix 紀元起算的微秒數表示（亦即 `time_t` 乘以 1 百萬）。如果 *`end_time`* 是 `-1`，逾時為無限。如果 *`end_time`* 是 `0`（或者實際上是現在之前的任何時間），則立即逾時（不阻塞）。逾時值可以方便地透過將所需的微秒數加到 [`PQgetCurrentTimeUSec`](libpq-misc.md#libpq-pqgetcurrenttimeusec) 的結果上來計算。請注意，底層系統呼叫的精確度可能低於微秒，因此實際的延遲可能不精確。

如果指定的條件已滿足，函式會傳回大於 `0` 的值；如果發生逾時，傳回 `0`；如果發生錯誤，則傳回 `-1`。錯誤可以透過檢查 `errno(3)` 的值取得。如果 *`forRead`* 與 *`forWrite`* 都為零，函式會立即傳回逾時指示。

`PQsocketPoll` 依平台不同，以 `poll(2)` 或 `select(2)` 實作。更多資訊請參閱 `poll(2)` 中的 `POLLIN` 與 `POLLOUT`，或 `select(2)` 中的 *`readfds`* 與 *`writefds`*。

<a id="LIBPQ-PQCONNDEFAULTS"></a>

### `PQconndefaults`<a id="id-1.7.3.8.2.11.7.1.2"></a> [#](#libpq-pqconndefaults) <a href="#libpq-pqconndefaults" id="libpq-pqconndefaults"></a>

傳回預設的連線選項。

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

傳回一個連線選項陣列。這可用來找出所有可能的 [`PQconnectdb`](libpq-connect.md#libpq-pqconnectdb) 選項及其目前的預設值。傳回值指向一個 `PQconninfoOption` 結構的陣列，該陣列以一個 `keyword` 為空指標的項目結尾。如果無法配置記憶體，則傳回空指標。請注意，目前的預設值（`val` 欄位）會取決於環境變數及其他環境狀態。缺少或無效的服務檔會被默默忽略。呼叫者必須將連線選項資料視為唯讀。

處理完選項陣列之後，請將它傳給 [`PQconninfoFree`](libpq-misc.md#libpq-pqconninfofree) 以釋放它。如果沒有這麼做，每次呼叫 [`PQconndefaults`](libpq-connect.md#libpq-pqconndefaults) 都會洩漏少量記憶體。

<a id="LIBPQ-PQCONNINFO"></a>

### `PQconninfo`<a id="id-1.7.3.8.2.11.8.1.2"></a> [#](#libpq-pqconninfo) <a href="#libpq-pqconninfo" id="libpq-pqconninfo"></a>

傳回作用中連線所使用的連線選項。

```

    PQconninfoOption *PQconninfo(PGconn *conn);
```

傳回一個連線選項陣列。這可用來找出所有可能的 [`PQconnectdb`](libpq-connect.md#libpq-pqconnectdb) 選項，以及連線到伺服器時所使用的值。傳回值指向一個 `PQconninfoOption` 結構的陣列，該陣列以一個 `keyword` 為空指標的項目結尾。前面關於 [`PQconndefaults`](libpq-connect.md#libpq-pqconndefaults) 的所有說明，也適用於 [`PQconninfo`](libpq-connect.md#libpq-pqconninfo) 的結果。

<a id="LIBPQ-PQCONNINFOPARSE"></a>

### `PQconninfoParse`<a id="id-1.7.3.8.2.11.9.1.2"></a> [#](#libpq-pqconninfoparse) <a href="#libpq-pqconninfoparse" id="libpq-pqconninfoparse"></a>

傳回從所提供之連線字串剖析出的連線選項。

```

    PQconninfoOption *PQconninfoParse(const char *conninfo, char **errmsg);
```

剖析連線字串，並以陣列形式傳回產生的選項；如果連線字串有問題，則傳回 `NULL`。此函式可用來取出所提供之連線字串中的 [`PQconnectdb`](libpq-connect.md#libpq-pqconnectdb) 選項。傳回值指向一個 `PQconninfoOption` 結構的陣列，該陣列以一個 `keyword` 為空指標的項目結尾。

所有合法的選項都會出現在結果陣列中，但對於連線字串中沒有出現的選項，其 `PQconninfoOption` 的 `val` 會設為 `NULL`；不會填入預設值。

如果 `errmsg` 不是 `NULL`，那麼成功時 `*errmsg` 會設為 `NULL`，否則設為一個以 `malloc` 配置、說明問題所在的錯誤字串。（`*errmsg` 也可能被設為 `NULL` 而函式傳回 `NULL`；這表示記憶體不足。）

處理完選項陣列之後，請將它傳給 [`PQconninfoFree`](libpq-misc.md#libpq-pqconninfofree) 以釋放它。如果沒有這麼做，每次呼叫 [`PQconninfoParse`](libpq-connect.md#libpq-pqconninfoparse) 都會洩漏一些記憶體。反之，如果發生錯誤且 `errmsg` 不是 `NULL`，請務必使用 [`PQfreemem`](libpq-misc.md#libpq-pqfreemem) 釋放錯誤字串。

<a id="LIBPQ-PQFINISH"></a>

### `PQfinish`<a id="id-1.7.3.8.2.11.10.1.2"></a> [#](#libpq-pqfinish) <a href="#libpq-pqfinish" id="libpq-pqfinish"></a>

關閉與伺服器的連線。同時釋放 `PGconn` 物件所使用的記憶體。

```

    void PQfinish(PGconn *conn);
```

請注意，即使伺服器連線嘗試失敗（由 [`PQstatus`](libpq-status.md#libpq-pqstatus) 指出），應用程式仍應呼叫 [`PQfinish`](libpq-connect.md#libpq-pqfinish) 以釋放 `PGconn` 物件所使用的記憶體。呼叫 [`PQfinish`](libpq-connect.md#libpq-pqfinish) 之後，就不得再使用 `PGconn` 指標。

<a id="LIBPQ-PQRESET"></a>

### `PQreset`<a id="id-1.7.3.8.2.11.11.1.2"></a> [#](#libpq-pqreset) <a href="#libpq-pqreset" id="libpq-pqreset"></a>

重設與伺服器之間的通訊通道。

```

    void PQreset(PGconn *conn);
```

此函式會關閉與伺服器的連線，並嘗試使用先前用過的所有相同參數建立新連線。如果正常運作的連線中斷，這可能有助於錯誤復原。

<a id="LIBPQ-PQRESETSTART"></a>

### `PQresetStart`<a id="id-1.7.3.8.2.11.12.1.2"></a><br>`PQresetPoll`<a id="id-1.7.3.8.2.11.12.2.2"></a> [#](#libpq-pqresetstart) <a href="#libpq-pqresetstart" id="libpq-pqresetstart"></a>

以非阻塞方式重設與伺服器之間的通訊通道。

```

    int PQresetStart(PGconn *conn);

    PostgresPollingStatusType PQresetPoll(PGconn *conn);
```

這些函式會關閉與伺服器的連線，並嘗試使用先前用過的所有相同參數建立新連線。如果正常運作的連線中斷，這可以用來進行錯誤復原。它們與 [`PQreset`](libpq-connect.md#libpq-pqreset)（前述）的差別在於它們以非阻塞方式運作。這些函式受到與 [`PQconnectStartParams`](libpq-connect.md#libpq-pqconnectstartparams)、`PQconnectStart` 及 `PQconnectPoll` 相同的限制。

要開始重設連線，請呼叫 [`PQresetStart`](libpq-connect.md#libpq-pqresetstart)。如果它傳回 0，表示重設失敗。如果它傳回 1，就使用 `PQresetPoll` 輪詢重設過程，方式與使用 `PQconnectPoll` 建立連線時完全相同。

<a id="LIBPQ-PQPINGPARAMS"></a>

### `PQpingParams`<a id="id-1.7.3.8.2.11.13.1.2"></a> [#](#libpq-pqpingparams) <a href="#libpq-pqpingparams" id="libpq-pqpingparams"></a>

[`PQpingParams`](libpq-connect.md#libpq-pqpingparams) 回報伺服器的狀態。它接受與前述 [`PQconnectdbParams`](libpq-connect.md#libpq-pqconnectdbparams) 完全相同的連線參數。要取得伺服器狀態，不需要提供正確的使用者名稱、密碼或資料庫名稱值；不過，如果提供的值不正確，伺服器會記錄一次失敗的連線嘗試。

```

    PGPing PQpingParams(const char * const *keywords,
                        const char * const *values,
                        int expand_dbname);
```

此函式傳回下列值之一：

- <a id="LIBPQ-PQPINGPARAMS-PQPING_OK"></a>`PQPING_OK` [#](#LIBPQ-PQPINGPARAMS-PQPING_OK)

  伺服器正在執行，而且看起來正在接受連線。

- <a id="LIBPQ-PQPINGPARAMS-PQPING_REJECT"></a>`PQPING_REJECT` [#](#LIBPQ-PQPINGPARAMS-PQPING_REJECT)

  伺服器正在執行，但處於不允許連線的狀態（啟動中、關閉中或當機復原中）。

- <a id="LIBPQ-PQPINGPARAMS-PQPING_NO_RESPONSE"></a>`PQPING_NO_RESPONSE` [#](#LIBPQ-PQPINGPARAMS-PQPING_NO_RESPONSE)

  無法與伺服器聯繫。這可能表示伺服器沒有在執行，或者所提供的連線參數有問題（例如連接埠號碼錯誤），或者有網路連通性問題（例如防火牆阻擋了連線請求）。

- <a id="LIBPQ-PQPINGPARAMS-PQPING_NO_ATTEMPT"></a>`PQPING_NO_ATTEMPT` [#](#LIBPQ-PQPINGPARAMS-PQPING_NO_ATTEMPT)

  沒有嘗試聯繫伺服器，因為所提供的參數明顯不正確，或者用戶端有某些問題（例如記憶體不足）。

<a id="LIBPQ-PQPING"></a>

### `PQping`<a id="id-1.7.3.8.2.11.14.1.2"></a> [#](#libpq-pqping) <a href="#libpq-pqping" id="libpq-pqping"></a>

[`PQping`](libpq-connect.md#libpq-pqping) 回報伺服器的狀態。它接受與前述 [`PQconnectdb`](libpq-connect.md#libpq-pqconnectdb) 完全相同的連線參數。要取得伺服器狀態，不需要提供正確的使用者名稱、密碼或資料庫名稱值；不過，如果提供的值不正確，伺服器會記錄一次失敗的連線嘗試。

```

    PGPing PQping(const char *conninfo);
```

傳回值與 [`PQpingParams`](libpq-connect.md#libpq-pqpingparams) 相同。

<a id="LIBPQ-PQSETSSLKEYPASSHOOK-OPENSSL"></a>

### `PQsetSSLKeyPassHook_OpenSSL`<a id="id-1.7.3.8.2.11.15.1.2"></a> [#](#libpq-pqsetsslkeypasshook-openssl) <a href="#libpq-pqsetsslkeypasshook-openssl" id="libpq-pqsetsslkeypasshook-openssl"></a>

`PQsetSSLKeyPassHook_OpenSSL` 讓應用程式可以覆寫 libpq 對[加密之用戶端憑證金鑰檔的預設處理方式](libpq-ssl.md#libpq-ssl-clientcert)，也就是使用 [sslpassword](libpq-paramkeywords.md#libpq-connect-sslpassword) 或互動式提示。

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

### `PQgetSSLKeyPassHook_OpenSSL`<a id="id-1.7.3.8.2.11.16.1.2"></a> [#](#libpq-pqgetsslkeypasshook-openssl) <a href="#libpq-pqgetsslkeypasshook-openssl" id="libpq-pqgetsslkeypasshook-openssl"></a>

`PQgetSSLKeyPassHook_OpenSSL` 傳回目前的用戶端憑證金鑰密碼掛鉤；如果尚未設定任何掛鉤，則傳回 `NULL`。

```

    PQsslKeyPassHook_OpenSSL_type PQgetSSLKeyPassHook_OpenSSL(void);
```

<a id="LIBPQ-CONNSTRING"></a>

### 32.1.1. 連線字串 [#](#libpq-connstring) <a href="#libpq-connstring" id="libpq-connstring"></a>

[閱讀完整小節：32.1.1. 連線字串](libpq-connstring.md#libpq-connstring)

<a id="LIBPQ-PARAMKEYWORDS"></a>

### 32.1.2. 參數關鍵字 [#](#libpq-paramkeywords) <a href="#libpq-paramkeywords" id="libpq-paramkeywords"></a>

[閱讀完整小節：32.1.2. 參數關鍵字](libpq-paramkeywords.md#libpq-paramkeywords)


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-connect.html)（原文版本：18.6；核對日期：2026-10-18）
