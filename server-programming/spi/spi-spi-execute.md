<a id="id-1.8.12.8.4.1"></a>

## SPI_execute

SPI_execute — 執行一個指令

## 概要

```

int SPI_execute(const char * command, bool read_only, long count)
```

<a id="id-1.8.12.8.4.5"></a>

## 描述

`SPI_execute` 會針對 *`count`* 筆資料列執行所指定的 SQL 指令。如果 *`read_only`* 為 `true`，該指令必須是唯讀的，而且執行的額外負擔會稍微減少。

這個函式只能從已連線的 C 函式中呼叫。

如果 *`count`* 為零，該指令就會對所有適用的資料列執行。如果 *`count`* 大於零，則最多只會取回 *`count`* 筆資料列；達到該筆數時就會停止執行，很像是在查詢中加上 `LIMIT` 子句。例如，

```

SPI_execute("SELECT * FROM foo", true, 5);
```

最多會從該資料表取回 5 筆資料列。請注意，這種限制只有在指令真的會回傳資料列時才有效。例如，

```

SPI_execute("INSERT INTO foo SELECT * FROM bar", false, 5);
```

會插入 `bar` 中的所有資料列，忽略 *`count`* 參數。不過，若寫成

```

SPI_execute("INSERT INTO foo SELECT * FROM bar RETURNING *", false, 5);
```

則最多只會插入 5 筆資料列，因為在取回第五筆 `RETURNING` 結果資料列之後執行就會停止。

你可以在單一字串中傳入多個指令；`SPI_execute` 會回傳最後執行的那個指令的結果。*`count`* 限制會分別套用到每一個指令上（即使實際上只會回傳最後一個結果）。這個限制不會套用到規則所產生的任何隱藏指令。

當 *`read_only`* 為 `false` 時，`SPI_execute` 會在執行字串中的每一個指令之前遞增指令計數器並計算一個新的*快照*。如果目前的交易隔離等級是 `SERIALIZABLE` 或 `REPEATABLE READ`，快照實際上不會改變；但在 `READ COMMITTED` 模式下，快照的更新讓每個指令都能看到其他工作階段中新近提交之交易的結果。當這些指令會修改資料庫時，這對於行為的一致性至關重要。

當 *`read_only`* 為 `true` 時，`SPI_execute` 不會更新快照，也不會更新指令計數器，而且只允許指令字串中出現單純的 `SELECT` 指令。這些指令會使用先前為外圍查詢所建立的快照來執行。由於省去了每個指令的額外負擔，這種執行模式比讀寫模式稍快一些。它也讓真正*穩定*（stable）的函式得以建立：因為連續多次執行都會使用同一個快照，結果不會有所改變。

在使用 SPI 的單一函式中混用唯讀與讀寫指令，通常並不明智；那可能導致非常令人困惑的行為，因為唯讀查詢看不到讀寫查詢所做的任何資料庫更新的結果。

（最後一個）指令實際執行所涉及的資料列筆數，會回傳在全域變數 `SPI_processed` 中。如果函式的回傳值是 `SPI_OK_SELECT`、`SPI_OK_INSERT_RETURNING`、`SPI_OK_DELETE_RETURNING`、`SPI_OK_UPDATE_RETURNING` 或 `SPI_OK_MERGE_RETURNING`，那麼你就可以使用全域指標 `SPITupleTable *SPI_tuptable` 來存取結果資料列。有些工具指令（例如 `EXPLAIN`）也會回傳資料列集合，在這些情況下 `SPI_tuptable` 同樣會含有結果。有些工具指令（`COPY`、`CREATE TABLE AS`）不會回傳資料列集合，因此 `SPI_tuptable` 為 NULL，但它們仍然會在 `SPI_processed` 中回傳所處理的資料列筆數。

`SPITupleTable` 結構定義如下：

