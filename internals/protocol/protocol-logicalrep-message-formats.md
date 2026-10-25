<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS"></a>

## 54.9. 邏輯複寫訊息格式 [#](#protocol-logicalrep-message-formats) <a href="#protocol-logicalrep-message-formats" id="protocol-logicalrep-message-formats"></a>

本節說明每種邏輯複寫訊息的詳細格式。這些訊息由複寫插槽的 SQL 介面傳回，或由 walsender 傳送。若由 walsender 傳送，這些訊息會封裝在[第 54.4 節](protocol-replication.md)所述的複寫協定 WAL 訊息之中，且大致遵循與實體複寫相同的訊息流程。

<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-BEGIN"></a>

Begin [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-BEGIN)
:   Byte1('B')
    :   將此訊息識別為 Begin 訊息。

    Int64 (XLogRecPtr)
    :   交易的最終 LSN。

    Int64 (TimestampTz)
    :   交易的提交時間戳記。此值為自 PostgreSQL 紀元（2000-01-01）起算的微秒數。

    Int32 (TransactionId)
    :   交易的 Xid。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-MESSAGE"></a>

Message [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-MESSAGE)
:   Byte1('M')
    :   將此訊息識別為邏輯解碼訊息。

    Int32 (TransactionId)
    :   交易的 Xid（僅出現於串流傳送的交易）。此欄位自協定版本 2 起提供。

    Int8
    :   旗標；0 表示沒有旗標，1 表示該邏輯解碼訊息具交易性。

    Int64 (XLogRecPtr)
    :   邏輯解碼訊息的 LSN。

    String
    :   邏輯解碼訊息的前綴。

    Int32
    :   內容的長度。

    Byte*`n`*
    :   邏輯解碼訊息的內容。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-COMMIT"></a>

Commit [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-COMMIT)
:   Byte1('C')
    :   將此訊息識別為 Commit 訊息。

    Int8(0)
    :   旗標；目前未使用。

    Int64 (XLogRecPtr)
    :   提交的 LSN。

    Int64 (XLogRecPtr)
    :   交易的結束 LSN。

    Int64 (TimestampTz)
    :   交易的提交時間戳記。此值為自 PostgreSQL 紀元（2000-01-01）起算的微秒數。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-ORIGIN"></a>

Origin [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-ORIGIN)
:   Byte1('O')
    :   將此訊息識別為 Origin 訊息。

    Int64 (XLogRecPtr)
    :   來源伺服器上提交的 LSN。

    String
    :   來源的名稱。

    請注意，單一交易內可能有多個 Origin 訊息。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-RELATION"></a>

Relation [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-RELATION)
:   Byte1('R')
    :   將此訊息識別為 Relation 訊息。

    Int32 (TransactionId)
    :   交易的 Xid（僅出現於串流傳送的交易）。此欄位自協定版本 2 起提供。

    Int32 (Oid)
    :   關聯的 OID。

    String
    :   命名空間（`pg_catalog` 為空字串）。

    String
    :   關聯名稱。

    Int8
    :   該關聯的複本識別設定（與 `pg_class` 中的 `relreplident` 相同）。

    Int16
    :   欄位數。

    接著，發佈中所包含的每個欄位各會出現下列訊息部分：

    Int8
    :   欄位的旗標。目前可以是 0，表示沒有旗標；或 1，將該欄位標示為鍵的一部分。

    String
    :   欄位名稱。

    Int32 (Oid)
    :   欄位資料型別的 OID。

    Int32
    :   欄位的型別修飾詞（`atttypmod`）。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-TYPE"></a>

Type [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-TYPE)
:   Byte1('Y')
    :   將此訊息識別為 Type 訊息。

    Int32 (TransactionId)
    :   交易的 Xid（僅出現於串流傳送的交易）。此欄位自協定版本 2 起提供。

    Int32 (Oid)
    :   資料型別的 OID。

    String
    :   命名空間（`pg_catalog` 為空字串）。

    String
    :   資料型別的名稱。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-INSERT"></a>

Insert [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-INSERT)
:   Byte1('I')
    :   將此訊息識別為 Insert 訊息。

    Int32 (TransactionId)
    :   交易的 Xid（僅出現於串流傳送的交易）。此欄位自協定版本 2 起提供。

    Int32 (Oid)
    :   對應於 Relation 訊息中 ID 的關聯 OID。

    Byte1('N')
    :   將其後的 TupleData 訊息識別為新元組。

    TupleData
    :   表示新元組內容的 TupleData 訊息部分。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-UPDATE"></a>

