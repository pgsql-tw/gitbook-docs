---
description: 版本：11
---

# 33.2. 連線狀態函數

這些函數可用於查詢現有資料庫連線物件的狀態。

**提醒**  
libpq 應用程式設計師應該小心地使用 PGconn 的功能。使用下面描述的函數功能以獲取 PGconn 的內容。建議不要使用 libpq-int.h 引用內部 PGconn 變數，因為它們將來可能會有所改變。

以下函數回傳在連線建立時的參數值。這些值在連線的生命週期之間是不變的。如果使用多主機連線字串，則在使用同樣的 PGconn 物件建立新連線時，PQhost，PQport 和 PQpass 的值可能會變動。其他值在 PGconn 物件的生命週期內是不變的。

`PQdb`

回傳連線的資料庫名稱。

```text
char *PQdb(const PGconn *conn);
```

`PQuser`

回傳連線的使用者名稱。

```text
char *PQuser(const PGconn *conn);
```

`PQpass`

回傳連線所使用的密碼。

```text
char *PQpass(const PGconn *conn);
```

`PQhost`

回傳連線的伺服器主機名稱。如果連線是透過 Unix-domain socket，則可以是主機名稱，IP 位址或目錄路徑。（路徑會區分大小寫，因為它始終是一個絕對路徑，並以 / 開頭。）

```text
char *PQhost(const PGconn *conn);
```

`PQport`

回傳連線的連接埠號碼。

```text
char *PQport(const PGconn *conn);
```

`PQtty`

回傳連線的除錯 TTY。（這已經過時了，因為伺服器不再關注 TTY 設定，但此功能仍然存在是為了相容性。）

```text
char *PQtty(const PGconn *conn);
```

`PQoptions`

回傳連線請求中傳遞的命令列選項。

```text
char *PQoptions(const PGconn *conn);
```

以下函數回傳狀態資訊，這些資訊會在 PGconn 物件上執行操作時變動。

`PQstatus`

回傳連線的狀態。

```text
ConnStatusType PQstatus(const PGconn *conn);
```

狀態可以是許多值中的一個。但是，在非同步連線過程之外只能看到其中的兩個：CONNECTION\_OK 和 CONNECTION\_BAD。與資料庫的良好連線時是 CONNECTION\_OK 狀態。CONNECTION\_BAD 狀態表示連線嘗試失敗。通常情況下，OK 狀態將保持不變，直到 PQfinish，但網路故障可能導致狀態提前更改為 CONNECTION\_BAD。在這種情況下，應用程式可以嘗試透過呼叫 PQreset 進行恢復。

有關可能回傳的其他狀態代碼，請參閱 PQconnectStartParams，PQconnectStart 和 PQconnectPoll 的項目。

`PQtransactionStatus`

回傳伺服器的目前在交易事務中狀態。

```text
PGTransactionStatusType PQtransactionStatus(const PGconn *conn);
```

狀態可以是 PQTRANS\_IDLE（目前空閒），PQTRANS\_ACTIVE（命令正在進行中），PQTRANS\_INTRANS（空閒，在有效的事務區塊中）或PQTRANS\_INERROR（空閒，在失敗的事務區塊中）。 如果連線錯誤，則回報 PQTRANS\_UNKNOWN。僅當查詢已發送到伺服器但尚未完成時才會回報 PQTRANS\_ACTIVE。

`PQparameterStatus`

查詢伺服器的目前參數設定。

```text
const char *PQparameterStatus(const PGconn *conn, const char *paramName);
```

伺服器在連線啟動時或其值發生變化時會自動回報某些參數值。PQparameterStatus 可用於查詢這些設定。如果參數已知，則回傳參數的目前值；如果參數未知，則回傳 NULL。

截至目前版本可回報的參數包括 server\_version，server\_encoding，client\_encoding，application\_name，is\_superuser，session\_authorization，DateStyle，IntervalStyle，TimeZone，integer\_datetimes 和 standard\_conforming\_strings。（8.0 之前的版本沒有 server\_encoding，TimeZone 和 integer\_datetimes；8.1 之前的版本沒有 standard\_conforming\_strings；8.4 之前的版本沒有 IntervalStyle；9.0 之前的版本沒有 application\_name。）請注意 server\_version，server\_encoding 和 integer\_datetimes 啟動後無法更改。

3.0 之前的協定，伺服器不回報參數設定，但 libpq 包括了無論如何都要取得 server\_version 和 client\_encoding 的值的邏輯，所以鼓勵應用程式使用 PQparameterStatus 而不是直接的程式碼來確定這些值。（請注意，在 3.0 之前的連線上，在連線啟動後透過 SET 更改 client\_encoding 將不會為 PQparameterStatus 所反映。）對於 server\_version，另請參閱 PQserverVersion，它以更容易比較的數字形式回傳資訊。

如果沒有回報 standard\_conforming\_strings 的值，則應用程式可以假設它已經關閉；而倒斜線在字串文字中被視為轉置符號。此外，可以將此參數的存在視為接受轉置字串語法（E'...'）的指示。

雖然回傳的指標被宣告為 const，但它實際上指向與 PGconn 結構相關聯的可變的儲存空間。假設指標在查詢中保持有效是不明智的。

`PQprotocolVersion`

詢問正在使用的前端/後端協定。

```text
int PQprotocolVersion(const PGconn *conn);
```

