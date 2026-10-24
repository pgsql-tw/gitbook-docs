<a id="LO-INTERFACES"></a>

## 33.3. 用戶端介面 [#](#LO-INTERFACES)

[33.3.1. 建立大型物件](lo-interfaces.md#LO-CREATE)

[33.3.2. 匯入大型物件](lo-interfaces.md#LO-IMPORT)

[33.3.3. 匯出大型物件](lo-interfaces.md#LO-EXPORT)

[33.3.4. 開啟既有的大型物件](lo-interfaces.md#LO-OPEN)

[33.3.5. 將資料寫入大型物件](lo-interfaces.md#LO-WRITE)

[33.3.6. 從大型物件讀取資料](lo-interfaces.md#LO-READ)

[33.3.7. 在大型物件中移動位置](lo-interfaces.md#LO-SEEK)

[33.3.8. 取得大型物件的目前位置](lo-interfaces.md#LO-TELL)

[33.3.9. 截斷大型物件](lo-interfaces.md#LO-TRUNCATE)

[33.3.10. 關閉大型物件描述子](lo-interfaces.md#LO-CLOSE)

[33.3.11. 移除大型物件](lo-interfaces.md#LO-UNLINK)

本節說明 PostgreSQL 的 libpq
用戶端介面函式庫為存取大型物件所提供的功能。
PostgreSQL 的大型物件介面
是仿照 Unix 檔案系統介面設計的，
具有 `open`、`read`、
`write`、
`lseek` 等的對應功能。

所有使用這些函式的大型物件操作
都*必須*在 SQL 交易區塊內進行，
因為大型物件的檔案描述子只在交易期間
有效。寫入操作（包括以 `INV_WRITE` 模式執行的
`lo_open`）不允許在唯讀
交易中進行。

若在執行這些函式中的任何一個時發生錯誤，
該函式會傳回在其他情況下不可能出現的值，通常是 0 或 -1。
描述錯誤的訊息會儲存在連線物件中，
可以用 [`PQerrorMessage`](../libpq/libpq-status.md#libpq-pqerrormessage) 取得。

使用這些函式的用戶端應用程式應該引入標頭檔
`libpq/libpq-fs.h`，並與
libpq 函式庫連結。

當 libpq 連線處於管線模式時，用戶端應用程式不能使用這些函式。

<a id="LO-CREATE"></a>

### 33.3.1. 建立大型物件 [#](#LO-CREATE)

<a id="id-1.7.4.8.7.2.1"></a>
函式

```

Oid lo_create(PGconn *conn, Oid lobjId);
```

會建立一個新的大型物件。要指派的 OID 可以
由 *`lobjId`* 指定；
若有指定，且該 OID 已被某個大型物件使用，
就會失敗。若 *`lobjId`*
為 `InvalidOid`（零），則 `lo_create`
會指派一個未使用的 OID。
傳回值是指派給新大型物件的 OID，
失敗時則為 `InvalidOid`（零）。

範例：

```

inv_oid = lo_create(conn, desired_oid);
```

<a id="id-1.7.4.8.7.4.1"></a>
較舊的函式

```

Oid lo_creat(PGconn *conn, int mode);
```

也會建立新的大型物件，且一律指派一個未使用的 OID。
傳回值是指派給新大型物件的 OID，
失敗時則為 `InvalidOid`（零）。

在 PostgreSQL 8.1 及之後的版本中，
*`mode`* 會被忽略，
因此 `lo_creat` 完全等同於
第二個引數為零的 `lo_create`。
不過，除非你需要與 8.1 之前的伺服器搭配使用，
否則沒有什麼理由使用 `lo_creat`。
若要與這類舊伺服器搭配使用，你必須
使用 `lo_creat` 而非 `lo_create`，
而且必須將 *`mode`* 設為
`INV_READ`、`INV_WRITE`
或 `INV_READ` `|` `INV_WRITE` 其中之一。
（這些符號常數定義於
標頭檔 `libpq/libpq-fs.h` 中。）

範例：

```

inv_oid = lo_creat(conn, INV_READ|INV_WRITE);
```

<a id="LO-IMPORT"></a>

### 33.3.2. 匯入大型物件 [#](#LO-IMPORT)

<a id="id-1.7.4.8.8.2.1"></a>
若要將作業系統檔案匯入為大型物件，請呼叫

```

Oid lo_import(PGconn *conn, const char *filename);
```

*`filename`*
指定要匯入為大型物件之檔案
在作業系統中的名稱。
傳回值是指派給新大型物件的 OID，
失敗時則為 `InvalidOid`（零）。
請注意，檔案是由用戶端介面函式庫讀取，而不是由
伺服器讀取；因此它必須存在於用戶端檔案系統中，且
用戶端應用程式必須能夠讀取它。

<a id="id-1.7.4.8.8.3.1"></a>
函式

```

Oid lo_import_with_oid(PGconn *conn, const char *filename, Oid lobjId);
```

也會匯入一個新的大型物件。要指派的 OID 可以
由 *`lobjId`* 指定；
若有指定，且該 OID 已被某個大型物件使用，
就會失敗。若 *`lobjId`*
為 `InvalidOid`（零），則 `lo_import_with_oid` 會指派一個未使用的
OID（這與 `lo_import` 的行為相同）。
傳回值是指派給新大型物件的 OID，
失敗時則為 `InvalidOid`（零）。

`lo_import_with_oid` 是自 PostgreSQL
8.4 起新增的，並在內部使用 8.1 新增的 `lo_create`；若對 8.0 或更早版本執行此函式，
它會失敗並傳回 `InvalidOid`。

<a id="LO-EXPORT"></a>

### 33.3.3. 匯出大型物件 [#](#LO-EXPORT)

<a id="id-1.7.4.8.9.2.1"></a>
若要將大型物件
匯出為作業系統檔案，請呼叫

```

int lo_export(PGconn *conn, Oid lobjId, const char *filename);
```

*`lobjId`* 引數指定要匯出之大型
物件的 OID，*`filename`* 引數則
指定檔案在作業系統中的名稱。請注意，檔案是
由用戶端介面函式庫寫入，而不是由伺服器寫入。成功時傳回 1，
失敗時傳回 -1。

<a id="LO-OPEN"></a>

### 33.3.4. 開啟既有的大型物件 [#](#LO-OPEN)

<a id="id-1.7.4.8.10.2.1"></a>
若要開啟既有的大型物件以進行讀取或寫入，請呼叫

```

int lo_open(PGconn *conn, Oid lobjId, int mode);
```

*`lobjId`* 引數指定要開啟之大型
物件的 OID。*`mode`* 位元控制
物件是以讀取（`INV_READ`）、寫入
（`INV_WRITE`）或兩者兼具的方式開啟。
（這些符號常數定義於
標頭檔 `libpq/libpq-fs.h` 中。）
`lo_open` 會傳回一個（非負的）大型物件
描述子，供之後在 `lo_read`、
`lo_write`、`lo_lseek`、
`lo_lseek64`、`lo_tell`、
`lo_tell64`、`lo_truncate`、
`lo_truncate64` 與 `lo_close` 中使用。
此描述子只在
目前交易期間有效。
失敗時傳回 -1。

伺服器目前不區分
`INV_WRITE` 與 `INV_READ` `|`
`INV_WRITE` 模式：在這兩種情況下，你都可以從描述子讀取。
然而，這些模式與單獨使用 `INV_READ` 之間有重大差異：使用 `INV_READ` 時，
你不能寫入該描述子，而且從中讀取的資料
會反映執行 `lo_open` 時作用中的交易快照當時
大型物件的內容，
不論之後本交易或其他交易是否有寫入。從
以 `INV_WRITE` 開啟的描述子讀取時，傳回的
資料會反映其他已提交交易的所有寫入，以及
目前交易的寫入。這類似於一般 SQL `SELECT` 命令在
`REPEATABLE READ` 與 `READ COMMITTED` 交易
模式下的行為差異。

若大型物件沒有可用的 `SELECT`
權限，或者指定了 `INV_WRITE` 但沒有可用的 `UPDATE`
權限，`lo_open` 就會失敗。
（在 PostgreSQL 11 之前，這些權限
檢查是改在第一次使用該描述子實際進行讀取或寫入呼叫時執行。）
這些權限檢查可以用
[lo_compat_privileges](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-LO-COMPAT-PRIVILEGES) 執行期參數停用。

範例：

```

inv_fd = lo_open(conn, inv_oid, INV_READ|INV_WRITE);
```

<a id="LO-WRITE"></a>

### 33.3.5. 將資料寫入大型物件 [#](#LO-WRITE)

<a id="id-1.7.4.8.11.2.1"></a>
函式

```

int lo_write(PGconn *conn, int fd, const char *buf, size_t len);
```

會從 *`buf`*（其大小必須為 *`len`*）
將 *`len`* 個位元組寫入大型物件
描述子 *`fd`*。*`fd`* 引數必須
是先前某次 `lo_open` 所傳回的。
傳回值是實際寫入的位元組數（在目前的
實作中，除非發生錯誤，否則一律等於 *`len`*）。
發生錯誤時，傳回值為 -1。

雖然 *`len`* 參數宣告為
`size_t`，此函式會拒絕大於
`INT_MAX` 的長度值。實務上，無論如何最好以
最多幾 MB 的區塊來傳輸資料。

<a id="LO-READ"></a>

### 33.3.6. 從大型物件讀取資料 [#](#LO-READ)

<a id="id-1.7.4.8.12.2.1"></a>
函式

```

int lo_read(PGconn *conn, int fd, char *buf, size_t len);
```

會從大型物件描述子 *`fd`*
讀取最多 *`len`* 個位元組到 *`buf`*（其大小必須
為 *`len`*）中。*`fd`*
引數必須是先前某次
`lo_open` 所傳回的。傳回值是實際讀取的位元組數；
若先到達大型物件的結尾，此值會小於 *`len`*。
發生錯誤時，傳回值為 -1。

雖然 *`len`* 參數宣告為
`size_t`，此函式會拒絕大於
`INT_MAX` 的長度值。實務上，無論如何最好以
最多幾 MB 的區塊來傳輸資料。

<a id="LO-SEEK"></a>

### 33.3.7. 在大型物件中移動位置 [#](#LO-SEEK)

<a id="id-1.7.4.8.13.2.1"></a>
若要變更與大型物件描述子相關聯的目前讀取或寫入位置，
請呼叫

```

int lo_lseek(PGconn *conn, int fd, int offset, int whence);
```

此函式會將由 *`fd`* 識別之大型物件描述子的
目前位置指標，移到由
*`offset`* 指定的新位置。*`whence`* 的有效值
為 `SEEK_SET`（從物件開頭移動）、
`SEEK_CUR`（從目前位置移動）與
`SEEK_END`（從物件結尾移動）。傳回值為
新的位置指標，發生錯誤時則為 -1。

<a id="id-1.7.4.8.13.3.1"></a>
處理大小可能超過 2GB 的大型物件時，
請改用

```

int64_t lo_lseek64(PGconn *conn, int fd, int64_t offset, int whence);
```

此函式的行為與
`lo_lseek` 相同，但它可以接受大於 2GB 的
*`offset`*，和／或傳回大於
2GB 的結果。
請注意，若新的位置
指標會大於 2GB，`lo_lseek` 就會失敗。

`lo_lseek64` 是自 PostgreSQL
9.3 起新增的。若對較舊版本的伺服器執行此函式，它會
失敗並傳回 -1。

<a id="LO-TELL"></a>

### 33.3.8. 取得大型物件的目前位置 [#](#LO-TELL)

<a id="id-1.7.4.8.14.2.1"></a>
若要取得大型物件描述子目前的讀取或寫入位置，
請呼叫

```

int lo_tell(PGconn *conn, int fd);
```

若發生錯誤，傳回值為 -1。

<a id="id-1.7.4.8.14.3.1"></a>
處理大小可能超過 2GB 的大型物件時，
請改用

```

int64_t lo_tell64(PGconn *conn, int fd);
```

此函式的行為與
`lo_tell` 相同，但它可以傳回大於
2GB 的結果。
請注意，若目前的
讀取／寫入位置大於 2GB，`lo_tell` 就會失敗。

`lo_tell64` 是自 PostgreSQL
9.3 起新增的。若對較舊版本的伺服器執行此函式，它會
失敗並傳回 -1。

<a id="LO-TRUNCATE"></a>

### 33.3.9. 截斷大型物件 [#](#LO-TRUNCATE)

<a id="id-1.7.4.8.15.2.1"></a>
若要將大型物件截斷為給定長度，請呼叫

```

int lo_truncate(PGconn *conn, int fd, size_t len);
```

此函式會將大型物件描述子 *`fd`* 所指的大型物件截斷為長度 *`len`*（原文此處寫作將描述子截斷，但實際被截斷的是描述子所指的大型物件，描述子本身並沒有長度）。
*`fd`* 引數必須是先前某次
`lo_open` 所傳回的。若 *`len`*
大於大型物件目前的長度，該大型物件
會以空位元組（'\0'）延伸到指定的長度。
成功時，`lo_truncate` 傳回
零。發生錯誤時，傳回值為 -1。

與描述子 *`fd`* 相關聯的讀取／寫入位置
不會改變。

雖然 *`len`* 參數宣告為
`size_t`，`lo_truncate` 會拒絕大於
`INT_MAX` 的長度值。

<a id="id-1.7.4.8.15.5.1"></a>
處理大小可能超過 2GB 的大型物件時，
請改用

```

int lo_truncate64(PGconn *conn, int fd, int64_t len);
```

此函式的行為與 `lo_truncate` 相同，
但它可以接受超過 2GB 的
*`len`* 值。

`lo_truncate` 是自 PostgreSQL
8.3 起新增的；若對較舊版本的伺服器執行此函式，它會
失敗並傳回 -1。

`lo_truncate64` 是自 PostgreSQL
9.3 起新增的；若對較舊版本的伺服器執行此函式，它會
失敗並傳回 -1。

<a id="LO-CLOSE"></a>

### 33.3.10. 關閉大型物件描述子 [#](#LO-CLOSE)

<a id="id-1.7.4.8.16.2.1"></a>
大型物件描述子可以藉由呼叫下列函式來關閉

```

int lo_close(PGconn *conn, int fd);
```

其中 *`fd`* 是
由 `lo_open` 傳回的大型物件描述子。
成功時，`lo_close` 傳回零。發生
錯誤時，傳回值為 -1。

在交易結束時仍保持開啟的任何大型物件描述子
都會自動關閉。

<a id="LO-UNLINK"></a>

### 33.3.11. 移除大型物件 [#](#LO-UNLINK)

<a id="id-1.7.4.8.17.2.1"></a>
若要從資料庫中移除大型物件，請呼叫

```

int lo_unlink(PGconn *conn, Oid lobjId);
```

*`lobjId`* 引數指定要移除之大型物件
的 OID。成功時傳回 1，失敗時傳回 -1。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/lo-interfaces.html)（原文版本：18.6；核對日期：2026-10-18）