```

typedef struct SPITupleTable
{
    /* Public members */
    TupleDesc   tupdesc;        /* tuple descriptor */
    HeapTuple  *vals;           /* array of tuples */
    uint64      numvals;        /* number of valid tuples */

    /* Private members, not intended for external callers */
    uint64      alloced;        /* allocated length of vals array */
    MemoryContext tuptabcxt;    /* memory context of result table */
    slist_node  next;           /* link for internal bookkeeping */
    SubTransactionId subid;     /* subxact in which tuptable was created */
} SPITupleTable;
```

`tupdesc`、`vals` 與 `numvals` 這幾個欄位可供 SPI 呼叫端使用；其餘欄位屬於內部使用。`vals` 是一個指向資料列的指標陣列。資料列的筆數由 `numvals` 給出（基於某些歷史因素，這個計數也會回傳在 `SPI_processed` 中）。`tupdesc` 則是一個資料列描述子，你可以把它傳給處理資料列的 SPI 函式。

`SPI_finish` 會釋放目前這個 C 函式執行期間所配置的所有 `SPITupleTable`。如果你已經用完某個特定的結果資料表，也可以呼叫 `SPI_freetuptable` 提早釋放它。

<a id="id-1.8.12.8.4.6"></a>

## 引數

`const char * command`
:   含有要執行之指令的字串

`bool read_only`
:   `true` 表示唯讀執行

`long count`
:   要回傳的資料列筆數上限，`0` 表示沒有限制

<a id="id-1.8.12.8.4.7"></a>

## 回傳值

如果指令執行成功，就會回傳下列（非負）值之一：

`SPI_OK_SELECT`
:   若執行的是 `SELECT`（但不是 `SELECT INTO`）

`SPI_OK_SELINTO`
:   若執行的是 `SELECT INTO`

`SPI_OK_INSERT`
:   若執行的是 `INSERT`

`SPI_OK_DELETE`
:   若執行的是 `DELETE`

`SPI_OK_UPDATE`
:   若執行的是 `UPDATE`

`SPI_OK_MERGE`
:   若執行的是 `MERGE`

`SPI_OK_INSERT_RETURNING`
:   若執行的是 `INSERT RETURNING`

`SPI_OK_DELETE_RETURNING`
:   若執行的是 `DELETE RETURNING`

`SPI_OK_UPDATE_RETURNING`
:   若執行的是 `UPDATE RETURNING`

`SPI_OK_MERGE_RETURNING`
:   若執行的是 `MERGE RETURNING`

`SPI_OK_UTILITY`
:   若執行的是工具指令（例如 `CREATE TABLE`）

`SPI_OK_REWRITTEN`
:   若該指令被[規則](../rules/README.md)改寫成另一種指令（例如 `UPDATE` 變成了 `INSERT`）

發生錯誤時，會回傳下列負值之一：

`SPI_ERROR_ARGUMENT`
:   若 *`command`* 為 `NULL`，或 *`count`* 小於 0

`SPI_ERROR_COPY`
:   若嘗試執行 `COPY TO stdout` 或 `COPY FROM stdin`

`SPI_ERROR_TRANSACTION`
:   若嘗試執行交易操作指令（`BEGIN`、`COMMIT`、`ROLLBACK`、`SAVEPOINT`、`PREPARE TRANSACTION`、`COMMIT PREPARED`、`ROLLBACK PREPARED`，或其任何變體）

`SPI_ERROR_OPUNKNOWN`
:   若指令類型不明（不應該發生）

`SPI_ERROR_UNCONNECTED`
:   若是從未連線的 C 函式中呼叫

<a id="id-1.8.12.8.4.8"></a>

## 註記

所有 SPI 查詢執行函式都會設定 `SPI_processed` 與 `SPI_tuptable`（只設定指標，不含結構的內容）。如果你需要在之後的呼叫中跨越性地存取 `SPI_execute` 或其他查詢執行函式的結果資料表，請把這兩個全域變數存到 C 函式的區域變數中。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-execute.html)（原文版本：18.6；核對日期：2026-09-13）
