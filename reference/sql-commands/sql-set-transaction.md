<a id="id-1.9.3.178.1"></a><a id="id-1.9.3.178.2"></a><a id="id-1.9.3.178.3"></a><a id="id-1.9.3.178.4"></a>

## SET TRANSACTION

SET TRANSACTION — 設定目前交易的特性

## 語法

```

SET TRANSACTION transaction_mode [, ...]
SET TRANSACTION SNAPSHOT snapshot_id
SET SESSION CHARACTERISTICS AS TRANSACTION transaction_mode [, ...]

where transaction_mode is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

<a id="id-1.9.3.178.8"></a>

## 說明

`SET TRANSACTION` 命令會設定目前交易的特性。
它對之後的任何交易不會有任何影響。`SET SESSION
CHARACTERISTICS` 會設定工作階段中後續交易的預設交易特性。
這些預設值可以在個別交易中以 `SET TRANSACTION` 覆寫。

可用的交易特性有交易隔離等級、交易存取模式
（讀寫或唯讀），以及可延遲模式。
此外，也可以選擇快照，不過僅限於目前交易，無法作為工作階段的預設值。

交易的隔離等級決定了當其他交易同時執行時，該交易能看到哪些資料：

`READ COMMITTED`
:   陳述式只能看到在其開始之前已提交的資料列。這是預設值。

`REPEATABLE READ`
:   目前交易中所有的陳述式，只能看到在此交易中第一個查詢
    或資料修改陳述式執行之前已提交的資料列。

`SERIALIZABLE`
:   目前交易中所有的陳述式，只能看到在此交易中第一個查詢
    或資料修改陳述式執行之前已提交的資料列。若並行的可序列化交易之間，
    讀取與寫入的模式會產生一種無法在這些交易以任何序列（一次一個）方式
    執行時發生的情況，其中一個交易就會被回復，並出現
    `serialization_failure` 錯誤。

SQL 標準還定義了另一個等級，即 `READ
UNCOMMITTED`。
在 PostgreSQL 中，`READ
UNCOMMITTED` 會被視為 `READ COMMITTED` 處理。

交易隔離等級無法在交易的第一個查詢或資料修改陳述式
（`SELECT`、`INSERT`、`DELETE`、
`UPDATE`、`MERGE`、
`FETCH`，或
`COPY`）執行之後再變更。關於交易隔離與並行控制的
更多資訊，請參閱[第 13 章](../../the-sql-language/mvcc/README.md)。

交易存取模式決定了該交易是讀寫交易還是唯讀交易。預設為讀寫。
當交易為唯讀時，下列 SQL 命令會被禁止使用：
`INSERT`、`UPDATE`、
`DELETE`、`MERGE`，以及當寫入目標
並非暫存資料表時的 `COPY FROM`；
所有的 `CREATE`、`ALTER` 與
`DROP` 命令；`COMMENT`、
`GRANT`、`REVOKE`、
`TRUNCATE`；以及當 `EXPLAIN ANALYZE`
與 `EXECUTE` 所要執行的命令屬於上述清單之一時，
這兩者也會被禁止。這只是高階層次上的唯讀概念，
並不會阻止所有寫入磁碟的動作。

`DEFERRABLE`（可延遲）交易屬性，只有在交易同時為
`SERIALIZABLE` 與 `READ ONLY` 時才會有效果。
當一個交易同時選取了這三種屬性時，
該交易在第一次取得快照時可能會被阻塞，之後它就能在不具備
一般 `SERIALIZABLE` 交易額外負擔、也不會有導致或被
序列化失敗取消的風險的情況下執行。此模式非常適合長時間執行的
報表或備份作業。

`SET TRANSACTION SNAPSHOT` 命令可讓新交易以與現有交易
相同的*快照*來執行。既存的交易必須已透過
`pg_export_snapshot` 函式匯出其快照
（見 [9.28.5 節](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)）。
該函式會回傳一個快照識別碼，必須將其提供給 `SET TRANSACTION
SNAPSHOT`，以指定要匯入哪一個快照。此命令中該識別碼必須寫成字串常值，
例如 `'00000003-0000001B-1'`。
`SET TRANSACTION SNAPSHOT` 只能在交易開始時、
於該交易的第一個查詢或資料修改陳述式
（`SELECT`、`INSERT`、`DELETE`、
`UPDATE`、`MERGE`、
`FETCH`，或
`COPY`）之前執行。此外，該交易必須已經設定為
`SERIALIZABLE` 或 `REPEATABLE READ` 隔離等級
（否則該快照會立即被捨棄，因為 `READ COMMITTED` 模式
會為每個命令取得新的快照）。若匯入端交易使用
`SERIALIZABLE` 隔離等級，那麼匯出該快照的交易
也必須使用相同的隔離等級。此外，非唯讀的可序列化交易，
無法從唯讀交易匯入快照。

<a id="id-1.9.3.178.9"></a>

## 注意事項

若在沒有先執行 `START TRANSACTION` 或 `BEGIN`
的情況下執行 `SET TRANSACTION`，
會發出警告，且不會產生其他任何效果。

也可以不使用 `SET TRANSACTION`，而是改在
`BEGIN` 或 `START TRANSACTION` 中直接指定
所需的 *`transaction_modes`*。
但這個做法不適用於 `SET TRANSACTION
SNAPSHOT`。

工作階段預設的交易模式，也可以透過組態參數
[default_transaction_isolation](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TRANSACTION-ISOLATION)、
[default_transaction_read_only](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TRANSACTION-READ-ONLY)
與
[default_transaction_deferrable](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TRANSACTION-DEFERRABLE)
來設定或查看。
（事實上，`SET SESSION CHARACTERISTICS` 只是以
`SET` 設定這些變數的一種詳細寫法。）
這代表可以在組態檔中、透過
`ALTER DATABASE` 等方式設定這些預設值。
詳情請參閱[第 19 章](../../server-administration/runtime-config/README.md)。

目前交易的模式，同樣可以透過組態參數
[transaction_isolation](../../server-administration/runtime-config/runtime-config-client.md#GUC-TRANSACTION-ISOLATION)、
[transaction_read_only](../../server-administration/runtime-config/runtime-config-client.md#GUC-TRANSACTION-READ-ONLY)
與
[transaction_deferrable](../../server-administration/runtime-config/runtime-config-client.md#GUC-TRANSACTION-DEFERRABLE)
來設定或查看。設定這些參數之一，效果與對應的
`SET
TRANSACTION` 選項相同，且具有相同的時機限制。
不過，這些參數無法在組態檔中設定，也無法透過即時 SQL 以外的
任何方式設定。

<a id="id-1.9.3.178.10"></a>

## 範例

要以與既有交易相同的快照開始一個新交易，首先要從既有交易中
匯出快照。這會回傳快照識別碼，例如：

```

BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT pg_export_snapshot();
 pg_export_snapshot
---------------------
 00000003-0000001B-1
(1 row)
```

接著在新開啟交易的一開始，於 `SET TRANSACTION
SNAPSHOT` 命令中提供該快照識別碼：

```

BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION SNAPSHOT '00000003-0000001B-1';
```

<a id="R1-SQL-SET-TRANSACTION-3"></a>

## 相容性

這些命令是在 SQL 標準中定義的，但 `DEFERRABLE`
交易模式以及 `SET TRANSACTION SNAPSHOT` 形式除外，
這兩者是 PostgreSQL 的擴充功能。

在標準中，`SERIALIZABLE` 是預設的交易隔離等級。
在 PostgreSQL 中，預設值通常是
`READ COMMITTED`，但你可以如上所述變更它。

在 SQL 標準中，還有另一項可以用這些命令設定的交易特性：
診斷區域的大小。這個概念是內嵌 SQL 所特有的，
因此並未在 PostgreSQL 伺服器中實作。

SQL 標準要求連續的 *`transaction_modes`* 之間必須以逗號分隔，
但基於歷史因素，PostgreSQL 允許省略逗號。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-set-transaction.html)（原文版本：18.6；核對日期：2026-09-28）