應用程式可能希望使用此函數來確定是否支援某些功能。目前，可能的值是 2（2.0 協議），3（3.0 協議）或零（連線錯誤）。 連線啟動完成後協定的版本不會改變，但理論上它可以在連線重置期間改變。通常在與 PostgreSQL 7.4 或更高版本的伺服器連線時使用 3.0 協議；7.4 之前的伺服器僅支持協定 2.0。（協定 1.0 已過時，libpq 不支援。）

`PQserverVersion`

回傳伺服器版本的整數表示。

```text
int PQserverVersion(const PGconn *conn);
```

應用程式可以使用此函數來確定它們所連線的資料庫伺服器版本。結果是以伺服器的主要版本號乘以 10000 再加上次要版本號所組成的。例如，版本 10.1 將回傳為 100001，版本 11.0 將回傳為 110000。如果連線錯誤，則回傳零。

在主要版本 10 之前，PostgreSQL 使用三個部分的版本號碼，其中前兩個部分一起代表主要版本。對於這些版本，PQserverVersion 對每個部分使用兩位數字；例如，版本 9.1.5 將回傳為 90105，版本 9.2.0 將回傳為 90200。

因此，為了符合功能相容性，應用程式應將 PQserverVersion 的結果除以 100 而不是 10000，以確定主版本號碼。在所有版本系列中，只有最後兩位數字在次要版本（錯誤修復版本）之間有所不同。

`PQerrorMessage`

回傳最近於連線操作產生的錯誤訊息。

```text
char *PQerrorMessage(const PGconn *conn);
```

如果 PQerrorMessage 失敗，幾乎所有的 libpq 函數都會為它們設定一條訊息。請注意，根據 libpq 的規則，非空的 PQerrorMessage 結果可以包含多行，並且將包含最後的換行符號。呼叫者不應該直接輸出結果。當關聯的 PGconn 物件傳遞給 PQfinish 時，它將被釋放。不應期望結果字串在 PGconn 結構的操作中保持相同。

`PQsocket`

Obtains the file descriptor number of the connection socket to the server. A valid descriptor will be greater than or equal to 0; a result of -1 indicates that no server connection is currently open. \(This will not change during normal operation, but could change during connection setup or reset.\)

```text
int PQsocket(const PGconn *conn);
```

`PQbackendPID`

Returns the process ID \(PID\) of the backend process handling this connection.

```text
int PQbackendPID(const PGconn *conn);
```

The backend PID is useful for debugging purposes and for comparison to `NOTIFY` messages \(which include the PID of the notifying backend process\). Note that the PID belongs to a process executing on the database server host, not the local host!

`PQconnectionNeedsPassword`

Returns true \(1\) if the connection authentication method required a password, but none was available. Returns false \(0\) if not.

```text
int PQconnectionNeedsPassword(const PGconn *conn);
```

This function can be applied after a failed connection attempt to decide whether to prompt the user for a password.

`PQconnectionUsedPassword`

Returns true \(1\) if the connection authentication method used a password. Returns false \(0\) if not.

```text
int PQconnectionUsedPassword(const PGconn *conn);
```

This function can be applied after either a failed or successful connection attempt to detect whether the server demanded a password.

The following functions return information related to SSL. This information usually doesn't change after a connection is established.

`PQsslInUse`

Returns true \(1\) if the connection uses SSL, false \(0\) if not.

```text
int PQsslInUse(const PGconn *conn);
```

`PQsslAttribute`

Returns SSL-related information about the connection.

```text
const char *PQsslAttribute(const PGconn *conn, const char *attribute_name);
```

The list of available attributes varies depending on the SSL library being used, and the type of connection. If an attribute is not available, returns NULL.

The following attributes are commonly available:

`library`

Name of the SSL implementation in use. \(Currently, only `"OpenSSL"` is implemented\)

`protocol`

SSL/TLS version in use. Common values are `"TLSv1"`, `"TLSv1.1"` and `"TLSv1.2"`, but an implementation may return other strings if some other protocol is used.

`key_bits`

Number of key bits used by the encryption algorithm.

`cipher`

A short name of the ciphersuite used, e.g. `"DHE-RSA-DES-CBC3-SHA"`. The names are specific to each SSL implementation.

`compression`

If SSL compression is in use, returns the name of the compression algorithm, or "on" if compression is used but the algorithm is not known. If compression is not in use, returns "off".

`PQsslAttributeNames`

Return an array of SSL attribute names available. The array is terminated by a NULL pointer.

```text
const char * const * PQsslAttributeNames(const PGconn *conn);
```

`PQsslStruct`

Return a pointer to an SSL-implementation-specific object describing the connection.

```text
void *PQsslStruct(const PGconn *conn, const char *struct_name);
```

The struct\(s\) available depend on the SSL implementation in use. For OpenSSL, there is one struct, available under the name "OpenSSL", and it returns a pointer to the OpenSSL `SSL` struct. To use this function, code along the following lines could be used:

```text
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

This structure can be used to verify encryption levels, check server certificates, and more. Refer to the OpenSSL documentation for information about this structure.`PQgetssl`

Returns the SSL structure used in the connection, or null if SSL is not in use.

```text
void *PQgetssl(const PGconn *conn);
```

This function is equivalent to `PQsslStruct(conn, "OpenSSL")`. It should not be used in new applications, because the returned struct is specific to OpenSSL and will not be available if another SSL implementation is used. To check if a connection uses SSL, call `PQsslInUse` instead, and for more details about the connection, use `PQsslAttribute`.