Update [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-UPDATE)
:   Byte1('U')
    :   將此訊息識別為 Update 訊息。

    Int32 (TransactionId)
    :   交易的 Xid（僅出現於串流傳送的交易）。此欄位自協定版本 2 起提供。

    Int32 (Oid)
    :   對應於 Relation 訊息中 ID 的關聯 OID。

    Byte1('K')
    :   將其後的 TupleData 子訊息識別為鍵。此欄位為選擇性，只有在更新變更了屬於 REPLICA IDENTITY 索引之任一欄位的資料時才會出現。

    Byte1('O')
    :   將其後的 TupleData 子訊息識別為舊元組。此欄位為選擇性，只有在發生更新的資料表將 REPLICA IDENTITY 設為 FULL 時才會出現。

    TupleData
    :   表示舊元組或主鍵內容的 TupleData 訊息部分。只有在前面出現 'O' 或 'K' 部分時才會出現。

    Byte1('N')
    :   將其後的 TupleData 訊息識別為新元組。

    TupleData
    :   表示新元組內容的 TupleData 訊息部分。

    Update 訊息可能包含 'K' 訊息部分或 'O' 訊息部分，或兩者皆無，但絕不會同時包含兩者。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-DELETE"></a>

Delete [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-DELETE)
:   Byte1('D')
    :   將此訊息識別為 Delete 訊息。

    Int32 (TransactionId)
    :   交易的 Xid（僅出現於串流傳送的交易）。此欄位自協定版本 2 起提供。

    Int32 (Oid)
    :   對應於 Relation 訊息中 ID 的關聯 OID。

    Byte1('K')
    :   將其後的 TupleData 子訊息識別為鍵。若發生刪除的資料表使用索引作為 REPLICA IDENTITY，就會出現此欄位。

    Byte1('O')
    :   將其後的 TupleData 訊息識別為舊元組。若發生刪除的資料表將 REPLICA IDENTITY 設為 FULL，就會出現此欄位。

    TupleData
    :   表示舊元組或主鍵內容的 TupleData 訊息部分，取決於前一個欄位。

    Delete 訊息可能包含 'K' 訊息部分或 'O' 訊息部分，但絕不會同時包含兩者。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-TRUNCATE"></a>

Truncate [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-TRUNCATE)
:   Byte1('T')
    :   將此訊息識別為 Truncate 訊息。

    Int32 (TransactionId)
    :   交易的 Xid（僅出現於串流傳送的交易）。此欄位自協定版本 2 起提供。

    Int32
    :   關聯數

    Int8
    :   `TRUNCATE` 的選項位元：1 表示 `CASCADE`，2 表示 `RESTART IDENTITY`

    Int32 (Oid)
    :   對應於 Relation 訊息中 ID 的關聯 OID。每個關聯都會重複此欄位。

下列訊息（Stream Start、Stream Stop、Stream Commit 與 Stream Abort）自協定版本 2 起提供。

<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-START"></a>

Stream Start [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-START)
:   Byte1('S')
    :   將此訊息識別為 Stream Start 訊息。

    Int32 (TransactionId)
    :   交易的 Xid。

    Int8
    :   值為 1 表示這是此 XID 的第一個串流區段，其他任何串流區段則為 0。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-STOP"></a>

Stream Stop [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-STOP)
:   Byte1('E')
    :   將此訊息識別為 Stream Stop 訊息。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-COMMIT"></a>

Stream Commit [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-COMMIT)
:   Byte1('c')
    :   將此訊息識別為 Stream Commit 訊息。

    Int32 (TransactionId)
    :   交易的 Xid。

    Int8(0)
    :   旗標；目前未使用。

    Int64 (XLogRecPtr)
    :   提交的 LSN。

    Int64 (XLogRecPtr)
    :   交易的結束 LSN。

    Int64 (TimestampTz)
    :   交易的提交時間戳記。此值為自 PostgreSQL 紀元（2000-01-01）起算的微秒數。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-ABORT"></a>

Stream Abort [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-ABORT)
:   Byte1('A')
    :   將此訊息識別為 Stream Abort 訊息。

    Int32 (TransactionId)
    :   交易的 Xid。

    Int32 (TransactionId)
    :   子交易的 Xid（對於最上層交易，會與該交易的 xid 相同）。

    Int64 (XLogRecPtr)
    :   中止操作的 LSN，只有在串流模式（streaming）設為平行（parallel）時才會出現。此欄位自協定版本 4 起提供。

    Int64 (TimestampTz)
    :   交易的中止時間戳記，只有在串流模式（streaming）設為平行（parallel）時才會出現。此值為自 PostgreSQL 紀元（2000-01-01）起算的微秒數。此欄位自協定版本 4 起提供。

