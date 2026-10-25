<a id="LIBPQ-STATUS"></a>

## 32.2. 連線狀態函式 [#](#libpq-status) <a href="#libpq-status" id="libpq-status"></a>

這些函式可用來查詢現有資料庫連線物件的狀態。

### 提示

<a id="id-1.7.3.9.3.1.1"></a>
<a id="id-1.7.3.9.3.1.2"></a>
libpq 應用程式的程式設計者應該小心維持 `PGconn` 的抽象性。請使用下面所述的存取函式來取得 `PGconn` 的內容。不建議透過 `libpq-int.h` 參照 `PGconn` 的內部欄位，因為這些欄位未來可能會變更。

下列函式傳回連線時所建立的參數值。這些值在連線存續期間固定不變。如果使用多主機連線字串，那麼在使用同一個 `PGconn` 物件建立新連線時，[`PQhost`](libpq-status.md#libpq-pqhost)、[`PQport`](libpq-status.md#libpq-pqport) 與 [`PQpass`](libpq-status.md#libpq-pqpass) 的值可能會改變。其他值則在 `PGconn` 物件的存續期間固定不變。

<a id="LIBPQ-PQDB"></a>

### `PQdb`<a id="id-1.7.3.9.4.6.1.1.2"></a> [#](#libpq-pqdb) <a href="#libpq-pqdb" id="libpq-pqdb"></a>

傳回連線的資料庫名稱。

```

    char *PQdb(const PGconn *conn);
```

<a id="LIBPQ-PQUSER"></a>

### `PQuser`<a id="id-1.7.3.9.4.6.2.1.2"></a> [#](#libpq-pquser) <a href="#libpq-pquser" id="libpq-pquser"></a>

傳回連線的使用者名稱。

```

    char *PQuser(const PGconn *conn);
```

<a id="LIBPQ-PQPASS"></a>

### `PQpass`<a id="id-1.7.3.9.4.6.3.1.2"></a> [#](#libpq-pqpass) <a href="#libpq-pqpass" id="libpq-pqpass"></a>

傳回連線的密碼。

```

    char *PQpass(const PGconn *conn);
```

[`PQpass`](libpq-status.md#libpq-pqpass) 會傳回連線參數中指定的密碼；若連線參數中沒有指定密碼，而密碼是從[密碼檔](libpq-pgpass.md)取得的，則傳回該密碼。在後者的情況下，如果連線參數中指定了多個主機，那麼在連線建立之前，不能依賴 [`PQpass`](libpq-status.md#libpq-pqpass) 的結果。連線的狀態可以使用函式 [`PQstatus`](libpq-status.md#libpq-pqstatus) 檢查。

<a id="LIBPQ-PQHOST"></a>

### `PQhost`<a id="id-1.7.3.9.4.6.4.1.2"></a> [#](#libpq-pqhost) <a href="#libpq-pqhost" id="libpq-pqhost"></a>

傳回目前作用中連線的伺服器主機名稱。這可能是主機名稱、IP 位址，或者在透過 Unix 網域通訊端連線時是目錄路徑。（路徑的情況可以區分出來，因為它一律是以 `/` 開頭的絕對路徑。）

```

    char *PQhost(const PGconn *conn);
```

如果連線參數同時指定了 `host` 與 `hostaddr`，那麼 [`PQhost`](libpq-status.md#libpq-pqhost) 會傳回 `host` 的資訊。如果只指定了 `hostaddr`，則傳回它。如果連線參數中指定了多個主機，[`PQhost`](libpq-status.md#libpq-pqhost) 會傳回實際連上的主機。

若 *`conn`* 引數為 `NULL`，[`PQhost`](libpq-status.md#libpq-pqhost) 會傳回 `NULL`。否則，若產生主機資訊時發生錯誤（可能是連線尚未完全建立或發生了錯誤），則傳回空字串。

如果連線參數中指定了多個主機，那麼在連線建立之前，不能依賴 [`PQhost`](libpq-status.md#libpq-pqhost) 的結果。連線的狀態可以使用函式 [`PQstatus`](libpq-status.md#libpq-pqstatus) 檢查。

<a id="LIBPQ-PQHOSTADDR"></a>

### `PQhostaddr`<a id="id-1.7.3.9.4.6.5.1.2"></a> [#](#libpq-pqhostaddr) <a href="#libpq-pqhostaddr" id="libpq-pqhostaddr"></a>

傳回目前作用中連線的伺服器 IP 位址。這可能是主機名稱解析所得的位址，或是透過 `hostaddr` 參數提供的 IP 位址。

```

    char *PQhostaddr(const PGconn *conn);
```

若 *`conn`* 引數為 `NULL`，[`PQhostaddr`](libpq-status.md#libpq-pqhostaddr) 會傳回 `NULL`。否則，若產生主機資訊時發生錯誤（可能是連線尚未完全建立或發生了錯誤），則傳回空字串。

<a id="LIBPQ-PQPORT"></a>

### `PQport`<a id="id-1.7.3.9.4.6.6.1.2"></a> [#](#libpq-pqport) <a href="#libpq-pqport" id="libpq-pqport"></a>

傳回目前作用中連線的連接埠。

```

    char *PQport(const PGconn *conn);
```

如果連線參數中指定了多個連接埠，[`PQport`](libpq-status.md#libpq-pqport) 會傳回實際連上的連接埠。

若 *`conn`* 引數為 `NULL`，[`PQport`](libpq-status.md#libpq-pqport) 會傳回 `NULL`。否則，若產生連接埠資訊時發生錯誤（可能是連線尚未完全建立或發生了錯誤），則傳回空字串。

如果連線參數中指定了多個連接埠，那麼在連線建立之前，不能依賴 [`PQport`](libpq-status.md#libpq-pqport) 的結果。連線的狀態可以使用函式 [`PQstatus`](libpq-status.md#libpq-pqstatus) 檢查。

<a id="LIBPQ-PQTTY"></a>

### `PQtty`<a id="id-1.7.3.9.4.6.7.1.2"></a> [#](#libpq-pqtty) <a href="#libpq-pqtty" id="libpq-pqtty"></a>

此函式已不再執行任何動作，保留它只是為了向後相容性。此函式一律傳回空字串；若 *`conn`* 引數為 `NULL`，則傳回 `NULL`。

```

    char *PQtty(const PGconn *conn);
```

<a id="LIBPQ-PQOPTIONS"></a>

### `PQoptions`<a id="id-1.7.3.9.4.6.8.1.2"></a> [#](#libpq-pqoptions) <a href="#libpq-pqoptions" id="libpq-pqoptions"></a>

傳回在連線要求中傳遞的命令列選項。

```

    char *PQoptions(const PGconn *conn);
```

下列函式傳回的狀態資料，可能會隨著對 `PGconn` 物件執行的操作而改變。

<a id="LIBPQ-PQSTATUS"></a>

### `PQstatus`<a id="id-1.7.3.9.5.2.1.1.2"></a> [#](#libpq-pqstatus) <a href="#libpq-pqstatus" id="libpq-pqstatus"></a>

傳回連線的狀態。

```

    ConnStatusType PQstatus(const PGconn *conn);
```

狀態可以是多個值中的一個。不過，在非同步連線程序之外只會看到其中兩個：`CONNECTION_OK` 與 `CONNECTION_BAD`。與資料庫的良好連線狀態為 `CONNECTION_OK`。連線嘗試失敗則以狀態 `CONNECTION_BAD` 表示。通常，OK 狀態會一直維持到 [`PQfinish`](libpq-connect.md#libpq-pqfinish) 為止，但通訊失敗可能會導致狀態提早變為 `CONNECTION_BAD`。在這種情況下，應用程式可以呼叫 [`PQreset`](libpq-connect.md#libpq-pqreset) 嘗試復原。

關於可能傳回的其他狀態碼，請參閱 [`PQconnectStartParams`](libpq-connect.md#libpq-pqconnectstartparams)、`PQconnectStart` 與 `PQconnectPoll` 的說明項目。

<a id="LIBPQ-PQTRANSACTIONSTATUS"></a>

### `PQtransactionStatus`<a id="id-1.7.3.9.5.2.2.1.2"></a> [#](#libpq-pqtransactionstatus) <a href="#libpq-pqtransactionstatus" id="libpq-pqtransactionstatus"></a>

傳回伺服器目前的交易內狀態。

```

    PGTransactionStatusType PQtransactionStatus(const PGconn *conn);
```

狀態可以是 `PQTRANS_IDLE`（目前閒置）、`PQTRANS_ACTIVE`（有命令正在執行中）、`PQTRANS_INTRANS`（閒置，位於有效的交易區塊中），或 `PQTRANS_INERROR`（閒置，位於失敗的交易區塊中）。若連線狀態不良，則回報 `PQTRANS_UNKNOWN`。只有在查詢已送至伺服器但尚未完成時，才會回報 `PQTRANS_ACTIVE`。

<a id="LIBPQ-PQPARAMETERSTATUS"></a>

### `PQparameterStatus`<a id="id-1.7.3.9.5.2.3.1.2"></a> [#](#libpq-pqparameterstatus) <a href="#libpq-pqparameterstatus" id="libpq-pqparameterstatus"></a>

查詢伺服器目前的某項參數設定。

```

    const char *PQparameterStatus(const PGconn *conn, const char *paramName);
```

某些參數值會在連線啟動時，或在其值改變時，由伺服器自動回報。[`PQparameterStatus`](libpq-status.md#libpq-pqparameterstatus) 可用來查詢這些設定。若已知參數的目前值，則傳回該值；若參數未知，則傳回 `NULL`。

截至目前的版本，會回報的參數包括：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="varname">application_name</code></td><td><code class="varname">scram_iterations</code></td></tr><tr><td><code class="varname">client_encoding</code></td><td><code class="varname">search_path</code></td></tr><tr><td><code class="varname">DateStyle</code></td><td><code class="varname">server_encoding</code></td></tr><tr><td><code class="varname">default_transaction_read_only</code></td><td><code class="varname">server_version</code></td></tr><tr><td><code class="varname">in_hot_standby</code></td><td><code class="varname">session_authorization</code></td></tr><tr><td><code class="varname">integer_datetimes</code></td><td><code class="varname">standard_conforming_strings</code></td></tr><tr><td><code class="varname">IntervalStyle</code></td><td><code class="varname">TimeZone</code></td></tr><tr><td><code class="varname">is_superuser</code></td><td> </td></tr></table>

（14 之前的版本不會回報 `default_transaction_read_only` 與 `in_hot_standby`；16 之前的版本不會回報 `scram_iterations`；18 之前的版本不會回報 `search_path`。）請注意，`server_version`、`server_encoding` 與 `integer_datetimes` 在啟動之後無法改變。

如果沒有回報 `standard_conforming_strings` 的值，應用程式可以假定其為 `off`，也就是反斜線在字串常數中會被視為跳脫字元。此外，此參數的存在可以視為跳脫字串語法（`E'...'`）可被接受的跡象。

雖然傳回的指標宣告為 `const`，但它實際上指向與 `PGconn` 結構相關聯的可變儲存空間。假定此指標在多次查詢之間仍保持有效，並不明智。

<a id="LIBPQ-PQFULLPROTOCOLVERSION"></a>

### `PQfullProtocolVersion`<a id="id-1.7.3.9.5.2.4.1.2"></a> [#](#libpq-pqfullprotocolversion) <a href="#libpq-pqfullprotocolversion" id="libpq-pqfullprotocolversion"></a>

查詢目前使用的前端／後端協定。

```

    int PQfullProtocolVersion(const PGconn *conn);
```

應用程式可能會想使用此函式來判斷是否支援某些功能。結果的計算方式是將伺服器的主要版本號乘以 10000，再加上次要版本號（原文此處寫作「伺服器的」主要版本號；依後文範例，實際上是所使用協定的主要與次要版本號）。例如，版本 3.2 會傳回 30002，版本 4.0 會傳回 40000。若連線狀態不良，則傳回零。PostgreSQL 伺服器 7.4 以上的版本支援 3.0 協定。

協定版本在連線啟動完成之後不會改變，但理論上可能在連線重設期間改變。

<a id="LIBPQ-PQPROTOCOLVERSION"></a>

### `PQprotocolVersion`<a id="id-1.7.3.9.5.2.5.1.2"></a> [#](#libpq-pqprotocolversion) <a href="#libpq-pqprotocolversion" id="libpq-pqprotocolversion"></a>

查詢前端／後端協定的主要版本。

```

    int PQprotocolVersion(const PGconn *conn);
```

與 [`PQfullProtocolVersion`](libpq-status.md#libpq-pqfullprotocolversion) 不同，此函式只傳回使用中的主要協定版本，但支援它的 libpq 版本範圍更廣，可回溯至版本 7.4。目前可能的值為 3（3.0 協定）或零（連線狀態不良）。在 14.0 版之前，libpq 另外還可能傳回 2（2.0 協定）。

<a id="LIBPQ-PQSERVERVERSION"></a>

### `PQserverVersion`<a id="id-1.7.3.9.5.2.6.1.2"></a> [#](#libpq-pqserverversion) <a href="#libpq-pqserverversion" id="libpq-pqserverversion"></a>

傳回代表伺服器版本的整數。

```

    int PQserverVersion(const PGconn *conn);
```

應用程式可以使用此函式來判斷所連線的資料庫伺服器版本。結果的計算方式是將伺服器的主要版本號乘以 10000，再加上次要版本號。例如，版本 10.1 會傳回 100001，版本 11.0 會傳回 110000。若連線狀態不良，則傳回零。

在主要版本 10 之前，PostgreSQL 使用由三部分組成的版本號，其中前兩部分合起來代表主要版本。對於這些版本，[`PQserverVersion`](libpq-status.md#libpq-pqserverversion) 每個部分各使用兩位數字；例如版本 9.1.5 會傳回 90105，版本 9.2.0 會傳回 90200。

因此，為了判斷功能相容性，應用程式應該將 [`PQserverVersion`](libpq-status.md#libpq-pqserverversion) 的結果除以 100（而非 10000），以求得邏輯上的主要版本號。在所有發行系列中，次要版本（錯誤修正版本）之間只有最後兩位數字不同。

<a id="LIBPQ-PQERRORMESSAGE"></a>

### `PQerrorMessage`<a id="id-1.7.3.9.5.2.7.1.2"></a> <a id="id-1.7.3.9.5.2.7.1.3"></a> [#](#libpq-pqerrormessage) <a href="#libpq-pqerrormessage" id="libpq-pqerrormessage"></a>

傳回該連線上的操作最近一次產生的錯誤訊息。

```

    char *PQerrorMessage(const PGconn *conn);
```

幾乎所有 libpq 函式在失敗時都會為 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage) 設定訊息。請注意，依照 libpq 的慣例，非空的 [`PQerrorMessage`](libpq-status.md#libpq-pqerrormessage) 結果可能由多行組成，並且會包含結尾的換行字元。呼叫端不應直接釋放此結果。當相關聯的 `PGconn` 代號（handle）傳給 [`PQfinish`](libpq-connect.md#libpq-pqfinish) 時，它會被釋放。不應預期此結果字串在對 `PGconn` 結構進行多次操作之間保持不變。

<a id="LIBPQ-PQSOCKET"></a>

### `PQsocket`<a id="id-1.7.3.9.5.2.8.1.2"></a> [#](#libpq-pqsocket) <a href="#libpq-pqsocket" id="libpq-pqsocket"></a>

取得連往伺服器的連線通訊端的檔案描述子編號。有效的描述子會大於或等於 0；結果為 -1 表示目前沒有開啟的伺服器連線。（此值在正常運作期間不會改變，但可能在連線設定或重設期間改變。）

```

    int PQsocket(const PGconn *conn);
```

<a id="LIBPQ-PQBACKENDPID"></a>

### `PQbackendPID`<a id="id-1.7.3.9.5.2.9.1.2"></a> [#](#libpq-pqbackendpid) <a href="#libpq-pqbackendpid" id="libpq-pqbackendpid"></a>

傳回處理此連線之後端程序的程序 ID（PID）<a id="id-1.7.3.9.5.2.9.2.1.2"></a>。

```

    int PQbackendPID(const PGconn *conn);
```

後端 PID 可用於除錯，以及與 `NOTIFY` 訊息（其中包含發出通知之後端程序的 PID）進行比對。請注意，此 PID 屬於在資料庫伺服器主機上執行的程序，而不是本機上的程序！

<a id="LIBPQ-PQCONNECTIONNEEDSPASSWORD"></a>

### `PQconnectionNeedsPassword`<a id="id-1.7.3.9.5.2.10.1.2"></a> [#](#libpq-pqconnectionneedspassword) <a href="#libpq-pqconnectionneedspassword" id="libpq-pqconnectionneedspassword"></a>

若連線的認證方法需要密碼，但沒有可用的密碼，則傳回 true（1）。否則傳回 false（0）。

```

    int PQconnectionNeedsPassword(const PGconn *conn);
```

此函式可在連線嘗試失敗後使用，以決定是否提示使用者輸入密碼。

<a id="LIBPQ-PQCONNECTIONUSEDPASSWORD"></a>

### `PQconnectionUsedPassword`<a id="id-1.7.3.9.5.2.11.1.2"></a> [#](#libpq-pqconnectionusedpassword) <a href="#libpq-pqconnectionusedpassword" id="libpq-pqconnectionusedpassword"></a>

若連線的認證方法使用了密碼，則傳回 true（1）。否則傳回 false（0）。

```

    int PQconnectionUsedPassword(const PGconn *conn);
```

此函式可在連線嘗試失敗或成功後使用，以偵測伺服器是否要求了密碼。

<a id="LIBPQ-PQCONNECTIONUSEDGSSAPI"></a>

### `PQconnectionUsedGSSAPI`<a id="id-1.7.3.9.5.2.12.1.2"></a> [#](#libpq-pqconnectionusedgssapi) <a href="#libpq-pqconnectionusedgssapi" id="libpq-pqconnectionusedgssapi"></a>

若連線的認證方法使用了 GSSAPI，則傳回 true（1）。否則傳回 false（0）。

```

    int PQconnectionUsedGSSAPI(const PGconn *conn);
```

此函式可用來偵測連線是否以 GSSAPI 進行認證。

下列函式傳回與 SSL 相關的資訊。這些資訊在連線建立之後通常不會改變。

<a id="LIBPQ-PQSSLINUSE"></a>

### `PQsslInUse`<a id="id-1.7.3.9.6.1.1.1.2"></a> [#](#libpq-pqsslinuse) <a href="#libpq-pqsslinuse" id="libpq-pqsslinuse"></a>

若連線使用 SSL，則傳回 true（1）；否則傳回 false（0）。

```

    int PQsslInUse(const PGconn *conn);
```

<a id="LIBPQ-PQSSLATTRIBUTE"></a>

### `PQsslAttribute`<a id="id-1.7.3.9.6.1.2.1.2"></a> [#](#libpq-pqsslattribute) <a href="#libpq-pqsslattribute" id="libpq-pqsslattribute"></a>

傳回關於連線的 SSL 相關資訊。

```

    const char *PQsslAttribute(const PGconn *conn, const char *attribute_name);
```

可用屬性的清單會因所使用的 SSL 函式庫與連線類型而異。若連線未使用 SSL，或所指定的屬性名稱對使用中的函式庫未定義，則傳回 NULL。

下列屬性通常可以使用：

- `library`

  使用中的 SSL 實作名稱。（目前只實作了 `"OpenSSL"`）

- `protocol`

  使用中的 SSL/TLS 版本。常見的值有 `"TLSv1"`、`"TLSv1.1"` 與 `"TLSv1.2"`，但若使用其他協定，實作可能會傳回其他字串。

- `key_bits`

  加密演算法所使用的金鑰位元數。

- `cipher`

  所使用密碼套件的簡短名稱，例如 `"DHE-RSA-DES-CBC3-SHA"`。這些名稱因各個 SSL 實作而異。

- `compression`

  若使用 SSL 壓縮，則傳回 "on"，否則傳回 "off"。

- `alpn`

  由 TLS 應用層協定協商（ALPN）擴充所選定的應用協定。libpq 唯一支援的協定是 `postgresql`，因此這主要用於檢查伺服器是否支援 ALPN。若未使用 ALPN，則為空字串。

作為特殊情況，可以將 NULL 作為 `conn` 引數傳入，在沒有連線的情況下查詢 `library` 屬性。結果會是預設的 SSL 函式庫名稱；若 libpq 編譯時未包含任何 SSL 支援，則為 NULL。（在 PostgreSQL 15 版之前，將 NULL 作為 `conn` 引數傳入一律會得到 NULL。需要區分此情況新舊實作的用戶端程式，可以檢查 `LIBPQ_HAS_SSL_LIBRARY_DETECTION` 功能巨集。）

<a id="LIBPQ-PQSSLATTRIBUTENAMES"></a>

### `PQsslAttributeNames`<a id="id-1.7.3.9.6.1.3.1.2"></a> [#](#libpq-pqsslattributenames) <a href="#libpq-pqsslattributenames" id="libpq-pqsslattributenames"></a>

傳回可用於 `PQsslAttribute()` 的 SSL 屬性名稱陣列。此陣列以 NULL 指標結尾。

```

    const char * const * PQsslAttributeNames(const PGconn *conn);
```

若 `conn` 為 NULL，則傳回預設 SSL 函式庫可用的屬性；若 libpq 編譯時未包含任何 SSL 支援，則傳回空清單。若 `conn` 不為 NULL，則傳回該連線所使用之 SSL 函式庫可用的屬性；若連線未加密，則傳回空清單。

<a id="LIBPQ-PQSSLSTRUCT"></a>

### `PQsslStruct`<a id="id-1.7.3.9.6.1.4.1.2"></a> [#](#libpq-pqsslstruct) <a href="#libpq-pqsslstruct" id="libpq-pqsslstruct"></a>

傳回指向描述此連線、特定於 SSL 實作之物件的指標。若連線未加密，或無法從該連線的 SSL 實作取得所要求類型的物件，則傳回 NULL。

```

    void *PQsslStruct(const PGconn *conn, const char *struct_name);
```

可用的結構取決於使用中的 SSL 實作。對 OpenSSL 而言，只有一個結構，可透過名稱 `OpenSSL` 取得，它會傳回指向 OpenSSL 的 `SSL` 結構的指標。要使用此函式，可以使用類似下列的程式碼：

```

    #include <libpq-fe.h>
    #include <openssl/ssl.h>

    ...

        SSL *ssl;

        dbconn = PQconnectdb(...);
        ...

        ssl = PQsslStruct(dbconn, "OpenSSL");
        if (ssl)
        {
            /* use OpenSSL functions to access ssl */
        }
```

此結構可用來驗證加密等級、檢查伺服器憑證等。關於此結構的資訊，請參閱 OpenSSL 的文件。

<a id="LIBPQ-PQGETSSL"></a>

### `PQgetssl`<a id="id-1.7.3.9.6.1.5.1.2"></a> [#](#libpq-pqgetssl) <a href="#libpq-pqgetssl" id="libpq-pqgetssl"></a>

<a id="id-1.7.3.9.6.1.5.2.1.1"></a>
傳回連線中使用的 SSL 結構；若未使用 SSL，則傳回 NULL。

```

    void *PQgetssl(const PGconn *conn);
```

此函式等同於 `PQsslStruct(conn, "OpenSSL")`。新的應用程式不應使用它，因為傳回的結構特定於 OpenSSL，在使用其他 SSL 實作時將無法取得。若要檢查連線是否使用 SSL，請改為呼叫 [`PQsslInUse`](libpq-status.md#libpq-pqsslinuse)；若要取得關於連線的更多細節，請使用 [`PQsslAttribute`](libpq-status.md#libpq-pqsslattribute)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-status.html)（原文版本：18.6；核對日期：2026-10-17）
