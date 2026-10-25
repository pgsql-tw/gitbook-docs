<a id="LIBPQ-COPY"></a>

## 32.10. 與 `COPY` 命令相關的函式 [#](#libpq-copy) <a href="#libpq-copy" id="libpq-copy"></a>

[32.10.1. 傳送 `COPY` 資料的函式](libpq-copy.md#libpq-copy-send)

[32.10.2. 接收 `COPY` 資料的函式](libpq-copy.md#libpq-copy-receive)

[32.10.3. 已過時的 `COPY` 函式](libpq-copy.md#libpq-copy-deprecated)

<a id="id-1.7.3.17.2"></a>

PostgreSQL 中的 `COPY` 命令具有從 libpq 所使用的網路連線讀取或寫入的選項。本節所述的函式讓應用程式能夠藉由提供或取用所複製的資料，來善用這項功能。

整體流程是：應用程式先透過 [`PQexec`](libpq-exec-main.md#libpq-pqexec) 或其中一個同等的函式發出 SQL `COPY` 命令。對此的回應（如果命令沒有錯誤）會是一個帶有狀態碼 `PGRES_COPY_OUT` 或 `PGRES_COPY_IN`（取決於指定的複製方向）的 `PGresult` 物件。接著應用程式應該使用本節的函式來接收或傳送資料列。資料傳輸完成時，會再傳回另一個 `PGresult` 物件，表示傳輸成功或失敗。成功時其狀態為 `PGRES_COMMAND_OK`，若遇到問題則為 `PGRES_FATAL_ERROR`。此時即可再透過 [`PQexec`](libpq-exec-main.md#libpq-pqexec) 發出其他 SQL 命令。（在 `COPY` 操作進行期間，無法使用同一個連線執行其他 SQL 命令。）

如果 `COPY` 命令是透過 [`PQexec`](libpq-exec-main.md#libpq-pqexec) 在可能包含其他命令的字串中發出的，那麼應用程式在完成 `COPY` 流程之後，必須繼續透過 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 擷取結果。只有在 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 傳回 `NULL` 時，才能確定 [`PQexec`](libpq-exec-main.md#libpq-pqexec) 的命令字串已執行完畢，可以安全地發出更多命令。

本節的函式應該只在從 [`PQexec`](libpq-exec-main.md#libpq-pqexec) 或 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 取得 `PGRES_COPY_OUT` 或 `PGRES_COPY_IN` 結果狀態之後執行。

帶有上述其中一個狀態值的 `PGresult` 物件，會攜帶一些關於即將開始之 `COPY` 操作的額外資料。這些額外資料可以使用同樣用於查詢結果的函式取得：

<a id="LIBPQ-PQNFIELDS-1"></a>

`PQnfields`<a id="id-1.7.3.17.7.3.1.1.2"></a> [#](#LIBPQ-PQNFIELDS-1)

傳回要複製的欄位數。

<a id="LIBPQ-PQBINARYTUPLES-1"></a>

`PQbinaryTuples`<a id="id-1.7.3.17.7.3.2.1.2"></a> [#](#LIBPQ-PQBINARYTUPLES-1)

0 表示整體複製格式為文字格式（資料列以換行字元分隔、欄位以分隔字元分隔，依此類推）。1 表示整體複製格式為二進位格式。更多資訊請參閱 [COPY](../../reference/sql-commands/sql-copy.md)。

<a id="LIBPQ-PQFFORMAT-1"></a>

`PQfformat`<a id="id-1.7.3.17.7.3.3.1.2"></a> [#](#LIBPQ-PQFFORMAT-1)

傳回複製操作中每個欄位所關聯的格式代碼（0 表示文字，1 表示二進位）。當整體複製格式為文字格式時，各欄位的格式代碼一律為零，但二進位格式可以同時支援文字與二進位欄位。（不過，就目前 `COPY` 的實作而言，二進位複製中只會出現二進位欄位；因此目前各欄位的格式一律與整體格式相符。）

<a id="LIBPQ-COPY-SEND"></a>

### 32.10.1. 傳送 `COPY` 資料的函式 [#](#libpq-copy-send) <a href="#libpq-copy-send" id="libpq-copy-send"></a>

這些函式用於在 `COPY FROM
STDIN` 期間傳送資料。若在連線不處於 `COPY_IN` 狀態時呼叫，這些函式將會失敗。

<a id="LIBPQ-PQPUTCOPYDATA"></a>

`PQputCopyData`<a id="id-1.7.3.17.8.3.1.1.2"></a> [#](#LIBPQ-PQPUTCOPYDATA)

在 `COPY_IN` 狀態期間將資料送往伺服器。

```

    int PQputCopyData(PGconn *conn,
                      const char *buffer,
                      int nbytes);
```

將指定的 *`buffer`* 中長度為 *`nbytes`* 的 `COPY` 資料傳送到伺服器。若資料已排入佇列，結果為 1；若因緩衝區已滿而未排入佇列（這只會在非阻塞模式下發生），結果為零；若發生錯誤，結果為 -1。（若傳回值為 -1，請使用 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage) 取得詳細資訊。若傳回值為零，請等待可寫入後再試一次。）

應用程式可以將 `COPY` 資料串流切分成任何方便大小的緩衝區載量。傳送時，緩衝區載量的邊界不具任何語意上的意義。資料串流的內容必須符合 `COPY` 命令所預期的資料格式；詳細資訊請參閱 [COPY](../../reference/sql-commands/sql-copy.md)。

<a id="LIBPQ-PQPUTCOPYEND"></a>

`PQputCopyEnd`<a id="id-1.7.3.17.8.3.2.1.2"></a> [#](#LIBPQ-PQPUTCOPYEND)

在 `COPY_IN` 狀態期間向伺服器傳送資料結束指示。

```

    int PQputCopyEnd(PGconn *conn,
                     const char *errormsg);
```

若 *`errormsg`* 為 `NULL`，則成功結束 `COPY_IN` 操作。若 *`errormsg`* 不為 `NULL`，則 `COPY` 會被強制失敗，並以 *`errormsg`* 所指向的字串作為錯誤訊息。（不過，不應假設伺服器一定會傳回這則確切的錯誤訊息，因為伺服器可能已經基於自身的原因使 `COPY` 失敗。）

若已送出終止訊息，結果為 1；在非阻塞模式下，這可能只表示終止訊息已成功排入佇列。（在非阻塞模式下，為了確定資料已經送出，接下來你應該等待可寫入，然後呼叫 [`PQflush`](libpq-async.md#libpq-pqflush)，重複此步驟直到它傳回零為止。）零表示函式因緩衝區已滿而無法將終止訊息排入佇列；這只會在非阻塞模式下發生。（在這種情況下，請等待可寫入，然後再次呼叫 [`PQputCopyEnd`](libpq-copy.md#LIBPQ-PQPUTCOPYEND)。）若發生嚴重錯誤，則傳回 -1；你可以使用 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage) 取得詳細資訊。

成功呼叫 [`PQputCopyEnd`](libpq-copy.md#LIBPQ-PQPUTCOPYEND) 之後，請呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 以取得 `COPY` 命令的最終結果狀態。你可以用一般的方式等待此結果就緒。然後再回到正常操作。

<a id="LIBPQ-COPY-RECEIVE"></a>

### 32.10.2. 接收 `COPY` 資料的函式 [#](#libpq-copy-receive) <a href="#libpq-copy-receive" id="libpq-copy-receive"></a>

這些函式用於在 `COPY TO
STDOUT` 期間接收資料。若在連線不處於 `COPY_OUT` 狀態時呼叫，這些函式將會失敗。

<a id="LIBPQ-PQGETCOPYDATA"></a>

`PQgetCopyData`<a id="id-1.7.3.17.9.3.1.1.2"></a> [#](#LIBPQ-PQGETCOPYDATA)

在 `COPY_OUT` 狀態期間從伺服器接收資料。

```

    int PQgetCopyData(PGconn *conn,
                      char **buffer,
                      int async);
```

嘗試在 `COPY` 期間從伺服器取得另一個資料列。資料一律一次傳回一個資料列；如果只有部分資料列可用，則不會傳回。成功傳回一個資料列時，會配置一塊記憶體來存放資料。*`buffer`* 參數必須不為 `NULL`。*`*buffer`* 會被設為指向所配置的記憶體，或在沒有傳回緩衝區的情況下設為 `NULL`。不為 `NULL` 的結果緩衝區在不再需要時，應該使用 [`PQfreemem`](libpq-misc.md#libpq-pqfreemem) 釋放。

成功傳回一個資料列時，傳回值為該資料列中資料的位元組數（一律大於零）。傳回的字串一律以 null 結尾，不過這大概只對文字格式的 `COPY` 有用。結果為零表示 `COPY` 仍在進行中，但尚無可用的資料列（這只有在 *`async`* 為 true 時才可能發生）。結果為 -1 表示 `COPY` 已完成。結果為 -2 表示發生錯誤（原因請查閱 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage)）。

當 *`async`* 為 true（非零）時，[`PQgetCopyData`](libpq-copy.md#LIBPQ-PQGETCOPYDATA) 不會阻塞等待輸入；若 `COPY` 仍在進行中但沒有完整的資料列可用，它會傳回零。（在這種情況下，請等待可讀取，然後先呼叫 [`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput)，再次呼叫 [`PQgetCopyData`](libpq-copy.md#LIBPQ-PQGETCOPYDATA)。）當 *`async`* 為 false（零）時，[`PQgetCopyData`](libpq-copy.md#LIBPQ-PQGETCOPYDATA) 會阻塞，直到有資料可用或操作完成為止。

[`PQgetCopyData`](libpq-copy.md#LIBPQ-PQGETCOPYDATA) 傳回 -1 之後，請呼叫 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 以取得 `COPY` 命令的最終結果狀態。你可以用一般的方式等待此結果就緒。然後再回到正常操作。

<a id="LIBPQ-COPY-DEPRECATED"></a>

### 32.10.3. 已過時的 `COPY` 函式 [#](#libpq-copy-deprecated) <a href="#libpq-copy-deprecated" id="libpq-copy-deprecated"></a>

這些函式代表處理 `COPY` 的舊方法。雖然它們仍然可以運作，但由於錯誤處理不佳、偵測資料結束的方法不便，以及不支援二進位或非阻塞傳輸，因此已被棄用。

<a id="LIBPQ-PQGETLINE"></a>

`PQgetline`<a id="id-1.7.3.17.10.3.1.1.2"></a> [#](#LIBPQ-PQGETLINE)

將一行以換行字元結尾的字元（由伺服器傳送）讀入大小為 *`length`* 的緩衝區字串中。

```

    int PQgetline(PGconn *conn,
                  char *buffer,
                  int length);
```

此函式最多會將 *`length`*-1 個字元複製到緩衝區中，並將結尾的換行字元轉換為零位元組。[`PQgetline`](libpq-copy.md#LIBPQ-PQGETLINE) 在輸入結束時傳回 `EOF`；若已讀取整行，則傳回 0；若緩衝區已滿但尚未讀到結尾的換行字元，則傳回 1。

請注意，應用程式必須檢查新的一行是否由兩個字元 `\.` 組成，這表示伺服器已經完成傳送 `COPY` 命令的結果。如果應用程式可能接收到長度超過 *`length`*-1 個字元的行，就需要小心確保它能正確辨識 `\.` 這一行（例如，不要把長資料行的結尾誤認為終止行）。

<a id="LIBPQ-PQGETLINEASYNC"></a>

`PQgetlineAsync`<a id="id-1.7.3.17.10.3.2.1.2"></a> [#](#LIBPQ-PQGETLINEASYNC)

以不阻塞的方式將一列 `COPY` 資料（由伺服器傳送）讀入緩衝區。

```

    int PQgetlineAsync(PGconn *conn,
                       char *buffer,
                       int bufsize);
```

此函式類似於 [`PQgetline`](libpq-copy.md#LIBPQ-PQGETLINE)，但可供必須以非同步方式（也就是不阻塞）讀取 `COPY` 資料的應用程式使用。發出 `COPY` 命令並取得 `PGRES_COPY_OUT` 回應之後，應用程式應該呼叫 [`PQconsumeInput`](libpq-async.md#libpq-pqconsumeinput) 與 [`PQgetlineAsync`](libpq-copy.md#LIBPQ-PQGETLINEASYNC)，直到偵測到資料結束訊號為止。

與 [`PQgetline`](libpq-copy.md#LIBPQ-PQGETLINE) 不同，此函式自行負責偵測資料結束。

每次呼叫時，若 libpq 的輸入緩衝區中有完整的資料列可用，[`PQgetlineAsync`](libpq-copy.md#LIBPQ-PQGETLINEASYNC) 就會傳回資料。否則，在該資料列的其餘部分到達之前，不會傳回任何資料。若已辨識到複製資料結束標記，函式傳回 -1；若沒有可用的資料，則傳回 0；否則傳回一個正數，表示所傳回資料的位元組數。若傳回 -1，呼叫端接下來必須呼叫 [`PQendcopy`](libpq-copy.md#LIBPQ-PQENDCOPY)，然後再回到正常處理。

傳回的資料不會跨越資料列的邊界。如果可能，一次會傳回一整個資料列。但如果呼叫端提供的緩衝區太小，無法容納伺服器送來的一個資料列，就會傳回部分資料列。對於文字資料，可以藉由檢查最後傳回的位元組是否為 `\n` 來偵測這種情況。（在二進位 `COPY` 中，則需要實際剖析 `COPY` 資料格式，才能做出同等的判斷。）傳回的字串不以 null 結尾。（如果你想加上結尾的 null，請務必傳入比實際可用空間小一的 *`bufsize`*。）

<a id="LIBPQ-PQPUTLINE"></a>

`PQputline`<a id="id-1.7.3.17.10.3.3.1.2"></a> [#](#LIBPQ-PQPUTLINE)

將以 null 結尾的字串送往伺服器。成功時傳回 0，若無法送出字串則傳回 `EOF`。

```

    int PQputline(PGconn *conn,
                  const char *string);
```

透過一連串 [`PQputline`](libpq-copy.md#LIBPQ-PQPUTLINE) 呼叫所送出的 `COPY` 資料串流，其格式與 [`PQgetlineAsync`](libpq-copy.md#LIBPQ-PQGETLINEASYNC) 所傳回的格式相同，只是應用程式不必在每次 [`PQputline`](libpq-copy.md#LIBPQ-PQPUTLINE) 呼叫中剛好送出一個資料列；每次呼叫送出部分行或多行都可以。

### 注意

在 PostgreSQL 協定 3.0 之前，應用程式必須明確地送出兩個字元 `\.` 作為最後一行，以向伺服器表示它已完成傳送 `COPY` 資料。雖然這樣做仍然可行，但已被棄用，而且 `\.` 的特殊意義預期會在未來的版本中移除。（它在 `CSV` 模式下已經會出現異常行為。）送出實際資料之後，呼叫 [`PQendcopy`](libpq-copy.md#LIBPQ-PQENDCOPY) 就足夠了。

<a id="LIBPQ-PQPUTNBYTES"></a>

`PQputnbytes`<a id="id-1.7.3.17.10.3.4.1.2"></a> [#](#LIBPQ-PQPUTNBYTES)

將不以 null 結尾的字串送往伺服器。成功時傳回 0，若無法送出字串則傳回 `EOF`。

```

    int PQputnbytes(PGconn *conn,
                    const char *buffer,
                    int nbytes);
```

此函式與 [`PQputline`](libpq-copy.md#LIBPQ-PQPUTLINE) 完全相同，只是資料緩衝區不必以 null 結尾，因為要傳送的位元組數是直接指定的。傳送二進位資料時，請使用此函式。

<a id="LIBPQ-PQENDCOPY"></a>

`PQendcopy`<a id="id-1.7.3.17.10.3.5.1.2"></a> [#](#LIBPQ-PQENDCOPY)

與伺服器同步。

```

    int PQendcopy(PGconn *conn);
```

此函式會等待，直到伺服器完成複製為止。它應該在使用 [`PQputline`](libpq-copy.md#LIBPQ-PQPUTLINE) 將最後一個字串送往伺服器之後，或在使用 `PQgetline` 從伺服器接收最後一個字串之後呼叫。必須呼叫此函式，否則伺服器將會與用戶端「失去同步」。從此函式返回時，伺服器已準備好接收下一個 SQL 命令。成功完成時傳回值為 0，否則為非零。（若傳回值為非零，請使用 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage) 取得詳細資訊。）

使用 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 時，應用程式應該以重複執行 [`PQgetline`](libpq-copy.md#LIBPQ-PQGETLINE) 來回應 `PGRES_COPY_OUT` 結果，並在看到終止行之後呼叫 [`PQendcopy`](libpq-copy.md#LIBPQ-PQENDCOPY)。接著它應該回到 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 迴圈，直到 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 傳回空指標為止。同樣地，`PGRES_COPY_IN` 結果的處理方式是一連串的 [`PQputline`](libpq-copy.md#LIBPQ-PQPUTLINE) 呼叫，接著呼叫 [`PQendcopy`](libpq-copy.md#LIBPQ-PQENDCOPY)，然後回到 [`PQgetResult`](libpq-async.md#libpq-pqgetresult) 迴圈。這樣的安排可確保嵌在一連串 SQL 命令中的 `COPY` 命令能正確執行。

較舊的應用程式很可能會透過 [`PQexec`](libpq-exec-main.md#libpq-pqexec) 送出 `COPY`，並假設在 [`PQendcopy`](libpq-copy.md#LIBPQ-PQENDCOPY) 之後交易就已完成。只有當 `COPY` 是命令字串中唯一的 SQL 命令時，這樣做才會正確運作。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-copy.html)（原文版本：18.6；核對日期：2026-10-18）
