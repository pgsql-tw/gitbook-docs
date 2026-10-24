<a id="LIBPQ-EVENTS"></a>

## 32.14. 事件系統 [#](#libpq-events) <a href="#libpq-events" id="libpq-events"></a>

[32.14.1. 事件類型](libpq-events.md#libpq-events-types)

[32.14.2. 事件回呼程序](libpq-events.md#libpq-events-proc)

[32.14.3. 事件支援函式](libpq-events.md#libpq-events-funcs)

[32.14.4. 事件範例](libpq-events.md#libpq-events-example)

libpq 的事件系統用來將值得關注的 libpq 事件（例如 `PGconn` 與 `PGresult` 物件的建立或銷毀）通知已註冊的事件處理常式。主要的使用情境是讓應用程式能將自己的資料與 `PGconn` 或 `PGresult` 相關聯，並確保這些資料在適當的時機被釋放。

每個已註冊的事件處理常式都與兩項資料相關聯，對 libpq 而言，它們只是不透明的 `void *` 指標。其一是*傳遞（pass-through）*指標，由應用程式在將事件處理常式註冊到 `PGconn` 時提供。在該 `PGconn` 以及由它產生的所有 `PGresult` 的存續期間，傳遞指標都不會改變；因此若有使用，它必須指向長期存在的資料。此外還有一個*執行個體資料（instance data）*指標，它在每個 `PGconn` 與 `PGresult` 中的初始值都是 `NULL`。這個指標可以使用 [`PQinstanceData`](libpq-events.md#LIBPQ-PQINSTANCEDATA)、[`PQsetInstanceData`](libpq-events.md#LIBPQ-PQSETINSTANCEDATA)、[`PQresultInstanceData`](libpq-events.md#LIBPQ-PQRESULTINSTANCEDATA) 與 [`PQresultSetInstanceData`](libpq-events.md#LIBPQ-PQRESULTSETINSTANCEDATA) 函式操作。請注意，與傳遞指標不同，`PGconn` 的執行個體資料不會自動由從它建立的 `PGresult` 繼承。libpq 並不知道傳遞指標與執行個體資料指標指向什麼（如果有指向任何東西的話），也絕不會嘗試釋放它們——那是事件處理常式的責任。

<a id="LIBPQ-EVENTS-TYPES"></a>

### 32.14.1. 事件類型 [#](#libpq-events-types) <a href="#libpq-events-types" id="libpq-events-types"></a>

列舉型別 `PGEventId` 命名了事件系統所處理的事件類型。它的所有值的名稱都以 `PGEVT` 開頭。每一種事件類型都有對應的事件資訊結構，用來攜帶傳給事件處理常式的參數。事件類型如下：

<a id="LIBPQ-PGEVT-REGISTER"></a>

`PGEVT_REGISTER` [#](#LIBPQ-PGEVT-REGISTER)

註冊事件在呼叫 [`PQregisterEventProc`](libpq-events.md#LIBPQ-PQREGISTEREVENTPROC) 時發生。這是初始化事件程序可能需要的任何 `instanceData` 的理想時機。每個連線的每個事件處理常式只會觸發一次註冊事件。若事件程序失敗（傳回零），則註冊會被取消。

```

    typedef struct
    {
        PGconn *conn;
    } PGEventRegister;
```

收到 `PGEVT_REGISTER` 事件時，應將 *`evtInfo`* 指標轉型為 `PGEventRegister *`。此結構包含一個應處於 `CONNECTION_OK` 狀態的 `PGconn`；若在取得正常的 `PGconn` 後立即呼叫 [`PQregisterEventProc`](libpq-events.md#LIBPQ-PQREGISTEREVENTPROC)，即可保證如此。傳回失敗代碼時，必須完成所有清理工作，因為不會送出 `PGEVT_CONNDESTROY` 事件。

<a id="LIBPQ-PGEVT-CONNRESET"></a>

`PGEVT_CONNRESET` [#](#LIBPQ-PGEVT-CONNRESET)

連線重設事件會在 [`PQreset`](libpq-connect.md#LIBPQ-PQRESET) 或 `PQresetPoll` 完成時觸發。在這兩種情況下，只有重設成功時才會觸發此事件。在 PostgreSQL v15 及更新版本中，事件程序的傳回值會被忽略。不過在更早的版本中，傳回成功（非零值）很重要，否則連線將會被中止。

```

    typedef struct
    {
        PGconn *conn;
    } PGEventConnReset;
```

收到 `PGEVT_CONNRESET` 事件時，應將 *`evtInfo`* 指標轉型為 `PGEventConnReset *`。雖然其中包含的 `PGconn` 剛剛被重設，所有事件資料仍保持不變。此事件應用於重設／重新載入／重新查詢任何相關聯的 `instanceData`。請注意，即使事件程序處理 `PGEVT_CONNRESET` 失敗，在連線關閉時它仍會收到 `PGEVT_CONNDESTROY` 事件。

<a id="LIBPQ-PGEVT-CONNDESTROY"></a>

`PGEVT_CONNDESTROY` [#](#LIBPQ-PGEVT-CONNDESTROY)

連線銷毀事件會因應 [`PQfinish`](libpq-connect.md#LIBPQ-PQFINISH) 而觸發。由於 libpq 沒有能力管理這些記憶體，正確清理其事件資料是事件程序的責任。未進行清理將導致記憶體洩漏。

```

    typedef struct
    {
        PGconn *conn;
    } PGEventConnDestroy;
```

收到 `PGEVT_CONNDESTROY` 事件時，應將 *`evtInfo`* 指標轉型為 `PGEventConnDestroy *`。此事件會在 [`PQfinish`](libpq-connect.md#LIBPQ-PQFINISH) 執行任何其他清理工作之前觸發。由於無法從 [`PQfinish`](libpq-connect.md#LIBPQ-PQFINISH) 回報失敗，事件程序的傳回值會被忽略。此外，事件程序的失敗不應中止清理不再需要之記憶體的過程。

<a id="LIBPQ-PGEVT-RESULTCREATE"></a>

`PGEVT_RESULTCREATE` [#](#LIBPQ-PGEVT-RESULTCREATE)

結果建立事件會因應任何產生結果的查詢執行函式而觸發，包括 [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT)。此事件只會在結果成功建立之後才觸發。

```

    typedef struct
    {
        PGconn *conn;
        PGresult *result;
    } PGEventResultCreate;
```

收到 `PGEVT_RESULTCREATE` 事件時，應將 *`evtInfo`* 指標轉型為 `PGEventResultCreate *`。*`conn`* 是用來產生該結果的連線。這是初始化需要與該結果相關聯之任何 `instanceData` 的理想位置。若事件程序失敗（傳回零），在該結果剩餘的存續期間內都會忽略該事件程序；也就是說，對於此結果或從它複製出的結果，該事件程序都不會收到 `PGEVT_RESULTCOPY` 或 `PGEVT_RESULTDESTROY` 事件。

<a id="LIBPQ-PGEVT-RESULTCOPY"></a>

`PGEVT_RESULTCOPY` [#](#LIBPQ-PGEVT-RESULTCOPY)

結果複製事件會因應 [`PQcopyResult`](libpq-misc.md#LIBPQ-PQCOPYRESULT) 而觸發。此事件只會在複製完成之後才觸發。只有已成功處理來源結果之 `PGEVT_RESULTCREATE` 或 `PGEVT_RESULTCOPY` 事件的事件程序，才會收到 `PGEVT_RESULTCOPY` 事件。

```

    typedef struct
    {
        const PGresult *src;
        PGresult *dest;
    } PGEventResultCopy;
```

收到 `PGEVT_RESULTCOPY` 事件時，應將 *`evtInfo`* 指標轉型為 `PGEventResultCopy *`。*`src`* 結果是被複製的對象，而 *`dest`* 結果是複製的目的地。由於 `PQcopyResult` 無法做到深層複製，此事件可用來提供 `instanceData` 的深層複製。若事件程序失敗（傳回零），在新結果剩餘的存續期間內都會忽略該事件程序；也就是說，對於該結果或從它複製出的結果，該事件程序都不會收到 `PGEVT_RESULTCOPY` 或 `PGEVT_RESULTDESTROY` 事件。

<a id="LIBPQ-PGEVT-RESULTDESTROY"></a>

`PGEVT_RESULTDESTROY` [#](#LIBPQ-PGEVT-RESULTDESTROY)

結果銷毀事件會因應 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 而觸發。由於 libpq 沒有能力管理這些記憶體，正確清理其事件資料是事件程序的責任。未進行清理將導致記憶體洩漏。

```

    typedef struct
    {
        PGresult *result;
    } PGEventResultDestroy;
```

收到 `PGEVT_RESULTDESTROY` 事件時，應將 *`evtInfo`* 指標轉型為 `PGEventResultDestroy *`。此事件會在 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 執行任何其他清理工作之前觸發。由於無法從 [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) 回報失敗，事件程序的傳回值會被忽略。此外，事件程序的失敗不應中止清理不再需要之記憶體的過程。

<a id="LIBPQ-EVENTS-PROC"></a>

### 32.14.2. 事件回呼程序 [#](#libpq-events-proc) <a href="#libpq-events-proc" id="libpq-events-proc"></a>

<a id="LIBPQ-PGEVENTPROC"></a>

`PGEventProc`<a id="id-1.7.3.21.5.2.1.1.2"></a> [#](#LIBPQ-PGEVENTPROC)

`PGEventProc` 是指向事件程序之指標的型別定義（typedef）；事件程序即接收來自 libpq 之事件的使用者回呼函式。事件程序的簽章必須是

```

    int eventproc(PGEventId evtId, void *evtInfo, void *passThrough)
```

*`evtId`* 參數指出發生了哪一個 `PGEVT` 事件。必須將 *`evtInfo`* 指標轉型為適當的結構型別，才能取得該事件的進一步資訊。*`passThrough`* 參數是註冊該事件程序時提供給 [`PQregisterEventProc`](libpq-events.md#LIBPQ-PQREGISTEREVENTPROC) 的指標。此函式成功時應傳回非零值，失敗時應傳回零。

特定的事件程序在任何一個 `PGconn` 中都只能註冊一次。這是因為該程序的位址會被當作查找鍵，用來識別相關聯的執行個體資料。

### 小心

在 Windows 上，函式可能有兩個不同的位址：一個是從 DLL 外部可見的位址，另一個是從 DLL 內部可見的位址。應該小心確保 libpq 的事件程序函式只使用其中一個位址，否則會造成混亂。撰寫可正常運作之程式碼的最簡單規則，是確保事件程序都宣告為 `static`。若該程序的位址必須在其所屬原始檔之外取得，請另外提供一個傳回該位址的函式。

<a id="LIBPQ-EVENTS-FUNCS"></a>

### 32.14.3. 事件支援函式 [#](#libpq-events-funcs) <a href="#libpq-events-funcs" id="libpq-events-funcs"></a>

<a id="LIBPQ-PQREGISTEREVENTPROC"></a>

`PQregisterEventProc`<a id="id-1.7.3.21.6.2.1.1.2"></a> [#](#LIBPQ-PQREGISTEREVENTPROC)

向 libpq 註冊一個事件回呼程序。

```

    int PQregisterEventProc(PGconn *conn, PGEventProc proc,
                            const char *name, void *passThrough);
```

對於每一個你想接收其事件的 `PGconn`，都必須註冊一次事件程序。除了記憶體之外，可註冊到一個連線的事件程序數量沒有限制。此函式成功時傳回非零值，失敗時傳回零。

*`proc`* 引數會在觸發 libpq 事件時被呼叫。它的記憶體位址也被用來查找 `instanceData`。*`name`* 引數用於在錯誤訊息中指稱該事件程序。此值不能是 `NULL` 或長度為零的字串。名稱字串會被複製到 `PGconn` 中，因此所傳入的字串不需要長期存在。每當有事件發生時，*`passThrough`* 指標都會傳給 *`proc`*。此引數可以是 `NULL`。

<a id="LIBPQ-PQSETINSTANCEDATA"></a>

`PQsetInstanceData`<a id="id-1.7.3.21.6.2.2.1.2"></a> [#](#LIBPQ-PQSETINSTANCEDATA)

將連線 *`conn`* 中對應程序 *`proc`* 的 `instanceData` 設為 *`data`*。成功時傳回非零值，失敗時傳回零。（只有在 *`proc`* 未在 *`conn`* 中正確註冊時才可能失敗。）

```

    int PQsetInstanceData(PGconn *conn, PGEventProc proc, void *data);
```

<a id="LIBPQ-PQINSTANCEDATA"></a>

`PQinstanceData`<a id="id-1.7.3.21.6.2.3.1.2"></a> [#](#LIBPQ-PQINSTANCEDATA)

傳回連線 *`conn`* 中與程序 *`proc`* 相關聯的 `instanceData`；若沒有，則傳回 `NULL`。

```

    void *PQinstanceData(const PGconn *conn, PGEventProc proc);
```

<a id="LIBPQ-PQRESULTSETINSTANCEDATA"></a>

`PQresultSetInstanceData`<a id="id-1.7.3.21.6.2.4.1.2"></a> [#](#LIBPQ-PQRESULTSETINSTANCEDATA)

將結果中對應 *`proc`* 的 `instanceData` 設為 *`data`*。成功時傳回非零值，失敗時傳回零。（只有在 *`proc`* 未在該結果中正確註冊時才可能失敗。）

```

    int PQresultSetInstanceData(PGresult *res, PGEventProc proc, void *data);
```

請注意，*`data`* 所代表的任何儲存空間都不會被 [`PQresultMemorySize`](libpq-misc.md#LIBPQ-PQRESULTMEMORYSIZE) 計入，除非它是使用 [`PQresultAlloc`](libpq-misc.md#LIBPQ-PQRESULTALLOC) 配置的。（建議這麼做，因為如此一來，在結果被銷毀時就不需要另行明確釋放這類儲存空間。）

<a id="LIBPQ-PQRESULTINSTANCEDATA"></a>

`PQresultInstanceData`<a id="id-1.7.3.21.6.2.5.1.2"></a> [#](#LIBPQ-PQRESULTINSTANCEDATA)

傳回結果中與 *`proc`* 相關聯的 `instanceData`；若沒有，則傳回 `NULL`。

```

    void *PQresultInstanceData(const PGresult *res, PGEventProc proc);
```

<a id="LIBPQ-EVENTS-EXAMPLE"></a>

### 32.14.4. 事件範例 [#](#libpq-events-example) <a href="#libpq-events-example" id="libpq-events-example"></a>

以下是一個骨架範例，示範如何管理與 libpq 連線及結果相關聯的私有資料。

```


/* required header for libpq events (note: includes libpq-fe.h) */
#include <libpq-events.h>

/* The instanceData */
typedef struct
{
    int n;
    char *str;
} mydata;

/* PGEventProc */
static int myEventProc(PGEventId evtId, void *evtInfo, void *passThrough);

int
main(void)
{
    mydata *data;
    PGresult *res;
    PGconn *conn =
        PQconnectdb("dbname=postgres options=-csearch_path=");

    if (PQstatus(conn) != CONNECTION_OK)
    {
        /* PQerrorMessage's result includes a trailing newline */
        fprintf(stderr, "%s", PQerrorMessage(conn));
        PQfinish(conn);
        return 1;
    }

    /* called once on any connection that should receive events.
     * Sends a PGEVT_REGISTER to myEventProc.
     */
    if (!PQregisterEventProc(conn, myEventProc, "mydata_proc", NULL))
    {
        fprintf(stderr, "Cannot register PGEventProc\n");
        PQfinish(conn);
        return 1;
    }

    /* conn instanceData is available */
    data = PQinstanceData(conn, myEventProc);

    /* Sends a PGEVT_RESULTCREATE to myEventProc */
    res = PQexec(conn, "SELECT 1 + 1");

    /* result instanceData is available */
    data = PQresultInstanceData(res, myEventProc);

    /* If PG_COPYRES_EVENTS is used, sends a PGEVT_RESULTCOPY to myEventProc */
    res_copy = PQcopyResult(res, PG_COPYRES_TUPLES | PG_COPYRES_EVENTS);

    /* result instanceData is available if PG_COPYRES_EVENTS was
     * used during the PQcopyResult call.
     */
    data = PQresultInstanceData(res_copy, myEventProc);

    /* Both clears send a PGEVT_RESULTDESTROY to myEventProc */
    PQclear(res);
    PQclear(res_copy);

    /* Sends a PGEVT_CONNDESTROY to myEventProc */
    PQfinish(conn);

    return 0;
}

static int
myEventProc(PGEventId evtId, void *evtInfo, void *passThrough)
{
    switch (evtId)
    {
        case PGEVT_REGISTER:
        {
            PGEventRegister *e = (PGEventRegister *)evtInfo;
            mydata *data = get_mydata(e->conn);

            /* associate app specific data with connection */
            PQsetInstanceData(e->conn, myEventProc, data);
            break;
        }

        case PGEVT_CONNRESET:
        {
            PGEventConnReset *e = (PGEventConnReset *)evtInfo;
            mydata *data = PQinstanceData(e->conn, myEventProc);

            if (data)
              memset(data, 0, sizeof(mydata));
            break;
        }

        case PGEVT_CONNDESTROY:
        {
            PGEventConnDestroy *e = (PGEventConnDestroy *)evtInfo;
            mydata *data = PQinstanceData(e->conn, myEventProc);

            /* free instance data because the conn is being destroyed */
            if (data)
              free_mydata(data);
            break;
        }

        case PGEVT_RESULTCREATE:
        {
            PGEventResultCreate *e = (PGEventResultCreate *)evtInfo;
            mydata *conn_data = PQinstanceData(e->conn, myEventProc);
            mydata *res_data = dup_mydata(conn_data);

            /* associate app specific data with result (copy it from conn) */
            PQresultSetInstanceData(e->result, myEventProc, res_data);
            break;
        }

        case PGEVT_RESULTCOPY:
        {
            PGEventResultCopy *e = (PGEventResultCopy *)evtInfo;
            mydata *src_data = PQresultInstanceData(e->src, myEventProc);
            mydata *dest_data = dup_mydata(src_data);

            /* associate app specific data with result (copy it from a result) */
            PQresultSetInstanceData(e->dest, myEventProc, dest_data);
            break;
        }

        case PGEVT_RESULTDESTROY:
        {
            PGEventResultDestroy *e = (PGEventResultDestroy *)evtInfo;
            mydata *data = PQresultInstanceData(e->result, myEventProc);

            /* free instance data because the result is being destroyed */
            if (data)
              free_mydata(data);
            break;
        }

        /* unknown event ID, just return true. */
        default:
            break;
    }

    return true; /* event processing succeeded */
}
```

譯註：此骨架範例中的 res_copy 並未在 main 函式中宣告（實際編譯時需另行宣告 PGresult *res_copy;）；get_mydata、dup_mydata、free_mydata 也是假設由應用程式自行提供的函式。程式碼依原文保留。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-events.html)（原文版本：18.6；核對日期：2026-10-18）