下列訊息（Begin Prepare、Prepare、Commit Prepared、Rollback Prepared、Stream Prepare）自協定版本 3 起提供。

<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-BEGIN-PREPARE"></a>

Begin Prepare [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-BEGIN-PREPARE)
:   Byte1('b')
    :   將此訊息識別為預備交易的開始訊息。

    Int64 (XLogRecPtr)
    :   準備作業（prepare）的 LSN。

    Int64 (XLogRecPtr)
    :   預備交易的結束 LSN。

    Int64 (TimestampTz)
    :   交易的準備時間戳記。此值為自 PostgreSQL 紀元（2000-01-01）起算的微秒數。

    Int32 (TransactionId)
    :   交易的 Xid。

    String
    :   使用者為預備交易定義的 GID。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-PREPARE"></a>

Prepare [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-PREPARE)
:   Byte1('P')
    :   將此訊息識別為預備交易訊息。

    Int8(0)
    :   旗標；目前未使用。

    Int64 (XLogRecPtr)
    :   準備作業（prepare）的 LSN。

    Int64 (XLogRecPtr)
    :   預備交易的結束 LSN。

    Int64 (TimestampTz)
    :   交易的準備時間戳記。此值為自 PostgreSQL 紀元（2000-01-01）起算的微秒數。

    Int32 (TransactionId)
    :   交易的 Xid。

    String
    :   使用者為預備交易定義的 GID。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-COMMIT-PREPARED"></a>

Commit Prepared [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-COMMIT-PREPARED)
:   Byte1('K')
    :   將此訊息識別為預備交易的提交訊息。

    Int8(0)
    :   旗標；目前未使用。

    Int64 (XLogRecPtr)
    :   預備交易之提交的 LSN。

    Int64 (XLogRecPtr)
    :   預備交易之提交的結束 LSN。

    Int64 (TimestampTz)
    :   交易的提交時間戳記。此值為自 PostgreSQL 紀元（2000-01-01）起算的微秒數。

    Int32 (TransactionId)
    :   交易的 Xid。

    String
    :   使用者為預備交易定義的 GID。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-ROLLBACK-PREPARED"></a>

Rollback Prepared [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-ROLLBACK-PREPARED)
:   Byte1('r')
    :   將此訊息識別為預備交易的復原訊息。

    Int8(0)
    :   旗標；目前未使用。

    Int64 (XLogRecPtr)
    :   預備交易的結束 LSN。

    Int64 (XLogRecPtr)
    :   預備交易之復原的結束 LSN。

    Int64 (TimestampTz)
    :   交易的準備時間戳記。此值為自 PostgreSQL 紀元（2000-01-01）起算的微秒數。

    Int64 (TimestampTz)
    :   交易的復原時間戳記。此值為自 PostgreSQL 紀元（2000-01-01）起算的微秒數。

    Int32 (TransactionId)
    :   交易的 Xid。

    String
    :   使用者為預備交易定義的 GID。
<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-PREPARE"></a>

Stream Prepare [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-PREPARE)
:   Byte1('p')
    :   將此訊息識別為串流預備交易訊息。

    Int8(0)
    :   旗標；目前未使用。

    Int64 (XLogRecPtr)
    :   準備作業（prepare）的 LSN。

    Int64 (XLogRecPtr)
    :   預備交易的結束 LSN。

    Int64 (TimestampTz)
    :   交易的準備時間戳記。此值為自 PostgreSQL 紀元（2000-01-01）起算的微秒數。

    Int32 (TransactionId)
    :   交易的 Xid。

    String
    :   使用者為預備交易定義的 GID。

下列訊息部分由上述訊息共用。

<a id="PROTOCOL-LOGICALREP-MESSAGE-FORMATS-TUPLEDATA"></a>

TupleData [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-TUPLEDATA)
:   Int16
    :   欄位數。

    接著，每個已發佈的欄位各會出現下列其中一個子訊息：

    Byte1('n')
    :   將此資料識別為 NULL 值。

    或

    Byte1('u')
    :   識別未變更的 TOAST 值（不會傳送實際的值）。

    或

    Byte1('t')
    :   將此資料識別為文字格式的值。

    或

    Byte1('b')
    :   將此資料識別為二進位格式的值。

    Int32
    :   欄位值的長度。

    Byte*`n`*
    :   欄位的值，採二進位或文字格式（依前面的格式位元組所指定）。*`n`* 為上述長度。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/protocol-logicalrep-message-formats.html)（原文版本：18.6；核對日期：2026-10-12）
