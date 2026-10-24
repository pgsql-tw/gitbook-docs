<a id="LIBPQ-CANCEL"></a>

## 32.7. 取消進行中的查詢 [#](#libpq-cancel) <a href="#libpq-cancel" id="libpq-cancel"></a>

[32.7.1. 傳送取消請求的函式](libpq-cancel.md#libpq-cancel-functions)

[32.7.2. 已過時的傳送取消請求函式](libpq-cancel.md#libpq-cancel-deprecated)

<a id="id-1.7.3.14.2"></a><a id="id-1.7.3.14.3"></a>

<a id="LIBPQ-CANCEL-FUNCTIONS"></a>

### 32.7.1. 傳送取消請求的函式 [#](#libpq-cancel-functions) <a href="#libpq-cancel-functions" id="libpq-cancel-functions"></a>

<a id="LIBPQ-PQCANCELCREATE"></a>

`PQcancelCreate`<a id="id-1.7.3.14.4.2.1.1.2"></a> [#](#LIBPQ-PQCANCELCREATE)

準備一個可用來傳送取消請求的連線。

```

    PGcancelConn *PQcancelCreate(PGconn *conn);
```

[`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE) 會建立一個 `PGcancelConn`<a id="id-1.7.3.14.4.2.1.2.2.3"></a> 物件，但不會立即開始透過此連線傳送取消請求。取消請求可以使用 [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) 以阻塞的方式透過此連線傳送，也可以使用 [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART) 以非阻塞的方式傳送。傳回值可以傳給 [`PQcancelStatus`](libpq-cancel.md#LIBPQ-PQCANCELSTATUS)，以檢查 `PGcancelConn` 物件是否已成功建立。`PGcancelConn` 物件是不透明的結構，不打算讓應用程式直接存取。此 `PGcancelConn` 物件可用來以執行緒安全的方式取消原始連線上正在執行的查詢。

為取消請求建立連線時，會重複使用原始用戶端的許多連線參數。重要的是，如果原始連線要求連線加密及（或）驗證目標主機（使用 `sslmode` 或 `gssencmode`），那麼為取消請求建立的連線也會套用這些相同的要求。不過，只在認證期間或用戶端認證之後才使用的連線選項都會被忽略，因為取消請求不需要認證，而且連線會在取消請求送出後立即關閉。

請注意，當 `PQcancelCreate` 傳回非 null 指標時，你在用完之後必須呼叫 [`PQcancelFinish`](libpq-cancel.md#LIBPQ-PQCANCELFINISH)，以釋放該結構以及任何相關的記憶體區塊。即使取消請求失敗或被放棄，也必須這樣做。

<a id="LIBPQ-PQCANCELBLOCKING"></a>

`PQcancelBlocking`<a id="id-1.7.3.14.4.2.2.1.2"></a> [#](#LIBPQ-PQCANCELBLOCKING)

以阻塞的方式請求伺服器放棄處理目前的命令。

```

    int PQcancelBlocking(PGcancelConn *cancelConn);
```

此請求是透過給定的 `PGcancelConn` 發出的，該物件需要以 [`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE) 建立。若取消請求已成功送出，[`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) 的傳回值為 1，否則為 0。若不成功，可以使用 [`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE) 取得錯誤訊息。

不過，成功送出取消請求並不保證該請求會產生任何效果。如果取消生效，被取消的命令會提早終止並傳回錯誤結果。如果取消失敗（例如，因為伺服器已經處理完該命令），則完全不會有任何可見的結果。

<a id="LIBPQ-PQCANCELSTART"></a>

`PQcancelStart`<a id="id-1.7.3.14.4.2.3.1.2"></a><br>`PQcancelPoll`<a id="id-1.7.3.14.4.2.3.2.2"></a> [#](#LIBPQ-PQCANCELSTART)

以非阻塞的方式請求伺服器放棄處理目前的命令。

```

    int PQcancelStart(PGcancelConn *cancelConn);

    PostgresPollingStatusType PQcancelPoll(PGcancelConn *cancelConn);
```

此請求是透過給定的 `PGcancelConn` 發出的，該物件需要以 [`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE) 建立。若取消請求能夠開始，[`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART) 的傳回值為 1，否則為 0。若不成功，可以使用 [`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE) 取得錯誤訊息。

若 `PQcancelStart` 成功，下一個階段是輪詢 libpq，讓它能夠繼續進行取消連線的流程。請使用 [`PQcancelSocket`](libpq-cancel.md#LIBPQ-PQCANCELSOCKET) 取得資料庫連線底層通訊端的描述子。（小心：不要假設通訊端在多次 `PQcancelPoll` 呼叫之間會保持不變。）迴圈的進行方式如下：若 `PQcancelPoll(cancelConn)` 上一次傳回 `PGRES_POLLING_READING`，請等待通訊端可讀取（由 `select()`、`poll()` 或類似的系統函式指示）。然後再次呼叫 `PQcancelPoll(cancelConn)`。反之，若 `PQcancelPoll(cancelConn)` 上一次傳回 `PGRES_POLLING_WRITING`，請等待通訊端可寫入，然後再次呼叫 `PQcancelPoll(cancelConn)`。在第一次迭代時，也就是你尚未呼叫過 `PQcancelPoll(cancelConn)` 時，請視同它上一次傳回 `PGRES_POLLING_WRITING` 來處理。持續這個迴圈，直到 `PQcancelPoll(cancelConn)` 傳回 `PGRES_POLLING_FAILED`（表示連線流程已失敗），或傳回 `PGRES_POLLING_OK`（表示取消請求已成功送出）為止。

不過，成功送出取消請求並不保證該請求會產生任何效果。如果取消生效，被取消的命令會提早終止並傳回錯誤結果。如果取消失敗（例如，因為伺服器已經處理完該命令），則完全不會有任何可見的結果。

在連線期間的任何時候，都可以呼叫 [`PQcancelStatus`](libpq-cancel.md#LIBPQ-PQCANCELSTATUS) 來檢查連線的狀態。若此呼叫傳回 `CONNECTION_BAD`，表示取消流程已失敗；若此呼叫傳回 `CONNECTION_OK`，表示取消請求已成功送出。這兩種狀態同樣都可以從上述 `PQcancelPoll` 的傳回值偵測到。在非同步連線流程期間（而且只在此期間）也可能出現其他狀態。這些狀態表示連線流程目前所處的階段，例如可能有助於向使用者提供回饋。這些狀態如下：

- <a id="LIBPQ-CANCEL-CONNECTION-ALLOCATED"></a>`CONNECTION_ALLOCATED` [#](#LIBPQ-CANCEL-CONNECTION-ALLOCATED)

  等待呼叫 [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART) 或 [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING)，以實際開啟通訊端。這是剛呼叫 [`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE) 或 [`PQcancelReset`](libpq-cancel.md#LIBPQ-PQCANCELRESET) 之後的連線狀態。此時尚未發起任何連往伺服器的連線。要實際開始傳送取消請求，請使用 [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART) 或 [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING)。

- <a id="LIBPQ-CANCEL-CONNECTION-STARTED"></a>`CONNECTION_STARTED` [#](#LIBPQ-CANCEL-CONNECTION-STARTED)

  等待建立連線。

- <a id="LIBPQ-CANCEL-CONNECTION-MADE"></a>`CONNECTION_MADE` [#](#LIBPQ-CANCEL-CONNECTION-MADE)

  連線正常；等待傳送。

- <a id="LIBPQ-CANCEL-CONNECTION-AWAITING-RESPONSE"></a>`CONNECTION_AWAITING_RESPONSE` [#](#LIBPQ-CANCEL-CONNECTION-AWAITING-RESPONSE)

  等待伺服器的回應。

- <a id="LIBPQ-CANCEL-CONNECTION-SSL-STARTUP"></a>`CONNECTION_SSL_STARTUP` [#](#LIBPQ-CANCEL-CONNECTION-SSL-STARTUP)

  正在協商 SSL 加密。

- <a id="LIBPQ-CANCEL-CONNECTION-GSS-STARTUP"></a>`CONNECTION_GSS_STARTUP` [#](#LIBPQ-CANCEL-CONNECTION-GSS-STARTUP)

  正在協商 GSS 加密。

請注意，雖然這些常數會繼續保留（以維持相容性），但應用程式絕不應該依賴這些狀態以特定順序出現、甚至依賴它們一定會出現，也不應該依賴狀態一定是這些已記載的值之一。應用程式可以像這樣處理：

```

    switch(PQcancelStatus(conn))
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

使用 `PQcancelPoll` 時，`connect_timeout` 連線參數會被忽略；是否已經過太長的時間，由應用程式負責判斷。除此之外，`PQcancelStart` 加上後續的 `PQcancelPoll` 迴圈，等同於 [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING)。

<a id="LIBPQ-PQCANCELSTATUS"></a>

`PQcancelStatus`<a id="id-1.7.3.14.4.2.4.1.2"></a> [#](#LIBPQ-PQCANCELSTATUS)

傳回取消連線的狀態。

```

    ConnStatusType PQcancelStatus(const PGcancelConn *cancelConn);
```

狀態可以是許多值之一。不過，在非同步取消流程之外只會看到其中三個值：`CONNECTION_ALLOCATED`、`CONNECTION_OK` 與 `CONNECTION_BAD`。以 [`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE) 成功建立的 `PGcancelConn`，其初始狀態為 `CONNECTION_ALLOCATED`。已成功送出的取消請求，其狀態為 `CONNECTION_OK`。失敗的取消嘗試則以狀態 `CONNECTION_BAD` 表示。OK 狀態會一直維持，直到呼叫 [`PQcancelFinish`](libpq-cancel.md#LIBPQ-PQCANCELFINISH) 或 [`PQcancelReset`](libpq-cancel.md#LIBPQ-PQCANCELRESET) 為止。

關於可能傳回的其他狀態碼，請參閱 [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART) 的條目。

不過，成功送出取消請求並不保證該請求會產生任何效果。如果取消生效，被取消的命令會提早終止並傳回錯誤結果。如果取消失敗（例如，因為伺服器已經處理完該命令），則完全不會有任何可見的結果。

<a id="LIBPQ-PQCANCELSOCKET"></a>

`PQcancelSocket`<a id="id-1.7.3.14.4.2.5.1.2"></a> [#](#LIBPQ-PQCANCELSOCKET)

取得連往伺服器之取消連線通訊端的檔案描述子編號。

```

    int PQcancelSocket(const PGcancelConn *cancelConn);
```

有效的描述子會大於或等於 0；結果為 -1 表示目前沒有開啟的伺服器連線。在 `PGcancelConn` 上呼叫本節中的任何函式（[`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE) 與 `PQcancelSocket` 本身除外），都可能使此值改變。

<a id="LIBPQ-PQCANCELERRORMESSAGE"></a>

`PQcancelErrorMessage`<a id="id-1.7.3.14.4.2.6.1.2"></a> <a id="id-1.7.3.14.4.2.6.1.3"></a> [#](#LIBPQ-PQCANCELERRORMESSAGE)

傳回取消連線上的操作最近產生的錯誤訊息。

```

    char *PQcancelErrorMessage(const PGcancelConn *cancelconn);
```

幾乎所有接受 `PGcancelConn` 的 libpq 函式在失敗時，都會為 [`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE) 設定一則訊息。請注意，依照 libpq 的慣例，非空的 [`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE) 結果可能由多行組成，並且會包含結尾的換行字元。呼叫端不應直接釋放此結果。當相關的 `PGcancelConn` 控制代碼被傳給 [`PQcancelFinish`](libpq-cancel.md#LIBPQ-PQCANCELFINISH) 時，結果就會被釋放。不應預期結果字串在對 `PGcancelConn` 結構進行多次操作之間保持不變。

<a id="LIBPQ-PQCANCELFINISH"></a>

`PQcancelFinish`<a id="id-1.7.3.14.4.2.7.1.2"></a> [#](#LIBPQ-PQCANCELFINISH)

關閉取消連線（如果它尚未完成傳送取消請求）。同時釋放 `PGcancelConn` 物件所使用的記憶體。

```

    void PQcancelFinish(PGcancelConn *cancelConn);
```

請注意，即使取消嘗試失敗（如 [`PQcancelStatus`](libpq-cancel.md#LIBPQ-PQCANCELSTATUS) 所示），應用程式也應該呼叫 [`PQcancelFinish`](libpq-cancel.md#LIBPQ-PQCANCELFINISH)，以釋放 `PGcancelConn` 物件所使用的記憶體。呼叫 [`PQcancelFinish`](libpq-cancel.md#LIBPQ-PQCANCELFINISH) 之後，不得再使用該 `PGcancelConn` 指標。

<a id="LIBPQ-PQCANCELRESET"></a>

`PQcancelReset`<a id="id-1.7.3.14.4.2.8.1.2"></a> [#](#LIBPQ-PQCANCELRESET)

重設 `PGcancelConn`，使其可以重複用於新的取消連線。

```

    void PQcancelReset(PGcancelConn *cancelConn);
```

若 `PGcancelConn` 目前正用於傳送取消請求，則此連線會被關閉。接著它會準備好 `PGcancelConn` 物件，使其可用於傳送新的取消請求。

這可用於為一個 `PGconn` 建立一個 `PGcancelConn`，並在原始 `PGconn` 的整個存續期間重複使用它多次。

<a id="LIBPQ-CANCEL-DEPRECATED"></a>

### 32.7.2. 已過時的傳送取消請求函式 [#](#libpq-cancel-deprecated) <a href="#libpq-cancel-deprecated" id="libpq-cancel-deprecated"></a>

這些函式代表傳送取消請求的舊方法。雖然它們仍然可以運作，但由於它們不會以加密的方式傳送取消請求（即使原始連線已指定 `sslmode` 或 `gssencmode` 來要求加密），因此已被棄用。所以，強烈不建議在新程式碼中使用這些舊方法，並建議將現有程式碼改為使用新的函式。

<a id="LIBPQ-PQGETCANCEL"></a>

`PQgetCancel`<a id="id-1.7.3.14.5.3.1.1.2"></a> [#](#LIBPQ-PQGETCANCEL)

建立一個資料結構，其中包含使用 [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) 取消命令所需的資訊。

```

    PGcancel *PQgetCancel(PGconn *conn);
```

[`PQgetCancel`](libpq-cancel.md#LIBPQ-PQGETCANCEL) 會根據給定的 `PGconn` 連線物件建立一個 `PGcancel`<a id="id-1.7.3.14.5.3.1.2.2.3"></a> 物件。若給定的 *`conn`* 為 `NULL` 或是無效的連線，它會傳回 `NULL`。`PGcancel` 物件是不透明的結構，不打算讓應用程式直接存取；它只能傳給 [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) 或 [`PQfreeCancel`](libpq-cancel.md#LIBPQ-PQFREECANCEL)。

<a id="LIBPQ-PQFREECANCEL"></a>

`PQfreeCancel`<a id="id-1.7.3.14.5.3.2.1.2"></a> [#](#LIBPQ-PQFREECANCEL)

釋放由 [`PQgetCancel`](libpq-cancel.md#LIBPQ-PQGETCANCEL) 建立的資料結構。

```

    void PQfreeCancel(PGcancel *cancel);
```

[`PQfreeCancel`](libpq-cancel.md#LIBPQ-PQFREECANCEL) 會釋放先前由 [`PQgetCancel`](libpq-cancel.md#LIBPQ-PQGETCANCEL) 建立的資料物件。

<a id="LIBPQ-PQCANCEL"></a>

`PQcancel`<a id="id-1.7.3.14.5.3.3.1.2"></a> [#](#LIBPQ-PQCANCEL)

[`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) 是 [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) 的已棄用且不安全的變體，但它可以在訊號處理常式（signal handler）中安全地使用。

```

    int PQcancel(PGcancel *cancel, char *errbuf, int errbufsize);
```

[`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) 只是基於向後相容性的理由而存在。應該改用 [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING)。[`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) 唯一的好處是，若 *`errbuf`* 是訊號處理常式中的區域變數，它就可以從訊號處理常式中安全地呼叫。不過，一般認為這項好處並不足以抵銷此函式所帶來的安全性問題。

就 [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) 而言，`PGcancel` 物件是唯讀的，因此也可以從與操作 `PGconn` 物件的執行緒不同的另一個執行緒呼叫它。

若取消請求已成功送出，[`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL) 的傳回值為 1，否則為 0。若未成功，*`errbuf`* 會被填入說明性的錯誤訊息。*`errbuf`* 必須是大小為 *`errbufsize`* 的字元（char）陣列（建議大小為 256 位元組）。

<a id="LIBPQ-PQREQUESTCANCEL"></a>

`PQrequestCancel`<a id="id-1.7.3.14.5.4.1.1.2"></a> [#](#LIBPQ-PQREQUESTCANCEL)

[`PQrequestCancel`](libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) 是 [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) 的已棄用且不安全的變體。

```

    int PQrequestCancel(PGconn *conn);
```

[`PQrequestCancel`](libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) 只是基於向後相容性的理由而存在。應該改用 [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING)。使用 [`PQrequestCancel`](libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) 並不比使用 [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) 有任何好處。

請求伺服器放棄處理目前的命令。它直接對 `PGconn` 物件操作，並在失敗時將錯誤訊息存放在 `PGconn` 物件中（可以從那裡透過 [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) 取得）。雖然功能相同，但這種做法在多執行緒程式或訊號處理常式中並不安全，因為覆寫 `PGconn` 的錯誤訊息可能會擾亂該連線上目前正在進行的操作。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-cancel.html)（原文版本：18.6；核對日期：2026-10-18）
